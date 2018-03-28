# string

## [count and say](https://leetcode.com/problems/count-and-say/description/)

1. Recursion
> edge case is when `n === 1`
> key observation:
> count & say -> save the `cnt` (the current streak length) & say `${cnt}{streakNumber}`.
> The timing to say is when you find a new streak or iterate is done, otherwise you need to update the cnt of the streak.

```
const isNewStreak = i => (i === len || (i > 0 && lastSeq[i] !== lastSeq[i - 1]));
```


```javascript
var countAndSay = function(n) {
    if (n === 1) return '1';
    let lastSeq = countAndSay(n - 1);
    // e.g. 1211 is returned as last seqence
    return sayNext(lastSeq);
};

var countAndSay = function(n) {
    let seq = '1';
    for (let i = 1; i < n; i++) {
        seq = sayNext(seq);
    }
    return seq;
};

function sayNext(lastSeq) {
    let cnt = 0;
    let curSeq = [];
    // for (let i = 0; i < lastSeq.length; i++) {
    let len = lastSeq.length;
    const isNewStreak = i => (i === len || (i > 0 && lastSeq[i] !== lastSeq[i - 1])); //streak pattern
    for (let i = 0; i <= len; i++) {
        if (isNewStreak(i)) {
            curSeq.push(`${cnt}${lastSeq[i - 1]}`); //save the previous streak
            cnt = 1; //reset the streak
        } else {
            cnt++; //update the streak
        }
    }
    // not elegant : curSeq.push(`${cnt}${lastSeq[lastSeq.length - 1]}`);
    return curSeq.join('');
};
```

---
## [add binary](https://leetcode.com/problems/add-binary/description/)

1. Two index simulate add operation
> scan from right to left until both pointers are out of range (which means nothing left to add).
> Check if carry is empty, if not add the carry.

```javascript
var addBinary = function(a, b) {
    let result = [];
    let i = a.length - 1, j = b.length - 1;
    let carry = 0;
    while (i >= 0 || j >= 0) {
        let digit1 = i >= 0 ? Number(a[i]) : 0;
        let digit2 = j >= 0 ? Number(b[j]) : 0;
        let sum = (digit1 + digit2 + carry) % 2;
        carry = ~~((digit1 + digit2 + carry) / 2);
        result.unshift(sum);
        i--;
        j--;
    }
    if (carry > 0) result.unshift(carry);
    return result.join('');
};
```
---
## [multiply strings](https://leetcode.com/problems/multiply-strings/description/)

![1](https://drscdn.500px.org/photo/130178585/m%3D2048/300d71f784f679d5e70fadda8ad7d68f)

> 长度为m, n 的两个int相乘，最多长度为 m + n.
> num1[i] * nums2[j] 的结果会影响 result[i + j] & result [i + j + 1]
> 记住就行
> `num1[i] * num2[j]` 的product要加上result 相应位置的已有乘积作为sum，然后在取模放在`i + j + 1` 上，carry 补到`i + j` 上

```javascript
var multiply = function(num1, num2) {
    let pos = new Array(num1.length + num2.length).fill(0);
    for (let i = num1.length - 1; i >= 0; i--) {
        for (let j = num2.length - 1; j >= 0; j--) {
            let mul = Number(num1[i]) * Number(num2[j]);
            let sum = mul + pos[i + j + 1];
            pos[i + j] += Math.floor(sum / 10);
            pos[i + j + 1] = sum % 10;
        }
    }
    let i;
    for (i = 0; i < pos.length; i++) {
        if (pos[i] !== 0) {
            break;
        }
    }
    result = pos.slice(i).join("");
    return result === '' ? '0': result;
};
```
---
## [roman to integer](https://leetcode.com/problems/roman-to-integer/description/)

1. mapping
> Use hashtable to store roman to integer mapping.
> Iterate through the roman characters.
> Key observation:
> `IV` , `IX`, `XL`, `XC`, `CD`, `CM` are special cases
> in these cases `I, X, C` doesn't serve as `+1, +10, +100` , they server as `-1, -10, -100` instead
> check if two char integer apply first, then check if one char integer apply

```javascript
// Symbol	I	V	X	L	C	D	M
// Value	1	5	10	50	100	500	1,000

// 1776 as MDCCLXXVI
// 1954 as MCMLIV
// 1990 as MCMXC
// 2014 as MMXIV

var romanToInt = function(s) {
    let map = new Map([
        ['I', 1], ['V', 5], ['X', 10], ['L', 50], ['C', 100], ['D', 500], ['M', 1000],
        ['IV', 4], ['IX', 9], ['XL', 40], ['XC', 90], ['CD', 400], ['CM', 900]
    ]);
    let result = 0;
    for (let i = 0; i < s.length; i++) {
        if (i < s.length - 1 && map.has(s.slice(i, i + 2))) {
            result += map.get(s.slice(i, i + 2));
            i++;
        } else {
            result += map.get(s[i]);
        }
    }
    return result;
};
```
---
## [integer to roman](https://leetcode.com/problems/integer-to-roman/description/)

> Input is guaranteed to be within the range from 1 to 3999.
> 只需要最多看四位digit
> 从低到高用余10除10法剥除低位的digit. 对每一位digit分别用对应于（个，十，白，千）的罗马
字符表示.

```javascript
var intToRoman = function(num) {
    let ones = ["I", "X", "C", "M"];
    let fives = ["V", "L", "D"];
    let tens = ["X", "C", "M"];

    let result = "";

    const getRomanDigit = (num, one, five, ten) => {
        switch (num) {
            case 0:
                return "";
            case 1:
            case 2:
            case 3:
                return one.repeat(num);
            case 4:
                return `${one}${five}`;
            case 5:
            case 6:
            case 7:
            case 8:
                let ones = one.repeat(num - 5);
                return `${five}${ones}`
            case 9:
                return `${one}${ten}`
        }
    }

    for (let shift = 0; num > 0 && shift < 4; shift++) {
        let digit = num % 10;
        let roman = getRomanDigit(digit, ones[shift], fives[shift], tens[shift]);
        result = `${roman}${result}`;
        num = Math.floor(num / 10);
    }

    return result;
};
```
---
## [integer to english words](https://leetcode.com/problems/integer-to-english-words/description/)

1. stage by stage
> cases:
1) Thousands , for those >= 1000
2) Houndreds , for those >= 100
3) Tens, for those >= 20
4) less than 20, for those < 20.
> Main loop deals with Thousand , Million, and Billion one by one if that exists .
```
while (num > 0) [
	if (num % 1000 !== 0) ...
	num = ~~(num / 1000)
}
```
> `num % 1000` yields the number `< 1000` so we can use helper function to discuss case by case:

