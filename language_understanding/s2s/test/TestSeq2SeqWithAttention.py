from s2s.Seq2SeqWithAttention import Seq2SeqWithAttention
import tensorflow as tf
import numpy as np
import unittest
import random

class Test_Seq2SeqWithAttention(unittest.TestCase):

    def test_Forward(self):
        s2s = Seq2SeqWithAttention()

        encoder_inputs = np.array([[1,2,0],[1,2,0]], dtype = np.int32)
        encoder_inputs_mask = np.array([[1,1,0],[1,1,0]], dtype = np.int32)
        decoder_inputs = np.array([[2,3,4,0],[2,3,4,0]], dtype = np.int32)
        decoder_outputs = np.array([[2,3,4,0],[2,3,4,0]], dtype = np.int32)
        decoder_outputs_mask = np.array([[1,1,0,0],[1,1,0,0]], dtype = np.int32)

        batch_size = 2
        decoder_state_size = 4
        decoder_vocab_size = 5

        #encoder_inputs = np.array([[1,2,0]], dtype = np.int32)
        #encoder_inputs_mask = np.array([[1,1,0]], dtype = np.int32)
        #decoder_inputs = np.array([[2,3,4,0]], dtype = np.int32)
        #decoder_outputs = np.array([[2,3,4,0]], dtype = np.int32)
        #decoder_outputs_mask = np.array([[1,1,0,0]], dtype = np.int32)        
        
        # A Graph contains operations and tensors.
        # with keyword to specify that ops created within the scope of 
        # a block should be added to this graph
        self.graph = tf.Graph()
        with self.graph.as_default():
            tf.set_random_seed(13)
            session_conf = tf.ConfigProto(
              allow_soft_placement = True,
              log_device_placement = False)
            self.sess = tf.Session(config = session_conf)            
        
            s2s.BuildGraphForTrain(batch_size = batch_size, 
                                   encoder_state_size = 2,
                                   encoder_vocab_size = 3,
                                   decoder_state_size = decoder_state_size,
                                   decoder_vocab_size = decoder_vocab_size,
                                   dropout = 0.0,                          
                                   wb_init = tf.constant_initializer(1.0),
                                   encoder_embedding_init = tf.constant_initializer(1.0),
                                   decoder_embedding_init = tf.constant_initializer(1.0))

            feed_dict = {s2s.encoder_inputs: encoder_inputs,
                         s2s.encoder_inputs_mask:encoder_inputs_mask,
                         s2s.decoder_inputs:decoder_inputs,
                         s2s.decoder_outputs:decoder_outputs,
                         s2s.decoder_outputs_mask:decoder_outputs_mask
            }
            
            self.sess.run(tf.global_variables_initializer())

            decoder_output_logits = tf.reshape(tf.matmul(tf.reshape(s2s.decoder_outputs_map["decoder_states"],
                                                                    [-1, decoder_state_size]),
                                                         s2s.decoder.v),
                                               [-1, batch_size, decoder_vocab_size])

            encoder_states, attentions, decoder_output_logits, loss, = \
                tuple(self.sess.run([s2s.encoder_outputs_map["encoder_states"],
                                     s2s.decoder_outputs_map["attentions"],
                                     decoder_output_logits,
                                     s2s.loss],
                                     feed_dict))

            np.testing.assert_almost_equal(encoder_states, 
                                           np.array([[[ 0.11491495,0.11491495],
                                                    [ 0.11491495,0.11491495]],
                                                    [[ 0.19853912,0.19853912],
                                                    [ 0.19853912,0.19853912]],
                                                    [[ 0.19853912,0.19853912 ],
                                                    [ 0.19853912,0.19853912]]]),
                                           4)           
            np.testing.assert_almost_equal(attentions, 
                                           np.array([[[ 0.16301678,0.16301678],
                                                    [ 0.16301678,0.16301678]],
                                                    [[ 0.1628101,0.1628101 ],
                                                    [ 0.1628101,0.1628101 ]],
                                                    [[ 0.16259719,0.16259719],
                                                    [ 0.16259719,0.16259719]],
                                                    [[ 0.16238275,0.16238275],
                                                    [ 0.16238275,0.16238275]]]), 
                                           4)
            np.testing.assert_almost_equal(decoder_output_logits, 
                                           np.array([[[ 0.05217111,0.05217111,0.05217111,0.05217111,0.05217111],
                                                    [ 0.05217111,0.05217111,0.05217111,0.05217111,0.05217111]],
                                                    [[ 0.10109854,0.10109854,0.10109854,0.10109854,0.10109854],
                                                    [ 0.10109854,0.10109854,0.10109854,0.10109854,0.10109854]],
                                                    [[ 0.14715986,0.14715986,0.14715986,0.14715986,0.14715986],
                                                    [ 0.14715986,0.14715986,0.14715986,0.14715986,0.14715986]],
                                                    [[ 0.19067053,0.19067053,0.19067053,0.19067053,0.19067053],
                                                    [ 0.19067053,0.19067053,0.19067053,0.19067053,0.19067053]]]), 
                                           4)
            np.testing.assert_almost_equal(loss, 1.5717735, 2)
        
    def test_Train(self):
        s2s = Seq2SeqWithAttention()
        s2s.Train(data_file = './train.tsv',
                  vocab_keep_ratio = 1.0,
                  model_file = './model/s2s',
                  batch_size = 2,
                  encoder_state_size = 128,
                  decoder_state_size = 256,
                  dropout = 0.0,
                  iteration = 100,
                  verbose = True)

        loaded_s2s = Seq2SeqWithAttention()
        loaded_s2s.Load(model_file = './model/s2s')
        predict = loaded_s2s.Predict("where is the capital of china", beam_size = 1)
        print(predict)
        self.assertEqual(tuple(predict[0]), ('<GO>', 'beijing', '<EOS>'))
        predict = loaded_s2s.Predict("what is the weather")
        print(predict)
        self.assertEqual(tuple(predict[0]), ('<GO>', 'it', 'is', 'sunny', '<EOS>'))

if __name__ == "__main__":
    random.seed(13)
    unittest.main()
 
