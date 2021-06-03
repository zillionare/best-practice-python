
2020年，欧洲太空署（European Space Agency，简称ESA)打算向火星派出一个探测器，把一些岩石样品带回地球，以检测火星上是否存在生命。但是探测器只能带回500g的火星岩石。因此，在样本被带回来之前，必须精挑细选。科学家们准备构建一个现场挑选器，这个挑选器必须有视觉重建能力，因此他们构建了一个人工神经网络。在这项任务中，无论是构建多CPU集群，还是通过PyCUDA来使用NVIIDA的CUDA库，都重度依赖Python。

![](http://images.jieyu.ai/images/202106/mars-67522_1920.jpg) 
_图片来源: [mars-rover-space-traveler]_

上一个登陆火星的编程语言，则是Java。它由勇气(Spirit)号探测器携带，于2004年1月4号着陆在火星上。这一次，为了完成更复杂、更智慧的任务，科学家们选择了Python。

做出这个选择并不困难，实际上，随着人工智能的兴起，Python已成为当前最炙手可热的开发语言，其排名在[TIOBE]排行榜上逐年攀升：

![](http://images.jieyu.ai/images/202105/20210522223629.png)

不仅如此，自从[TIOBE]开始编制各种开发语言的排行榜以来，Python还分别于2020年、2018年、2010年和2007年获得年度之星称号，这也是惟一一个四次获得该称号的开发语言：

![](http://images.jieyu.ai/images/202105/20210522224627.png)

那么，Python究竟是一门什么样的语言？它在开发上究竟有什么优势，以致于得到如此这般的青睐？如果它是这样的优秀，为何在中文社区里，似乎又很少见使用Python开发的著名案例？这本书将尝试回答这些问题，特别是从软件工程的角度，阐述应该遵循什么样的开发流程和规范，才能更加快速地开发出复杂的大型应用程序。

Python是一门有着悠久历史的开发语言，它由出生于荷兰的程序员Guido Van Rossum开发。Guido Van Rossum在国内被粉丝亲切地称作“龟叔”。从创立这门语言起的长达30年时间里，Guido Van Rossum一直以他的热情和热爱指引着这门语言的未来发展方向，被称作“仁慈的终身独裁者”（the benevolent dictator for life）。大约在2018年他有过一段短暂的退休，不过很快于2020年重新回归社区，加入微软并继续领导Python的开发。

Python的最初版本于1994年1月发布，甚至还要早于Java[^JAVA]。一开始它吸收了很多Lisp语言的特性，比如引入了函数式编程工具，其痕迹一直遗留到今天 -- 这就是现在仍然在广泛使用的`reduce`, `filter`, `map`等函数的出处。在那时，Perl还是一种非常流行的脚本语言， Python也从中吸收了很多成熟模块的功能，这样就成功地留住了一批寻找Perl的替换语言的用户。

2000年Python发布2.0版，引入了列表表达式。

2001年底，Python 2.2发布，从而使得Python也成为一门纯粹的面向对象的编程语言。这一段时间，Java在企业应用端开枝散叶，而Python则在数据和基础设施管理方面找到用武之地。

2008年，Python 3.0版本发布，这个版本与2.x完全不兼容，这也是史上最具争议的一个Python版本，但也就此甩掉了长久以来积累的一些沉重包袱。此后Python轻装上阵，直到3.6版本开始，成为Python 3系列第一个比较稳定可靠的版本。也是在这个过程中，随着大数据、机器学习与人工智能的快速演进，Python进一步发挥出它的优势，被越来越多的人认识和使用。

## Python软件开发的优势
为什么Python这么受开发者欢迎？

首先得益于它的优美、简洁的语法。Python是一门优雅、迷人和高效的开发语言。从一开始起，它就把优美易读，接近自然语言作为第一设计目标，从而提高了程序开发的效率，把编程的快乐重新还给开发者。从那时起，“人生苦短，我用Python”就成为Python狂热爱好者的口号。

与其它开发语言相比，实现同样的功能，在不借助于函数库的前提下，Python代码始终是最简单、最易读的。如果在c、Java和Python三者间进行比较的话，Java是代码量最大的语言，要比c语言长1.5倍，而比Python则长3~4倍。我们以输出一个数组的元素为例来体验一下：

```python
arr = ["Hello, World!", "Hi there, Everyone!", 6]
for i in arr:
    print(i)
```

```java
public class Test {
    public static void main(String args[]) {
        String array[] = {"Hello, World", "Hi there, Everyone", "6"};
        for (String i : array) {
          System.out.println(i);
        }
    }
}
```
仅看定义和输出数组元素值的那部分。两种语言都需要三行代码，但是Python的代码明显更短，更不要说Python还有所谓的“pythonic"的写法：
```python
arr = ["Hello, World!", "Hi there, Everyone!", 6]
[print(i) for i in arr]
```

我们再看一个变量交换的例子：

```c
// C program to swap two variables in single line
#include <stdio.h>
int main()
{
	int x = 5, y = 10;
	//(x ^= y), (y ^= x), (x ^= y);
    int c;
    c = y;
    y = x;
    x = c;
	printf("After Swapping values of x and y are %d %d", x, y);
	return 0;
}
```

```java
// Java program to swap two variables in a single line
class GFG {
	public static void main(String[] args)
	{
		int x = 5, y = 10;
		//x = x ^ y ^ (y = x);
        int c;
        c = y;
        y = x;
        x = c;
		System.out.println("After Swapping values"+" of x and y are " + x + " " + y);
	}
}
```

```python
# Python program to swap two variables in a single line
x = 5
y = 10
x, y = y, x
print("After Swapping values of x and y are", x, y)
```

Python的语法显然更简单，也不需要复杂的技巧。c和java虽然也都能不借助第三个变量，实现一行代码完成变量的值交换，但这样的代码需要一定的技巧，因而更容易出错。

简洁（但不需要借助于复杂的技巧）的代码显然更加容易阅读和理解，从而大大加快了开发的速度。的确，在这个信息过载的时代，简洁越来越显示出强大的力量：json替换xml成为更多人用来传递数据的工具；markdown替代了html、reStructuredText和Word

删繁就简三秋树，标新立异二月花。繁琐、夸张的巴洛克艺术，无论其多么恢宏、多么吸引眼球，都再也无法在这个高度内卷的年代逃脱批判。语言的简洁、优美在Python中的地位是如此重要，以至于它被写进了Python“宪章” -- PEP20[^PEP20](2004年8月）： 

!!! cite "Zen of Python -  by Tim Peters[^Tim_Peters]"     
    Beautiful is better than ugly.
    优美胜于丑陋

    Explicit is better than implicit.
    明了胜于晦涩

    Simple is better than complex.
    简单优于复杂

    Complex is better than complicated.
    复杂优于凌乱

    Flat is better than nested.
    扁平好过嵌套

    Sparse is better than dense.
    稀疏强于稠密

    Readability counts.
    可读性很重要！

    Special cases aren't special enough to break the rules.
    特例亦不可违背原则

    Although practicality beats purity.
    即使实用战胜了纯粹

    Errors should never pass silently.
    错误绝不能悄悄忽略

    Unless explicitly silenced.
    除非我们确定需要如此

    In the face of ambiguity, refuse the temptation to guess.
    面对不确定性，拒绝妄加猜测

    There should be one -- and preferably only one -- obvious way to do it.
    永远都应该只有一种显而易见的解决之道

    Although that way may not be obvious at first unless you're Dutch.
    即便解决之道起初看起来并不显而易见

    Now is better than never.
    做总比不做强

    Although never is often better than *right* now.
    然而不假思索还不如不做

    If the implementation is hard to explain, it's a bad idea.
    难以名状的，必然是坏的

    If the implementation is easy to explain, it may be a good idea.
    易以言传的，可能是好的

    Namespaces are one honking great idea -- let's do more of those!
    名字空间是个绝妙的主意，请好好使用！

这段文字甚至还以复活节彩蛋的方式出现。如果执行以下的命令：

```bash
python -c 'import this'
```
就会输出上面的文字。

[^JAVA]: Java 1.0版本发布于1996年1月。
[^PEP20]: PEP是Python Ehancement Proposals的首字母缩写。它是将新特性引入Python的重要方式。
[^Tim_Peters]: Tim Peters是Python的重要贡献者之一，也是Timsort排序算法的发明人，这种算法被广泛使用于包括Python在内的各种语言，比如Chrome v8引擎和nodejs。
[^Dropbox]: Dropbox当时使用的是Python 2.x。
[TIOBE]: https://www.tiobe.com/tiobe-index/


其次，作为一种解释性语言，Python的开发体验非常好。象c,Java这样的语言，如果你写完一小段程序，想看看它是如何运行的，你必须等待它完成编译 -- 这个时间可能是几十秒或者以分钟、甚至小时计:
![](http://images.jieyu.ai/images/202106/27ed4c0b74066c8bb0ab8b5bfb2afe88_1440w.png)

对于Python，你随时可以打开它的交互式界面(即IPython)，输入一小段代码并马上看到它的运行结果。下图显示了如何在ipython界面下计算数学问题:

![](http://images.jieyu.ai/images/202105/20210522232747.png)


即使不使用IPython，随手写一个Unittest,通过Unittest来测试你刚写的方法也是非常容易。因此，使用Python，你会发现学习和成长是如此容易！

最后，Python语言社区十分活跃，有大量的第三方库可以立即拿来使用，而无须从头造轮子，这也使得Python非常适合快速原型开发。Python作为象Google,Dropbox这样的大型企业的第一门开发语言，

## Python软件开发的过程
## Python高质量软件开发的关键点
### 严格执行软件开发流程
### 重视开发中3个核心步骤
### 选用高效的开发工具

[mars-rover-space-traveler]: https://pixabay.com/photos/mars-mars-rover-space-travel-rover-67522/

