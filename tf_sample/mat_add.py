import tensorflow as tf

a = tf.get_variable('a',
                    shape=[2, 3, 4],
                    initializer=tf.contrib.layers.xavier_initializer())

b = tf.get_variable('b',
                    shape=[3, 4],
                    initializer=tf.contrib.layers.xavier_initializer())
sum = tf.add(a, b)
sess = tf.Session()
sess.run(tf.initialize_all_variables())
print(sess.run(a))
print(sess.run(b))
print(sess.run(sum))
