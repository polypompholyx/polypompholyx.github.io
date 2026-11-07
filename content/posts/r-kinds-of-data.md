---
title: Kinds of data
date: '2014-01-13T10:47:27Z'
lastmod: '2020-02-13T15:35:21Z'
url: /2014/01/r-kinds-of-data/
slug: r-kinds-of-data
draft: false
wp_id: 1310
categories:
- R
---

The sort of data you want to analyse in R may come in many forms. You will often be trying to model the interaction of some **independent variables** (a.k.a. input, predictor or explanatory variables, the things you'd plot on an *x* axis) to explain the values of some **dependent variable** (a.k.a. output, outcome or response variable, the thing you'd put on a *y* axis).

**Categorical (qualitative)** data is data that is most clearly expressed as a one of a fixed number of **levels** of a **factor**. The factor "[rock type](http://en.wikipedia.org/wiki/Rock_(geology)#Classification "Classification of rocks at Wikipedia")" has three conventional levels: "igneous", "sedimentary" and "metamorphic". You could code these **nominal** levels numerically as '1', '2' and '3', but the named levels are easier to use, and do not imply the data is ordered in the way numerical coding of the levels might. However, some kinds of categorical data *are* sensibly arranged in an order, like "disagree", "neutral" and "agree"; these are **ordinal** data. The difference between ordinal data and true numerical data is that the interval (the 'gap') between the categories of pure ordinal data is impossible to quantify: is the difference between "neutral" and "agree" really the same as between "agree" and "strongly agree", and is that question even meaningful?  Categorical data that can only take one of two values is **binary** data: a light-switch can be on or off; a human can be dead or alive.

**Numerical (quantitative)** data is data that is most sensibly expressed as a number, like human height. The key difference from ordinal categorical data is that the interval between the values of a numerical variable is consistent and meaningful: the difference between 1 apple and 2 apples is the same as the difference between 5 apples and 6 apples, but you can't say that of the difference between having "A-levels" and "BSc" *vs.* "MSc" and "PhD". Numerical data that can take a *true* zero value is **ratio** data; that which lacks a true zero is **interval** data. The Celcius temperature scale can take a zero value, but "temperature in Celcius" is still interval data because the zero on this scale is  arbitrary: something at 40°C is not twice as hot as something at 20°C. However, "temperature in Kelvin" is ratio data because the zero is meaningful - it indicates a complete absence of molecular motion - so something at 400 K is in a genuine sense twice as hot as something at 200 K.

Whether interval or ratio, numeric data can also be **continuous** (*i.e.* real in the mathematical sense, *x* ∈ ℝ) or discrete. Human height is continuous, as any positive real value is possible, but it is also **bounded** at the lower end by zero, as human height cannot be negative. Analysis of bounded data can be problematic if many of the data are close to one or other bound (*e.g.* percentage attendance in exams: likely to be 90 to 100%); in other cases, the bounds may make no practical difference to the analysis (*e.g*. human height: very few individuals will be close to the bounds of 0 m or 3 m). Numeric data can also be **unbounded**. A company's profit is continuous and unbounded at both ends (negative profit = loss). Many continuous unbounded variables are distributed according to the **normal** distribution. **Percentage** data is a particular kind of numeric data that is strictly bounded between 0 and 100 (or between 0 and 1 if you prefer to express this as a frequency). If your dependent variable is percentage or frequency data, random variation in the variable is likely to be distributed according to the **binomial** distribution, and particular care must be taken in its analysis.

Numeric data can be **discrete** rather than continuous (*i.e.* an integer, *x* ∈ ℤ). The number of apples sold by a shop in a week is discrete and unbounded (they may "sell" a negative quantity if they buy more than they sell). Discrete numeric ratio data bounded at a true zero is **count** data. The number of offspring a cat has is discrete (*i.e.* it must be an integer), bounded count data, as a cat cannot sensibly have 2.4 kittens or minus-3 kittens. If your dependent variable is count data, random variation in the variable is likely to be distributed according to the **Poisson** distribution, and particular care must be taken in its analysis.

