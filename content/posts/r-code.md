---
title: Running R code
date: '2014-01-01T20:42:33Z'
lastmod: '2020-05-20T12:49:43Z'
url: /2014/01/r-code/
slug: r-code
draft: false
wp_id: 1269
categories:
- R
wp_comments:
- id: 583526
  author: Ethan Sim
  url: ''
  date: '2020-05-18T06:52:10Z'
  kind: comment
  html: '<p>Hi Dr. Cook,</p>

    <p>I''ve been trying out the problems here, and I can''t quite seem to get the same result as Question 3''s final bit:</p>

    <p>A260.sorted[13] gives me the 13th item in the vector "A260.sorted", which is 0.255.</p>

    <p>Doing this manually shows that the 13th highest value is  0.310, while the 13th smallest value is 0.274.</p>

    <p>I think this might require the FastR package -  the various solutions on StackOverflow run into problems when there are repeated values within the same vector.</p>'
  depth: 0
- id: 583539
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2020-05-20T12:51:09Z'
  kind: comment
  html: '<p>Nah, it''s just me making an error: it <em>is</em> 0.255. I must have got muddled with the median value when I was typing this up originally. Bug now squashed. Thank you!</p>'
  depth: 1
---

The R interpreter is controlled by typing in plain-text commands at its command-line prompt `>|`. R commands are just text, so you can prepare a chunk of them in a text-editor, and then copy-and-paste them directly into R to run them immediately. Try copying and pasting the line below at the prompt:  

```r
print("Hello world")
```

  
Lo and behold, R will spit out what you knew it would:  

```text
[1] "Hello world"
```

  
R comes with its own simple text-editor, which you can open using the "File…New script" menu option. You can edit R code in this box, execute everything that is currently in the editor by pressing Ctrl-A and then Ctrl-R, and save the code using "File…Save as" for later reloading and use with "File…Open script". Avoid preparing R scripts in Word: by default, Word 'corrects' quote characters ("…") to smart-quotes (“…”) which R does not understand.

Even more critically, **avoid copying-and-pasting chunks of R code you do not understand**: blindly shovelling data into a black-box and assuming the output is correct and meaningful will eventually lead to embarrassing catastrophe.

If you enter data into R directly by typing at the `>|` prompt, R will just spit it back out at you, preceded by a numeric label `[1]`.  

```r
42
```

  

```text
[1] 42
```

  
To store a number for later use, you need to assign it to a variable, such as `a`, with the `<-`**assignment operator** ("**gets-arrow**"):  

```r
a<-42
```

  
R doesn’t output anything here, but if you want to see the value you have stored in the variable named `a`, you can `print()` it:  

```r
print( a )
```

  

```text
[1] 42
```

  
You can also just type:  

```r
a
```

  

