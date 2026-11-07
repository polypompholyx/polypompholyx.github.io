---
title: 'Comparison of variances: the F test'
date: '2014-02-03T09:00:13Z'
lastmod: '2018-01-25T13:22:00Z'
url: /2014/02/r-f-test/
slug: r-f-test
draft: false
wp_id: 1289
math: true
categories:
- R
---

An *F* test is used to compare the **variances** of two data sets:  

- As it is used to compare variances, the dependent data must - by definition - be [numeric](/2014/01/r-kinds-of-data/ "Kinds of data").
- As it is used to compare two distinct sets of data, these sets represent the [two levels of a factor](/2014/01/r-kinds-of-data/ "Kinds of data").

  
The test statistic we use to compare the variances of the two data sets is called *F*, and it is defined very simply: *F* is the larger of the two variances divided by the smaller.

<span class="math">\(F = \frac{s_1}{s_2}\)</span>  
The reference distribution for the *F* test is [Fisher's *F*](http://en.wikipedia.org/wiki/F-distribution "Fisher's F at Wikipedia") distribution. This reference distribution has two parameters: the number of degrees of freedom in the first data set, and the number of degrees of freedom in the second data set.

An *F* test compares the *F* statistic from your experimental data with the Fisher's *F* value [under the null hypothesis](/2014/02/r-statistical-testing/ "Statistical testing") for the given degrees of freedom. The [*p* value](http://en.wikipedia.org/wiki/P-value "P value at Wikipedia") of the test is the probability of obtaining a test *F* statistic at least as extreme as the one that was *actually* observed, assuming that the null hypothesis ("the variances are equal") is true. *i.e.* the *p* value is the probability of observing your data (or something even more extreme), if the variances really *are* equal.

The comparison is only valid if the sample data sets are:  

- Both **representative of the larger population.** The larger the data set, the more likely this is to be true; however, it is also critical that the data be collected in an **unbiased** way, *i.e.* with suitable **randomisation**.
- Both [**normally distributed**](http://en.wikipedia.org/wiki/Normal_distribution "Normal distribution at WIkipedia"). If you plot the data as box-and-whisker plots, gross deviations from normality are often obvious. You can also use normal quantile-quantile (QQ) plots to examine the data: `help(qqnorm)`
- **Independent of one another**, *i.e.* there is no reason to suppose that the data in the first set are correlated with the data in the second set. If the data represent samples from the same organism at two different times, there is every reason to suppose they will be correlated. If the data represent paired samples, *e.g.* from one male child and from one female child, repeated across many families, there is again every reason to suppose they will be correlated.

  
Do not use an *F* test if these assumptions are broken.

In R, an *F*-test is performed using `var.test()`. Here we generate thirty items of random normal data using `rnorm()` and compare two such data sets. The output of your code will differ as the data is random:  

```r
dataset1<-rnorm(30)
dataset2<-rnorm(30)
var.test( dataset1, dataset2 )
```

  

```text
        F test to compare two variances
data: dataset1 and dataset2
F = 1.7706, num df = 29, denom df = 29, p-value = 0.1298
alternative hypothesis: true ratio of variances is not equal to 1
95 percent confidence interval:
 0.8427475  3.7200422
sample estimates:
ratio of variances
1.770609
```

  
Here the *p* value is greater than 0.05, so we say the difference in variances is not significant.

Like `plot()`, it is usually more convenient to use the '**modelled-by' tilde** `~` operator to perform *F* tests within named data frames, rather than supplying the test with two vectors of data. Here we use the [dog_whelks.csv](/wp-content/uploads/2014/01/dog_whelks.csv) data again.  

```r
dog.whelks<-read.csv( "H:/R/dog_whelks.csv" )
var.test( Height ~ Exposure, data = dog.whelks )
```

  

```text
        F test to compare two variances
data:  Height by Exposure
F = 0.9724, num df = 25, denom df = 29, p-value = 0.9504
alternative hypothesis: true ratio of variances is not equal to 1
95 percent confidence interval:
 0.4540033 2.1297389
sample estimates:
ratio of variances 
    0.9724247
```

  
You can read this as:

"Do an *F* test on the data in the dog.whelks data frame, using Height as the dependent variable, and grouping the data into two sets according to the Exposure factor"

Exercises

See the next post on [the *t* test](/2014/02/r-t-test/ "Comparison of means: the t test").
