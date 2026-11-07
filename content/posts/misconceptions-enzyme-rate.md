---
title: Enzymes don't necessarily increase the rate at which products are formed
date: '2013-04-09T15:29:39Z'
lastmod: '2013-04-23T14:17:58Z'
url: /2013/04/misconceptions-enzyme-rate/
slug: misconceptions-enzyme-rate
draft: false
wp_id: 932
categories:
- Maths
- Misconceptions
- Teaching
---

> An enzyme increases the rate of product formation

What happens if you add the enzyme malate dehydrogenase to a mixture of of its substrates NAD and malate (both at 1 mM for the sake of argument)?

[A brief look on BRENDA](http://www.brenda-enzymes.org/php/result_flat.php4?ecno=1.1.1.37 "MDH on BRENDA") indicates that the reaction malate dehydrogenase catalyses is:  

malate + NAD → oxaloacetate + NADH

  
So you might very well expect that the NAD would oxidise the malate, and the products oxaloacetate and NADH would rapidly accumulate.

Your expectation might well be incorrect if there is even a small trace of oxaloacetate or NADH already in the system. According to Voet & Voet (2004), the standard free energy change for malate oxidation is 29.7 kJ mol<sup>−1</sup>, which means the equilibrium constant (*K<sub>eq</sub>*) for this reaction at standard temperature and pressure is:

*K<sub>eq</sub>* = *e<sup>−(∆G⁰/RT)</sup>* = *e*<sup>−(29700/(8.314×298))</sup> = 6.22×10<sup>−6</sup>

As you can see, this number is tiny. *K<sub>eq</sub>* is the ratio of the concentrations of products to reactants at equilibrium. It is therefore a measure of the ratio of oxaloacetate (and NADH) to malate (and NAD) at the 'end' of the experiment.

*K<sub>eq</sub>* = \[oxaloacetate\]<sub>eq</sub>\[NADH\]<sub>eq</sub>/\[malate\]<sub>eq</sub>\[NAD\]<sub>eq</sub> = 6.22×10<sup>−6</sup>

At equilibrium, the concentration of oxaloacetate is likely to be much, much smaller than the concentration of malate. If both malate and NAD start off at 1 mM, the [equilibrium concentration\*](#calculations) of oxaloacetate will increase from zero to the heady heights of 2.5 µM, and the concentration of malate will decrease so little you'd be hard-pressed to detect the change!

Addition of the malate dehydrogenase enzyme *would* cause product accumulation in this case, but the amount of product formed would be microscopic.

It gets worse. Pose this question:  

>   
>
> **If you added malate dehydrogenase to a mixture of malate, oxaloacetate, NAD and NADH (all at 1 mM) what would happen?**
>
>   

  
In this case, the concentration of malate would actually *increase*, to nearly 2 mM, and the concentration of oxaloacetate would *drop* to almost nothing. The alleged 'products' of the reaction would react with one another and convert back to 'reactants'.

The reason for this is that enzymes speed up the rate at which **equilibrium** is attained. They do not necessarily speed up the accumulation of 'products'. What happens depends critically on the relative concentrations of all the reactants and products in the reaction, and their relationship to the equilibrium constant for the reaction. The leftward reaction's products are the rightward reaction's reactants, and *vice versa*.

We actually exploit this 'unexpected' behaviour in a first-year practical I run, where malate dehydrogenase activity is assayed by how rapidly it degrades NADH in the presence of oxaloacetate.  
<span id="calculations"></span>  

## Calculations

  
At the start of the reaction where only malate and NAD are present, the concentrations are:  

  

  

  

malate

  

NAD

  

oxaloacetate

  

NADH

  

  

  

10<sup>−3</sup> M

  

10<sup>−3</sup> M

  

0 M

  

0 M

  

  

  

  
At equilibrium, the concentrations of malate and NADH will be lower by some value *x*, whilst the concentrations of oxaloacetate and NADH will be higher by the same value, because of the 1:1:1:1 stoichiometry of the reaction:  

  

  

  

malate

  

NAD

  

oxaloacetate

  

NADH

  

  

  

(10<sup>−3</sup> − *x*) M

  

(10<sup>−3</sup> − *x*) M

  

*x* M

  

*x* M

  

  

  

  
Working out *x,* the final concentration of the oxaloacetate (and indeed the NADH) is fairly straightforward:

*K<sub>eq</sub>* = \[oxaloacetate\]\[NADH\]/\[malate\]\[NAD\] = 6.22×10<sup>−6</sup>  
*K<sub>eq</sub>* = (*x*·*x*) / (10<sup>−3</sup> − *x*)(10<sup>−3</sup> − *x*)  
*K<sub>eq</sub>* = *x*<sup>2</sup> / (10<sup>−3</sup> − *x*)<sup>2</sup>  
√*K<sub>eq</sub>* = *x* / (10<sup>−3</sup> − *x*)  
*x* = ( 10<sup>−3</sup> · √*K<sub>eq</sub>* ) / (1 + √*K<sub>eq</sub>* )  
*x* = ( 10<sup>−3</sup> · √(6.22×10<sup>−6</sup>) ) / (1 + √(6.22×10<sup>−6</sup>) )  
*x* = 2.49×10<sup>−6</sup> M

This gives final concentrations of:  

  

  

  

malate

  

NAD

  

oxaloacetate

  

NADH

  

  

  

0.998 mM

  

0.998 mM

  

2.49 µM

  

2.49 µM

  

  

  

  
If instead we start with all four compounds at the same concentration (call it *c*, where *c* = 1 mM in the text above), and allow things to progress to equilibrium, we get final concentrations of:  

  

  

  

malate

  

NAD

  

oxaloacetate

  

NADH

  

  

  

(*c* − *x*)

  

(*c* − *x*)

  

(*c* + *x*)

  

(*c* + *x*)

  

  

  

  
and working through the rearrangements, we get

*x* = *c* · ( √*K<sub>eq</sub>* − 1 ) / (1 + √*K<sub>eq</sub>* )  
*x* = −0.995 mM

That *x* is negative indicates a *decrease* in the quantity of 'product', and an increase in the quantity of 'reactant'.  

  

  

  

malate

  

NAD

  

oxaloacetate

  

NADH

  

  

  

1.995 mM

  

1.995 mM

  

5 µM

  

5 µM

  

  

  

  

## References

  

- Voet, D. & Voet, J. G. (2004) Citric acid cycle. In: Biochemistry. 3rd edition. New York, John Wiley and Sons, Inc., pp. 765-796.
