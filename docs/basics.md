# 基础知识

## 字符编码
由于计算机是美国人发明的，因此，最早只有127个字符被编码到计算机里，也就是大小写英文字母、数字和一些符号，这个编码表被称为ASCII编码，比如大写字母A的编码是65，小写字母z的编码是122。

但是要处理中文显然一个字节是不够的，至少需要两个字节，而且还不能和ASCII编码冲突，所以，中国制定了GB2312编码，用来把中文编进去。

你可以想得到的是，全世界有上百种语言，日本把日文编到Shift_JIS里，韩国把韩文编到Euc-kr里，各国有各国的标准，就会不可避免地出现冲突，结果就是，在多语言混合的文本中，显示出来会有乱码。

因此，**Unicode** 应运而生。Unicode把所有语言都统一到一套编码里，这样就不会再有乱码问题了。

现在，捋一捋ASCII编码和Unicode编码的区别：ASCII编码是1个字节，而Unicode编码通常是2个字节。

新的问题又出现了：如果统一成Unicode编码，乱码问题从此消失了。但是，如果你写的文本基本上全部是英文的话，用Unicode编码比ASCII编码需要多一倍的存储空间，在存储和传输上就十分不划算。

所以，本着节约的精神，又出现了把Unicode编码转化为“可变长编码”的UTF-8编码。UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节。如果你要传输的文本包含大量英文字符，用UTF-8编码就能节省空间：

```
字符	ASCII	      Unicode	           UTF-8
A	   01000001	   00000000 01000001	01000001
中	  x	           01001110 00101101  11100100 10111000 10101101
```

在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。

用记事本编辑的时候，从文件读取的UTF-8字符被转换为Unicode字符到内存里，编辑完成后，保存的时候再把Unicode转换为UTF-8保存到文件：

浏览网页的时候，服务器会把动态生成的Unicode内容转换为UTF-8再传输到浏览器：

所以你看到很多网页的源码上会有类似<meta charset="UTF-8" />的信息，表示该网页正是用的UTF-8编码。

[UTF-8 Validation](https://leetcode.com/problems/utf-8-validation/description/)
```
|        UTF-8 octet sequence
|              (binary)
+---------------------------------------------
| 0xxxxxxx (一字节)
| 110xxxxx 10xxxxxx (二字节)
| 1110xxxx 10xxxxxx 10xxxxxx
| 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
```
---
## regexp

```
const isAlphaDigit = c => /[0-9a-zA-Z]/.test(c);
```

## bit operator

```
Bitwise AND	a & b	Returns a 1 in each bit position for which the corresponding bits of both operands are 1's.
Bitwise OR	a | b	Returns a 1 in each bit position for which the corresponding bits of either or both operands are 1's.
Bitwise XOR	a ^ b	Returns a 1 in each bit position for which the corresponding bits of either but not both operands are 1's.
Bitwise NOT	~ a	Inverts the bits of its operand.
Left shift	a << b	Shifts a in binary representation b (< 32) bits to the left, shifting in 0's from the right.
Sign-propagating right shift	a >> b	Shifts a in binary representation b (< 32) bits to the right, discarding bits shifted off.
Zero-fill right shift	a >>> b	Shifts a in binary representation b (< 32) bits to the right, discarding bits shifted off, and shifting in 0's from the left.
```

## set get next values
let i = this.map.get(val).values().next().value;

## splice
```
this.arr.splice(idx, 1); //remove arr[idx]
this.arr.splice(idx, 0, newNum); //add new number to arr[idx]
```