```javascript
var numberToWords = function(num) {
    const LESS_THAN_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"];
    const TENS = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"];
    const THOUSANDS =  ["", "Thousand", "Million", "Billion"];

    function helper(num) {
        if (num === 0) return '';
        if (num < 20) return LESS_THAN_20[num] + ' ';
        // bug : extra space for 50 if (num < 100) return TENS[~~(num / 10)] + ' ' + LESS_THAN_20[num % 10] + ' ';
        if (num < 100) return TENS[~~(num / 10)] + ' ' + helper(num % 10);
        // num >= 100 && num < 1000
        return LESS_THAN_20[~~(num / 100)] + ' Hundred ' + helper(num % 100);
    }

    if (num === 0) return 'Zero';
    let i = 0; //the thousand index
    let words = '';
    while (num > 0) {
        if (num % 1000 !== 0) {
            words = `${helper(num % 1000)}${THOUSANDS[i]} ${words}`
        }
        num = ~~(num / 1000);
        i++;
    }
    return words.trim();
};
```
---
## [excel sheet column title](https://leetcode.com/problems/excel-sheet-column-title/description/)

1. 特殊的26进制 （底数为1）

这题有点奇怪，长得像26进制，但是却没有0，底数为1.
但是要取模必须得有0.(取模之后可以把0看成A，25看成Z）

`BZ = 26 * 2 + 26` 是这个26进制数的第72个数，也就是index为71的家伙。
如果直接除以26， 余数是0。为了表现出index，将其本身的值 --n. 得到的家伙就是
index.

对于每一位的数，本来正常的26进制的底数都是0，所以求值都是直接取mod。然后这个畸形的26进制却要求减1之后取模。

```javascript
var convertToTitle = function(n) {
    return n === 0 ? '' : (
        convertToTitle(~~((n - 1) / 26)) + String.fromCharCode((n - 1) % 26 + 'A'.charCodeAt(0))
    );
};
```
---
## [text justification](https://leetcode.com/problems/text-justification/description/)

1. `buffer + overflow`
> keep tracker of actually # of letters and space of the current line.
> if the current line overflow (reaches the limit) , dump the contents of the current line.
> There must be one line left because after the last word, nothing triggers the overflow action.
> round robin的时候最后一个word不用加space。
> 0 % 0 === NaN
```
for (let word of words) {
	// calc curLen = # of letters + # of spaces + incomming word len
	// if (curLen > maxWidth) construct the line by adding spaces in between in round robin fashion
	// push the incomming word to the line
}
fill the last line with spaces to the right and push it to the result
```

```javascript
var fullJustify = function(words, maxWidth) {
    let result = [], line = [], letterNum = 0;
    for (let word of words) {
        let curLen = letterNum + line.length + word.length;
        if (curLen > maxWidth) {
            let spaceNum = maxWidth - letterNum;
            for (let i = 0; i < spaceNum; i++) {
                // bug1 i % line.length
                line[i % ((line.length - 1) || 1)] += ' ';
            }
            result.push(line.join(''));
            line = [];
            letterNum = 0;
        }
        line.push(word);
        letterNum += word.length;
    }
    // bug2 lastLine = line.join('')
    let lastLine = line.join(' ');
    while (lastLine.length < maxWidth) lastLine += ' ';
    result.push(lastLine);
    return result;
};
```
---

## [implement strstr](https://leetcode.com/problems/implement-strstr/description/)

```
`edge case` when `needle === '0'`

don't forget to prune the comparison.
```

```javascript
var strStr = function(haystack, needle) {
    let m = haystack.length, n = needle.length;
    if (m < n) return -1;
    for(let i = 0; i + n <= m; i++) {
        if (haystack.slice(i, i + n) === needle) return i;
    }
    return -1;
};
```

---

## [valid palindrom](https://leetcode.com/problems/valid-palindrome/description/)

```
igore the nonAlphaNumeric chars by lo++ or hi--.
if both are valid character and they're different , return false.
```

```javascript
var isPalindrome = function(s) {
    let lo = 0, hi = s.length - 1;
    const isAlphaDigit = c => /[0-9a-zA-Z]/.test(c);
    while (lo < hi) {
        if (!isAlphaDigit(s[lo])) {
            lo++;
        } else if (!isAlphaDigit(s[hi])) {
            hi--;
        } else {
            if (s[lo].toLowerCase() !== s[hi].toLowerCase()) {
                return false;
            }
            lo++;
            hi--;
        }
    }
    return true;
};
```

----

## [valid palindrom II](https://leetcode.com/problems/valid-palindrome-ii/description/)

```
we have one chance to make mismatch.

if there is a mismatch, we delete either one of the char and then see if the rest is palindrome.
```

```javascript
var validPalindrome = function(s) {
    let n = s.length;
    if (n < 2) return true;
    if (s[0] === s[n - 1]) return validPalindrome(s.slice(1, n - 1));
    return isPalindrome(s.slice(1)) || isPalindrome(s.slice(0, n - 1));
};

function isPalindrome(s) {
    let lo = 0, hi = s.length - 1;
    while (lo < hi) {
        if (s[lo] !== s[hi]) return false;
        lo++;
        hi--;
    }
    return true;
}

var validPalindrome = function(s) {
    return valid(s, 0, s.length - 1, false);
};

function valid(s, lo, hi, deleted) {
    if (lo >= hi) return true;
		//bug1 maintain deleted status
    if (s[lo] === s[hi]) return valid(s, lo + 1, hi - 1, deleted);
    return !deleted && (valid(s, lo + 1, hi, true) || valid(s, lo, hi - 1, true));
}
```

---

## [one edit distance](https://leetcode.com/problems/one-edit-distance/description/)

```
`simplify problem`
make sure s.length < t.length

`edge case` length of two strings differ more than 1.

find the first mismatch.
and then analyze case by case.
1) if all chars of s is matched
2) if mismatch happen somewhere in S.
2.1) m === n
2.2) m < n
```

```javascript
var isOneEditDistance = function(s, t) {
    let m = s.length, n = t.length;
    if (m > n) return isOneEditDistance(t, s);
    if (n - m > 1) return false;
    // n - m === 0 || 1
    let i = 0;
    while (i < m && s[i] === t[i]) i++;
    if (i === m) return n - m === 1;
    // i < m && s[i] !== t[i]
    if (m < n) return s.slice(i) === t.slice(i + 1);
    return s.slice(i + 1) === t.slice(i + 1);
};
```

---

## [valid number](https://leetcode.com/problems/valid-number/description/)

```
We start with trimming.
If we see [0-9] we reset the number flags.
We can only see . if we didn't see e or ..
We can only see e if we didn't see e but we did see a number. We reset numberAfterE flag.
We can only see + and - in the beginning and after an e
any other character break the validation.
At the and it is only valid if there was at least 1 number and if we did see an e then a number after it as well.
```

```javascript
var isNumber = function(s) {
    let pointSeen = false, eSeen = false, numSeen = false, numAfterE = false;
    const isDigit = c => /[0-9]/.test(c);
    s = s.trim();
    for (let i = 0; i < s.length; i++) {
        let c = s[i];
        if (isDigit(c)) {
            numSeen = true;
            if (eSeen) numAfterE = true;
        } else if (c === '.') {
            if (pointSeen || eSeen) return false;
            pointSeen = true;
        } else if (c === 'e') {
            if (eSeen || !numSeen) return false;
            eSeen = true;
        } else if (c === '+' || c === '-') {
            if (i > 0 && s[i - 1] !== 'e') return false;
        } else {
            return false;
        }
    }
    return numSeen && (!eSeen || numAfterE);
};
```

---
