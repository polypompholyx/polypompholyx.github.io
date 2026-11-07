---
title: The Michaelis-Menten model is not applicable to most enzymes in a cell
date: '2013-05-01T15:32:48Z'
lastmod: '2018-01-14T16:59:28Z'
url: /2013/05/misconceptions-mmm/
slug: misconceptions-mmm
draft: false
wp_id: 1108
categories:
- Maths
- Misconceptions
- Teaching
tags:
- enzyme
- kinetics
- Michaelis Menten
wp_comments:
- id: 6422
  author: Elena
  url: ''
  date: '2014-01-07T16:02:27Z'
  kind: comment
  html: <p>Really wonderful explanation. As a first year biologist myself, I was quite disappointed when we got through the Michaelis-Menten lab only to find that it was inapplicable in "most" circumstances -- excellent to find out exactly which, why, and how. Thank you!</p>
  depth: 0
- id: 6446
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2014-01-09T11:05:30Z'
  kind: comment
  html: <p>Cheers! Although just because it's not directly applicable, doesn't mean it's not useful :) The 'forward' Km and kcat values you'd get from a S-and-no-P assay are still needed if you want to model the behaviour under equilibrium conditions; you just need a set of 'backwards' parameters too, from P-and-no-S assays too.</p>
  depth: 1
- id: 405204
  author: Thomas Luedeke
  url: ''
  date: '2015-08-09T23:44:27Z'
  kind: comment
  html: '<p>Loved the article, and howled in laughter at:</p>

    <p>"During the Veneration and Memorisation of the Derivation, these assumptions may be dashed past by the lecturer doing the mathematical masturbation, and may be ignored by the students trying to grasp the point of the modelling."</p>

    <p>Sitting here forcing myself to venerate and memorize the Michaelis-Menten approach for the MCAT, and simultaneously spitting nails because it is clear that the whole approach has assumptions that prevent the expression from having any utility in the real world....</p>'
  depth: 0
- id: 405513
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2015-08-11T08:07:50Z'
  kind: comment
  html: <p>I wouldn't go so far as to say it has no applications in the real world. It's a really useful model for understanding enzymes in test tubes (which is a very small part of the real world), and it can be extended or replaced with similar kinds of model for enzymes in cells. I don't object to teaching the MMM, or even going through the derivation (maths is  good for the soul); it's just there needs to be a focus on the assumptions, and on the general principles of modelling, rather than on rote memorisation of the steps of the derivation.</p>
  depth: 1
- id: 562727
  author: Ryan
  url: ''
  date: '2017-12-04T14:48:58Z'
  kind: comment
  html: <p>Little nitpick for you- I would be careful about saying these reactions are AT equilibrium in the cell.  When a reaction is at equilibrium, it effectively does not proceed in either direction, regardless of whether or not an enzyme is present.  Enzymes do not alter a reaction's equilibrium, just the rate at which equilibrium is achieved.  They may be NEAR equilibrium in the cell, but really there's almost always flux going on in one direction or the other- as one enzyme catalyzes the formation of a metabolite, the next enzyme in the pathway consumes the new metabolite, keeping the concentration roughly constant but not quite at equilibrium.  Otherwise the pathways and the organism in question would die.</p>
  depth: 0
- id: 564649
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2018-01-14T17:00:16Z'
  kind: comment
  html: <p>Fair point, and apologies for not getting round to replying sooner. I've modified the post to make this clearer now.</p>
  depth: 1
---

> Enzymes in cells can be modelled using the Michaelis-Menten model

