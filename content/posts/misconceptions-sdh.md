---
title: The product of succinate dehydrogenase is ubiquinol not reduced flavin
date: '2013-04-09T11:20:05Z'
lastmod: '2013-04-16T10:37:07Z'
url: /2013/04/misconceptions-sdh/
slug: misconceptions-sdh
draft: false
wp_id: 910
aliases:
- /2013/04/misconceptions-sd/
categories:
- Misconceptions
- Teaching
tags:
- flavin
- quinone
- SDH
- succinate dehydrogenase
---

> Succinate dehydrogenase (SDH) produces reduced flavin (FADH<sub>2</sub>) as a product

This misconception is so widespread, even the exam boards get it wrong. [Page 41 of the Edexcel GCE specification for A-level biology (2008 onwards)](http://www.edexcel.com/quals/gce/gce08/biology/Pages/default.aspx "Edexcel A-level biology specification") states that students should be able to...

> Describe the role of the Krebs cycle in the complete oxidation of glucose and formation of carbon dioxide (CO<sub>2</sub>), ATP, reduced NAD and **reduced FAD** (names of other compounds are not required) and that respiration is a many-stepped process with each step controlled and catalysed by a specific intracellular enzyme. \[my emphasis\]

[Succinate dehydrogenase](http://en.wikipedia.org/wiki/Succinate_dehydrogenase "Succinate dehydrogenase at Wikipedia") (SDH) is an enzyme of the [Krebs (citric acid, tricarboxylic acid, *etc.*) cycle](http://en.wikipedia.org/wiki/Citric_acid_cycle "Krebs cycle at Wikipedia") found in mitochondria. It is the only enzyme of the Krebs cycle that is membrane-bound. Its job is to oxidise the organic acid succinate by removing two of its electrons, and then to pass those electrons on to a fatty molecule called ubiquinone, reducing this molecule to ubiquinol.

<figure class="wp-caption aligncenter" style="max-width:237px"><a href="/wp-content/uploads/2013/04/succinate_dehydrogenase.png"><img loading="lazy" alt="Succinate dehydrogenase [CC-BY-SA-3.0 Steve Cook, based on PDB 1NEK: Yankovskaya, V., Horsefield, R., Tornroth, S., Luna-Chavez, C., Miyoshi, H., Leger, C., Byrne, B., Cecchini, G., Iwata, S. (2003) Architecture of succinate dehydrogenase and reactive oxygen species generation. Science 299:700-704 doi: 10.1126/science.1079605]" src="/wp-content/uploads/2013/04/succinate_dehydrogenase-237x300.png" /></a><figcaption>Succinate dehydrogenase [CC-BY-SA-3.0 Steve Cook, based on <a title="Yankovskaya, V., Horsefield, R., Tornroth, S., Luna-Chavez, C., Miyoshi, H., Leger, C., Byrne, B., Cecchini, G., Iwata, S. (2003) Architecture of succinate dehydrogenase and reactive oxygen species generation. Science 299:700-704" href="http:/dx.doi.org/10.1126/science.1079605">PDB 1NEK</a>] The 'top' of the enzyme pokes into the mitochondrial matrix and oxidises succinate; the 'bottom' of the enzyme is dissolved in the lipid of inner mitochondrial membrane, and reduces ubiquinone.</figcaption></figure>

To see why "SDH produces reduced FAD" is a misconception, you need only compare it with some of the other enzymes of Krebs cycle. Pose this question:  

>   
>
> **If SDH produces reduced FAD, what does α-ketoglutarate dehydrogenase produce?**
>
>   

  
[α-ketoglutarate dehydrogenase](http://en.wikipedia.org/wiki/Oxoglutarate_dehydrogenase_complex "Oxoglutarate dehydrogenase complex at Wikipedia") is a big, multi-subunit enzyme which catalyses a complicated reaction, the details of which...  

- **α-ketoglutarate** + thiamine pyrophosphate → COOHCH<sub>2</sub>CH<sub>2</sub>C(OH)=TPP + **CO<sub>2</sub>**
- COOHCH<sub>2</sub>CH<sub>2</sub>C(OH)=TPP + lipoyl → succinyl-dihydrolipoyl + TPP
- succinyl-dihydrolipoyl + **coenzyme-A** → **succinyl-coenzyme-A** + dihydrolipoyl
- dihydrolipoly + FAD → FADH<sub>2</sub> + lipoyl
-  FADH<sub>2</sub> + **NAD** → FAD + **NADH**

  
...are certainly not part of the A-level biology specification. All the intermediates, *including the FAD,* cancel out, leaving only the bolded items behind. Even the net reaction of α-ketoglutarate dehydrogenase...  

- α-ketoglutarate + coenzyme-A + NAD → succinyl-coenzyme-A + CO<sub>2</sub> + NADH

  
...is not mentioned in the A-level specification. The gnarly details of α-ketoglutarate dehydrogenase's catalytic cycle, and even the overall reaction it catalyses are (rightly!) hidden behind the catch-all veil of the "formation of reduced NAD":  

>   
>
> Describe the role of the Krebs cycle in the complete oxidation of glucose and formation of carbon dioxide (CO<sub>2</sub>), ATP, **reduced NAD** and reduced FAD (names of other compounds are not required)
>
>   

  
However, for some reason, succinate dehydrogenase gets special-cased. SDH catalyses the reactions:  

- **succinate** + FAD → FADH<sub>2</sub> + **fumarate**
- FADH<sub>2</sub> + \[2Fe-2S\]<sub>ox</sub> → FAD + \[2Fe-2S\]<sub>red</sub>
- \[2Fe-2S\]<sub>red</sub> + \[4Fe-4S\]<sub>ox</sub> → \[2Fe-2S\]<sub>ox</sub> + \[4Fe-4S\]<sub>red</sub>
- \[4Fe-4S\]<sub>red</sub> + \[3Fe-4S\]<sub>ox</sub> → \[4Fe-4S\]<sub>ox</sub> + \[3Fe-4S\]<sub>red</sub>
- \[3Fe-4S\]<sub>red</sub> + haem-*b<sub>560</sub>*<sub>ox</sub> → \[3Fe-4S\]<sub>ox</sub> + haem-*b<sub>560</sub>*<sub>red</sub>
- haem-*b<sub>560</sub>*<sub>red</sub> + **ubiquinone** → haem-*b<sub>560</sub>*<sub>ox</sub> + **ubiquinol**

  
I've not balanced the protons for the sake of 'clarity'. The \[Fe-S\] things represent iron-sulfur clusters, essentially [tiny crystals of fool's gold](http://en.wikipedia.org/wiki/Pyrite "Iron pyrites at Wikipedia") inside the enzyme.

Like the FAD in α-ketoglutarate dehydrogenase's catalytic cycle, the FAD in succinate dehydrogenase is just an intermediate, one that (unusually for a flavin) is even covalently bound to the enzyme!

The FAD is part of the *wiring* inside the enzyme. The wiring's job is to move electrons from succinate to ubiquinone. The FAD is no more a product of succinate dehydrogenase than TPP, \[Fe-S\], lipoyl, FMN, haem, or any of the other dozens of cofactors the A-level specification avoids mentioning.

This misconception seems fairly trivial, but [I'm not the only one it annoys](http://sandwalk.blogspot.co.uk/2008/11/biochemistry-on-web-citric-acid-cycle.html "Citric acid cycle argument at Sandwalk"), and it exacerbates two other problems:  

- It's important to grasp that some [coenzymes](http://en.wikipedia.org/wiki/Cofactor_(biochemistry) "Coenzyme at Wikipedia") (like NADH, ATP and ubiquinol) can diffuse from one enzyme to another, and therefore act as exchangeable 'currency' within the cell. Flavins (like FAD and FMN) on the other hand have a tightly-bound, monogamous relationship with their enzyme. They cannot act as currency. By saying reduced FAD is the product of succinate dehydrogenase it gives the misleading impression that FAD is able to diffuse away from the enzyme and *do* something. It cannot: its mobility is fundamentally different from that of NADH, ATP and ubiquinol.
- It is important to be consistent in distinguishing the final products of an enzyme and its intermediate products. By saying reduced FAD is the product of succinate dehydrogenase, the real product of the enzyme, ubiquinol, is obscured, and one arbitrary intermediate of many is promoted into its place. It is very likely that many A-level students will not care to find out what happens to the 'reduced FAD' next. Those that do may question why reduced FAD is considered the product of succinate dehydrogenase but not of α-ketoglutarate dehydrogenase, to which there is no good answer beyond "that's what the exam-board says you must rote-learn". Rote-learning is bad; rote-learning inconsistent and arbitrary errors is worse.
