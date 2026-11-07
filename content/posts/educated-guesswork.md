---
title: Educated guesswork
date: '2012-10-03T11:15:46Z'
lastmod: '2016-08-19T15:43:32Z'
url: /2012/10/educated-guesswork/
slug: educated-guesswork
draft: false
wp_id: 189
categories:
- Maths
- Teaching
tags:
- cells
---

Someone recently asked me, "How many cells are there in the human body?"

I have quite a lot of correspondence of this kind, just to be clear.

I have to confess my first thought was "Not a bloody clue". My second thought was "I bet the Internet knows"; but my third was "The Internet is full of bloody lies".

My fourth thought went on for so long, it became part of the introduction to cell biology and genetics lecture I gave this year, and is reproduced below for your pleasure.

A good place to start is simply to divide the mass of the human body by the mass of a human cell:

***N<sub>cells</sub>* = *M<sub>human</sub>* / *M<sub>cell</sub>***

So the first thing we're going to need is a decent idea of the mass of a human, and an idea of the mass of an isolated human cell.

I am a very stumpy male human being, so my 60 kg of man-flesh will contain rather fewer cells than an 'average' human, but we have to start somewhere:

[<img src="/wp-content/uploads/2012/10/mass_of_steve-300x265.jpg" title="Mass of Steve [CC-BY-SA-3.0 Steve Cook]" class="aligncenter size-medium wp-image-272" width="300" height="265" alt="Mass of Steve [CC-BY-SA-3.0 Steve Cook]; apparently 60.8 kg" />](/wp-content/uploads/2012/10/mass_of_steve.jpg)

Given that I was wearing a *very* heavy pair of jeans, let's call that a nice round:

*M<sub>human</sub>* = **60 kg**

I would be doing several millennia of instrument makers and legislators a disservice if I didn't point out just how bloody amazing it is that you can find out how massive a human body is, with a cheap instrument, on an arbitrary but internationally recognised scale, to three significant figures. It seems a shame we so easily overlook the everyday magic of early 21st century civilisation.

The mass of a cell is a rather trickier thing to determine, so we're going to have to conjure up some ~~convenient half-truths~~ simplifying assumptions. It's a lot easier to measure the dimensions of a human cell than it is to measure its mass, as - thanks again to the instrument makers - we have microscopes available for this very purpose.

Conversion between mass and volume is a doddle as long as you know how dense the thing you're measuring  is. Fortunately, I went swimming last week, and know that the difference between me floating and sinking depends on whether I have taken a big gasp of air or not. So the human body must have very nearly the same density as water, which is a convenient:

*ρ<sub>water</sub>* = **1 kg L<sup>−1</sup>**

So my volume is about:

*Vhuman *= 60 × 1 = **60 L**

To work out the volume of a cell, we just need a picture and a scale. Below is just such a picture with a scale: something I scraped out of my cheek, under a microscope, with a "graticule" eye-piece ruler.  

[<img src="/wp-content/uploads/2012/10/cheek_cell.jpg" title="Human cheek cell at 1000 times magnification [CC-BY-SA-3.0 Steve Cook]" class="aligncenter size-full wp-image-273" width="240" height="249" alt="Human cheek cell at 1000 times magnification [CC-BY-SA-3.0 Steve Cook]" />](/wp-content/uploads/2012/10/cheek_cell.jpg)

  
Each small division on the eye-piece graticule you can see across the image is 1 µm: I know this on account of having put an actual ruler (of sorts) under the microscope and worked out the conversion factor. So this cheek cell is about 40 µm across.

