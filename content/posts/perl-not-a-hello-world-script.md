---
title: Not a hello world script
date: '2012-10-03T12:12:16Z'
lastmod: '2013-04-12T09:40:24Z'
url: /2012/10/perl-not-a-hello-world-script/
slug: perl-not-a-hello-world-script
draft: false
wp_id: 307
categories:
- Perl
---

Rather than employing the usual tactic of showing you how to write the accursed 'hello world' program, so beloved of all computer programming introductions, let's start with something entirely different:  

```perl
print "This is most definitely not a hello world script.\n";
```

  
If you save this as the file `thing.pl`, or similar, then you can run it from the command line (*i.e.* DOS prompt, bash shell, terminal window) thusly:  

``` input
perl thing.pl
```

  
And it will probably do what you expect.  
If you didn't misspell anything in the script, when executed it should do something along the lines of printing out:  

```text
This is most definitely not a hello world script.
```

  
If you're on a Unix or MacOSX, it's better if you write this instead:  

```perl
#!/usr/bin/perl
print "This is most definitely not a hello world script.\n";
```

  
or  

```perl
#!/bin/perl
print "This is most definitely not a hello world script.\n";
```

  
at the top of your script, all on its own. Then you can just type:  

``` input
thing.pl
```

  
at the command prompt. The `/usr/bin/perl` (or whatever) after the *shebang* (`#!`) is the path to the `perl` interpreter, and it tells the Unix shell where to find it. Windows will also cope with a naked `thing.pl` providing you have included  `C:\Perl\bin` in your `PATH` environment variable and added `*.PL` to the `PATHEXT` environment variable. The ActiveState installer sorts this all out for you.

It's generally considered polite to put a shebang at the top of scripts even if you're not on Unix, in the name of portability: `perl` works just about anywhere, and it's a nice idea to try and make your Perl scripts and modules work anywhere too. Note the subtle difference between `perl` (the executable program that interprets your program) and Perl (the language interpreted by the `perl` interpreter). This distinction, and even more so the fact that *neither* is written 'PERL' is a shibboleth: using 'PERL' will mark you out as a n00b, so Don't Do That.

So far so easy. The only thing I hope you may be wondering about is the `\n`. This means 'newline', and will print whatever your operating system thinks is a newline at the end of the output. The `\n` character is an *escape sequence* because whatever comes after a `\` has a special meaning to `perl`: `\n` is a newline, `\t` is a tab, and `\\` is a literal \\ character. We will come across many other sorts of escape sequence, especially when we get onto [regexes later](/2012/10/perl-regexes/ "Regexes").

Something very important to notice about the script that we have just written is the `;` semicolon at the end of the line: Perl statements must (almost) always end in a semicolon, unlike those in some [other languages beginning with p](http://www.python.org "Python"). Forgetting trailing semicolons is a frequent source of bugs.  

## Strings and quoting

  
One of Perl's strengths is the multitude of ways you can quote and manipulate a *string* like `"This is most definitely not a 'hello world' script"`. First, try this out:  

```perl
#!/usr/bin/perl
print 'This is most definitely not a hello world script.\n';
```

  
note the `'` single quote replacing the `"` double quote we used in the first script. If you run this, it will print out:  

```text
This is most definitely not a hello world script.\n
```

  
In Perl, *double quotes* will *interpolate* escape characters like `\n`, and `\t`, so an escape sequence like `\n` gets converted into a real, literal newline between double quotes. Single quotes will translate *only* the escape `\'` to a literal `'` and the escape `\\` to a literal `\`. Double quote are therefore what you need to do clever, intuitive things; and single quotes are what you need to do simple, literal things. Since single quotes only interpolate `\'` and `\\`, this is the way to insert single quotes into a single-quoted string:  

```perl
#!/usr/bin/perl
print 'This is most definitely not a \'hello world\' script.';
```

  
which prints out:  

```text
This is most definitely not a 'hello world' script.
```

  
with embedded single quotes around the 'hello world' bit. The reason we must escape the single quotes within our string is that if you *don't* escape the two single quotes around the `'hello world'` bit, `perl` will think you mean the string to end just before the hello, and will throw a tizzy:  

```perl
#!/usr/bin/perl
print 'This is most definitely not a 'hello world' script.\n';
```

  
without suitable escaping of the quotes, looks to `perl` like:  

```perl
#!/usr/bin/perl
print 'This is most definitely not a '
    # FIRST UNESCAPED SINGLE QUOTE ENDS THE STRING,
    # WHAT THE HELL IS THIS NEXT BIT SUPPOSED TO MEAN?
      script.\n';
```

  
The same applies to double quotes: if you want double quotes in a double-quoted string, you'll need to escape them too `\"`:  

```perl
#!/usr/bin/perl
print "I said \"hello world\". Are you deaf?\n";
```

  
In Perl, all strings (*i.e.* anything that isn't a number) should be quoted somehow or other. If you don't use quotes, `perl` will quite likely barf, probably saying something about 'bare-words'. You *must* put quotes around strings, so:  

    print "Nubbins";

  
is fine, as is:  

    print 'Nubbins';

  
but the bare-word `Nubbins` in this:  

    print Nubbins;

  
will not be interpreted as a string. Perl has several other methods of quoting strings like [heredocs and `printf`](/2012/10/perl-bits-and-bobs/ "Bits and bobs"), which we'll also cover later.

Next up...[input and output](/2012/10/perl-input-and-output/ "Input and output").