```text
[1] 42
```

  
with the same effect. Variable names should be given meaningful names (which `a` probably isn't). They must start with a letter, and should contain only `letters`, `numb3r5`, `full.stops` and `under_scores`. They are case-sensitive, so the variable `nubbin` is different from the variable `Nubbin` or the variable `NUBBIN`.  
In R, it is very common to want to handle vectors, which are ordered lists of numbers (or of other kinds of value) stored in a variable. You can create these using the `c()` function ('c' for concatenate):  

```r
radii<-c( 1, 1.2, 3, 3.6, 7, 9 )

# The white-space between the listed items is optional, but aids readability.
# These lines starting with a hash '#' are comments. They are ignored by R
# but can be useful to explain to yourself and others what the code is doing.
# Blank lines are also ignored.

radii
```

  

```text
[1] 1.0 1.2 3.0 3.6 7.0 9.0
```

  
Longer vectors will be output over multiple lines, with the numerical labels indicating the index of the first item on that row. Vectors are one example of a number of different kinds of object which R can use to store different kinds of data. We'll see data frame objects later. The usefulness of vectors becomes obvious when you find that R has functions like `mean()`, `max()` and `min()`:  

```r
mean( radii )
```

  

```text
[1] 4.133333
```

  

```r
max( radii )
```

  

```text
[1] 9
```

  

```r
min( radii )
```

  

```text
[1] 1
```

  
You can extract an item from a vector using square brackets to index into the vector like this:  

```r
fifth.item<-radii[5]
print( fifth.item )
```

  

```text
[1] 7
```

  
You can create simple vectors of integers from one number to another using the colon (`:`) syntax.  

```r
one.to.ten<-c(1:10)
print(one.to.ten)
```

  

```text
 [1]  1  2  3  4  5  6  7  8  9 10
```

  
R can perform mathematical calculations on numbers and objects:  

```r
a+3
```

  

```text
[1] 45
```

  
If you perform a calculation on a single vector, the calculation is applied individually to each item in the vector, and the resulting values can be captured into a new vector like this:  

```r
areas<-pi*(radii^2)
areas
```

  

```text
[1]   3.141593   4.523893  28.274334  40.715041 153.938040 254.469005
```

  
The usual mathematical operators (`+`, `-`, `*`, `/`, `^`), shorthand for scientific notation (`1E6`) and functions (`sin()`, `sqrt()`, `exp()`, `log()`) will do what you expect. Note that `log()` returns natural log, not base-10 log.  
As you create vectors and other kinds of object, you will begin to fill up R's namespace with variable names. To see what you currently have in memory, use:  

```r
ls()
```

  

```text
 [1] "asellus.gills"      "dog.whelks"         "enzyme.kinetics"   
 [4] "fly.agarics"        "main"               "radii"             
 [7] "reaction.rate"      "students"           "sycamore.seeds"
```

  
To delete moribund objects use:  

```r
rm( students )
```

  
To delete everything, use:  

```text
rm( list = ls() )
```

  
It is easy to find help on R from its own HTML documentation. If you know the name of the function you want help on, you can use either of these:  

```r
help( "t.test" )
?t.test
```

  
If you don't know the name of the function, you can search for a term in the documentation with:  

```r
help.search( "chi squared" )
```

  
The result of this search contains a link to the documentation for `stats::chisq.test()`, amongst other things.

When you make a mistake in R, it will tell you so:  

```r
2+lg( 3 )
```

  

```text
Error: could not find function "lg"
```

  
It can be frustrating to find that this is due to a simple typo, particularly if this is a long line of code. However, it is easy to recall, edit and replay the last command you typed: press the ↑ arrow key to scroll through the last command(s) you typed, use the ← and → arrow keys to move to the place you want to edit, edit the text, and then press the "Enter" key to re-run the command.  

## Exercises

  

1.  The molar absorbance coefficient (*ϵ*) of riboflavin at 440 nm is 54×10<sup>3</sup> L mol<sup>−1</sup> cm<sup>−1</sup>. In a cuvette with a path-length (*l*) of 1 cm, what is the absorbance (*A*) of a 10 µM solution? *A = ϵ C l*. Resist the temptation to do this with a calculator: use R as your calculator.
2.  What is the volume (*V*) of an *Escherichia coli* cell, in cubic micrometres, if you model it as a cylinder of height (*h*) 2 µm and radius (*r*) 0.25 µm? *V = π r<sup>2</sup> h*.
3.  In the data below of A<sub>260</sub> values from a protein-estimation practical, what is the largest value? The smallest value? The mean value? The median value? Create a vector called `A260.sorted` containing the values in ascending order so you can manually check these results. What is the thirteenth highest value? You can copy-and-paste the data below into R directly (and in so doing, you may note something helpful).

  

```r
0.457, 0.314, 0.298, 0.284, 0.298, 0.42, 0.266, 0.285, 0.31, 0.288, 0.312,
0.284, 0.31, 0.255, 0.297, 0.293, 0.274, 0.253, 0.331, 0.243, 0.314, 0.269,
0.711, 0.46, 0.23, 0.314, 0.336, 0.255, 0.307, 0.243, 0.42, 0.302, 0.46,
0.297, 0.284, 0.283, 0.282, 0.231, 0.266, 0.228, 0.228, 0.402, 0.282,
0.312, 0.26, 0.247, 0.283, 0.288, 0.302, 0.252, 0.902, 0.336, 0.247,
0.231, 0.261, 0.283, 0.307, 0.457, 0.274, 0.288, 0.288, 0.461, 0.293,
0.314, 0.404
```

  

4.  What do `seq(0,10,2)`, `rep(10,3)` and `A260[A260>0.5]` do?
5.  The mass of wood in a pine-tree of girth (circumference at ground-level) *c*, and of height *h* can be roughly approximated by considering the pine tree as a cone of volume *V =c<sup>2</sup> h / 12 π* , and of the same density as water (*i.e.* 1 t m<sup>−3</sup>). What are the masses of the following trees? We haven't covered the syntax for this explicitly, but see if you can work it out. R is a lot more intuitive than you might think.

  

  

  

  

Girth / m

  

Height / m

  

  

  

1

  

10

  

  

  

3.5

  

18

  

  

  

1.8

  

25

  

  

  

9

  

50

  

  

  

  

6.  What is the sum of all the numbers from 1 to 100?

  

## Answers

  

1.  Absorbance of riboflavin solution:

  

```r
54E3*10E-6
```

  

```text
[1] 0.54
```

  

2.  Volume of an *Escherichia coli* cell:

  

```r
pi*0.25^2*2
```

  

```text
[1] 0.3926991
```

  

3.  *A<sub>260</sub>* values:

  

```r
A260<-c(
0.457, 0.314, 0.298, 0.284, 0.298, 0.42, 0.266, 0.285, 0.31, 0.288, 0.312,
0.284, 0.31, 0.255, 0.297, 0.293, 0.274, 0.253, 0.331, 0.243, 0.314, 0.269,
0.711, 0.46, 0.23, 0.314, 0.336, 0.255, 0.307, 0.243, 0.42, 0.302, 0.46,
0.297, 0.284, 0.283, 0.282, 0.231, 0.266, 0.228, 0.228, 0.402, 0.282,
0.312, 0.26, 0.247, 0.283, 0.288, 0.302, 0.252, 0.902, 0.336, 0.247,
0.231, 0.261, 0.283, 0.307, 0.457, 0.274, 0.288, 0.288, 0.461, 0.293,
0.314, 0.404
)
# You'll notice you can paste this line-by-line: as R knows the expression
# isn't finished until you close the ')' parenthesis at the end, it will
# prompt you with a '+' rather than a '>' until you have entered the ')'
# These lines with hash '#' signs are also valid R syntax: R ignores
# lines starting with '#', and treats them as comments

max(A260)
```

  

```text
[1] 0.902
```

  

```r
min(A260)
```

  

```text
[1] 0.228
```

  

```r
mean(A260)
```

  

```text
[1] 0.3194769
```

  

```r
median(A260)
```

  

```text
[1] 0.288
```

  

```r
A260.sorted<-sort(A260)
A260.sorted[13]
```

  

```text
[1] 0.255
```

  

```r
print(A260.sorted)
```

  

```text
[1] 0.228 0.228 0.230 0.231 0.231 0.243 0.243 0.247 0.247 0.252 0.253 0.255
[13] 0.255 0.260 0.261 0.266 0.266 0.269 0.274 0.274 0.282 0.282 0.283 0.283
[25] 0.283 0.284 0.284 0.284 0.285 0.288 0.288 0.288 0.288 0.293 0.293 0.297
[37] 0.297 0.298 0.298 0.302 0.302 0.307 0.307 0.310 0.310 0.312 0.312 0.314
[49] 0.314 0.314 0.314 0.331 0.336 0.336 0.402 0.404 0.420 0.420 0.457 0.457
[61] 0.460 0.460 0.461 0.711 0.902
```

  

4.  Useful vector functions

  

```r
# Construct a vector containing integers from 0 to 10, but in steps of 2
seq(0,10,2)
```

  

```text
[1]  0  2  4  6  8 10
```

  

```r
# Construct a vector containing three repeats of the number 10
rep(10,3)
```

  

```text
[1] 10 10 10
```

  

```r
# Return just the numbers in a vector greater than some value
A260[A260>0.5]
```

  

```text
[1] 0.711 0.902
```

  

5.  Mass of wood in pine-trees:

  

```r
c<-c(1, 3.5, 1.8, 9)
h<-c(10, 18, 25, 50)
M<-1*c^2*h/(12*pi)
# Multiplication of two vectors of the same length in R results in
# a new vector of the same length containing the item-wise products.
# R can do 'vector multiplication' in the mathematical sense too (dot/cross)
# but using a different syntax
print(M)
```

  

```text
[1]   0.2652582   5.8489442   2.1485917 107.4295866
```

  

6.  Sum from 1 to 100

  

```r
sum(c(1:100))
```

  

```text
[1] 5050
```

  
Next up...[Kinds of data](/2014/01/r-kinds-of-data/ "Kinds of data").