Numerical and categorical data can and do blur into one another. Both categorical and integer data are inherently discrete, and you may also take more-or-less continuous data (like grades on an exam) and deliberately transform them to ordinal categorical data by dividing them into discrete **bins** (A, B, C...) because it is convenient or meaningful. But you can also look at count and percentage data and see them as a large collection of binary responses: a death rate of 20% in a sample of 5 people means you've counted 4 dead people and 1 living person, or - equivalently - the answers "no", "yes", "no", "yes", "yes" to the question "is this one still alive?" And you can even look at continuous data as discrete data where the intervals are so small that you can't distinguish them (or where the intervals become meaningless because quantum physics hates you).

Different kinds of statistical approach are appropriate to the analysis of different combinations of variables. For example, to test whether a continuous dependent variable (*e.g.* life-span) varies significantly across a categorical independent variable (*e.g.* handedness), then a *t* test might be appropriate. However, a *t* test would be *in*appropriate to test whether a continuous dependent variable (*e.g.* growth rate) varies significantly across a continuous independent variable (*e.g.* nutrient concentration): here some sort of regression would be required. **It is critical that you know what sorts of test are appropriate to different kinds of data.**

Certain kinds of data can be **approximated** as data of a different kind. It is also common to measure **proxies** of the data you are actually interested in: *e.g.* measuring optical density to quantify a number of bacterial cells; or mass to measure a number of molecules. However, you should be **careful about the assumptions you are making** in doing this, and you should also consider what your data analysis might be used for. The population of bacteria in a flask is really count data (1 cell, 2 cells ... a trillion cells), but you might reasonably approximate this as continuous data, even though "half a cell" is not possible. Whether the data is treated as count or continuous makes no real difference in calculating how much glucose you need to add to the flask to support the bacteria: the difference in the amount needed to support 1 trillion cells versus 1 trillion and 1 is negligible. Conversely, sex in humans is [continuous data](http://en.wikipedia.org/wiki/Intersex "Intersex at Wikipedia"), but often ends up being badly approximated as binary data. In a small sample of humans, you may not have any individuals who identify as intersex; however, they compose about 1% of the wider population, and their needs will never be noted - let alone met - if you approximate sex as binary data.  

## Exercises

  
What kinds of data are the following?  

1.  Wavelength of light
2.  Temperature
3.  Clutch size
4.  Rate of a reaction
5.  Eye-colour
6.  Score in Scrabble
7.  Degree class
8.  Ground-cover by grass in a quadrat
9.  Winning side in chess
10. Whether people "love", "like", "meh", "dislike" or "despise" this tutorial

  

## Answers

  

1.  Wavelength of light is ratio data - continuous, numeric, and bounded by a true zero. It has no upper bound, although for wavelengths you're likely to be interested in, the boundedness will make no practical difference to the analysis.
2.  Temperature is continuous numeric data. It is strictly bounded by [0 K](http://en.wikipedia.org/wiki/Absolute_zero "Absolute zero at Wikipedia") (unless you're [doing something very odd](http://en.wikipedia.org/wiki/Negative_temperature "Negative temperature at Wikipedia")). As we discussed above, it may be ratio or interval data depending on the units you use.
3.  Clutch size (number of eggs in a nest) is count data: discrete, numeric, ratio data, bounded at 0.
4.  Rate of a reaction is continuous, numeric, unbounded, ratio data: rate of reaction could be negative, *i.e.* products become reactants. (Quantum physicists may feel free to disagree).
5.  Eye-colour is (allegedly) nominal categorical data, but this is very likely to result in a lot of arbitrary pigeon-holing.
6.  Score in Scrabble is discrete numeric data, bounded at a true zero, but could probably be reasonably approximated as unbounded continuous numeric data as scores are generally quite large.
7.  Degree class is ordinal categorical data (1<sup>st</sup>, 2:1, 2:2, 3<sup>rd</sup>, fail) although it is based on underlying data that may be percentages, counts, or who knows what.
8.  Ground-cover by grass in a quadrat is percentage data: numeric, but strictly bounded between 0 and 100%. In theory it is continuous, but in practice, you'll really be scoring it into discrete bins.
9.  Winning side in chess is binary data: white or black (0 or 1). Unless there's a draw...
10. A Lickert scale is ordinal categorical data.

  
Next up...[Formatting data](/2014/01/r-formatting-data/ "Input and output").
