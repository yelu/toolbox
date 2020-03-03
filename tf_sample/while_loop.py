import tensorflow as tf

i = tf.constant(0)
res = tf.Variable(tf.zeros([1,0], dtype=tf.int32))
c = lambda i, res: tf.less(i, 10)
b = lambda i, res: [tf.add(i, 1), tf.concat([res, tf.expand_dims(tf.expand_dims(i, 0), 0)], axis=1)]
r = tf.while_loop(c, b, 
                 loop_vars = [i, res],
                 shape_invariants=[i.get_shape(), tf.TensorShape([1, None])])

sess = tf.Session()
sess.run(tf.initialize_all_variables())
print(sess.run(r))
