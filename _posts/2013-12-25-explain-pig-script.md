---
layout: post
title: "为 Pig 脚本画执行流程图"
categories: 编程
tags: [Apache Pig]
---

作为基于分布式计算平台的 hadoop 的高级过程语言, Apache Pig 允许程序员以极少的代码量分析大量的数据. 但对于写出来的程序, 人们并不能知道 Pig 是如何把脚本转换成 MapReduce 程序的, 从而难以对自己的代码进行优化. 为此, Pig 官方提供了一系列的命令和扩展用以对 Pig 代码进行[调优][efficient], 本文介绍如何使用 EXPLAIN 命令把 Pig 脚本的执行过程变成流程图.

首先看一段 Pig 代码:

	data = LOAD 'data' USING PigStorage(',') AS ( id, score:int );
	avg = FOREACH ( GROUP data BY id ) 
			GENERATE group AS id, AVG(data.score) AS avgScore;

如果此时输入:

	EXPLAIN avg

则此时屏幕将会输出一段关于 avg 如何被执行的一系列信息. Pig 在执行一段 Pig Latin 脚本的时候, 其将会经历三个阶段:

>* 逻辑计划(Logical Plan):
>	* Pig 首先会按照依赖关系把程序员定义的数据处理流程整理起来, 形成一个逻辑计划. 同时, 一些 Pig 认为不会影响输出结果但是能够提高计算性能的优化会在这一步被执行, 例如 FILTER 步骤会被尽量前推.
>* 物理计划(Physical Plan):
>	* 在这个阶段, Pig 会进一步对逻辑计划进行优化, 并产生一个物理计划, 描述在执行脚本过程中需要用到的物理操作符, 例如具体使用的加载函数和存储函数.
>* MapReduce 计划(MapReduce Plan):
>	* 在最后 Pig 会把所有的物理操作符合并成一个或数个 MapReduce 任务

EXPLAIN产生的代码其实并非易读, 因此 Pig 为 EXPLAIN 命令提供了一个非常有用的参数 *-dot*, 这个参数的作用是以 [dot格式][dot] 输出, 配合 *-out* 参数就可以在本地产生描述本地一个 dot 文件:

	EXPLAIN -dot -out exp.dot avg

运行上述命令之后, 此时在本地的目录下将会产生一个 exp.dot 文件. 这个文件是由一种文本图形描述语言写的. 要查看 dot 文件, 可以安装 graphviz 程序把 dot 文件转化成常见的图像格式. 其[官网][graphviz]上面分别有 Windows, Linux 和 Mac 等版本可以下载. 在 Ubuntu 下面可以直接使用 apt-get 安装:

	sudo apt-get install graphviz

使用 graphviz 把 dot 文件转换成图片. 方法很简单, 只要在终端执行:

	dot -Tsvg 输入 -o 输出.svg

命令就可以了. 这里的 "svg" 可以改为 "png" 从而让输出文件变成 png 格式. 但在此之前, 必须要注意的是 Pig 在输出文件的时候把三个计划都合并在一个文件输出了, 因此我们必须先用文本编辑器打开这个 exp.dot 文件, 然后把里面每一段形如下面为开头的部分复制到一个新的 dot 文件里面. 

	#--------------------------------------------------
	# Map Reduce Plan                                  
	#--------------------------------------------------
	digraph plan {
	compound=true;
	node \[shape=rect\];
	...

把文件分割之后我们得到以下三个执行计划, 左上角的是逻辑计划, 左下角的是物理计划, 右边的是MapReduce计划.

![执行计划][plan]





[efficient]: http://pig.apache.org/docs/r0.12.0/test.html "调试Pig"
[dot]: http://zh.wikipedia.org/wiki/DOT%E8%AF%AD%E8%A8%80 "DOT文件的WiKi"
[graphviz]: http://www.graphviz.org/ "Graphviz软件官网"

[plan]: /figure/2013-12-25-explain-pig-script/exp.png "执行计划"


