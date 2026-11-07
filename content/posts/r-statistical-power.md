---
title: Statistical power
date: '2015-08-26T15:35:13Z'
lastmod: '2017-04-14T11:18:43Z'
url: /2015/08/r-statistical-power/
slug: r-statistical-power
draft: false
wp_id: 1564
categories:
- Misconceptions
- R
---

In a [recent(ish) post](/2014/02/r-statistical-testing/), we saw that if a fair coin is flipped 30 times, the probability it will give us 10 or fewer heads is less than 5% (4.937% to be pointlessly precise). Fisher quantified this using the *p* value of a data set: the probability of obtaining data (or a test statistic based on those data) at least as extreme as that actually observed, assuming that the null hypothesis is true.

If you ask people (even people who use them on a daily basis) what a *p* value is, you will get a range of answers, probably including:  

- The probability of the data being due to random chance
- The probability of rejecting the null hypothesis incorrectly
- The probability of the data
- The probability of the null hypothesis being true
- The probability of the null hypothesis being false
- The probability that the data are significant
- The probability of the data being accurate

  
...none of which are correct. Some of these errors can be traced back to the historical mixing-up of Fisher's significance testing, and a different form of hypothesis testing proposed by Jerzy Neyman and Egon Pearson. Both of these involve calculating *p* values, and both frequently use the arbitrary cut-off of 0.05, but Neyman-Pearson testing is conceptually distinct. We'll try to untangle them here.

If we simulate a infinitely large **collective** of coin-flipping trials, each consisting of 30-flips of a fair coin, we will obtain a binomial distribution. Unfortunately, we don't have infinite time, so we'll make do with a randomly generated collection of one thousand 30-flip trials instead:  

