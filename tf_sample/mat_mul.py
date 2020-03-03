import tensorflow as tf

'''
a = tf.get_variable('a',
                    shape=[4, 3, 2],
                    initializer=tf.constant_initializer(0.1))

b = tf.get_variable('b',
                    shape=[2, 3],
                    initializer=tf.constant_initializer(0.2))
mul = tf.reshape(tf.matmul(tf.reshape(a, [-1, 2]), b), [4, -1, 3])
sess = tf.Session()
sess.run(tf.initialize_all_variables())
print(sess.run(mul))
'''

'''
a = tf.get_variable('a',
                    shape=[1, 3],
                    initializer=tf.contrib.layers.xavier_initializer())

b = tf.get_variable('b',
                    shape=[1, 2, 3],
                    initializer=tf.contrib.layers.xavier_initializer())
mul = tf.matmul(a, b)
sess = tf.Session()
sess.run(tf.initialize_all_variables())
print(sess.run(a))
print(sess.run(b))
print(sess.run(mul))
'''

a = tf.Variable(tf.random_uniform([2,3], 0, 10, dtype=tf.int32, seed=0))
b = tf.Variable(tf.random_uniform([2,3], 0, 10, dtype=tf.int32, seed=0))
c = tf.Variable(tf.random_uniform([2], 0, 10, dtype=tf.int32, seed=0))

mul_a_b = a * b
mul_c_a = a * (1-tf.expand_dims(c, -1))
sess = tf.Session()
sess.run(tf.initialize_all_variables())
print(sess.run(a))
print(sess.run(b))
print(sess.run(c))
print(sess.run(mul_a_b))
print(sess.run(mul_c_a))

