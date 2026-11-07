---
title: 'Analysis of variance: ANOVA (1 way)'
date: '2014-02-24T09:00:36Z'
lastmod: '2017-11-26T20:51:25Z'
url: /2014/02/r-anova-1-way/
slug: r-anova-1-way
draft: false
wp_id: 1299
categories:
- R
wp_comments:
- id: 554426
  author: student
  url: ''
  date: '2017-07-25T13:51:25Z'
  kind: comment
  html: '<p>Hi, I don''t quite understand how you reached this conclusion from the tukeyHSD <br/>

    "This confirms that – as the box-and-whisker plots suggested – the eggs laid in pipit and warbler nests are not significantly different in size, but those laid in wren nests are significantly smaller than those in the warbler or pipit nests"</p>

    <p>the p value 0.05 for wren-warbler.</p>'
  depth: 0
- id: 554601
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2017-07-28T10:33:28Z'
  kind: comment
  html: '<p>Yeah, that was a complete mess: sorry! I''ve corrected it now:</p>

    <p>"This confirms that - as the box-and-whisker plots suggested - the eggs laid in wren and warbler nests are not significantly different in size, but those laid in pipit nests are significantly larger than those in the warbler or wren nests."</p>'
  depth: 1
---

Analysis of variance is the technique to use when you might otherwise be considering a large number of pairwise *F* and *t* tests, *i.e.* where you want to know whether a factor with more than 2 levels is a useful predictor of a dependent variable.

For example, [cuckoo_eggs.csv](/wp-content/uploads/2014/01/cuckoo_eggs.csv) contains data on the length of cuckoo eggs laid into different host species, the (meadow) pipit, the (reed) warbler, and the wren.

A box-and-whisker plot is a useful way to view data of this sort:  

