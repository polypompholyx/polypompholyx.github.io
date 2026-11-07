---
title: 'Comparison of expected and observed count data: the χ² test'
date: '2014-02-17T09:00:40Z'
lastmod: '2014-02-24T17:02:19Z'
url: /2014/02/r-chi-squared-test/
slug: r-chi-squared-test
draft: false
wp_id: 1293
math: true
categories:
- R
wp_comments:
- id: 585770
  author: y8
  url: https://y8.world
  date: '2021-09-09T12:00:31Z'
  kind: comment
  html: <p>Great post, Thanks for providing us this great knowledge, Keep it up.</p>
  depth: 0
---

A *χ<sup>2</sup>* test is used to measure the discrepancy between the observed and expected values of count data.  

- The dependent data must - by definition - be count data.
- If there are independent variables, they must be categorical.

  
The test statistic derived from the two data sets is called *χ<sup>2</sup>*, and it is defined as the square of the discrepancy between the observed and expected value of a count variable divided by the expected value.

<span class="math">\(\chi^2 = \sum{ \frac{ (O - E)^2 }{ E } }\)</span>

The reference distribution for the *χ<sup>2</sup>* test is [Pearson's *χ<sup>2</sup>*](http://en.wikipedia.org/wiki/Chi-squared_distribution "Chi-squared distribution at Wikipedia"). This reference distribution has a single parameter: the number of degrees of freedom remaining in the data set.

A *χ<sup>2</sup>* test compares the *χ<sup>2</sup>* statistic from your empirical data with the Pearson's *χ<sup>2</sup>* value you'd expect under the null hypothesis given the degrees of freedom in the data set. The *p* value of the test is the probability of obtaining a test *χ<sup>2</sup>* statistic at least as extreme as the one that was actually observed, assuming that the null hypothesis ("there is no discrepancy between the observed and expected values") is true. *i.e.* The *p* value is the probability of observing your data (or something more extreme), if the data do not truly differ from your expectation.

The comparison is only valid if the data are:  

- **Representative of the larger population,** *i.e.*the counts are sampled in an unbiased way.
- Of **sufficiently large sample size**. In general, observed counts (and expected counts) less than 5 may make the test unreliable, and cause you to accept the null hypothesis when it is false (*i.e.* 'false negative'). R will automatically apply [Yates' correction](http://en.wikipedia.org/wiki/Yates's_correction_for_continuity "Yates' correction at WIkipedia]") to values less than 5, but will warn you if it thinks you're sailing too close to the wind.
- **Independent***.*

  
Do not use a *χ<sup>2</sup>* test unless these assumptions are met. The Fisher's exact test `fisher.test()` may be more suitable if the data set is small.

In R, a *χ<sup>2</sup>*-test is performed using `chisq.test()`. This acts on a contingency table, so the first thing you need to do is construct one from your raw data. The file [tit_distribution.csv](/wp-content/uploads/2014/01/tit_distribution.csv) contains counts of the total number of birds (the great tit, *Parus major*, and the blue tit, *Cyanistes caeruleus*) at different layers of a canopy over a period of one day.  

```r
tit.distribution<-read.csv( "H:/R/tit_distribution.csv" )
print( tit.distribution )
```

  
This will spit out all 706 observations: remember that the raw data you import into R should have a row for each 'individual', here each individual is a "This bird in that layer" observation. You can see just the start of the data using `head()`:  

```r
head( tit.distribution )
```

  

```text
     Bird  Layer
1 Bluetit Ground
2 Bluetit Ground
3 Bluetit Ground
4 Bluetit Ground
5 Bluetit Ground
6 Bluetit Ground
```

  
and look at a summary of the data frame object with `str()`:  

```r
str( tit.distribution )
```

  

```text
'data.frame':  
706 obs. of  2 variables:
 $ Bird :
Factor w/ 2 levels "Bluetit","Greattit": 1 1 1 1 1 1 1 1 1
1 ...
 $ Layer: Factor
w/ 3 levels "Ground","Shrub",..: 1 1 1 1 1 1 1 1 1 1 ...
```

  
To create a contingency table, use `table()`:  

```r
tit.table<-table( tit.distribution$Bird, tit.distribution$Layer )
tit.table
```

  

```text
           Ground Shrub Tree
  Bluetit      52   72  178
  Greattit     93  247   64
```

  
If you already had a table of the count data, and didn't fancy making the raw data CSV file from it, just to have to turn it back *into* a contingency table anyway, you could construct the table manually using `matrix()`:  

```r
tit.table<-matrix( c( 52, 72, 178, 93, 247, 64 ), nrow=2, byrow=TRUE )
# nrows means cut the vector into two rows
# byrow=TRUE means fill the data in horizontally (row-wise)
# rather than vertically (column-wise)
tit.table
```

  

```text
     [,1] [,2] [,3]
[1,]   52   72  178
[2,]   93  247   64
```

  
The matrix can be prettified with labels (if you wish) using `dimnames()`, which expects a `list()` of two vectors, the first of which are the row names, the second of which are the column names:  

```r
dimnames( tit.table )<-list( c("Bluetit","Greattit" ), c("Ground","Shrub","Tree" ) )
tit.table
```

  

```text
         Ground Shrub Tree
Bluetit      52    72  178
Greattit     93   247   64
```

  
To see whether the observed values (above) differ from the expected values, you need to know what those expected values *are*. For a simple **homogeneity** *χ<sup>2</sup>*-**test**, the expected values are simply calculated from the corresponding column (*C*), row (*R*) and grand (*N*) totals:

<span class="math">\(E = \frac{R \times C}{ N }\)</span>  

  

  

  

  

**Ground**

  

**Shrub**

  

**Tree**

  

*Row totals*

  

  

  

**Blue tit**

  

52

  

72

  

178

  

*302*

  

  

  

*E*

  

302×145/706 = 62.0

  

302×319/706 = 136.5

  

302×242/706 = 103.5

  

* *

  

  

  

*χ<sup>2</sup>*

  

(52−62)<sup>2</sup>/62 = **1.6**

  

(72−136.5)<sup>2</sup>/136.5 = **30.5**

  

(178−103.5)<sup>2</sup>/103.5 = **53.6**

  

* *

  

  

  

**Great tit**

  

93

  

247

  

64

  

*404*

  

  

  

E

  

404×145/706 = 83.0

  

404×319/706 = 182.5

  

404×242/706 = 138.5

  

  

  

  

*χ<sup>2</sup>*

  

(93−83)<sup>2</sup>/83 = **1.2**

  

(247−182.5)<sup>2</sup>/182.5 = **22.7**

  

(64−138.5)<sup>2</sup>/138.5 = **40.1**

  

  

  

  

*Column totals*

  

*145*

  

*319*

  

*242*

  

*706*

  

  

  

  
The individual *χ<sup>2</sup>* values show the discrepancies for each of the six individual cells of the table. Their sum is the overall *χ<sup>2</sup>* for the data, which is 149.7. R does all this leg-work for you, with the same result:  

```r
chisq.test( tit.table )
```

  

```text
       Pearson's Chi-squared test
data: tit.table 
X-squared = 149.6866, df = 2, p-value < 2.2e-16
```

  
The individual tits' distributions are significantly different from homogeneous, *i.e.* there are a lot more blue tits in the trees and great tits in the shrub layer than you would expect just from the overall distribution of birds.

Sometimes, the expected values are known, or can be calculated from a model. For example, if you have 164 observations of progeny from a [dihybrid selfing genetic cross](http://en.wikipedia.org/wiki/Dihybrid_cross "Dihybrid cross at Wikipedia"), where you expect a 9:3:3:1 ratio, you'd perform a *χ<sup>2</sup>* manually like this:  

  

  

  

  

*A- B-*

  

*A- bb*

  

*aa B-*

  

*aa bb*

  

  

  

*O*

  

94

  

33

  

28

  

9

  

  

  

E

  

164×9/16 = 92.25

  

164×3/16 = 30.75

  

164×3/16 = 30.75

  

164×1/16 = 10.25

  

  

  

*χ<sup>2</sup>*

  

(94−92.25)<sup>2</sup>/92.25 = **0.033**

  

(33−30.75)<sup>2</sup>/30.75 = **0.165**

  

(28−30.75)<sup>2</sup>/30.75 = **0.246**

  

(9−10.25)<sup>2</sup>/10.25 = **0.152**

  

  

  

  
For a total *χ<sup>2</sup>*of 0.596. To do the equivalent in R, you should supply `chisq.test()` with a second, named parameter called `p`, which is a vector of expected probabilities:  

```r
dihybrid.table<-matrix( c( 94, 33, 28, 9 ), nrow=1, byrow=TRUE )
dimnames( dihybrid.table )<-list( c( "Counts" ), c( "A-B-","A-bb","aaB-","aabb" ) )
dihybrid.table
```

  

```text
       A-B- A-bb aaB- aabb
Counts   94   33   28    9
```

  

```r
null.probs<-c( 9/16, 3/16, 3/16, 1/16 )
chisq.test( dihybrid.table, p=null.probs )
```

  

```text
    Chi-squared test for given probabilities
data: dihybrid.table 
X-squared = 0.5962, df = 3, p-value = 0.8973
```

  
The data are not significantly different from a 9:3:3:1 ratio, so the *A* and *B* loci appear to be unlinked and non-interacting, *i.e.* they are inherited in a Mendelian fashion.

The most natural way to plot count data is using a `barplot()` bar-chart:  

```r
barplot( dihybrid.table, xlab="Genotype", ylab="N", main="Dihybrid cross" )
```

  
[<img src="/wp-content/uploads/2014/01/maize_kernel_histogram-300x222.png" class="aligncenter size-medium wp-image-1421" width="300" height="222" alt="Maize kernel histogram [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/01/maize_kernel_histogram.png)  

## Exercises

  
Use the *χ<sup>2</sup>* test to investigate the following data sets.  

1.  Clover plants can produce cyanide in their leaves if they possess a particular gene. This is thought to deter herbivores. Clover seedlings of the CN<sup>+</sup> (cyanide producing) and CN<sup>−</sup> (cyanide free) phenotypes were planted out and the amount of rabbit nibbling to leaves was measured after 48 hr. Leaves with \>10% nibbling were scored as 'nibbled', those with less were scored as 'un-nibbled'. Do the data support the idea that cyanide reduces herbivore damage?

  

  

  

  

  

Nibbled

  

Un-nibbled

  

  

  

CN<sup>+</sup>

  

26

  

74

  

  

  

CN<sup>−</sup>

  

34

  

93

  

  

  

  

2.  In a dihybrid selfing cross between maize plants heterozygous for the *A/a* (*A* is responsible for anthocyanin production) and *Pr/pr* (*Pr* is responsible for modification of anthocyanins from red to purple) loci, we expect an F<sub>2</sub> ratio of 9 *A− Pr−*: 3 *A− pr pr*: 3 *a a Pr−* : 1 *a a pr pr*. The interaction between the loci results in the *a a Pr−*  and *a a pr pr* individuals being indistinguishable in the colour of their kernels. The file [maize_kernels.csv](/wp-content/uploads/2014/01/maize_kernels.csv) contains a tally of kernel colours. Do the data support the gene-interaction model?

  

## Answers

  

1.  As the data is already in a table, it is easier to construct it directly as a matrix. The data do not support the hypothesis that the two phenotype differ in their damage from rabbit nibbling

  

```r
clover.table<-matrix( c( 26, 74, 34, 93 ), nrow=2, byrow=TRUE )
dimnames( clover.table )<-list( 
  c( "CN.plus",  "CN.minus" ), 
  c( "Nibbled", "Un.nibbled" )
)
clover.table
```

  

```text
        Nibbled Un.nibbled
CN.plus      26         74
CN.minus     34         93
```

  

```r
chisq.test( clover.table )
```

  

```text
Pearson's Chi-squared test with Yates' continuity correction
data: clover.table 
X-squared = 0, df = 1, p-value = 1
```

  

2.  The data are in a file, so we construct a simple contingency table from that and then test against the expected frequencies of 9 purple : 3 red : 4 colourless. Make sure you get them in the right order! The data support the model, as the *χ<sup>2</sup>* value has a *p* value greater than 0.05, *i.e.* we can accept that the data are consistent with a 9:3:4 ratio.

  

```r
maize.kernels<-read.csv( "H:/R/maize_kernels.csv" )
head( maize.kernels )
```

  

```text
      Kernel
1        Red
2 Colourless
3 Colourless
4 Colourless
5     Purple
6 Colourless
```

  

```r
maize.table<-table( maize.kernels$Kernel )
maize.table
```

  

```text
Colourless    Purple        Red 
       229       485        160
```

  

```r
chisq.test( maize.table, p=c( 4/16, 9/16, 3/16 ) )
```

  

```text
Chi-squared test for given probabilities
data: maize.table 
X-squared = 0.6855, df = 2, p-value = 0.7098
```

  
Next up... [One-way ANOVA](/2014/02/r-anova-1-way/ "Analysis of variance: ANOVA (1 way)").
