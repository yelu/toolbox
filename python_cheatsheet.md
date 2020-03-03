# python cheatsheet

## 列表zip

	a=[1,2,3]
	b=[4,5,6]
	c=[7,8,9]
	zip(a,b,c)
	[(1, 4, 7), (2, 5, 8), (3, 6, 9)]
	d=[a,b,c]
	zip(*d)
	[(1, 4, 7), (2, 5, 8), (3, 6, 9)]

## 时间操作

时间差值计算

	import datetime
	import time
	start = datetime.datetime(2013,4,8,13,10,0)
	end = start + datetime.timedelta(minutes=2)
	print "%d-%.2d-%.2d %.2d:%.2d:%.2d"%(end.year, end.month, end.day, end.hour, end.minute, end.second)
	2013-04-08 13:12:00

获取当前时间

	curr_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

## json 格式化输出

使用json格式将字典或数组漂亮地格式化输出

	import json
	data = [{"a":1,"b":2},{"c":3,"d":4}]
	print json.dumps(data, sort_keys = False, indent = 4)
	[
	    {
	        "a": 1,
	        "b": 2
	    },
	    {
	        "c": 3,
	        "d": 4
	    }
	]

## 正则表达式替换子串

使用正则表达式模块的`re.sub`方法可以替换匹配出的字符串。

例如，在如下字符串的所有xml tag前加上O tag:

```python
import re

xmlStr = "set alarm at <start_time> ten fifty </start_time>"
startPattern = re.compile(r'(<[a-zA-Z0-9_]+>)')
xmlStr = startPattern.sub(r'</O>\1', xmlStr)
print xmlStr

#set alarm at </O><start_time> ten fifty </start_time>
```

目标字符串可以使用lamnda表达式动态生成：

```python
import re

text = "k1,k2 : ${k1,k2} !"
d = {"k1":"v1", "k2":"v2"}
replaced = re.sub(r'\$\{([a-z0-9]*)\,([a-z0-9]*)\}', (lambda m: d[m.group(1)] + "," + d[m.group(2)]), text)
print replaced
```

## 正则表达式查找子串

```python
pattern = re.compile(r'<(.*?)>(.*?)</(.*?)>')
matches = pattern.findall(line)
if matches:
    for match in matches:
        print(match)
```

In general, findall will return a tuple of all the groups of objects in the regular expression that are **enclosed within parentheses**.

## list逆序遍历

    a=[1,2,3,4,5]
    >>> for i in a[::-1]:
    ...     print i
    ...
    5
    4
    3
    2
    1

## split压缩连续分隔符

string的split方法的分割符参数如果不是None，则多个连续的分隔符不会被压缩，此时可以使用正则表达式模块re的split方法，其分隔符参数是一个正则表达式。

    import re
    a="/home//work/yelu"
    a.split('/')
    ['', 'home', '', 'work', 'yelu']
    re.split('/+', a)
    ['', 'home', 'work', 'yelu']

## 生成元素相同的列表

    >>> [0]*10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


## 变量交换

    >>> a='hello'
    >>> b=123
    >>> print a,b
    hello 123
    >>> a,b=b,a
    >>> print a,b
    123 hello


## 返回多个值

    >>> def func():
    	a,b='hello',123
    	return a,b

    >>> c,d=func()
    >>> print c,d
    hello 123


## zip

    >>> a=[1,2];b=['a','b','c']
    >>> c=zip(a,b)
    >>> print c
    [(1, 'a'), (2, 'b')]
    >>> d=zip(*c)
    >>> print d
    [(1, 2), ('a', 'b')]

## 字典操作

    #批量初始化
    >>> {}.fromkeys(['a','b','c'], 0)
    {'a': 0, 'c': 0, 'b': 0}

    #用setdefault移除if/else
    <code python>
    >>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    >>> d = {}
    >>> for k, v in s:
    	d.setdefault(k, []).append(v)

    >>> d
    {'blue': [2, 4], 'red': [1], 'yellow': [1, 3]}

    #由list构造字典
    >>> a=[1,1,2];b=['a','b','c']
    >>> c=zip(a,b)
    >>> dict(c)
    {1: 'b', 2: 'c'}

    #排序
    # 1.按key排序
    >>> d={"ok":1,"no":2}
    >>> sorted(d.items(), key=lambda d:d[0])
    [('no', 2), ('ok', 1)]
    # 2.按value排序
    >>> e={"ok":2,"no":1}
    >>> sorted(e.items(), key=lambda x:x[1])
    [('no', 1), ('ok', 2)]
    # 3.逆序
    >>> f={"ok":1,"no":2}
    >>> sorted(f.items(), key=lambda x:x[1], reverse=True)
    [('no', 2), ('ok', 1)]