```r
cuckoo.eggs<-read.csv( "H:/R/cuckoo_eggs.csv" )
boxplot( 
    egg.length ~ species,
    data = cuckoo.eggs,
    xlab = "Host species",
    ylab = "Egg length / mm"
)
```

  
[<img src="/wp-content/uploads/2014/02/cuckoo_eggs_boxplot-300x300.png" class="aligncenter size-medium wp-image-1519" width="300" height="300" alt="Cuckoo eggs boxplot [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/02/cuckoo_eggs_boxplot.png)

You might be tempted to try *t* testing each pairwise comparison (pipit *vs*. wren, warbler *vs*. pipit, and warbler *vs*. wren), but a one-factor analysis of variance (ANOVA) is what you actually want here. ANOVA works by fitting individual means to the three levels (warbler, pipit, wren) of the factor (host species) and seeing whether this results in a significantly smaller residual variance than fitting a simple overall mean to the entire data set.

Conceptually, this is very similar to what we did with linear regression: ANOVA compares the residuals on the model represented by the "*y* is a constant" graph below:

[<img src="/wp-content/uploads/2014/02/cuckoo_eggs_null_model-300x300.png" class="aligncenter size-medium wp-image-1521" width="300" height="300" alt="Cuckoo eggs null model [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/02/cuckoo_eggs_null_model.png)

…with a model where three individual means have been fitted, the "*y* varies by group" model:

[<img src="/wp-content/uploads/2014/02/cuckoo_eggs_anova_model-300x300.png" class="aligncenter size-medium wp-image-1522" width="300" height="300" alt="Cuckoo eggs ANOVA model [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/02/cuckoo_eggs_anova_model.png)

It's not immediately obvious that fitting three separate means has bought us much: the model is more complicated, but the length of the red lines doesn't seem to have changed hugely. However, R can tell us precisely whether or not this is the case. The syntax for categorical model fitting is `aov()`, for **a**nalysis **o**f **v**ariance:  

```r
aov( egg.length ~ species, data=cuckoo.eggs )
```

  

```text
Call:
   aov(formula = egg.length ~ species, data = cuckoo.eggs)
Terms:
                 species Residuals
Sum of Squares  35.57612  55.85047
Deg. of Freedom        2        57
Residual standard error: 0.989865
Estimated effects may be unbalanced
```

  
As with linear regression, you may well wish to save the model for later use. It is traditional to display the results of an ANOVA in tabular format, which can be produced using `anova()`  

```r
cuckoo.model<-aov( egg.length ~ species, data=cuckoo.eggs )
anova( cuckoo.model )
```

  

```text
Analysis of Variance Table
Response: egg.length
          Df Sum Sq Mean Sq F value    Pr(>F)    
species    2 35.576 17.7881  18.154 7.938e-07 ***
Residuals 57 55.850  0.9798                      
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
```

  
The "*y* is a constant" model has only one variance associated with it: the total sum of squares of the deviances from the overall mean (*SS<sub>T,</sub>* or *SS<sub>Y</sub>*, whichever you prefer) divided by the degrees of freedom in the data set (*n*−1).

The "*y* varies by group" model decomposes this overall variance into two components.  

- The first component (*SS<sub>A</sub>*) is associated with categorising the data into *k* groups (*k*=3 here). It is the sum of squares of the difference between the group-specific mean of each data point from the overall mean, divided by the number of degrees of freedom those *k* means have, (*k*−1). This represents the **between group** variation in the data.
- The second component (*SS<sub>E</sub>*) is the residual variance, left unexplained by assigning *k* different means to each of the *k* groups. It is the sum of squares of the data points from their group-specific mean, divided by the degrees of freedom left after estimating those *k* individual means, (*n*−*k*). This represents the **within group** variation in the data.

  
In the ANOVA table, the `Sum Sq` is the sum of the squares of the deviances of the data points from a mean. The `Df` is the degrees of freedom, and the `Mean Sq` is the sum of squares divided by the degrees of freedom, which *is* the corresponding variance.

The `F value` is the mean-square for `species` divided by the mean-square of the `Residuals`. The *p* value indicates that categorising the data into three groups *does* make a significant difference to explaining the variance in the data, *i.e.* estimating three separate mean for each host species, rather than one grand mean, *does* make a significant difference to how well we can explain the data. The length of the eggs the cuckoo lays *does* vary by species.

Compare this with linear regression, where you're trying to find out whether *y*=*a*+*bx* is a better model of the data than *y*=*y̅*. This is very similar to ANOVA, where we are trying to find out whether "*y* varies by group, *i.e.* the levels of a factor" is a better model than "*y* is a constant, *i.e.* the overall mean".

You might well now ask "but *which* means are different?" This can be investigated using `TukeyHSD()` (honest significant differences) which performs a (better!) version of the pairwise *t* test you were probably considering at the top of this post.  

```r
TukeyHSD( cuckoo.model )
```

  

```text
  Tukey multiple comparisons of means
    95% family-wise confidence level
Fit: aov(formula = egg.length ~ species, data = cuckoo.eggs)
$species
                 diff        lwr        upr    p adj
Warbler-Pipit -1.5395 -2.2927638 -0.7862362 0.000023
Wren-Pipit    -1.7135 -2.4667638 -0.9602362 0.000003
Wren-Warbler  -0.1740 -0.9272638  0.5792638 0.843888
```

  
This confirms that - as the box-and-whisker plots suggested - the eggs laid in wren and warbler nests are not significantly different in size, but those laid in pipit nests are significantly larger than those in the warbler or wren nests.

ANOVA has the same sorts of assumption as the *F* and *t* tests and as linear regression: normality of residuals, homoscedacity, representativeness of the sample, no error in the treatment variable, and independence of data points. You should therefore use the same checks after model fitting as you used for linear regression:  

```r
plot( residuals( cuckoo.model ) ~ fitted( cuckoo.model ) )
```

  
 

[<img src="/wp-content/uploads/2014/02/cuckoo_egg_residuals-300x300.png" class="aligncenter size-medium wp-image-1523" width="300" height="300" alt="Cuckoo eggs residuals [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/02/cuckoo_egg_residuals.png)

We do not expect a starry sky in the residual plot, as the fitted data are in three discrete levels. However, if the residuals are homoscedastic, we expect them to be of similar spread in all three treatments, *i.e.* the residuals shouldn't be more scattered around the zero line in the pipits than in the wrens, for example. This plot seems consistent with that.  

```r
qqnorm( residuals( cuckoo.model ) )
```

  
[<img src="/wp-content/uploads/2014/02/cuckoo_egg_normal_qq_plot-300x300.png" class="aligncenter size-medium wp-image-1524" width="300" height="300" alt="Cuckoo eggs normal QQ plot [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/02/cuckoo_egg_normal_qq_plot.png)On the normal Q-Q plot, we do expect a straight line, which - again - we appear to have (although it's a bit jagged, and a tiny bit S-shaped). We can accept that the residuals are more-or-less normal, and therefore that the analysis of variance was valid.  

## Exercises

  
Analyse the following data set with ANOVA  

1.  The file [venus_flytrap.csv](/wp-content/uploads/2014/01/venus_flytrap.csv) contains data on the wet biomass (g) of Venus flytraps prevented from catching flies (control), allowed to catch flies, or prevented from catching flies but instead given fertiliser applied to the soil. Does the feeding treatment significantly affect the biomass? If so, which of the three means differ significantly, and in what directions? Have a look at the residuals in the same way as you did for the regression. How do they look?

  

## Answers

  

1.  Venus flytrap biomass data

  

```r
venus.flytrap<-read.csv("H:/R/venus_flytrap.csv")
plot(
    biomass ~ feed,
    data = venus.flytrap,
    xlab = "Feeding treatment",
    ylab = "Wet biomass / g",
    main = expression("Venus flytrap feeding regime affects wet biomass")
)
```

  
[<img src="/wp-content/uploads/2014/01/venus_flytrap_boxplot-300x203.png" class="aligncenter size-medium wp-image-1435" width="300" height="203" alt="Venus flytrap boxplot [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/01/venus_flytrap_boxplot.png)  

```r
flytrap.model<-aov( biomass ~ feed, data = venus.flytrap )
anova( flytrap.model )
```

  

```text
Analysis of Variance Table
Response: biomass
         Df  Sum Sq Mean Sq F value    Pr(>F)   
feed      2  5.8597 2.92983  22.371 1.449e-08 ***
Residuals 87 11.3939 0.13096                      
---
Signif. codes: 
0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

  

```r
TukeyHSD( flytrap.model )
```

  

```text
  Tukey multiple comparisons of means
    95% family-wise confidence level
Fit: aov(formula = biomass ~ feed, data = venus.flytrap)
$feed
                         diff         lwr        upr     p adj
fertiliser-control -0.3086667 -0.53147173 -0.0858616 0.0039294
fly-control         0.3163333  0.09352827  0.5391384 0.0030387
fly-fertiliser      0.6250000  0.40219493  0.8478051 0.0000000
```

  
The feeding treatment makes a significant different to the wet biomass (*F*=22.3, *p*=1.45 × 10<sup>−8</sup>) and a Tukey HSD test shows that all three means are different, with the fly treatment having a beneficial effect (on average, the fly-treated plants are 0.32 g heavier than the control plants), but the fertiliser has an actively negative effect on growth, with these plants on average being 0.31 g lighter than the control plants.

To plot the residuals, we use the same code as for the linear regression:  

```r
plot( residuals(flytrap.model) ~ fitted(flytrap.model) )
```

  
[<img src="/wp-content/uploads/2014/01/venus_flytrap_residuals-300x203.png" class="aligncenter size-medium wp-image-1437" width="300" height="203" alt="Venus flytrap residuals [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/01/venus_flytrap_residuals.png)

There is perhaps a bit more scatter in the residuals of the control (the ones in the middle), but nothing much to worry about.  

```r
qqnorm( residuals( flytrap.model ) )
```

  
[<img src="/wp-content/uploads/2014/01/venus_flytrap_normal_qq_plot1-300x203.png" class="aligncenter size-medium wp-image-1443" width="300" height="203" alt="Venus flytrap normal QQ plot [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2014/01/venus_flytrap_normal_qq_plot1.png)

On the normal Q-Q plot, we do expect a straight line, which - again - we appear to have. We can accept that the residuals are essentially homoscedastic and normal, and therefore that the analysis of variance was valid.

Next up... [Two-way ANOVA](/2014/02/r-anova-2-way/ "Analysis of variance: ANOVA (2 way)").
