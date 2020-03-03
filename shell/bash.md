## 常用shell命令

### find查找文件

**在指定路径下递归查找文件**

    find /home/yelu -name "*.txt"

**按照修改时间查找**
    
    #最近一天内修改的文件
    find /home/yelu -mtime -1
    #一天前修改的文件
    find /home/yelu -mtime +1
    #多级通配符
    find /home/*/*.cpp -mtime +1

**使用正则表达式匹配文件名**
    
    find /home/yelu -regex “.*txt”

### xargs

把一个命令的输出，当作参数传给另一个命令。

    # 将查询到的文件mv为.bak
    # 推荐写法：
    find . -name "*" | xargs -I {} mv {} {}.bak
    # 一些版本的xargs有bug，需要用以下写法：
    find . -name "*" | xargs -i mv {} {}.bak

### 多任务管理：ctrl+z, fg, bg, jobs

ctrl+z:任务到后台，且暂停

fg:最后一个放入任务到前台，开始执行

bg:任务到后台，且执行

jobs:查看当前后台任务的状态

### ssh远程输出定向到本地

直接在ssh后输入要执行的命令即可。

    ssh yelu01@dbl-ao-ems00.dbl01 "cat /home/work/dr-ems/ems-count/log/logbk/storage.log.20130411* | awk '{if(match(\$0,/proctime:total:([0-9]+)/,arr)) print arr[1]}' | head" > ./tmp

注意加`""`，对于`$`需要转义。

还可以将本地保存的脚本作为参数运行，避免每次手动输入命令，以及字符转义等问题。

    ssh yelu01@dbl-ao-ems00.dbl01 'bash -s' < run_stat.sh > ./tmp

**ssh远程执行nohup命令**

Overcoming hanging

Note that nohupping backgrounded jobs is typically used to avoid terminating them when logging off from a remote SSH session. A different issue that often arises in this situation is that ssh is refusing to log off ("hangs"), since it refuses to lose any data from/to the background job(s). This problem can also be overcome by redirecting all three I/O streams:

    $ nohup ./myprogram > foo.out 2> foo.err < /dev/null &
    
Also note that a closing SSH session does not always send a HUP signal to depending processes. Among others, this depends on whether a pseudo-terminal was allocated or not.

### 查看目录的磁盘占用大小

    [yelu01@dbl-ao-ems01.dbl01.baidu.com ems-count]$ du -hs *
    8.5M    attila
    20M bin
    8.0K    conf
    0   load
    76G log

### 文件编码转换

    # gbk 转 utf8
    iconv -f gbk -t utf8 in_file > out_file

### 将一个文件拷贝到所有目录

    #将storage_reset.py拷贝到所有匹配./dr-ems-*/ems-tools/bin的目录下
    find ./dr-ems-*/ems-tools/bin -maxdepth 1 -type d -exec cp storage_reset.py {} \;

### 递归拷贝目录，但忽略特定文件（如隐藏文件）

    # a:保留权限，z：压缩传输，v：显示信息；--progress：显示进度；--exclude：忽略文件名匹配的文件，多个pattern需要写多个--exclude 
    rsync -azv --exclude='.*' --progress /source/ /destination
    # -u忽略本地修改过的文件
    rsync -azvu --exclude='.*' --progress /source/ /destination

### io状态查看

    iostat -d -x -k 1

详细说明参考[iostat][]。

### inode 与 ctime、mtime、atime

* ctime：create time，inode变动的时候会被更新。ls -lc查看ctime。stat可以查看文件的inode信息。inode包含文件的元信息：
* 文件的字节数
* 文件拥有者的User ID
* 文件的Group ID
* 文件的读、写、执行权限
* 文件的时间戳，共有三个：ctime指inode上一次变动的时间，mtime指文件内容上一次变动的时间，atime指文件上一次打开的时间。
* 链接数，即有多少文件名指向这个inode
* 文件数据block的位置
* atime：acess time，访问或执行的时候会被更新。ls -lu查看atime。
* mtime：modified time，文件内容改变是会被更新。ls -l默认显示mtime。
* linux 没有文件创建时间的概念。