```r
fair.heads<-rbinom( n=1000, size=30, prob=0.5 )

# breaks allows us to set the bin sizes for a histogram
hist( 
    fair.heads, 
    main   = "Number of heads in 30 coin-flips of a fair coin", 
    xlim   = c( 0, 30 ),
    breaks = seq( 0, 30, by = 1 ),
    xlab   = "Number of heads in 30 flips",
    ylab   = "Frequency"
)
```

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/08/fair_coin_simulation.png"><img loading="lazy" src="/wp-content/uploads/2015/08/fair_coin_simulation-300x300.png" alt="Fair coin simulation [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Fair coin simulated data (1000 trials)</figcaption></figure>

36 observations of 10 or fewer heads in 1000 observation is 3.6%, which is very nearly the 4.937% we expect from theory.  

  

  

  

`rbinom`

  

  

  

The function `rbinom(how.many, size=n, prob=P)` *is* R's implementation of a random binomial data generator. The 'r' stands for **random**.`rbinom(this.many, size=n, prob=P)` gives you `this.many` random variables drawn from a binomial distribution of `size` *n* with a coin producing heads at `prob` *P*.

`rbinom(1000, size=30, prob=0.5)` returns one thousand random variables, each representing the number of heads got from 30 flips of a fair coin.

Other distributions have similar random generator functions available: `rnorm` (normal), `rpois` (Poisson), `rt` (*t*), `rf` (*F*), *etc*.

  

  

  

  
To simplify things, we can go straight for the binomial distribution to give us a 'perfect' set of coin-flip data:  

```r
# create a vector into which we can put the number-of-heads-in-30-flips for 1000 observations
simulated.heads <- vector( "numeric" ) 

# This uses a for loop, the syntax for which is: 
# for ( variable in list { do.something.with( variable ) }

for ( k in 0:30 ) {
    # dbinom will give the pmf for each number of heads, k, in 30 flips
    # The number of observations of k-heads-in-30-flips is 1000 times this
    number.of.heads.in.30.flips <- round( 1000 * dbinom( k, size=30, prob=0.5 ) )
    
    # e.g. when k=10, append 28 repetitions of "10" to the simulated head-count data
    simulated.heads <- c( simulated.heads, rep( k, times = number.of.heads.in.30.flips ) )
}

hist( 
    simulated.heads, 
    main   = "Theoretical number of heads in 30 coin-flips of a fair coin", 
    xlim   = c( 0, 30 ), 
    breaks = seq( 0, 30, by = 1 ),
    xlab   = "Number of heads in 30 flips",
    ylab   = "Theoretical frequency"
)
```

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/08/fair_coin_theoretical.png"><img loading="lazy" src="/wp-content/uploads/2015/08/fair_coin_theoretical-300x300.png" alt="Fair coin theroretical [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Fair coin theoretical data (1000 trials)</figcaption></figure>

So, 10 heads in 30 flips would allow us to reject the null hypothesis that the coin is fair at a significance level of 0.05, but it tells us nothing about *how* biased the coin is. A coin that is only *slightly* biased to tails would also be unlikely to produce 10 heads in 30 flips, and a coin so biased that it *always* lands heads up, or *always* lands tails up is also inconsistent with 10 heads in 30 flips.

How can we decide between different hypotheses?

You might think: "isn't that's what the *p* value shows?", but this is not correct. A *p* value tells you something about the probability of data under a *null* hypothesis (H<sub>0</sub>), but it does not tell you anything about the probability of data under any particular *alternative* hypothesis (H<sub>1</sub>). Comparing two hypotheses needs rather more preparatory work.

If we consider a coin that may be fair, or may be loaded to heads, we might have two competing hypotheses:  

- H<sub>0</sub>: the coin is fair, and the probability of heads is 1/2 (*P*=0.50).
- H<sub>1</sub>: the coin is loaded, and the probability of heads is 2/3 (*P*=0.666...).

  
Why *P*=2/3? And why is *P*=2/3 the alternative rather than the null hypothesis?

I've chosen *P*=2/3 because I have decided - **before I start the experiment** - that I am not bothered by coins any less biased that this. Perhaps this is for reasons of cost: making coins that are better balanced is not worth the investment in new coin-stamping dies. The difference in the probability of heads under the null and alternative hypotheses is called the **effect size**. Here, the effect size is the difference of 0.1666... in the probability of getting a head. [Other measures of effect size](https://en.wikipedia.org/wiki/Effect_size#Cohen.27s_d) are appropriate to different kinds of hypotheses.

I've made *P*=2/3 the alternative hypothesis because it is more costly to me if I accept that hypothesis when it is - in fact - false. Again, perhaps this is for reasons of cost: sticking with the old coin dies is a lot cheaper than replacing them, and it's unlikely that a coin will be used to decide anything important: just trivial nonsense like kick-offs in football that I'm not really bothered by.

If you're already objecting to this pre-emptive bean-counting approach to scientific data collection, you have hit upon one of the things Fisher didn't like about Neyman and Pearson's method, so you are in good company. That said...

**The Neyman-Pearson method tries to control for the long-term probability of making mistakes in deciding between hypotheses**. In the example above, we are trying to decide between two hypotheses, and there are four possible outcomes:

<table style="height: 87px;" width="427">
<tbody>
<tr>
<td></td>
<td colspan="2">Reality</td>
</tr>
<tr>
<td>Decision</td>
<td>H<sub>0</sub> is true</td>
<td>H<sub>0</sub> is false</td>
</tr>
<tr>
<td>Accept H<sub>0</sub></td>
<td>Correctly accept H<sub>0</sub></td>
<td>Type II error</td>
</tr>
<tr>
<td>Reject H<sub>0</sub></td>
<td>Type I error</td>
<td>Correctly reject H<sub>0</sub></td>
</tr>
</tbody>
</table>

In two of these outcomes, we make a mistake. These are called type I and type II errors:  

- Type I error: **rejecting the null hypothesis when it is - in fact - true**. This is a kind of false-positive error. The coin isn't really biased, but we're unlucky and get data that is unusually full of heads.
- Type II error: **accepting the null hypothesis when it is - in fact - false**. (If we are considering only two hypotheses, this is equivalent to **rejecting the alternative hypothesis when it is - in fact - true**) This is a kind of false-negative error. The coin really *is* biased, but we're unlucky and get data that looks like a 50:50 ratio of heads to tails.

  
If we were to repeat a coin-flipping experiment a very large number of times, any **decision rule** that allows us to decide between H<sub>0</sub> and H<sub>1</sub> *will* give us the wrong decision from time to time. There's nothing we can do about this, but we can arrange the experiment so that the probabilities of making either of the two mistakes are reduced to acceptable levels:  

- We call the long-term probability of making a type I error across a large number of repeats of the experiment, *α*. In probability notation, *α* = P(reject H<sub>0 </sub>\| H<sub>0</sub>), "the probability of rejecting the null hypothesis given (\|) that the null hypothesis is true".
- We call the long-term probability of making a type II error across a large number of repeats of the experiment, *β*. In probability notation, *β* = P(accept H<sub>0 </sub>\| ¬H<sub>0</sub>), "the probability of accepting the null hypothesis given that the null hypothesis is not (¬) true".

  
We can choose whatever values we think appropriate for *α* and *β*, but typically we set *α* to 0.05. This is one of the things that results in the confusion between the Neyman-Pearson and Fisher approaches.

For two coins - one fair, and one biased to give 2/3 heads - the probability distributions for 30 flips look like this:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/08/fair_loaded_coin_distribution_overlaps.png"><img loading="lazy" src="/wp-content/uploads/2015/08/fair_loaded_coin_distribution_overlaps-300x300.png" alt="Fair and loaded coin pmf distribution overlaps [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Fair (left) and 2/3-loaded (right) coin PMF distributions, showing overlaps</figcaption></figure>

The vertical line cuts the *x*-axis at 19 heads. This is the **critical value**, *i.e.* the number of heads above which we would reject the null hypothesis, because the probability of getting 19 heads or more heads in 30 flips of a fair coin is less than 0.05. The blue area on the right is therefore 5% of the area beneath the fair coin's PMF curve, and it represents the probability of a false positive: *i.e.* rejecting the null hypothesis when it is - in fact - true, which is *α*.

The value '19' is easily determined using `qbinom`, which - [as we saw in the last post](/2014/02/r-statistical-testing/) - gives us the number of heads corresponding to a specified *p*-value.  

```r
critical.value = qbinom( p=0.05, size=30, prob=0.5, lower.tail=FALSE )
```

  
For coin-flipping, the statistic of interest - the one that we can use to make a decision between the null and alternative hypotheses - is simply the number of heads. For other kinds of test, it may be something more complicated (*e.g.* a [*t* value](/2014/02/r-t-test/), or [*F* ratio](/2014/02/r-f-test/)), but the same general principle applies: there is a critical value of the test statistic above which *p* is less than 0.05, and above which we can therefore reject the null hypothesis with a long-term error rate of *α.*

The red region on the left is the portion of the 2/3-loaded coin's PMF that is 'cut off' when we decide on a long-term false positive rate of 5%. Its area represents the probability of a false negative: *i.e.* accepting the null hypothesis when it is - in fact - false. This is *β*.

You can hopefully see that *β* is equal by `pbinom( critical.value, size=30, prob=2/3 )`. Its value - in this case 0.42 - depends on:  

1.  The critical value (which depends on the **choice of *α***).
2.  The number of coin-flips (here 30), *i.e.* the **sample size**.
3.  The bias of the coin under the alternative hypothesis (2/3), which is related to the **effect size**, *i.e.* the smallest difference in 'fair' and 'loaded' behaviour that we are interested in (2/3 - 1/2 = 0.1666...)

  
This is where the Neyman-Pearson approach diverges from Fisher's. **Fisher's approach makes no mention of an alternative hypothesis, so it makes no attempt to quantify the false-negative rate**. Neyman-Pearson sets up two competing hypotheses, and forces you to explicitly consider - and preferably control - *β*.

If the sample size and effect size are held constant, then decreasing *α**** ***increases *β*, *i.e.* there is a trade-off between the false-positive rate and the false-negative rate: imagine sliding the vertical line left or right, and consider what would happen to the red and blue areas. For the decision between 'fair' *vs*. '2/3-loaded', on a sample size of 30, beta is 0.42: we are *eight times* as likely to make a type II error as a type I error. It is very likely that we will wrongly say a coin is fair when in fact it is biased, and it is much more likely that we will make that mistake than we will call a fair coin biased when it isn't. A mere 30 coin-flips is therefore woefully **underpowered** to distinguish between *P*=1/2 and *P*=2/3.

The **power of a test**, *π*, is:

*π* = 1 - *β* = P( reject H<sub>0</sub> \| H<sub>1</sub> )

and is somewhat more convenient than *β* to remember:  

- *α* = P(reject H<sub>0 </sub>\| H<sub>0</sub>)
- *π* = P(reject H<sub>0 </sub>\| H<sub>1</sub>)

  
What is a good power to aim for? Typically, we want an experiment to have a *β* of 0.20 (*i.e.* a power of 0.8). You might ask "why the asymmetry?" between choosing *α*=0.05 and *β*=0.20*.* There's no particularly good general reason to want *β* to be larger than *α.* You might justify this on the basis that type II errors are less costly so you don't mind making them more often than type I errors (do you *really* want to replace all those coin dies?) but the real reason is usually more pragmatic: detecting even small effect sizes requires quite large sample sizes:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/08/coin_overlap_for_different_sample_sizes.png"><img loading="lazy" src="/wp-content/uploads/2015/08/coin_overlap_for_different_sample_sizes-300x300.png" alt="Coin distribution overlaps for increasing sample size [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Coin distribution overlaps for increasing sample size</figcaption></figure>

\[To make R plot graphs on a grid like this, you want: `par( mfrow=c( 2, 2 ) )` which sets up a 2-by-2 grid: each call to `plot` then adds a new graph until it fills up\]

In the graphs, you can see that as we increase the sample size from 15 through to 120, the distributions get 'tighter', the overlap gets smaller, the blue area (*β*) gets smaller (and so the power of the test gets higher). If we plot the value of *β* against the sample size, we get this:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/08/coin_power_versus_sample_size.png"><img loading="lazy" src="/wp-content/uploads/2015/08/coin_power_versus_sample_size-300x300.png" alt="Coin power vessus sample size [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>We need 60-odd flips to detect a 2/3-biased coin with a β of 0.20, but we need nearly 100 flips for a β of 0.05. The weird scatteriness is because the binomial distribution is discrete</figcaption></figure>

The sample size needed to detect a 2/3-loaded coin is *c.* 60 flips for a *β* of 0.20 (a power of 0.80), and *c.* 100 flips for a *β* of 0.05 (a power of 0.95). If we have already decided on the value of *α* and the effect size of interest, then **fixing the sample size is the only control we have over the type II error rate**.

It is fairly rare for people to do power calculations of this sort before they start collecting data: more often than not, they simply collect a sample as large as they can afford. This means that - whilst type I errors are controlled at 0.05 - type II errors are often ignored, assumed (wrongly!) to be low, or - at best - calculated retrospectively. Retrospective calculations can give unpleasant surprises: as we saw above, 30 flips will result in quite a lot of quite badly loaded coins going undetected.

**Ideally, you should calculate the sample size needed for a particular power *before* the experiment**: that way, you will collect precisely the amount of data needed to give you the long-term error rates you think are acceptable (0.05 for *α* and 0.20 for *β*, or whatever). This brings us on to the last major confusion between Fisher and Neyman-Pearson testing:  

- *p* is the probability of a test statistic being at least as extreme as the test statistic we actually got, assuming that the null hypothesis is true.
- *α* is the long-term probability of mistakenly rejecting the null hypothesis when it is actually true, if we were to repeat the experiment many times.

  
In Neyman-Pearson testing, we calculate a test statistic from our data (in this case just the number of heads), and compare that to the critical value of that test statistic. If the calculated value is larger than the critical value, we reject the null hypothesis. However, we can make exactly the same decision by calculating a *p* value from our data, and if it is less than *α*, rejecting the null hypothesis. Both of these approaches result in the same decision. The former used to be much more common because it was easy to obtain printed tables of critical values of test statistics like *t* and *F* for *α*=0.05. More recently, since computing power has made it far easier to calculate the *p* value directly, the latter approach has become more common.

Remember that in Fisher's approach, a *p* value of 0.01 is 'more significant' than a *p* value of 0.05, and Fisher suggested ([wrongly](https://en.wikipedia.org/wiki/Bayesian_probability), IMHO) that this should give you more confidence in your rejection of the null. In Neyman-Pearson testing, if a *p* value is calculated at all, it is only to compare it to *α*. If you have done the power calculation, and collected the correct sample size, working out the *p* value is simply a means to an end: either it is larger than *α* (...accept null) or it is smaller than *α* (...reject null), but its value has no further importance. **In Neyman-Pearson hypothesis testing, there is no such thing as "highly significant, *p*=0.01"**. Unfortunately, a lot of people want to have their statistical cake and eat it: they don't do a power calculation and collect a sample size that is expedient rather than justified (screw you Neyman-Pearson!), but they then want to interpret a very low *p* value (yay Fisher!) as being evidence for a particular alternative hypothesis (love you really, Neyman-Pearson!) This isn't really very coherent, and many statisticians now prefer to side-step the whole issue and go for [confidence intervals](https://en.wikipedia.org/wiki/Confidence_interval) or [Bayesian approaches](https://en.wikipedia.org/wiki/Bayesian_statistics) instead, which I leave to others to explain.

This brings us to the question - finally! - of how many coin-flips we *should* collect to distinguish a loaded coin from a fair one. There are several answers to this, depending on our constraints, but two are particularly important:  

1.  We have limited money and time, so we can only do 30 flips. **What is the minimum effect size we can reliably detect?**
2.  We have unlimited money and time (ha ha ha!), so we can only do as many flips as is necessary, but we're only interested in coins that are biased to 2/3 heads or more. **What sample size do we need to reliably detect a particular effect size of interest**?

  
So, firstly, for the number of flips we can be bothered to make, what is the minimum effect size we can reliably (*α*=0.05, *β*=0.20) detect? For some common tests, R has built-in power calculations, but in general, the simplest way to work this out is by simulation. This requires a little code. In this case, it's only actually about 12 lines, but I've commented it heavily as it's a little tricky:  

```r
# Set up empty vectors to contain numeric data. sample.size will be filled in 
# with the minimum sample size needed to distinguish a fair coin from a
# loaded coin of various degrees of bias. effect.size will be filled in
# with the effect size for each loaded coin

sample.size <- vector('numeric')
effect.size <- vector('numeric')

# We'll try out numbers of flips between 0 and 200

size  <- c(0:200)

# Loop though some values of 'loaded' from 19/32 to 1. We don't go any
# lower than this because even 18/32 requires more than 200 flips!

for ( loaded in seq( from=19/32, to=32/32, by=1/32 ) ) {
    
    # since 'size' is a vector, qbinom will return a vector of 'crit' values
    # for all trial sizes between 0 and 200 coin-flips; and pbinom will then
    # return the beta values for each ('crit', 'size') pair.

    crit <- qbinom( p=0.05, size=size, prob=0.5, lower.tail=FALSE )
    beta <- pbinom( crit,   size=size, prob=loaded )

    # 'which' returns all the indices into the beta vector for which
    # the beta value is <= to 0.20. Since these were put in in 'size' 
    # order (i.e. beta item number 5 is the beta value for a trial of 5 flips)
    # using 'min' to return the smallest of these indices 
    # immediately gives us the smallest sample size required to
    # reliably detect a bias in the coin of 'loaded'

    smallest.needed <- min( which( beta <= 0.20 ) )
    
    # Append the value we've just worked out to the sample.size vector
    
    sample.size     <- c( sample.size, smallest.needed )
    
    # Effect size is the degree of bias minus the P for a fair coin (0.5)
    
    effect.size     <- c( effect.size, loaded - 0.5 )
}

# Which is the first index into sample.size for which the value is 30 or less?

index.for.thirty <- min( which( sample.size <= 30 ) )

# Since effect.size and sample.size were made in parallel, using this index
# into effect.size will give the minimum effect size that could be detected
# on 30 coin flips

effect.size[ index.for.thirty ]
```

  
The answer is that **30 flips is enough to reliably detect a bias only if the effect size is at least 0.25**, *i.e.* to distinguish between a fair coin and a coin that is biased to give 3/4 heads. Does this surprise you? You need quite a lot of flips to distinguish even a large bias.

\[NB - we made rather coarse steps of 1/32 in the loop that generated this data. If you do smaller steps of 1/64, or 1/128, you'll find the real value is nearer 0.23\]

A graph of effect size against sample size for (*α*=0.05, *β*=0.20) is useful in answering this question and the next:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/08/coin_effect_versus_sample_size.png"><img loading="lazy" src="/wp-content/uploads/2015/08/coin_effect_versus_sample_size-300x300.png" alt="Coin flipping effect size vs sample size [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Effect size and sample size are inversely related: a small sample size can only detect a large bias; a large sample size is needed to detect a small bias</figcaption></figure>

Secondly, **what is the minimum sample size we need to reliably (*α*=0.05, *β*=0.20) detect an effect size of interest to us?**

The same code as above generates the necessary data, but now we want:  

```r
index.for.twothirds <- min( which( effect.size >= 2/3 - 1/2 ) )
sample.size[ index.for.twothirds ]
```

  
**At least 45 flips are needed to distinguish a fair coin from a coin biased to give 2/3 heads**. \[Again, bear in mind the coarseness of the loop: the real value is closer to 59\].

All this may sound like an awful lot of bother merely to be told that your sample size is woefully inadequate, or that you are going to miss lots of biased coins. Fortunately, R makes it easy to obtain this unwelcome information, at least for common tests like *[t](/2014/02/r-t-test/)* and [ANOVA](/2014/02/r-anova-1-way/), and easy-ish for some other tests, through [the `pwr` package](https://cran.r-project.org/web/packages/pwr/index.html), which you can install from CRAN with:  

```r
install.packages( "pwr" )
```

  
...load into a script with:  

```r
library(pwr)
```

  
...and find information about usage with:  

```r
??power
```

  

## Exercises

  

1.  What sample size is needed to distinguish a fair coin from a slightly heads-biased coin (*P*=0.55) with *α*=0.05, and a power of 0.80? What is the critical number of heads that would allow you to reject the null?

  

## Answers

  

1.  A power of 0.80 means *β*=0.20. The same code we used for the effect *vs*. sample size calculation can be modified to give us the data we want. The `paste()` function allows us to put the value of variables into strings for use in `print()` statements or as axis titles, *etc*. Note that number of heads required to convince us of *P*=0.55 rather than *P*=0.50 is actually only 330/621 = 0.53, because the sample size is so large.

  

```r
size <- c(0:1000)
crit <- qbinom( p=0.05, size=size, prob=0.50, lower.tail=FALSE )
beta <- pbinom( crit,   size=size, prob=0.55 )
n    <- min( which( beta <= 0.20 ) )

print( paste( "Critical value is", crit[n], "heads" ) )
print( paste( "Sample size required is", n ) )
```

  

```text
"Critical value is 330 heads"
"Sample size required is 621"
```

  
Next up... [The *F*-test](/2014/02/r-f-test/).
