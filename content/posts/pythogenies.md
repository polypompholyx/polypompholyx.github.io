---
title: Pythogenies
date: '2020-03-23T11:01:25Z'
lastmod: '2020-03-23T11:01:25Z'
url: /2020/03/pythogenies/
slug: pythogenies
draft: false
wp_id: 2473
categories:
- Uncategorized
tags:
- phylogenetics
- Python
---

I had to teach myself a bit of Python recently, so decided to do it by implementing this [parse_phylogeny.py](/wp-content/uploads/2020/03/parse_phylogeny.txt) thing (it's uploaded here as a text file). It takes a nice intuitive mark-down for phylogenetic trees (below) and spits out a Newick file (`-f nwk`), or a [Wikipedia clade](https://en.wikipedia.org/wiki/Template:Clade) format (`-f wp`). It's not amazing (hey, it was my first attempt at Python in anger) and I know there's a bunch of repetitious stuff in the functions that could be lifted out, but whatever. Maybe you'll find a use for it.  

    -Embryophyta
      -Liverworts
        -_____
          -_____
            -Hornworts
            -Tracheophytes
              -Euphyllophytes
                -Spermatophytes
                  -Gymnosperms
                  -Angiosperms
                -Ferns
              -Lycopods
        -Mosses