## 列表操作

    # 列表输出
    >>> '\t'.join(map(str,[1,2,3]))
    '1\t2\t3'
    # 列表批量类型转换
    # 前2列int，后5列float，最后1列字符串
    >>> line='1\t2\t3.0\t4.0\t5.0\t6.0\t7.0\thello'
    >>> func=[int]*2 + [float]*5 + [str]
    >>> map(lambda x,y:x(y), func, line.strip().split('\t'))
    [1, 2, 3.0, 4.0, 5.0, 6.0, 7.0, 'hello']
    # 排序。使用sorted，见字典操作

## 链式比较
    <code python>
    >>> x = 5
    >>> 1 < x < 10
    True
    >>> 10 < x < 20
    False
    >>> x < 10 < x*10 < 100
    True
    >>> 10 > x <= 9
    True
    >>> 5 == x > 4
    True
    </code>

按照通常的逻辑，1<x<10可能会被解析为1<x，返回true，true<10，返回true，整个表达式返回true。其实，python会将其解析为1<x and x<10。

## enumerate

    <code python>
    >>> a = ['a', 'b', 'c', 'd', 'e']
    >>> for index, item in enumerate(a): print index, item
    ...
    0 a
    1 b
    2 c
    3 d
    4 e
    >>>

    >>> f1 = open('test.txt','r')
    >>> for index, line in enumerate(f1,1):
            print index,line.strip()
    1 1,2,3,4
    2 1,3,4
    3 1,2,4
    4 1,2,3
    </code>

## 迭代器

以下代码可以产生一个迭代器：

    <code python>
    x=(n for n in foo if bar(n))
    </code>

加上()使得接下来可以使用for来遍历结果：

    <code python>
    for n in x:
    </code>

这种写法的优势在于，python不会缓存上一步的计算结果，而是“按需执行”：如果后一个for说"我需要下一个值"，上一个for才会继续执行，知道输出一个值。相比下面的写法有空间复杂度上的优势：

    <code python>
    x = [n for n in foo if bar(n)]
    </code>

对多个list同时遍历并组合也是可行的：

    <code python>
    >>> n = ((a,b) for a in range(0,2) for b in range(4,6))
    >>> for i in n:
    ...   print i

    (0, 4)
    (0, 5)
    (1, 4)
    (1, 5)
    </code>

## groupby-简化hadoop reduce程序

通常情况下，hadoop reduce程序包含两段相同的数据输出代码，而且程序的流程控制代码和逻辑代码混合在一起：

    <code python>
    pre_key = None
    curr_key = None
    total = 0

    for line in sys.stdin:
        curr_key, value = line.strip().split('\t', 1)
        if curr_key == pre_key:
            total += int(value)
        else:
            if pre_key:
                # write result to STDOUT
                print '%s\t%d' % (curr_key_word, total)
                total = 0
            pre_key = curr_key

    # do not forget to output the last word if needed!
    if curr_key:
        print '%s\t%s' % (current_word, current_count)
    </code>

使用groupby来取出重复代码：

    <code python>
    from itertools import groupby
    from operator import itemgetter

    def reduce_fun(key_values):
    	for key_value in key_values:
    		# do sth

    def read_mapper_output(f):
    	for line in f:
    		fields = line.strip().split('\t')
    		yield fields

    def main():
    	data = read_mapper_output(sys.stdin)
    	# 用itemgetter挑选列，按照这些列将输入流切割为多个迭代器
    	for curr_key, key_values in groupby(data, itemgetter(0)):
    		reduce_fun(key_values)
    </code>

## iter

iter() can take a callable argument,For instance:

    <code python>
    def seek_next_line(f):
        for c in iter(lambda: f.read(1),'\n'):
            pass
    </code>

