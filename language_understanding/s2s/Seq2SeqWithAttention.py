import os,sys
import pickle
import json
import time
import csv
import tensorflow as tf
import numpy as np
from random import shuffle
from .Encoder import Encoder
from .DecoderWithAttention import DecoderWithAttention
from .DataReader import DataReader

class Seq2SeqWithAttention(object):

    def __init__(self):
        tf.logging.set_verbosity(tf.logging.WARN)
        pass 

    def BuildGraphForTrain(self, 
                            batch_size,
                            encoder_state_size,
                            encoder_vocab_size,
                            decoder_state_size,
                            decoder_vocab_size, 
                            dropout,
                            wb_init = tf.contrib.layers.xavier_initializer(),
                            encoder_embedding_init = tf.contrib.layers.xavier_initializer(),
                            decoder_embedding_init = tf.contrib.layers.xavier_initializer()):
        # [batch_size, num_steps]
        self.encoder_inputs = tf.placeholder(shape = [batch_size, None], 
                                             dtype = tf.int32,
                                             name="encoder_inputs")
        # [batch_size, num_steps, encoder_state_size]
        self.encoder_inputs_mask = tf.placeholder(shape = [batch_size, None],
                                                  dtype = tf.int32, 
                                                  name="encoder_inputs_mask") 

        self.decoder_inputs = tf.placeholder(shape = [batch_size, None],
                                             dtype = tf.int32,
                                             name="decoder_inputs") 
        self.decoder_outputs = tf.placeholder(shape = [batch_size, None],
                                             dtype = tf.int32,
                                             name="decoder_outputs")
        # [batch_size, num_steps, encoder_state_size]  
        self.decoder_outputs_mask = tf.placeholder(shape = [batch_size, None],
                                                   dtype = tf.int32,
                                                   name="decoder_outputs_mask")
        
        self.encoder = Encoder()  
        self.encoder_outputs_map = self.encoder.BuildGraph(inputs={"encoder_inputs":self.encoder_inputs,
                                                                   "encoder_inputs_mask":self.encoder_inputs_mask},
                                                            batch_size = batch_size,
                                                            encoder_state_size = encoder_state_size,
                                                            encoder_vocab_size = encoder_vocab_size,                                             
                                                            wb_init = wb_init,
                                                            encoder_embedding_init = encoder_embedding_init)
        self.decoder = DecoderWithAttention()
        self.decoder_outputs_map = self.decoder.BuildGraphForTrain(inputs={"decoder_inputs":self.decoder_inputs,
                                                                            "decoder_outputs":self.decoder_outputs,
                                                                            "decoder_outputs_mask":self.decoder_outputs_mask,
                                                                            "encoder_inputs_mask":self.encoder_inputs_mask,
                                                                            "encoder_states":self.encoder_outputs_map["encoder_states"]},
                                                                    batch_size = batch_size,
                                                                    encoder_state_size = encoder_state_size,
                                                                    decoder_state_size = decoder_state_size,
                                                                    decoder_vocab_size = decoder_vocab_size,
                                                                    dropout = dropout,                                                          
                                                                    wb_init = wb_init,
                                                                    decoder_embedding_init = decoder_embedding_init)
        self.loss = self.decoder_outputs_map["loss"]

    def BuildGraphForPredict(self, 
                             encoder_state_size,
                             encoder_vocab_size,
                             decoder_state_size,
                             decoder_vocab_size, 
                             decoder_go_symbol,
                             decoder_eos_symbol):
        batch_size = 1
        # [batch_size, num_steps]
        self.encoder_inputs = tf.placeholder(shape = [batch_size, None], 
                                             dtype = tf.int32,
                                             name="encoder_inputs")
        # [batch_size, num_steps, encoder_state_size]
        self.encoder_inputs_mask = tf.placeholder(shape = [batch_size, None],
                                                  dtype = tf.int32, 
                                                  name="encoder_inputs_mask")

        self.encoder = Encoder()  
        self.encoder.BuildGraph(inputs={"encoder_inputs":self.encoder_inputs,
                                        "encoder_inputs_mask":self.encoder_inputs_mask},
                                batch_size = 1,
                                encoder_state_size = encoder_state_size,
                                encoder_vocab_size = encoder_vocab_size,
                                wb_init = tf.constant_initializer(0.0),
                                encoder_embedding_init = tf.constant_initializer(0.0))

        self.encoder_states = tf.placeholder(shape = [None, 1, encoder_state_size],
                                             dtype = tf.float32,
                                             name = "encoder_states_1")
        self.decoder_state_pre = tf.placeholder(shape = [1, decoder_state_size],
                                                dtype = tf.float32,
                                                name = "decoder_state_pre")
        self.decoder_output_pre = tf.placeholder(shape = [1],
                                                dtype = tf.int32,
                                                name = "decoder_output_pre")
        self.decoder = DecoderWithAttention()
        self.decoder.BuildGraphForBeamSearch(inputs={"encoder_states":self.encoder_states,
                                                    "encoder_inputs_mask":self.encoder_inputs_mask,
                                                    "decoder_state_pre":self.decoder_state_pre,
                                                    "decoder_output_pre":self.decoder_output_pre},
                                            encoder_state_size = encoder_state_size,
                                            decoder_state_size = decoder_state_size,
                                            decoder_vocab_size = decoder_vocab_size,
                                            decoder_go_symbol = decoder_go_symbol,
                                            decoder_eos_symbol = decoder_eos_symbol)

    def Train(self,            
              data_file,
              vocab_keep_ratio,
              max_token,
              model_file,
              batch_size,
              encoder_state_size,
              decoder_state_size,
              dropout,
              iteration,
              verbose = False):
        
        model_dir = os.path.dirname(model_file)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        sorted_data_file = os.path.join(model_dir, "train.sorted.tsv")
        self._PreprocessData(data_file, sorted_data_file)

        self.src_seq_reader = DataReader()
        self.src_seq_reader.Load(sorted_data_file, "src_seq", max_token, vocab_keep_ratio)

        self.dst_seq_reader = DataReader()
        self.dst_seq_reader.Load(sorted_data_file, "dst_seq", max_token, vocab_keep_ratio)
        
        # pickle reader
        # TODO: need to remove loaded data before pickle.
        with open(os.path.join(model_dir, 'src_vocab_processor.p'), 'wb') as f:
            pickle.dump(self.src_seq_reader, f)
        with open(os.path.join(model_dir, 'dst_vocab_processor.p'), 'wb') as f:
            pickle.dump(self.dst_seq_reader, f)

        # remember some configs of the model, for future model re-loading.
        model_config = {"encoder_state_size":encoder_state_size, 
                        "decoder_state_size":decoder_state_size,
                        "max_token":max_token}
        with open(os.path.join(model_dir, "model_config.json"), 'w') as f:
            json.dump(model_config, f)

        self.graph = tf.Graph()
        with self.graph.as_default():
            session_conf = tf.ConfigProto(
              allow_soft_placement = True,
              log_device_placement = False)
            self.sess = tf.Session(graph = self.graph, config = session_conf)            
            with self.sess.as_default():
                self.BuildGraphForTrain(batch_size = batch_size,
                                        encoder_state_size = encoder_state_size,
                                        encoder_vocab_size = self.src_seq_reader.GetVocabularySize(),
                                        decoder_state_size = decoder_state_size,
                                        decoder_vocab_size = self.dst_seq_reader.GetVocabularySize(),
                                        dropout = dropout)         
                
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
                saver = tf.train.Saver()

                def train_step(encoder_inputs, encoder_inputs_mask,
                               decoder_inputs, decoder_outputs, decoder_outputs_mask):
                    feed_dict = {
                                  self.encoder_inputs: encoder_inputs,
                                  self.encoder_inputs_mask:encoder_inputs_mask,
                                  self.decoder_inputs:decoder_inputs,
                                  self.decoder_outputs:decoder_outputs,
                                  self.decoder_outputs_mask:decoder_outputs_mask
                                }
                    if verbose:
                        step, _, summary = self.sess.run([global_step, train_op, summary_op], feed_dict)
                        summary_writer.add_summary(summary, step)
                    else:
                        self.sess.run([train_op], feed_dict)
                
                start = time.time()
                src_seqs = list(self.src_seq_reader.Read(batch_size, False, False))
                input_dst_seqs = list(self.dst_seq_reader.Read(batch_size, True, False))
                output_dst_seqs = list(self.dst_seq_reader.Read(batch_size, False, True))
                zipped = list(zip(src_seqs, input_dst_seqs, output_dst_seqs))
                shuffle(zipped)
                for i in range(iteration):              
                    for j, batch in enumerate(zipped):
                        end = time.time()
                        print("\riteration=%d batch=%d time_elapsed=%s" % (i, j, str(end-start)), end="")
                        train_step(encoder_inputs = np.array(batch[0][0]),
                                   encoder_inputs_mask = np.array(batch[0][1]),
                                   decoder_inputs = np.array(batch[1][0]),
                                   decoder_outputs = np.array(batch[2][0]),
                                   decoder_outputs_mask = np.array(batch[2][1]))
                    # refer to https://www.tensorflow.org/api_docs/python/tf/train/Saver#save
                    # to control the behavior of save.
                    save_path = saver.save(self.sess, model_file, write_meta_graph=False, global_step = i)
                    print("\nmodel saved to \"%s\"" % save_path)

    def Load(self, model_file):
        model_dir = os.path.dirname(model_file)
        with open(os.path.join(model_dir, 'src_vocab_processor.p'), "rb") as f:
            self.src_seq_reader = pickle.load(f)
        with open(os.path.join(model_dir, 'dst_vocab_processor.p'), "rb") as f:
            self.dst_seq_reader = pickle.load(f)
        
        # restore some config variables first.
        with open(os.path.join(model_dir, "model_config.json"), 'r') as f:
            model_config = json.loads(f.read())

        self.decoder_state_size = model_config["decoder_state_size"]
        self.max_token = model_config["max_token"]
       
        self.graph = tf.Graph()
        session_conf = tf.ConfigProto(allow_soft_placement = True,
                                      log_device_placement = False)
        self.sess = tf.Session(graph = self.graph, config = session_conf)
        with self.graph.as_default(): 
            self.decoder_outputs = self.BuildGraphForPredict(
                                    encoder_state_size = model_config["encoder_state_size"],
                                    encoder_vocab_size = self.src_seq_reader.GetVocabularySize(),
                                    decoder_state_size = model_config["decoder_state_size"],
                                    decoder_vocab_size = self.dst_seq_reader.GetVocabularySize(), 
                                    decoder_go_symbol = self.dst_seq_reader.GetGoSymbol(),
                                    decoder_eos_symbol = self.dst_seq_reader.GetEOSSymbol())
            # here we only load variables, don't load model defination, 
            # since we need a different graph as training.
            saver = tf.train.Saver()
            ckpt = tf.train.get_checkpoint_state(model_dir)
            saver.restore(self.sess, ckpt.model_checkpoint_path)
            print("model loaded from \"%s\"" % ckpt.model_checkpoint_path)

    def Predict(self, query, beam_size = 4):
        tokens = query.split()
        if len(tokens) == 0:
            return None
        vec, mask, _ = self.src_seq_reader.Transform(tokens)
        feed_dict = {self.encoder_inputs: [vec],
                     self.encoder_inputs_mask:[mask]}
        encoder_states = self.sess.run(self.encoder.outputs["encoder_states"], feed_dict)
        predictions = self.BeamSearch(encoder_states, [mask], beam_size, self.decoder_state_size)
        return [self.dst_seq_reader.Lookup(prediction) for prediction in predictions]

    def BeamSearch(self, 
                    encoder_states, encoder_inputs_mask,
                    beam_size, decoder_state_size):
        candidates = [{"decoder_outputs" : [self.dst_seq_reader.GetGoSymbol()],
                       "decoder_state" : np.zeros([1, decoder_state_size]),
                       "score" : 0.0} ]
        # allow a max len to be 64 except for GO and EOS.
        # we will remove first(GO) and last(EOS) element when returning results.
        max_steps = self.max_token + 2
        dead_size = 0
        outputs = []
        for step in range(max_steps):
            new_candidates = []
            #print("##########")
            for output_pre in candidates:
                decoder_output_pre = [output_pre["decoder_outputs"][-1]]
                decoder_state_pre = output_pre["decoder_state"]
                feed_dict = {
                                self.encoder_states:encoder_states,
                                self.encoder_inputs_mask:encoder_inputs_mask,
                                self.decoder_state_pre:decoder_state_pre,
                                self.decoder_output_pre:decoder_output_pre,
                }
                decoder_output_prob, decoder_state = \
                    self.sess.run([self.decoder.outputs["decoder_output_prob"],
                                   self.decoder.outputs["decoder_state"]], feed_dict)
                neg_log_scores_np = (0.0 - np.log(decoder_output_prob))[0]
                neg_log_scores = neg_log_scores_np.tolist()
                sort_index = np.argsort(neg_log_scores_np).tolist()              
                for index in sort_index[0:beam_size - dead_size]:
                    new_candidates.append({"decoder_outputs":output_pre["decoder_outputs"] + [index],
                                           "decoder_state":decoder_state,
                                           "score":output_pre["score"] + neg_log_scores[index]})
            new_candidates_sorted = sorted(new_candidates, key = lambda x:x["score"])[0:beam_size - dead_size]
            candidates = []
            for candidate in new_candidates_sorted:
                #print((candidate["decoder_outputs"], candidate["score"]))
                if candidate["decoder_outputs"][-1] == self.dst_seq_reader.GetEOSSymbol():
                    outputs.append(candidate)
                    dead_size += 1
                else:
                    candidates.append(candidate)
            if len(outputs) >= beam_size:
                break

        if len(outputs) == 0:
            outputs = candidates
        outputs = sorted(outputs, key = lambda x:x["score"])
        return [x["decoder_outputs"][1:-1] for x in outputs]

    def _PreprocessData(self, data_file, sorted_data_file):
        with open(data_file, 'r', encoding="utf-8") as src_file, \
             open(sorted_data_file, 'w', encoding = 'utf-8') as dst_file:
            reader = csv.DictReader(src_file, delimiter='\t')
            lines = []          
            for row in reader:
                src_seq, dst_seq = row['src_seq'].strip(), row['dst_seq'].strip()
                tokenized_src_seq, tokenized_dst_seq = src_seq.split(), dst_seq.split()
                if len(tokenized_src_seq) == 0 or len(tokenized_dst_seq) == 0:
                    continue
                else:
                    lines.append((tokenized_src_seq, tokenized_dst_seq))
            # sort sentences by their token nums, this could reduce padding cost.
            lines_sorted = sorted(lines, key = lambda x:(len(x[0]) + len(x[1]), len(x[0]), len(x[1])))
            print("src_seq\tdst_seq", file = dst_file)          
            for src, dst in lines_sorted:
                print("%s\t%s" % (" ".join(src), " ".join(dst)), file = dst_file)