Enzymes can be, and often are, modelled by the [Michaelis-Menten](http://en.wikipedia.org/wiki/Michaelis%E2%80%93Menten_kinetics "Michaelis-Menten kinetics at Wikipedia") (well, Briggs-Haldane) model:

*v* = *v<sub>max</sub>* · *\[S\]* / (*K<sub>M</sub>* + *\[S\]*)

Where:

- *v* is the velocity of the enzyme, which is the rate at which product accumulates
- *v<sub>max</sub>* is the maximum velocity of the enzyme (*i.e.* the velocity to which it tends as substrate concentration increases towards infinity)
- *\[S\]* is the concentration of substrate
- *K<sub>M</sub>* is the Michaelis constant for the enzyme, which is the concentration of substrate needed to make the enzyme run at half its maximum velocity

This model works out very well when you mix together an enzyme and its substrate in a test-tube and measure the initial rate of product accumulation. Here are some data from a practical I run with my first-year biology students, showing a nice hyperbolic curve as predicted by the model:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2013/05/michaelis_menten_kinetics.png"><img loading="lazy" src="/wp-content/uploads/2013/05/michaelis_menten_kinetics-300x216.png" alt="Michaelis-Menten kinetics [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Wheat-germ acid phosphatase shows Michaelis-Menten kinetics when acting on <em>para</em>-nitrophenol phosphate, with a <em>v<sub>max</sub></em> of about 17 µM min<sup>−1</sup> and a <em>K<sub>M</sub></em> of about 0.5 mM.</figcaption></figure>

However, the Michaelis-Menten model relies on a number of assumptions. During the Veneration and Memorisation of the Derivation, these assumptions may be dashed past by the lecturer doing the mathturbation, and may be ignored by the students trying to grasp the point of the modelling. This is problematic, as not understanding the assumptions leads to the Michaelis-Menten being applied thoughtlessly in situations in which it does not apply.

Which turns out to be almost *all* situations.

The assumptions are:  

1.  The only relevant chemical species in the system are the enzyme (E), the substrate (S), the enzyme-substrate complex (ES<sup>‡</sup>), and the product (P).
2.  The only relevant chemical reactions occurring in the system are the reversible association of enzyme and substrate to form the enzyme-substrate complex; and the irreversible breakdown of the enzyme-substrate complex to product.
3.  The concentration of the enzyme-substrate complex is constant.

  
For the Michaelis-Menten model to be applicable to an enzyme in a cell, then these assumptions need to hold.  

>   
>
> **Are the only chemicals in a cell E, S, P and ES<sup>‡</sup>?**
>
>   

  
The answer is obviously no. Cells contain thousands of metabolites. To imagine that none of them have any relevant effect on the enzyme under consideration is patent nonsense, particularly when half of the rest of the enzymology course is about enzyme inhibitors, and enzyme regulation by small molecules.

In a test-tube, we can provide a pristine environment of E, S, P and ES<sup>‡</sup>, but a test-tube of four ingredients isn't a terribly realistic model of a cell. It's also not terribly realistic to expect P to sit back and do nothing...  

>   
>
> **Are enzyme-catalysed reactions in the cell irreversible?**
>
>   

  
The answer depends on *which* reaction you're talking about, but it is certainly true that many of reactions in the cell are very nearly at equilibrium under normal cellular conditions. For example, in [glycolysis](/2013/04/misconceptions-end-products/ "Metabolic pathways don’t really have end products"):  

Glucose → Glucose phosphate **⇄** Fructose phosphate → Fructose bisphosphate **⇄**

  

Triose phosphate **⇄** Bisphosphoglycerate **⇄** Phosphoglycerate **⇄** Phosphoenolpyruvate → Pyruvate

  
...all but three of the glycolytic reactions (those shown with a → rather than a **⇄**) are usually close to equilibrium in the cell. At equilibrium, the forward and reverse rates of reaction are equal, so for these enzymes, the Michaelis-Menten model is inappropriate because assumption \#2 is completely broken. The backwards reaction is appreciable because the concentration of product is relatively high. So for many enzymes in the cell, the answer to the question above is a resounding "no".

You *can* model these enzymes with a (substantially more complex) *reversible* version of Michaelis-Menten model, but at, or close to, equilibrium, these enzymes are most assuredly *not* causing products to accumulate in the way implied by a naïve glance at the graph above. Enzymes acting on near-equilibrium reactions are also exquisitely sensitive to changes in substrate and product concentrations. This is something else that is not obvious from the Michaelis-Menten graph, but which is vitally important, as we shall see below.

In a test-tube, we can provide a super-duper pristine environment of just E and S, which will give us more-or-less Michaelis-Menten kinetics *after* a little while (once the concentration of ES<sup>‡</sup> has settled down) and then *for* a little while (until P accumulates a bit and the reverse reaction becomes appreciable), but this is even less realistic than the four-ingredient tube above!

What of the remaining three reactions of glycolysis? It turns out these enzymes **have** to violate the assumptions of the Michaelis-Menten model, and for a very good reason.  

>   
>
> **If enzymes that catalyse irreversible reactions in the cell were to exhibit Michaelis-Menten kinetics, what would their response to substrate look like at low substrate concentrations?**
>
>   

  
Substrate concentrations in cells are typically lower than, but somewhere in the vicinity of, *K<sub>M</sub>*. When *\[S\]* is lower than *K<sub>M</sub>*, the Michaelis-Menten can be approximated as:  

*v* ≈ (*v<sub>max</sub>*/*K<sub>M</sub>*) · *\[S\]*

  
To double the velocity of such a reaction, you need to double the concentration of substrate: if you look at the graph above, you can see it's more-or-less a straight line between 0 and 0.5 mM.

Requiring the concentration of a chemical to double in order to get an appreciable increase in the rate of the reaction that consumes that chemical is often an extremely bad idea. Your blood normally contains glucose at a concentration between 4 and 6 mM. If your blood glucose needs to double to 10 mM before the enzymes in your body begin to deal with it properly, then [you are probably diabetic](http://en.wikipedia.org/wiki/Hyperglycemia "Hyperglycaemia at Wikipedia").

Enzymes acting at irreversible reactions have usually evolved a completely different response to substrate that is most certainly *not* modelled by the Michaelis-Menten equation:

<figure class="wp-caption aligncenter" style="max-width:300px"><a href="/wp-content/uploads/2013/05/sigmoidal_kinetics.png"><img loading="lazy" src="/wp-content/uploads/2013/05/sigmoidal_kinetics-300x272.png" alt="Sigmoidal kinetics [CC-BY-SA-3.0 Steve Cook]" /></a><figcaption>Enzymes acting at non-equilibrium reactions usually show sigmoidal kinetics, with a very sharp response to substrate: doubling the substrate concentration from 0.5 to 1 mM here leads to a six-fold increase in the velocity</figcaption></figure>

These enzymes are usually multimeric and can co-operatively bind multiple substrate molecules, so there are ES<sup>‡</sup>, ESS<sup>‡</sup>, ESSS<sup>‡</sup>, *etc.*, complexes in the system too. They are also often sensitive to feedback inhibition from other small molecules, so there are plenty of other relevant chemicals you need to take account of when modelling their behaviour. These enzymes violate assumption \#1 in the most thorough fashion, and have a sharp sigmoidal (S-shaped) response to substrate.

The Michaelis-Menten is a very good model of the activity of many enzymes in a test tube full of substrate. Its parameters *v<sub>max</sub>* and *K<sub>M</sub>* are genuinely useful bits of basic information to obtain about an enzyme, and they are easy to estimate in this simple system. However, Michaelis-Menten kinetics are **inapplicable** for most enzymes *within* a cell because most enzymes act on reactions that are close to equilibrium, and they are **unsuitable** for most of the other enzymes within a cell, because enzymes acting at far-from equilibrium reactions cannot afford to behave in such a lackadaisical fashion. Be really careful when applying toy models to real cells. Be really careful that you know the assumptions of any model you are using.
