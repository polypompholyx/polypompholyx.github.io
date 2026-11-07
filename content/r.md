---
title: R
date: '2014-01-01T20:42:05Z'
lastmod: '2017-03-14T11:41:51Z'
url: /r/
slug: r
draft: false
wp_id: 1265
wp_page: true
wp_comments:
- id: 554061
  author: student
  url: ''
  date: '2017-07-18T14:49:17Z'
  kind: comment
  html: <p>Please could you do a tutorial for mixed effect models?</p>
  depth: 0
- id: 554078
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2017-07-19T13:28:12Z'
  kind: comment
  html: <p>That's extremely tempting, but it would probably need me to write at least one, probably two, on generalised linear models first. I'll keep it in mind, but can't promise anything!</p>
  depth: 0
- id: 554228
  author: student
  url: ''
  date: '2017-07-21T15:26:42Z'
  kind: comment
  html: <p>ooh okay, thank you :)</p>
  depth: 1
- id: 567049
  author: Robert Berdan
  url: http://www.canadiannaturephotographer.com
  date: '2018-03-26T01:10:39Z'
  kind: comment
  html: '<p>Can I have permission to use your Stentor diagram on my web site www.canadiannaturephotographer.com? I am writing an article which will contain my own photomicrographs of Stentors and other ciliates. The sites purpose is education and inspiration. You are welcome to use some of my photographs if you like on your site.</p>

    <p>The article is to be posted in about 1-2 weeks it is still under development. <br/>

    Cheers<br/>

    Robert Berdan <br/>

    Calgary, Alberta</p>'
  depth: 0
- id: 567076
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2018-03-27T18:15:07Z'
  kind: comment
  html: <p>Yes, certainly. All my images and text are released under a <a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="nofollow ugc">Creative Commons Attribution ShareAlike</a> license, so if you're just planning on using it in a post on your site, you should feel free to reuse them as long as you say where they're from. I look forward to seeing your micrographs!</p>
  depth: 1
---

At the risk of [sounding like a broken record](/perl/ "Perl"), you're going to need three things to write R.  

- A computer.
- The `R` interpreter.
- A text editor.

  
R is a free software environment for statistical computing and graphics. You can download a copy from the [Comprehensive R Archive Network](http://cran.r-project.org "CRAN") (CRAN). Versions are available for Windows, MacOS and Unixen. Like Perl, R can run scripts written with a text-editor and saved to file; however, it is common to use R through its interactive command-line interface, at the `>| ` prompt.

Text that should be input into the R command line will look like this, in red:  

```r
t.test( c(1,2,3,4), c(4,6,7,6) )
```

  
In R itself, each input line will be preceded by the \> prompt, but I have missed these off so that you will be able to copy-and-paste input text directly into R, and have it run without any modification.

Text that is output from R will look like this, in blue:  

```text
Welch Two Sample t-test

data: c(1, 2, 3, 4) and c(4, 6, 7, 6)
t = -3.6056, df = 5.996, p-value = 0.0113
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
-5.455968 -1.044032
sample estimates:
mean of x mean of y
2.50 5.75
```

  
For everyday programming (which in my job, involves a lot of text-munging), I use [Perl](/perl/ "Perl"), so this tutorial for R does *not* cover all the ins-and-outs of R objects, closures, modules, functional programming, *etc.*, as I mostly use R in the limited domain of statistics and graphing. However, it does include some of the theory underlying the statistical tests. Unlike the Perl tutorial, which is more of a reference work, this tutorial is based around a large number of worked exercises, which will hopefully help you practice the material and stretch you beyond it.  

1.  [Running R code](/2014/01/r-code/ "Running R code"). Saving and running code to run in R. Loading data into R from CSVs. Vectors and functions for manipulating them. `c`, `mean`, `sum`, `max`, `min`, `seq` and `rep`.
2.  [Kinds of data](/2014/01/r-kinds-of-data/ "Kinds of data"). Discrete, categorical, (un)bounded, continuous, ordinal, numeric, and friends.
3.  [Formatting data](/2014/01/r-formatting-data/ "Formatting data"). Saving data from spreadsheets for import into R. `read`, `data.frame` and `write`.
4.  [Plotting data](/2014/01/r-plotting-data/ "Plotting  data"). Boxplots and basic graphical parameters in R. `plot`, `boxplot` and the `~` "modelled on" syntax.
5.  [Descriptive statistics](/2014/01/r-descriptive-statistics/ "Descriptive statistics"). Measures of central tendency. Measures of data variability. Histograms and degrees of freedom. `hist`, `var`, `sd`, `median` and `summary`.
6.  [Statistical testing](/2014/02/r-statistical-testing/ "Statistical testing"). Fisher *p*-value and significance, binomial distributions. `binom.test`. Distribution functions: `dbinom`, `pbinom` and `qbinom`
7.  [Statistical power](/2015/08/r-statistical-power/). Neyman-Pearson hypothesis testing. Type I and II errors. Random variables from distributions: `rbinom`. Installing packages.
8.  [The *F* test](/2014/02/r-f-test/ "Comparison of variances: the F test"). Comparison of the variance of two sets of continuous data. `var.test`, and `rnorm`.
9.  [The *t* test](/2014/02/r-t-test/ "Comparison of means: the t test"). Comparison of the means of two sets of continuous data. `t.test`, `tapply` and `qqnorm`
10. [Linear regression](/2014/02/r-linear-regression/ "Correlation of data: linear regression"). Correlation of two sets of continuous data. Checking residuals for normality. `lm`, `segments`, `abline`, `predict`, `residuals` and `fitted`
11. [The *χ*² test](/2014/02/r-chi-squared-test/ "Comparison of expected and observed count data: the χ² test"). Comparison of expected and observed count data. `chisq.test`, `head`, `str`, `table`, `list`, `matrix` and `dimnames`.
12. [Analysis of variance (ANOVA)](/2014/02/r-anova-1-way/ "Analysis of variance: ANOVA (1 way)"). Basics, and one-way ANOVA. `aov`, `anova` and `TukeyHSD`.
13. [Two way ANOVA](/2014/02/r-anova-2-way/ "Analysis of variance: ANOVA (2 way)"). Interaction plots and model simplification. `interaction.plot` and `update`.
14. [Nonlinear regression](/2014/03/r-nonlinear-regression/ "Nonlinear regression"). Non-linear least squares curve fitting. `nls`, `coef`, `log` and `lines`.

  
The posts above don't cover every conceivable test, but here's a handy flowchart that will help you find out what test you actually need. It's not perfect though: an ANOVA is a perfectly sensible technique for analysing a one-factor two-level design with a continuous response variable with normal errors, but the flow-chart will lead you to *t*. There's rarely a single, correct answer to 'how should I analyse this data set?', but there are certainly many answers to that question!

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2014/01/statistics_flowchart.png"><img loading="lazy" src="/wp-content/uploads/2014/01/statistics_flowchart-300x225.png" alt="Statistics flowchart [Public domain]" /></a><figcaption>Statistics flowchart</figcaption></figure>
