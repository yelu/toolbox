import tensorflow as tf
import numpy as np

class ConvPool(object):

    def __init__(self, input_x, seq_len, vocab_size, embedding_dim, filter_sizes, channel, auxiliary, auxiliary_dim = 0):

        # embedding layer
        with tf.device('/cpu:0'), tf.name_scope('embedding'):
            w = tf.Variable(tf.random_uniform([vocab_size, embedding_dim], -1.0, 1.0), name="w")
            seq_embeded = tf.nn.embedding_lookup(w, input_x)           
            self.seq_embeded_expanded = tf.expand_dims(seq_embeded, -1)

        # conv & maxpooling
        all_pooled = []
        for filter_size in filter_sizes:
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                # conv
                filter_shape = [filter_size, embedding_dim, 1, channel]
                # in every filter/channel, w & b are shared
                w = tf.Variable(tf.truncated_normal(filter_shape, stddev = 0.1), name = 'w')
                b = tf.Variable(tf.constant(0.1, shape = [channel]), name = 'b')
                # Input: Batch size x Height x Width x Channels
                # Filter: Height x Width x Input Channels x Output Channels (e.g. [5, 5, 3, 64])
                # Strides: 4 element 1-D tensor, strides in each direction (often [1, 1, 1, 1] or [1, 2, 2, 1])
                # Output: Batch size x Height~ x Width~ x Output Channels
                conv = tf.nn.conv2d(self.seq_embeded_expanded,
                                    w, 
                                    strides = [1,1,1,1],
                                    padding = "VALID",
                                    name = "conv")

                # activation
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name = "relu")
                # pooling. batch * 1 * 1 * channels
                pooled = tf.nn.max_pool(h,
                                        ksize = [1, seq_len - filter_size + 1, 1, 1],
                                        strides = [1,1,1,1],
                                        padding = "VALID",
                                        name = "pool")
                all_pooled.append(pooled)

        # combine all pooled features. batch *  1 * 1 * (channels * channel)
        pooled_concat = tf.concat(all_pooled, 3)
        pooled_flat = tf.reshape(pooled_concat, [-1, channel * len(filter_sizes)])      
        self.output = tf.concat([pooled_flat, auxiliary], 1)
