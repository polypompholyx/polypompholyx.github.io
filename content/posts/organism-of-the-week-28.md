---
title: 'Organism of the week #28 - Fractal art'
date: '2015-09-17T12:49:05Z'
lastmod: '2015-10-05T15:13:51Z'
url: /2015/09/organism-of-the-week-28/
slug: organism-of-the-week-28
draft: false
wp_id: 1843
categories:
- Maths
- Organism of the week
- R
tags:
- Athyrium
- fern
- fractal
- Humata
wp_comments:
- id: 418845
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2015-09-17T13:18:01Z'
  kind: comment
  html: <p>I've just googled for "Barnsley fern R" and found <a href="https://maggielinyu.wordpress.com/2012/02/25/barnsleys-fern-in-r" rel="nofollow ugc">this</a>, which is so similar I wish I <em>had</em> plagiarised it, rather than converging on more-or-less the same code!</p>
  depth: 0
---

> Flowers are essentially tarts. Prostitutes for the bees. ([Uncle Monty, *Withnail and I*](http://www.imdb.com/character/ch0162809/quotes))

Our tiny garden has only passing acquaintance with sunshine, so about the only plants that really thrive in its dingy clutches are shade-loving ferns. This Japanese painted fern is my current favourite: who needs flowers anyway, when leaves look like this?

<figure class="wp-caption aligncenter" style="max-width:225px"><a href="/wp-content/uploads/2015/08/Athyrium_niponicum_cv._Pictum.jpg"><img loading="lazy" src="/wp-content/uploads/2015/08/Athyrium_niponicum_cv._Pictum-225x300.jpg" alt="Athyrium niponicum cv. Pictum [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Japanese painted fern (<em>Athyrium niponicum</em> cv. Pictum)</figcaption></figure>

The colour is spectacular, but I also love the shape of the leaves. I have a rabbit's-foot fern on my windowsill at `$WORK`, which branches not once, not twice, not thrice, but fwice, with each leaflet at each level looking very much like a miniaturised version of the whole leaf:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/09/Humata_tyermannii_fractal.jpg"><img loading="lazy" src="/wp-content/uploads/2015/09/Humata_tyermannii_fractal-300x213.jpg" alt="Humata tyermannii [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption><em>Humata tyermannii</em></figcaption></figure>

Self-similar shapes like this are called [fractals](https://en.wikipedia.org/wiki/Fractal). This fern's leaf is not a *true* mathematical fractal, because its self-similarity goes only four levels deep, rather than infinitely so. Also, from a developmental point of view, the leaves of ferns are produced by interactions between signalling molecules that have very little in common with the maths of fractals. However, it is remarkable how easy it is to produce a fractal that looks very much like a fern - especially when someone else has done all the hard work of discovering one for you. This one is called the Barnsley fern fractal, after [Michael Barnsley](https://en.wikipedia.org/wiki/Michael_Barnsley):

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2015/08/barnsley_fern.png"><img loading="lazy" src="/wp-content/uploads/2015/08/barnsley_fern-300x300.png" alt="Barnsley fern [Public domain]" /></a><figcaption>Barnsley fern</figcaption></figure>

This [rather cute simulator](http://www.chradams.co.uk/fern/maker.html) allows you to play about with the Barnsley fern without going to the hassle of coding up any R yourself, but for those who enjoy such things, here's my version of the [code written in R](/r/), based on the coefficients from its [Wikipedia article](https://en.wikipedia.org/wiki/Barnsley_fern). An entirely imaginary prize is available for anyone who can produce a good simulation of either of the two ferns above.  

```r
fm <- vector( "list", 4 )
fc <- vector( "list", 4 )
fp <- vector( "list", 4 )

# Stem
fm[[1]] <- matrix( c( 0.00, 0.00, 0.00, 0.16 ), nrow=2, byrow=TRUE )
fc[[1]] <- matrix( c( 0.00, 0.00 ), nrow=2 )
fp[[1]] <- 0.01

# Leaflets
fm[[2]] <- matrix( c( 0.85, 0.04, -0.04, 0.85 ), nrow=2, byrow=TRUE )
fc[[2]] <- matrix( c( 0.00, 1.60 ), nrow=2 )
fp[[2]] <- 0.85

# Left largest leaflet
fm[[3]] <- matrix( c( 0.20, -0.26, 0.23, 0.22 ), nrow=2, byrow=TRUE )
fc[[3]] <- matrix( c( 0.00, 1.60 ), nrow=2 )
fp[[3]] <- 0.07

# Right largest leaflet
fm[[4]] <- matrix( c( -0.15, 0.28, 0.26, 0.24 ), nrow=2, byrow=TRUE )
fc[[4]] <- matrix( c( 0.00, 0.44 ), nrow=2 )
fp[[4]] <- 0.07

n<-250000 # you might want to make this smaller if it takes forever to render
x <- numeric( n )
y <- numeric( n )
x[1] <- 0
y[1] <- 0

for( i in 1:(n-1) ) {
  choice  <- sample( 1:4, prob=fp, size=1 )
  xy.next <- fm[[ choice ]] %*% c( x[i], y[i] ) + fc[[ choice ]]
  x[i+1]  <- xy.next[1]
  y[i+1]  <- xy.next[2]
}

plot( x, y, cex=0.05, col="dark green" )
```
