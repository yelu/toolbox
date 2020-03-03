import tensorflow as tf

a = tf.one_hot([2, 3, 4],5)

sess = tf.Session()
sess.run(tf.initialize_all_variables())
print(sess.run(a))
