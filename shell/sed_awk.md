## sed & awk

### sed tips

* 不支持 `.*?` 非贪婪匹配
* 使用`-r`参数，否则所有括号作为元字符需要\转义

### awk tips

* NF : field count
* if you change field `$n(n>=1)`, `$0` will change at the same time.

### awk match函数提取字段

    #从以下日志行中提取proctime字段：
    NOTICE: 04–10 23:10:56: storage \* 31245 [ logid:302275822 ][proctime:total:0(ms) rev:0+proc:0+write:0 ]
    cat log | awk '{if(match($0,/proctime:total:([0-9]+)/,arr)) print arr[1]}'

注意：match匹配出的结果arr[1]会被视为字符串，如果需要转换为数字，使用`0+arr[1]`触发awk进行类型转换。


### replace string

**with sed**
	
	# simple replace
	sed -i 's/foo/bar/g' input.txt
	
	# multiple replace
	sed \
	    -r -e 's/(<\/\w*>)\s*(envio|enviados|enviado|creados|trabaje) /\1 <file_action> \2 <\/file_action> /g' \
	    -e 's/carpeta <data_source> /<data_source> carpeta /g' \
	    -e 's/<keyword> envio <\/keyword>/<file_action> envio <\/file_action>/g' \
	    < $file > $new_file

`-e`可以串联替换指令，将前一个指令的替换结果作为当前指令的输入。

**with awk**

    awk '{ x=gensub("regex pattern to be replaced", "replace with", "G", $3); printf x "+" } END{ print "0" }' /tmp/data.txt

`G` stands for replace all.


### split file to be multiple files

**Split the file into 3 different files, one for each item**
    
	$ cat file1
    Item1,200
    Item2,500
    Item3,900
    Item2,800
    Item1,600
	
	$ awk -F, '{print $2 > $1".txt"}' file1
	$ cat Item1.txt
	200
	600
	
**Split file randomly**

	gawk '
    	BEGIN {srand()}
    	{f = (rand() <= 0.8 ? "xx.80" : "xx.20"); print > f}
	' file

### select columns

**with cut**

	cut -d " " -f 3- input_filename > output_filename
	
Explanation:

	cut: invoke the cut command
	-d " ": use a single space as the delimiter (cut uses TAB by default)
	-f: specify fields to keep
	3-: all the fields starting with field 3
	input_filename: use this file as the input
	> output_filename: write the output to this file.

**with awk**

	awk '{$1=""; $2=""; sub("  ", " "); print}' input_filename > output_filename
	
Explanation:

	awk: invoke the awk command
	$1=""; $2="";: set field 1 and 2 to the empty string
	sub(...);: clean up the output fields because fields 1 & 2 will still be delimited by " "
	print: print the modified line
	input_filename > output_filename: same as above.
	
	