import tensorflow as tf

a = tf.Variable(tf.random_uniform([2, 3, 2], 1, 10, dtype=tf.float32, seed=0))
b = tf.Variable(tf.random_uniform([2, 3], 0, 2, dtype=tf.int32, seed=0))

losses = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=a, labels=b)
loss = tf.reduce_sum(losses)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
print(sess.run(a))
print(sess.run(b))
print(sess.run(losses))
print(sess.run(loss))
