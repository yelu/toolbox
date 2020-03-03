import os,sys
import tensorflow as tf
import numpy as np

class Encoder(object):

    def __init__(self):
        self.outputs = {}
    
    def _DefineParams(self, 
                      encoder_state_size,
                      encoder_vocab_size,
                      wb_init, 
                      encoder_embedding_init):
        self.embeddings = tf.get_variable("embeddings",
                                         shape = [encoder_vocab_size, encoder_state_size],
                                         initializer = encoder_embedding_init)
        self.u = tf.get_variable('u',
                                shape=[3, encoder_state_size, encoder_state_size],
                                initializer=wb_init)
        self.w = tf.get_variable('w', 
                            shape=[3, encoder_state_size, encoder_state_size],
                            initializer=wb_init)

    def BuildGraph(self,
                    inputs, 
                    batch_size, 
                    encoder_state_size,
                    encoder_vocab_size,                
                    wb_init = tf.contrib.layers.xavier_initializer(),
                    encoder_embedding_init = tf.contrib.layers.xavier_initializer()):
        
        '''
        inputs["encoder_inputs"] : [batch_size, num_steps]
        inputs["encoder_inputs_mask"] : [batch_size, num_steps]
        '''
        
        with tf.variable_scope('encoder'):
            self._DefineParams(encoder_state_size,
                               encoder_vocab_size,
                               wb_init, 
                               encoder_embedding_init)

        # 1. embedding layer
        with tf.device('/cpu:0'), tf.variable_scope('encoder_embedding'):
            encoder_inputs_embedded = tf.nn.embedding_lookup(self.embeddings, 
                                                             inputs["encoder_inputs"])

        # 2. encoder
        with tf.variable_scope('encoder'):
            def step(pre, cur):
                s_pre, _ = pre
                x, mask = cur
                z = tf.sigmoid(tf.matmul(x, self.u[0]) + tf.matmul(s_pre, self.w[0]))
                r = tf.sigmoid(tf.matmul(x, self.u[1]) + tf.matmul(s_pre, self.w[1]))
                h = tf.tanh(tf.matmul(x, self.u[2]) + tf.matmul(r*s_pre, self.w[2]))
                mask_expanded = tf.cast(tf.expand_dims(mask, -1), tf.float32)
                # when mask bit is 1, update gru state as usual.
                # when mask bit is 0, keep s_pre as current s.
                s = ((1-z)*h + (z*s_pre)) * mask_expanded + s_pre * (1.0 - mask_expanded)
                return (s, mask)

            #[num_steps, batch_size, encoder_state_size]
            scan_results = tf.scan(step, 
                                     (tf.transpose(encoder_inputs_embedded, [1, 0, 2]), tf.transpose(inputs["encoder_inputs_mask"], [1, 0])),
                                     initializer = (tf.zeros([batch_size, encoder_state_size], dtype = tf.float32),
                                                    tf.zeros([batch_size], dtype = tf.int32))) 
            self.outputs["encoder_states"] = scan_results[0]  # scan_result not only contains encoder_states
        
        return self.outputs
