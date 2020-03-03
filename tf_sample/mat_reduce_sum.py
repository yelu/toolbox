import tensorflow as tf

a = tf.Variable(tf.random_uniform([2, 3, 4], 0, 10, dtype=tf.int32, seed=0))

sum = tf.reduce_sum(a, 2)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
print(sess.run(a))
print(sess.run(sum))