The iter(callable, until_value) function repeatedly calls callable and yields its result until until_value is returned.

## 生成器

    <code python>
    >>> def fibonacci():
    	a,b=0,1
    	while True:
    		yield b
    		a,b=b,a+b


    >>> for num in fibonacci():
    	if num > 100: break
    	print num

    1
    1
    2
    3
    5
    8
    13
    21
    34
    55
    89
    </code>

## 函数式编程map/reduce

**map**

    <code python>
    #遍历list中元素执行指定操作
    #空列表引发异常
    >>> map(lambda x:x+1, [1,2,3,4,5])
    [2, 3, 4, 5, 6]
    </code>

**reduce**

    #以指定规则合并list元素
    #指定默认值避免空列表异常
    <code python>
    >>> reduce(lambda x,y:x+y, [1,2,3,4,5], 0)
    15
    </code>

**filter**

    <code python>
    #以指定规则过滤list元素
    >>> filter(lambda x:x>4, [1,2,3,4,5])
    [5]
    </code>

**lambda**

    <code python>
    #随地定义函数
    >>> a=lambda x:x+1
    >>> a(1)
    2
    </code>

## named farmating

使用字典中的值来替换并格式化字符串。

    <code python>
    >>> def func(**kwargv):
    	print "The %(num)s is %(value)d." % kwargv


    >>> func(num="number",value=12)
    The number is 12.
    </code>

logging库的log格式化代码就是用了这种格式化方式：

    <code python>
    formatter = logging.Formatter(’%(asctime)s %(levelname)s %(message)s’)
    </code>

## with...as...