To convert this into a volume, we also need to know how thick this cell is, whereupon we hit trouble, as I have no idea at all. However, I do know that blood cells are round-ish (or at least Werther's Original-ish), as they tumble about, but they turn out to be a much smaller 7 µm across:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2012/10/red_blood_cells.jpg"><img loading="lazy" title="Human red blood cell at times 400 maginification [CC-BY-SA-3.0 Steve Cook]" src="/wp-content/uploads/2012/10/red_blood_cells-300x290.jpg" alt="Human red blood cell at times 400 maginification [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>These are at ×400 rather than ×1000, so each graticule unit is 2.5 µm rather than 1 µm, so the cells are about 7 µm across</figcaption></figure>

Hmm. Given that looking at just two sorts of cell is already giving us trouble, it seems reasonable to make some more ~~stuff up~~ simplifying assumptions, and pretend that human cells are perfect cubes with sides 10 µm by 10 µm by 10 µm.

Such idealised cells have a total volume of 1000 µm<sup>3</sup> , otherwise known as a picolitre:  

- 1 L<sup> </sup>= cube of side 100 mm
- 1 mL = 10<sup>−3</sup> L = cube of side 10 mm
- 1 µL = 10<sup>−6 </sup>L  = cube of side 1 mm
- 1 nL = 10<sup>−9 </sup>L <sup> </sup>= cube of side 0.1 mm (100 µm)
- 1 pL = 10<sup>−12 </sup>L  = cube of side 0.01 mm (10 µm)
- 1 fL = 10<sup>−15 </sup>L  = cube of side 0.001 mm (1 µm)

  
So the volume of one of my cells is about:

*V<sub>cell</sub>* = **10<sup>−12 </sup>L**

If we pretend my body is made entirely of slightly oversized, cubical red blood cells, then it would contain:

*N<sub>cells</sub>* = *V<sub>human</sub>* / *V<sub>cell </sub>*= 60 L / 10<sup>−12 </sup>L =  **6 × 10<sup>13 </sup>cells**

*i.e.* about 60 trillion of them.

QED?

No. We have made a number of simplifying assumptions, and now is the time to worry about them, and their effects. Some are fairly trivial, others very foolhardy.  

- We have assumed that humans have the same density as water, when in fact they're usually a bit denser, at least when they're deflated.
- We have assumed cells are cubes, when they ([usually](http://en.wikipedia.org/wiki/Haloquadratum "Haloquadratum at Wikipedia")) demonstrably are not. A sphere is only about 52% the volume of the cube that could contain it, although [spheres can pack](http://en.wikipedia.org/wiki/Kepler_conjecture "Kepler conjecture at Wikipedia") in a way that leaves only 26% space between them.
- We have assumed that I am a representative human being, when I already confessed to being stumpy.

  
All these assumptions are iffy, but none of them would make a massive difference to our estimate of the total number of cells: at most, we're talking halving or doubling the 60 trillion.

The more serious problems with our assumptions are two we didn't really state explicitly. Firstly, human beings are *not* perfectly packed bags of cells; and indeed, much of what constitutes a human body is not cells at all. Secondly, the hand-waving about the size of an average cell hides a great mass of complications, only barely hinted at by the  cheek cells versus red blood cell disparity.

Humans are made lots of different kinds of stuff, almost 100% of which is things other than cubical red blood cells. The internet is indeed full of lies, but much of it can be cross-checked with common-sense. The figures below (culled from Wikipedia) seem to fit with what I've seen when converting non-human animals into pies. Obviously, the numbers vary greatly from person to person, but this whole calculation has been a ~~tissue of lies~~ rough-and-ready estimate, so let's not get too hung up about them:  

- Bones = 35% = 20 L
- Muscles = 40% = 24 L
- Blood = 10% = 6 L
- Faeces = 3% = 2 L

  
Bones *do* contain cells, but what they contain a lot more of is [calcium phosphate](http://en.wikipedia.org/wiki/Hydroxyapatite "Hydoxyapatite at Wikipedia") and [collagen](http://en.wikipedia.org/wiki/Collagen "Collagen at Wikipedia"), neither of which is cellular. The 35% of you that is bone doesn't actually contribute significantly to the total number of cells in you. We should therefore knock-off about 20 L from the original 60 L of my body we assumed was made of cells.

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2012/10/Gray_anatomy_bone.png"><img loading="lazy" title="Gray's anatomy bone tissue [Out of copyright]" src="/wp-content/uploads/2012/10/Gray_anatomy_bone-300x297.png" alt="Gray's anatomy bone tissue [Out of copyright]" /></a><figcaption>Only the 'bone corpuscles' (black blobs) in this image of a section of bone are actually cells; the rest of the bone is a non-cellular matrix of collagen and calcium phosphate</figcaption></figure>

Skeletal muscles are made of very large cells, about 1 cm long (*i.e. *10 000 µm by 10 µm by 10 µm). So, skeletal muscle cells are about 1000 times more voluminous than normal cells. With our original assumptions, the cells in 24 L of my body are being over-counted by a factor of 1000! Since this is such a massive difference, we can excusably pretend that muscles are non-cellular: despite being 40% of my volume, they contribute less than 1% of my cells! It's also worth noting that skeletal muscles cells often contain [more than one nucleus](http://en.wikipedia.org/wiki/Coenocyte "Coenocyte at Wikipedia"), so even calling them 'cells' should give you pause for thought.

Blood is about half plasma, which is non-cellular, so we can knock off another 3 L.

The human cells in faeces are mostly dead, so we can probably also knock those off the total too. All told, 49 L out of my 60 L are non-cellular, or nearly so. We need to reduce the 60 trillion estimate by five sixths, giving a (hopefully more reliable) estimate of:

**10 trillion human cells**

But.

And it's a big butt (ba-dum-tish).

The faeces we dismissed as inhuman non-cellular muck, are actually packed with cells, only they're not human ones. Much of my faeces (and I presume yours too, but I'd rather not check) is made of bacteria; and bacterial cells are titchy:

[<img src="/wp-content/uploads/2012/10/Enterobacter-300x297.jpg" title="Enterobacter W1 [CC-BY-SA-3.0 Steve Cook]" class="aligncenter size-medium wp-image-276" width="300" height="297" alt="Enterobacter W1 [CC-BY-SA-3.0 Steve Cook]; cylindrical cells about a micron long" />](/wp-content/uploads/2012/10/Enterobacter.jpg)

The bacteria above are *Enterobacter *sp., which *are* found in the human gut, although this strain ('W1') is of interest to me because they break down a wood preservative. They're about 2 µm long by 0.5 µm wide, so they have a volume of just 0.5 femtolitres, some 2000 times less voluminous than the human cells we modelled above.

*Vbacterium* = **0.5 × 10<sup>−15 </sup>L**

Assuming my faeces are made of perfectly packed bacteria, 2 L of it contains:

*N<sub>bacteria</sub>* = *V<sub>poo</sub>* / *V<sub>bacterium </sub>*= 2 L / 0.5 × 10<sup>−15 </sup>L =  **4 × 10<sup>15 </sup>cells**

**4 quadrillion bacterial cells**

By this estimate, there are about 500 times more bacterial cells in 2 L of my poo than in the other 58 L of 'me'. Even if we've over-estimated the proportion of faeces that is bacteria by a factor of 500 (unlikely!), the human cells in my body are still outnumbered by bacterial cells.

This leads us to two rather startling conclusions:  

1.  To a good first approximation, none of the human body is made of cells.
2.  To a good second approximation, none of the cells in the human body are human.

  
This is why I love maths, and this is why *how* you answer a question is always far more interesting than *what* that answer is.