### 磁盘、内存、进程和cpu信息查看

    # 查看所有硬盘分区
    sudo fdisk -l
    
    # 查看磁盘整体占用情况
    df -hl
    
    # 查看文件/文件夹大小
    du -h --max-depth=1 ./yelu/
    du -hs ./yelu/*
    

    # 查看内存总体使用情况
    [work@db-iris-tp00.db01.baidu.com ~]$ free
              total       used       free     shared    buffers     cached
    Mem:      16400776    1169448   15231328          0      54664     197880
    -/+ buffers/cache:     916904   15483872
    Swap:      1020088       5444    1014644
    # cache和buffer一些数据是可以立刻拿来使用的。所以当前可用内存=free+buffers+cached=total-used
    </code>

    # 动态查看进程内存占用
    top -d 1 -p pid [,pid ...]  //设置为delay 1s，默认是delay 3s ，如果想根据内存使用量进行排序，可以shift + m（Sort by memory usage）

    # 显示进程信息
    ps aux

    # 查看cpu占用率
    mpstat -P ALL 1

### 网络相关信息

    # 探测某个端口是否可以访问。用telnet连接指定端口。
    # 1. 一直显示正在连接，则指定的ip没有开放此端口。
    # 2. 反之，提示其他，则端口开放。
    telnet [ip] [port]
    telnet 192.168.1.1 135  

    # 查看进程端口
    netstat -tlp
    # --all show listening and non-listening sockets. 
    # --program show the PID and name of the program to which socket belongs
    netstat --all --program | grep '3265'  

    # 通过端口查看进程
    /usr/sbin/lsof -i:<port>   

    # ip、域名转换
    # 已知ip，查看域名
    [root@yf-dr-itac02.yf01.baidu.com yelu]# host 10.38.73.51
    51.73.38.10.in-addr.arpa domain name pointer yf-dr-itac02.yf01.baidu.com.
    # 已知域名，查看ip
    [root@yf-dr-itac02.yf01.baidu.com yelu]# hostname -i localhost
    10.38.73.51
      

### 获取时间

    #获取指定日期YYmmdd前/后n天日期
    [yelu@yf-dr-itac02.yf01.baidu.com src]$ DATE=20121017
    [yelu@yf-dr-itac02.yf01.baidu.com src]$ date --date="${DATE:0:4}-${DATE:4:2}-${DATE:6:2} -7 days" +%Y%m%d
    20121010

### SSH Automatic Login

如果希望在`UserA@HostA`执行`ssh UserB@HostB`可以无需输入密码登录HostB，执行如下操作：

1.在HostA上登录用户UserA，执行如下命令创建公钥，无视它出来的任何提示，一路回车到底

    ssh-keygen -t rsa

2.把HostA机器上产生的公钥id\_rsa.pub复制到HostB的`/home/username/.ssh`目录并命名为`authorized_keys`

    cat ~/.ssh/id_rsa.pub | ssh UserB@HostB "mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys"

3.将HostB的.ssh目录和文件和文件authorized\_keys赋予正确的权限，目录.ssh的权限是700，authorized\_keys文件的权限是600，权限不对或者权限太大都无法达成信任

    ssh UserB@HostB "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"

## svn设置可执行权限

To add the "executable bit" in svn

    svn propset svn:executable on <list of files>
    
To remove the "executable bit" in svn

    svn propdel svn:executable <list of files>

When you want to make a versioned file executable, do not run ”chmod +x file”; instead run “svn propset svn:executable ON file”. When you want to remove the executable bit from a versioned file, do not run “chmod -x file”; instead run “svn propdel svn:executable file”.
 
  [iostat]: http://www.orczhou.com/index.php/2010/03/iostat-detail/

### special characters with echo

echo tab and other escaping characters.

    echo -e "a\tb\n\c\td"

echo without newline character.
    echo -n "text"
 
### bash commands

**for循环**

    # for循环遍历文件，匹配通配符
    for file in ./*
    do
        echo $file
    done
    # 输出：
    ./1212_seed_weight.txt
    ./base
    ./knowledge.file
    ./prepare_data.sh
    ./sf_herring_word_term
    ./winfo_csmclk
    ./worddict_1-3-4_BL
    ./wordlist

    # 接收其他命令的输出，加上``比较安全
    for file in `ls`
    do
        echo $file
    done

    # 给定循环遍历的列表
    for file in 1 2 3
    do
        echo $file
    done

    # 自动产生连续数字序列，起始数字为1
    for i in $(seq 10); do echo $i; done

**bash按行读取文件**

    #! /bin/bash

    Domain="alarm"
    File="./data/${Domain}/chs_${Domain}.SLOT.TRAIN.tsv"
    while read line
    do
        Sample=`grep $line $File | head -n 1 | awk 'BEGIN{FS="\t"}{print $5}'`
        echo -e "$line\t$Sample"
    done < "./data/${Domain}/slots.txt"

**命令行参数**

    #! /bin/bash

    if [ $# -le 0 ]; then
        echo "USAGE: $0 DOMAIN"
        exit 1
    fi

    Domain="$1"

### 随机抽样文件

if you have that many lines, are you sure you want exactly 1% or a statistical estimate would be enough?

In that second case, just randomize at 1% at each line...

    awk 'BEGIN {srand()} !/^$/ { if (rand() <= .01) print $0}'
    
If you'd like the header line plus a random sample of lines after, use:

    awk 'BEGIN {srand()} !/^$/ { if (rand() <= .01 || FNR==1) print $0}'
    
### sort排序

sort this file according to the specific column:

    sort -k 2 file.txt

You can use multiple -k flags to sort on more than one column. For example, to sort by family name then first name as a tie breaker:

    sort -k 2,2 -k 1,1 file.txt

### Regular expression to match string not containing a word

[http://stackoverflow.com/questions/406230/regular-expression-to-match-string-not-containing-a-word](stack-overflow)

A wrong way using group:

    ^(hede)

Right approch:
    ^((?!hede).)*$

### rsync同步文件

rsync默认情况下，使用“quick check”算法，仅同步大小或最后一次修改时间已更改的文件。

    $ rsync -rtv src_folder/ machineB:/home/luye/dst_folder
    # windows下或cygwin中需要对包含空格或者网络共享的路径加单引号
    "C:\Program Files (x86)\cwRsync_5.4.1_x86_Free\rsync.exe" -rtv '//Suzhost-18/d$/wp/es-es/QASPerprocess/' '//stcsuz/root/users/luye/es-es/QASPerprocess'

使用-t选项后，rsync会将源文件的“modify time”同步到目标机器。如果目的端的文件的时间戳、大小和源端完全一致，但是内容恰巧不一致时，rsync是发现不了的。

    $ rsync -t main.c machineB:/home/userB

-I选项会让rsync挨个文件去发起数据同步。放弃“quick check”策略。

    $ rsync -I main.c machineB:/home/userB

想同步文件夹，要加上-r选项

    $  rsync -r superman/ machineB:/home/userB
    
### Use chown to change ownership

    sudo chown -R username:group directory
    