详细解释见[python with statement](http://effbot.org/zone/python-with-statement.htm)。最常见的应用场合为(但绝对不仅限于该场合)：

- 安全地释放外部资源

**安全地操作文件**

open会保证无论with/as代码块中的代码发生什么异常均会执行文件的close方法。

    <code python>
    with open("x.txt") as f:
        data = f.read()
        do something with data
    </code>

**安全地操作数据库**

在操作关联外部资源的对象时，通常需要特别注意异常时资源的释放。外部资源的一个例子是上面提到的文件，另外一个常见例子就是数据库。如果想让数据库操作也能像文件操作那样具有自动资源管理特性，需要自己写一个类似open的函数。实现这个类似open的函数有两种方式，实现一个类和借助装饰器decotator特性(该装饰器已经在库中实现了)，借助装饰器代码更加简洁：

    <code python>
    from contextlib import contextmanager

    @contextmanager
    def db_transaction(connection):
        cursor = connection.cursor()
        try:
            yield cursor
        except:
            connection.rollback()
            raise
        else:
            connection.commit()

    db = DatabaseConnection()
    with db_transaction(db) as cursor:
        ...
    </code>

## 装饰器decorator

Decorator其实就是一个对函数的封装，它可以让你不改变函数本身的情况下对函数的执行进行干预，比如在执行前进行权限认证，日志记录，甚至修改传入参数，或者在执行后对返回结果进行预处理，甚至可以截断函数的执行等等。在python中以符号@开头的语句即为使用decorator特性。常见的例子包括@classmethod、@staticmethod，@property等，这些是已经存在于python库中事先定义好的修饰器。

decorator是python中比较高级的语言特性，理解起来不想其它特性那么直接。很多介绍性的文章让问十分困惑，但以下两篇绝对让人受益匪浅：

- [Python Decorators Don't Have to be (that) Scary](http://www.siafoo.net/article/68)
- [Decorators I/II/III](http://www.artima.com/weblogs/viewpost.jsp?thread=240808)
- [Decorators I/II/III 中文版](http://blog.csdn.net/beckel/article/details/3585352)

下面的例子定义了一个修饰器print_args，被它修饰的函数可以在调用前打印出参数列表:

    <code python>
    >>> def print_args(function):
    >>>     def wrapper(*args, **kwargs):
    >>>         print 'Arguments:', args, kwargs
    >>>         return function(*args, **kwargs)
    >>>     return wrapper

    >>> @print_args
    >>> def write(text):
    >>>     print text

    >>> write('foo')
    Arguments: ('foo',) {}
    foo
    </code>

类也可以作为修饰器，前提是该类必须实现__call__方法(__call__方法是一个特殊的方法，它使得调用该类的对象就是调用自由函数一样，这类似于C++中通过重载类的operator()来定义仿函数)：

    <code python>
    class entryExit(object):
        def __init__(self, f):
            self.f = f

        def __call__(self):
            print "Entering", self.f.__name__
            self.f()
            print "Exited", self.f.__name__

    @entryExit
    def func1():
        print "inside func1()"

    func1()
    func2()

    # output:

    Entering func1
    inside func1()
    Exited func1

    </code>


**decorator与AOP**

AOP面向切面编程(也叫面向方面)：Aspect Oriented Programming(AOP)，是目前软件开发中的一个热点，也是Spring框架中的一个重要内容。利用AOP可以对业务逻辑的各个部分进行隔离，从而使得业务逻辑各部分之间的耦合度降低，提高程序的可重用性，同时提高了开发的效率。AOP常见的场合包括：日志记录，性能统计，安全控制，事务处理，异常处理等等。

通过以上的例子，可以看出decorator本身已经有很多AOP的影子了：Decorators允许在函数和类中嵌入或修改代码。例如，假设你想在一个函数的入口和出口处做点手脚(比如做一些安全、跟踪和锁等等一切AOP标准操作)。

## descriptor

Descriptor是访问对象成员时的一个中间层，为我们提供了自定义对象成员访问的方式。Descriptor的定义很简单，如果一个类包含以下三个方法（之一），则可以称之为一个Descriptor：

    object.__get__(self, instance, owner) #成员被访问时调用，instance为成员所属的对象、owner为instance所属的类型
    object.__set__(self, instance, value) #成员被赋值时调用
    object.__delete__(self, instance) #成员被删除时调用

以下为一些内置的descriptor：

classmethod：编译器并没有为其提供专门的语法规则，而是使用Descriptor返回instancemethod来封装func，从而实现类似obj.func()的调用方式；

staticmethod：decorator将创建一个StaticMethod并在其中保存func对象，StaticMethod是一个Descriptor，其__get__函数中返回前面所保存的func对象；

property：创建一个property对象，在其__get__、__set__和__delete__方法中分别执行构造对象是传入的fget、fset、和fdel函数。现在知道为什么Property只提供这三个函数作为参数么？

一个使用descriptor的例子：

    <code python>
    class RevealAccess(object):
        """A data descriptor that sets and returns values
           normally and prints a message logging their access.
        """

        def __init__(self, initval=None, name='var'):
            self.val = initval
            self.name = name

        def __get__(self, obj, objtype):
            print 'Retrieving', self.name
            return self.val

        def __set__(self, obj, val):
            print 'Updating' , self.name
            self.val = val

    >>> class MyClass(object):
        x = RevealAccess(10, 'var "x"')
        y = 5

    >>> m = MyClass()
    >>> m.x
    Retrieving var "x"
    10
    >>> m.x = 20
    Updating var "x"
    >>> m.x
    Retrieving var "x"
    20
    >>> m.y
    5
    </code>

python有内置的descriptor来简化这一操作--property：

    <code property>
    class C(object):
        def getx(self): return self.__x
        def setx(self, value): self.__x = value
        def delx(self): del self.__x
        x = property(getx, setx, delx, "I'm the 'x' property.")
    </code>

等等，其实还有一种控制属性访问的方法：使用@property

    <code python>
    class C(object):
        def __init__(self):
            self._x = None

        @property
        def x(self):
            """I'm the 'x' property."""
            return self._x

        @x.setter
        def x(self, value):
            self._x = value

        @x.deleter
        def x(self):
            del self._x
    </code>

## 调用其他程序

    <code python>
    #方法一，支持nohup的调用
    cmd = "nohup ./bin/broker &"
    log.info(cmd)
    ret = os.system(cmd)
    ret >>= 8
    if ret:
        raise RuntimeError, "%s failed with %d."%(cmd, ret)
    #方法二
    import commands
    cmd = "kill %d"%pid
    log.info(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status:
        raise RuntimeError, "%s failed. [ret:%d][%s]."%(cmd, status, output)
    </code>

## 根据端口获得pid(linux only)

    <code python>
    def get_pid(port):
            '''detect process id by port.'''
            cmd = "/usr/sbin/lsof -i:%d | grep ':%d'"%(port, port)
            log.info(cmd)
            (status, out) = commands.getstatusoutput(cmd)
            if status:
                raise RuntimeError, "failed to get pid."
            pid = out.strip().split()[1]
            return pid
    </code>

## 获取ip

    <code python>
    import socket
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    myaddr_int32 = map(int, myaddr.strip().split('.'))
    </code>

## 时间操作

    <code python>
    import time
    # 获取当前时间
    curr_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    </code>

## print格式化输出

    <code python>
    # print不输出换行，在末尾加上逗号。注意：print的以下用法在python 3以上版本已经不支持了。
    print "hello",
    </code>

## 退出进程

    <code python>
    #异常抛出版本，在退出程序的同时会抛出SystemExit异常，有两个问题：
    #1.通常会用try...except...将主程序包住，以接住其中抛出的任何异常，如果在程序执行途中用此方法退出会抛出一个异常导致程序进入异常处理代码，进而返回非期望的错误码；
    #2.会不友好地在退出时打印traceback信息，容易让人误认为程序执行异常。
    exit(0)
    #只返回退出码，无异常抛出，但不会刷新缓冲区，打印到标准输出流中的数据可能会部分丢失(该问题曾经碰到过)。
    os._exit(0)
    </code>

## 多行字符串

    s = """ this is a very
            long string if I had the
            energy to type more and more ..."""

            You can use single quotes(3 of them of course at start and end) and treat the resulting string s just like any other string.

NOTE: Just as with any string, anything between the starting and ending quotes becomes part of the string, so this example has a leading blank (as pointed out by @root45). This string will also contain both blanks and newlines.

I.e.,:

    ' this is a very\n        long string if I had the\n        energy to type more and more ...'

Finally, one can also construct long lines in Python like this:

    s = ("this is a very"
      "long string too"
      "for sure ..."
     )

which will not include any extra blanks or newlines:

    'this is a verylong string toofor sure ...'

## 文件名模糊查询

glob模块是最简单的模块之一，内容非常少。用它可以查找符合特定规则的文件路径名。跟使用windows下的文件搜索差不多。查找文件只用到三个匹配符："*", "?", "[]"。"*"匹配0个或多个字符；"?"匹配单个字符；"[]"匹配指定范围内的字符，如：[0-9]匹配数字。

glob.glob返回所有匹配的文件路径列表。它只有一个参数pathname，定义了文件路径匹配规则，这里可以是绝对路径，也可以是相对路径。

    import glob  

    #获取指定目录下的所有图片  
    print glob.glob(r"E:\Picture\*\*.jpg")  

    #获取上级目录的所有.py文件  
    print glob.glob(r'../*.py') #相对路径  

可迭代版本为glob.iglob。

## filter list

    >>> a = [1, 2, 3, 4, 2, 3, 4, 2, 7, 2]
    >>> a = [x for x in a if x != 2]
    >>> print a
    [1, 3, 4, 3, 4, 7]

## Python class

    class P(object):

        def __init__(self,x):
            self.x = x

        @staticmethod
        def the_static_method(x):
            print x

        @property
        def x(self):
            return self.__x

        @x.setter
        def x(self, x):
            if x < 0:
                self.__x = 0
            elif x > 1000:
                self.__x = 1000
            else:
                self.__x = x

## 遍历列表时获取编号

    list = [1,2,3,4]
    for num, line in enumerate(list):
        print "%s\t%s" % (num, line)

## clear punctuation in string

[string.translate](http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python) is the fastest.

	import string
	table = string.maketrans("","")
	res = str.translate(table, string.punctuation)

## get full class name

    obj.__module__ + "." + obj.__class__.__name__

## 反射

    def get_class( kls ):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m

## split file randomly

    def split_file(file_path, ratio, out_file_1, out_file_2):
        random.seed(3)
        with open(file_path, 'r') as in_file, \
             open(out_file_1, 'w') as out_file_1, \
             open(out_file_2, 'w') as out_file_2:
             for line in in_file:
                rnd_num = random.random()
                if rnd_num < ratio:
                    print >> out_file_1, line,
                else:
                    print >> out_file_2, line,

## data class

[The Ultimate Guide to Data Classes in Python 3.7](https://realpython.com/python-data-classes/)
