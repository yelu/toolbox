import os,sys
import tensorflow as tf
import numpy as np
from .ConvPool import ConvPool
from .DataReader import DataReader

class CNN(object):

    def __init__(self):
        tf.logging.set_verbosity(tf.logging.WARN)
        pass
    
    def BuildNet(self, seq_len, num_classes, vocab_size, embedding_dim, filter_sizes, channel, auxiliary_dim = 0):
        self.input_x = tf.placeholder(tf.int32, [None, seq_len], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
        self.input_aux = tf.placeholder(tf.float32, [None, auxiliary_dim], name="input_aux")
        
        conv_pool = ConvPool(self.input_x, seq_len, vocab_size, embedding_dim, filter_sizes, channel, self.input_aux, auxiliary_dim)
        
        self.conv_pooled = conv_pool.output

        # final scores and predictions
        with tf.name_scope("fully_connected"):
            w = tf.get_variable("w",
                                shape=[self.conv_pooled.get_shape().as_list()[1], num_classes],
                                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            self.scores = tf.nn.xw_plus_b(self.conv_pooled, w, b, name="scores")
        self.probs = tf.nn.softmax(logits = self.scores, name = "probs")    
        self.predictions = tf.argmax(self.scores, 1, name = "predictions")    

        # mean of cross-entropy loss
        with tf.name_scope("compute_loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits = self.scores, labels = self.input_y)
            self.loss = tf.reduce_mean(losses)

    def Train(self, train_file, model_file, 
              iteration, max_token, batch_size, 
              embedding_dim, filter_sizes = [3, 4, 5], 
              channel = 1, verbose = False):
    
        reader = DataReader()
        config, batches = reader.Read(train_file, batch_size, max_token)
        
        self.max_token = max_token
        self.auxiliary_dim = config["auxiliary_dim"]

        model_dir = os.path.dirname(model_file)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        # A Graph contains operations and tensors.
        # with keyword to specify that ops created within the scope of 
        # a block should be added to this graph
        self.graph = tf.Graph()
        with self.graph.as_default():
            session_conf = tf.ConfigProto(
              allow_soft_placement = True,
              log_device_placement = False)
            self.sess = tf.Session(config = session_conf)
            with self.sess.as_default():
                # remember some configs of the model.
                tensor_max_token = tf.constant(self.max_token, name = "max_token")
                tensor_auxiliary_dim = tf.constant(self.auxiliary_dim, name = "auxiliary_dim")
                self.BuildNet(
                    seq_len = max_token,
                    num_classes = config["classes"],
                    vocab_size = config["vocab_size"],
                    embedding_dim = embedding_dim,
                    filter_sizes = filter_sizes,
                    channel = channel,
                    auxiliary_dim = config["auxiliary_dim"])
                
                # define optimization steps.
                global_step = tf.Variable(0, name="global_step", trainable=False)
                optimizer = tf.train.AdamOptimizer(1e-3)
                grads_and_vars = optimizer.compute_gradients(self.loss)
                train_op = optimizer.apply_gradients(grads_and_vars, global_step = global_step)
                
                # add summary variables.
                if verbose:
                    tf.summary.scalar('loss', self.loss)
                    summary_op = tf.summary.merge_all()
                    summary_writer = tf.summary.FileWriter(os.path.join(model_dir, "summary"),
                                                           self.sess.graph)

                self.sess.run(tf.global_variables_initializer())

                def train_step(x_batch, aux_batch, y_batch):
                    feed_dict = {
                      self.input_x: x_batch,                     
                      self.input_aux: aux_batch,
                      self.input_y: y_batch
                    }
                    
                    if verbose:
                        step, _, summary = self.sess.run([global_step, train_op, summary_op], feed_dict)
                        summary_writer.add_summary(summary, step)
                    else:
                        self.sess.run([train_op], feed_dict)
                
                for i in range(iteration):
                    for x, aux, y in batches:
                        train_step(x, aux, y)
                    print("iteration %d finish" % i)

                saver = tf.train.Saver()
                save_path = saver.save(self.sess, model_file)
                print("model saved in file: %s" % save_path)

    def Load(self, model_file):
        self.graph = tf.Graph()
        # with keyword to specify that ops created within the scope of a block should be added to this graph
        with self.graph.as_default():
            session_conf = tf.ConfigProto(allow_soft_placement = True,
                                          log_device_placement = False)
            self.sess = tf.Session(config = session_conf)
            with self.sess.as_default():
                # read graph defination as well
                saver = tf.train.import_meta_graph(model_file + ".meta")
                saver.restore(self.sess, model_file)
                self.input_x = self.sess.graph.get_tensor_by_name("input_x:0")
                self.input_aux = self.sess.graph.get_tensor_by_name("input_aux:0")
                self.input_y = self.sess.graph.get_tensor_by_name("input_y:0")
                self.probs = self.sess.graph.get_tensor_by_name("probs:0")
                self.predictions = self.sess.graph.get_tensor_by_name("predictions:0")

                # restore configs(max_token, auxiliary_dim) first.
                tensor_max_token = self.sess.graph.get_tensor_by_name("max_token:0")
                tensor_auxiliary_dim = self.sess.graph.get_tensor_by_name("auxiliary_dim:0")
                self.max_token, self.auxiliary_dim = self.sess.run([tensor_max_token, tensor_auxiliary_dim])
                print("model loaded. max_token %d, auxiliary_dim %d" % \
                      (self.max_token, self.auxiliary_dim))

    def Predict(self, xs, auxs):
        with self.graph.as_default():
            with self.sess.as_default():
                padded_xs = []
                padded_auxs = []
                for x in xs:
                    if len(x) >= self.max_token:
                        padded_xs.append(x[0:self.max_token])
                    else:
                        padded_xs.append(x + [0] * (self.max_token - len(x)))
                for aux in auxs:
                    zeros = [0.0] * self.auxiliary_dim
                    if self.auxiliary_dim > 0:
                        for idx, v in aux:
                            zeros[idx] = v
                    padded_auxs.append(zeros)
                
                np_xs = np.array(padded_xs)
                np_auxs = np.array(padded_auxs)
                feed_dict = {self.input_x: np_xs,                     
                             self.input_aux: np_auxs}
                predictions = self.sess.run(self.predictions, feed_dict)
                probs = self.sess.run(self.probs, feed_dict)
                return (predictions, probs)

    def Test(self, test_file):
        reader = DataReader()
        config, batches = reader.Read(test_file, sys.maxint, self.max_token)

        ys = batches[0][2]
        predictions, probs = self.Predict(batches[0][0], batches[0][1])
        tp, fn, total = 0, 0, 0
        for y, prediction in zip(ys.tolist(), predictions):
            total += 1
            label = max(enumerate(y),key=lambda x: x[1])[0]
            if label == prediction:
                tp += 1
        print("test done. %d/%d passed" % (tp, total))
        return (tp, total)
