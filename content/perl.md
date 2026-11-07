---
title: Perl
date: '2012-10-03T12:33:19Z'
lastmod: '2013-10-20T14:44:02Z'
url: /perl/
slug: perl
draft: false
wp_id: 292
wp_page: true
wp_comments:
- id: 795
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2012-10-23T14:25:24Z'
  kind: comment
  html: <p>I hope to get old-fashioned objects done before the end of the year (2012), but I have a feeling I won't have this completely finished before February 2013. The other tutorial sections need a lot more work than the basic syntax ones; indeed, a couple of them need writing from scratch!</p>
  depth: 0
- id: 2490
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2013-02-09T11:52:27Z'
  kind: comment
  html: <p>Making promises I can't keep, it would appear. Easter 2013 is the new target for *all finished*.</p>
  depth: 0
---

You're going to need three things to write Perl.  

- A computer.
- The `perl` interpreter.
- A text editor.

  
The computer thing is easy, as I presume you have one to read this. You will need some basic familiarity with your computer's [file system](http://en.wikipedia.org/wiki/File_system "File system at Wikipedia"), and how to open its [command line interface](http://en.wikipedia.org/wiki/Command-line_interface "CLI at Wikipedia").

The `perl` interpreter works on just about any computer you can name, so whether you're running MacOS, Windows, or some flavour of Unix, then all is well. You can [download the source and binaries](http://www.cpan.org/ports/index.html "Perl source and binaries on CPAN") from CPAN, the [Comprehensive Perl Archive Network](http://www.cpan.org/ "CPAN"), where you can also obtain sundry modules. If you're running Linux or some other Unix (including MacOSX, which is BSD under the hood), you will almost certainly have a recent version of `perl` on your system anyway. If not, install it yourself by compiling the source code from CPAN with the C compiler of your system (*e.g. *`gcc`). If you're on Windows you can download a precompiled binary distribution from [Active State](http://www.activestate.com/activeperl/downloads) or [Strawberry Perl](http://strawberryperl.com/ "Strawberry Perl").

A text editor is something like vi or [vim](http://www.vim.org/ "vim"), [emacs](http://www.gnu.org/software/emacs/ "emacs"), [UltraEdit](http://www.ultraedit.com/ "Ultraedit"), [Notepad++](http://notepad-plus-plus.org/ "Notepad++"), or even (ugh) Notepad. It is *not* Word. You don't need a bells-and-whistles text editor, or integrated design environment to write decent code.

Some conventions I'll be using:  

```perl
Code to be entered into a text editor, saved and run
```

  

``` input
Things to type into a command line (bash/cmd/<em>etc.</em>)
```

  

```text
Output that perl spits onto the command line
```

  
You may find the following Perl sites useful:  

- [Perl dot org](http://www.perl.org "Perl dot org"), for all things perl.
- [Perl dot com](http://perl.com/ "Perl dot com"), for news and views.
- [CPAN](http://www.cpan.org "CPAN"), for modules.
- [Perlmonks](http://www.perlmonks.org "Perlmonks"), for help.

  
This tutorial was originally published on my [old website](http://www.steve.gb.com "Steve dot gb dot com"), but I stopped maintaining it and it became old and out-of-date, so I decided to pull it. I've recently ported it, updating it as I go along.  

1.  [Not a hello world script](/2012/10/perl-not-a-hello-world-script/ "Not a hello world script") - using `print`, shebangs, and running scripts.
2.  [Input and output](/2012/10/perl-input-and-output/ "Input and output") -input with `<STDIN>`, output with `print` and `say`, creating `$scalar` variables, and `chomp`.
3.  [Arrays and slices](/2012/10/arrays-and-slices/ "Arrays and slices") - creating and accessing simple `@array` data.
4.  [Hashes](/2012/10/perl-hashes/ "Hashes") - creating and accessing simple `%hash` data.
5.  [Simple loops](/2012/10/perl-simple-loops/ "Simple loops") - scalar and list context, `scalar`, array interpolation in strings, `increment++`, decrement`--`, C-style `for` loops, basic mathematical operators and concatenation.
6.  [Prettier loops and nicer code](/2012/10/perl-pretty-loops-nicer-code/ "Prettier loops and nicer code") - `foreach` loops, the default `$_` variable, quoting strings with `qq`, `q`, and `qw`, `$/` and statement modifier `foreach`.
7.  [Bondage, discipline and subroutines](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines") - creating user-defined functions with `sub` and `return`, the `@_` array, lexical scope, the `use strict` pragma and `my` variables, more loops (`while` and `until`) and things to do to arrays (`push`, `pop`, `shift`, `unshift`, `reverse` and `splice`).
8.  [Conditionals](/2012/10/perl-conditionals/ "Conditionals") - the truth according to Perl, `if`, `elsif`, `else`, `unless`, numerical (`==`) and string (`eq`) comparisons.
9.  [More hashes and sorting](/2012/10/perl-more-hashes-sorting/ "More hashes and sorting") - manipulating hashes with `each`, `keys` and `values`, sorting things with `sort`, the ASCIIbet, `sort` subroutines, Orcish manoeuvre and Schwartzian transform.
10. [Symbol table](/2012/10/perlsymbol-table/ "Symbol table") - the symbol table and typeglobs, dynamic `local` and lexical `my` scoping; follows on from hashes, but probably skippable for the casual reader.
11. [Files and directories](/2012/10/perl-files-and-directories/ "Files and directories") - opening, reading and writing files, opening and reading directories, `die` and `warn`, logical operators (`or`, `||` and friends), operator precedence, pipes, running external programs with `system`, and getting information with `perldoc`.
12. [Regexes](/2012/10/perl-regexes/ "Regexes") - regular expressions, `/ /`, `=~` and `!~`, character classes, quantifiers, alternation, capturing matches, back-references and modifiers.
13. [Substitutions, splitting and joining](/2012/10/perl-substitute-split-join/ "Substitutions, splitting and joining") - list manipulation with `split`, `join`, `grep` and `map`, the `s///` and `tr///` substitution and transliteration functions.
14. [References and data structures](/2012/10/perl-refs-data-structures/ "References and data structures") - taking and dereferencing references, arrayrefs, hashrefs, coderefs, closures, `do`, `Data::Dumper`.
15. [Bits and bobs](/2012/10/perl-bits-and-bobs/ "Bits and bobs") - capturing exceptions, `eval`, `$?`, telling the `localtime`, `sleep`, `sprintf` and `printf`, loop control with `LABELS:`, `last` and `next`, heredocs.
16. [Installing modules](/2012/10/perl-install-modules/ "Installing modules") - installing modules from CPAN, `ppm`, and some useful modules I couldn't live without: `Getopt::Long`, `DBI`, `File::`, `Net::`, `HTML::Template`.
17. [Packages and writing modules](/2013/02/perl-packages-modules/ "Packages and writing modules") - `h2xs`, `Module::Starter`, `Exporter` and documenting code with POD.
18. [Classes and objects](/2013/02/classes-and-objects/ "Classes and objects") - object oriented syntax, classes, objects, inheritance, hand-rolling `bless`ed hashrefs.
19. [Moose objects and roles](/2013/04/perl-moose-objects-roles/ "Moose objects and roles") - using `Moose` to define classes declaratively, code reuse with roles.
20. [Command-line](/2012/10/perlcommand-line/ "Command line") - one-liners, command-line switches.
21. [Debugging](/2012/10/perl-debugging/ "Debugging") - finding bugs and squashing them, avoiding creating bugs in the first place.
