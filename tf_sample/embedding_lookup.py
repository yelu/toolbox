import tensorflow as tf

params = tf.Variable(tf.random_uniform([2, 3,4], 0, 10, dtype=tf.int32, seed=0))
ids = tf.Variable(tf.random_uniform([5], 0, 3, dtype=tf.int32, seed=0))

embed  = tf.nn.embedding_lookup(params,ids)

sess = tf.Session()
sess.run(tf.initialize_all_variables())
print(sess.run(params))
print(sess.run(ids))
print(sess.run(embed))
