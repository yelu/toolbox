import os,sys
import tensorflow as tf
import numpy as np

class DecoderWithAttention(object):

    def __init__(self):
        self.outputs = {}
    
    def _DefineParams(self, 
                       encoder_state_size, 
                       decoder_state_size,
                       decoder_vocab_size,
                       wb_init,
                       decoder_embedding_init):
        self.embeddings = tf.get_variable("embeddings",
                                         shape = [decoder_vocab_size, decoder_state_size],
                                         initializer = decoder_embedding_init)
        self.att_wh = tf.get_variable('att_wh',
                                     shape=[encoder_state_size, encoder_state_size],
                                     initializer=wb_init)
        self.att_ws = tf.get_variable('att_ws',
                                     shape=[decoder_state_size, encoder_state_size],
                                     initializer=wb_init)
        self.att_v = tf.get_variable('att_v',
                                    shape=[encoder_state_size],
                                    initializer=wb_init)

        self.w_att_s = tf.get_variable('w_att_s',
                                shape=[3, encoder_state_size, decoder_state_size],
                                initializer=wb_init)
        self.w_y_s = tf.get_variable('w_y_s',
                                shape=[3, decoder_state_size, decoder_state_size],
                                initializer=wb_init)
        self.w = tf.get_variable('w',
                                shape=[3, decoder_state_size, decoder_state_size],
                                initializer=wb_init)
        self.v = tf.get_variable('v',
                                shape=[decoder_state_size, decoder_vocab_size],
                                initializer=wb_init)

    def BuildGraphForTrain(self,
                           inputs,
                           batch_size,
                           encoder_state_size, 
                           decoder_state_size,
                           decoder_vocab_size,
                           dropout,
                           wb_init = tf.contrib.layers.xavier_initializer(),
                           decoder_embedding_init = tf.contrib.layers.xavier_initializer()):
        '''
        inputs["encoder_states"]: [steps, batch_size, encoder_state_size]
        inputs["decoder_inputs"]: [batch_size, steps]
        inputs["decoder_outputs"]: [batch_size, steps]
        inputs["encoder_inputs_mask"]: [batch_size, steps]
        inputs["decoder_outputs_mask"]: [batch_size_steps]

        outputs["decoder_outputs"]: [steps, batch, decoder_vocab_size]

        note: 1. use batch >= 2 for training, since when batch = 1, 
        tf.nn.sampled_softmax_loss dosen't work well
        '''

        with tf.variable_scope('decoder_attention'):
            self._DefineParams(encoder_state_size, 
                               decoder_state_size,
                               decoder_vocab_size,
                               wb_init,
                               decoder_embedding_init)

        # 1. decoder with attention
        with tf.variable_scope('decoder_attention'):
            # att_h_part : [steps, batch_size, encoder_state_size]
            att_h_part = tf.reshape(tf.matmul(tf.reshape(inputs["encoder_states"], 
                                              [-1, encoder_state_size]),
                                    self.att_wh),
                                [-1, batch_size, encoder_state_size]) 
            def step(pre, loop_vars):
                s_pre, _ , _ = pre
                decoder_input, decoder_output = loop_vars
                decoder_input_embedded = tf.nn.embedding_lookup(self.embeddings, 
                                                                decoder_input)            
                s, attention = DecoderWithAttention.RecurrStep(inputs, encoder_state_size, batch_size,
                                                               att_h_part, self.att_ws, self.att_v,
                                                               self.w_att_s, self.w_y_s,
                                                               self.w, self.v,
                                                               s_pre, decoder_input_embedded)
                
                # use sampled softmax to accelerate.
                num_samples = 512
                if num_samples <= 0 or num_samples > decoder_vocab_size:
                    num_samples = decoder_vocab_size
                s_dropout = tf.nn.dropout(s, 1.0 - dropout)
                loss = tf.nn.sampled_softmax_loss(weights = tf.transpose(self.v, [1, 0]),
                                                  biases = tf.zeros([decoder_vocab_size]),
                                                  labels = tf.reshape(decoder_output, [batch_size, 1]),
                                                  inputs = s_dropout,                                                
                                                  num_sampled = num_samples,
                                                  num_classes = decoder_vocab_size,
                                                  partition_strategy = "div")
                return  (s, attention, loss)
                
            decoder_states, attentions, losses = \
                tf.scan(fn = step, 
                        elems = (tf.transpose(inputs["decoder_inputs"], [1, 0]),
                                 tf.transpose(inputs["decoder_outputs"], [1, 0])),
                        initializer = (tf.zeros([batch_size, decoder_state_size]),
                                       tf.zeros([batch_size, encoder_state_size]),
                                       tf.zeros([batch_size])))
            self.outputs["decoder_states"] = decoder_states
            self.outputs["attentions"] = attentions
            self.outputs["loss"] = DecoderWithAttention.MaskLossAndMean(tf.transpose(losses, [1, 0]),
                                                                        inputs["decoder_outputs_mask"])
            return self.outputs

    def BuildGraphForPredict(self,
                             inputs,
                             encoder_state_size,                         
                             decoder_state_size,
                             decoder_vocab_size, 
                             decoder_go_symbol,
                             decoder_eos_symbol):
        '''
        to be simple, batch_size in inputs should always be 1. we keep this dimension
        just to make ranks of interface tensors uniform.
        inputs["encoder_states"]: [steps, 1, encoder_state_size]
        inputs["encoder_inputs_mask"]: [1, steps]
        inputs["decoder_inputs"]: [1, steps]
        
        outputs["decoder_outputs"]: [steps, batch, decoder_vocab_size]
        '''

        with tf.variable_scope('decoder_attention'):
            self._DefineParams(encoder_state_size, 
                               decoder_state_size,
                               decoder_vocab_size,
                               tf.constant_initializer(0.0), 
                               tf.constant_initializer(0.0))

        # 1. decoder with attention
        with tf.variable_scope('decoder_attention'):
            all_outputs = tf.zeros([0,1], dtype=tf.int64)
            output_pre = tf.constant(decoder_go_symbol, shape = [1], dtype=tf.int64)
            s_pre = tf.zeros([1, decoder_state_size])
            loop_count = tf.constant(0)
            # att_h_part : [steps, batch_size, encoder_state_size]
            att_h_part = tf.reshape(tf.matmul(tf.reshape(inputs["encoder_states"], 
                                              [-1, encoder_state_size]),
                                    self.att_wh),
                                [-1, 1, encoder_state_size])

            def body(i, s_pre, output_pre, all_outputs):
                output_embeded = tf.nn.embedding_lookup(self.embeddings, 
                                                        output_pre)
                s, attention = DecoderWithAttention.RecurrStep(
                                                inputs, encoder_state_size, 1,
                                                att_h_part, self.att_ws, self.att_v,
                                                self.w_att_s, self.w_y_s,
                                                self.w, self.v,
                                                s_pre, output_embeded)
                o_logits = tf.matmul(s, self.v) # [batch_size, decoder_vocab_size]
                o = tf.argmax(o_logits, 1) # [batch_size]

                all_outputs = tf.concat([all_outputs, tf.expand_dims(o, 1)], axis = 0)
                return [i + 1, s, o, all_outputs]

            cond = lambda i, s, output, outputs: tf.logical_and(tf.less(i, 64),
                                                                tf.not_equal(output[0], decoder_eos_symbol))

            final = tf.while_loop(cond, body, 
                                  loop_vars = [loop_count, s_pre, output_pre, all_outputs],
                                  shape_invariants = [loop_count.get_shape(),
                                                      s_pre.get_shape(),
                                                      output_pre.get_shape(),
                                                      tf.TensorShape([None, 1])])
            self.outputs["decoder_outputs"] = final[3]
            return self.outputs

    def BuildGraphForBeamSearch(self,
                                inputs,
                                encoder_state_size,
                                decoder_state_size,
                                decoder_vocab_size, 
                                decoder_go_symbol,
                                decoder_eos_symbol):
        '''
        to be simple, batch_size in inputs should always be 1. we keep this dimension
        just to make ranks of interface tensors uniform.
        inputs["encoder_states"]: [steps, 1, encoder_state_size]
        inputs["encoder_inputs_mask"]: [1, steps]
        inputs["decoder_state_pre"]: [1, decoder_state_size]
        inputs["decoder_output_pre"]: [1, decoder_state_size]
        
        outputs["decoder_output_prob"]: [1, decoder_vocab_size]
        outputs["decoder_state"]: [1, decoder_state_size]
        '''

        with tf.variable_scope('decoder_attention'):
            self._DefineParams(encoder_state_size, 
                               decoder_state_size,
                               decoder_vocab_size,
                               tf.constant_initializer(0.0), 
                               tf.constant_initializer(0.0))

        # 1. decoder with attention
        with tf.variable_scope('decoder_attention'):
            # att_h_part : [steps, batch_size, encoder_state_size]
            att_h_part = tf.reshape(tf.matmul(tf.reshape(inputs["encoder_states"], 
                                              [-1, encoder_state_size]),
                                    self.att_wh),
                                    [-1, 1, encoder_state_size])


            output_embeded = tf.nn.embedding_lookup(self.embeddings, 
                                                    inputs["decoder_output_pre"])
            s, attention = DecoderWithAttention.RecurrStep(
                                            inputs, encoder_state_size, 1,
                                            att_h_part, self.att_ws, self.att_v,
                                            self.w_att_s, self.w_y_s,
                                            self.w, self.v,
                                            inputs["decoder_state_pre"],
                                            output_embeded)
            o_logits = tf.matmul(s, self.v) # [batch_size, decoder_vocab_size]
            self.outputs["decoder_output_prob"] = tf.nn.softmax(o_logits)
            self.outputs["decoder_state"] = s
            
            return self.outputs

    @staticmethod
    def RecurrStep(inputs, encoder_state_size,
                    batch_size,
                    att_h_part, att_ws, att_v,
                    w_att_s, w_y_s, w, v,
                    s_pre, y):
        '''
        output:
            s: latest hidden state
            attention: it is for testing purpose
        '''
        att_s_part = tf.matmul(s_pre, att_ws) # [batch_size, encoder_state_size]
        attention_1 = tf.add(att_h_part, att_s_part) # [steps, batch_size, encoder_state_size]
        attention_2 = tf.transpose(attention_1, [1, 0, 2]) # [batch_size, steps, encoder_state_size]
        attention_3 = tf.tanh(attention_2)
        attention_4 = tf.reduce_sum(tf.multiply(att_v, attention_3), 2) # [batch_size, steps]
        attention_5 = DecoderWithAttention.MaskAndSoftmax(attention_4, inputs["encoder_inputs_mask"])
        attention = tf.reshape(tf.matmul(tf.transpose(inputs["encoder_states"], [1, 2, 0]),
                                         tf.expand_dims(attention_5, -1)),
                               [batch_size, encoder_state_size])
        z = tf.sigmoid(tf.matmul(attention, w_att_s[0]) + 
                       tf.matmul(y, w_y_s[0]) + 
                       tf.matmul(s_pre, w[0]))
        r = tf.sigmoid(tf.matmul(attention, w_att_s[1]) + 
                       tf.matmul(y, w_y_s[1]) + 
                       tf.matmul(s_pre, w[1]))
        h = tf.tanh(tf.matmul(attention, w_att_s[2]) + 
                    tf.matmul(y, w_y_s[2]) + 
                    tf.matmul(r*s_pre, w[2]))
        s = (1-z)*h + (z*s_pre) # [batch_size, decoder_state_size]
        return (s, attention)

    @staticmethod
    def MaskAndSoftmax(t, mask):
        '''
        mask is a 0/1 matrix. all corresponding positions in t
        will be set to 0. then computer softmax, the masked out
        positions in t will not join the softmax, thus will be zero
        in softmax result.
        '''
        masked = t * tf.cast(mask, tf.float32)     
        return tf.nn.softmax(tf.cast((mask - 1) * (10**8), tf.float32) + masked)
    
    @staticmethod
    def MaskLossAndMean(losses, mask):
        mask_float = tf.cast(mask, tf.float32)
        return tf.divide(tf.reduce_sum(losses * mask_float), 
                         tf.reduce_sum(mask_float))
