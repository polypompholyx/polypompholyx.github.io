---
title: Regexes
date: '2012-10-04T09:38:51Z'
lastmod: '2013-04-12T10:23:27Z'
url: /2012/10/perl-regexes/
slug: perl-regexes
draft: false
wp_id: 409
categories:
- Perl
---

## Regular expressions

Before we looked at [file manipulation](/2012/10/perl-files-and-directories/ "Files and directories"), we covered [how to write comparisons with conditionals](/2012/10/perl-conditionals/ "Conditionals"):

```perl
if ( $string eq "Something we're interested in" ) {
    print "Ha, ha!";
}
else {
    print "Boring";
}
```

What happens if there's more than one thing you're interested in though? Writing a gigantic `if/elsif/else` structure or even a  `given/when` switch will make your head spin, and you'll never be sure you've got every possible version of the thing you'd like to match. Take for example, matching something as simple as a letter, number or underscore character:

```perl
if    ( $test eq "a" ) { print "OK" }
elsif ( $test eq "b" ) { print "OK" }
...
elsif ( $test eq "9" ) { print "OK" }
...
elsif ( $test eq "_" ) { print "OK" }
else                   { print "Not a letter, number or underscore!" }
```

This is a waste of time that will be over 63 eye-bending lines long, and still won't match the correct spelling of 'naïve', let alone хуёво. So, from time immemorial, there have been things called 'regular expressions' or 'regexes', which are a way of explaining to a programming language the things you want to match in a neat and tidy fashion. Regex are really a language all of their own (a form of logic programming). However, despite looking like executable line-noise, they are incredibly useful and powerful.

In Perl, regex are written in quotes, of a sort. Here is such a regex:  

```perl
/\w/
```

  
The `/ /` are the 'quotes' for the regex: the regex itself is just the `\w` bit. This regex does exactly what those 63 lines of code would do very badly: they match a single letter, number or underscore. As you know, the `\` is an escaping character: anything after it has some special meaning. The `w` stands for 'word', and `\w` will match a single occurrence of any 'word' character, which is defined as a letter, underscore or number (*i.e.* the things valid in the names of Perl variables and subroutines). The proper name for this is a character class, which we'll cover later. For the moment, suffice it to say `\w` is the same as `[A-Za-z0-9_]` (only it can also cope with non-ASCII letters in  Unicode). So the program we really want to write is:  

```perl
#!/usr/bin/perl
use strict;
use warnings;

chomp( my $test = <STDIN> );
if   ( $test =~ /\w/ ) { print "OK" }
else { print "Not a letter, number or underscore!" }
```

  
The `=~` is the 'binding operator'. It makes `perl` *do* the regex on the right *to* the variable on the left. So:  

```perl
$test =~ /\w/;
```

  
and  

```perl
$_ =~ /\w/;
```

  
will test `$test` and `$_` for wordiness respectively. In fact, (as usual), there's a shorthand for the second one: `$_` is the default variable, and if `perl` finds a naked slash-delimited regex, it'll assume you mean `$_ =~ /naked_regex/`:  

```perl
$_ =~ /\w/;
```

  
and  

```perl
/\w/;
```

  
are the same thing. If a regex matches, it returns TRUE, so:

`print "Match" if /\w/;`

will `print` "Match" only if `$_` contains a word character.

Another useful way to write this is with a logical operator:  

```perl
/\w/ && print "Match";
```

  
Which does the same thing: the `&&` is a short-circuit operator, so if the first thing is FALSE (*i.e.* `$_` is not wordy), it doesn't bother evaluating the second (*i.e.* `print "Match"`). If you want the match to fail (return FALSE) if it matches a word character, you can use `!~` :  

```perl
$test !~ /\w/;
```

  
or simply negate a naked regex with the not `!` operator:  

```perl
! /\w/;
```

  

## The ternary if/then/else operator

  
To make our original program even tinier, we can use this default shorthand, and a new operator, the **`? :`** operator:  

```perl
chomp( $_ = <STDIN>);
print /\w/ ? "OK" : "Not a letter, number or underscore!";
```

  
The **`? :`** operator is like a tiny 'if else' statement:  

```perl
print (
    if $_ matches /\w/ ?
    then return "OK" :
    else return "Not a letter, number or underscore!"
);
```

  
`A ? B : C` will test A to see if it is TRUE. If it is TRUE, it returns B, if it is false, it returns C. `print` then gets handed whatever this statement returns, *i.e.* "OK", or "Not a letter…".  

## One-or-more word characters

  
Now, what if we want to match more than one word character?  

```perl
/\w+/;
```

  
will do just that: a `+` means 'one or more of the preceding character'. So this pattern will match `a`, `bbbbbb`, `d_99` and so on. However, it will *also* match `999;;;plop`, because `999` matches `/\w+/` (`perl` never bothers going as far as the 'plop', as it's already satisfied the match with the 999 - in fact, just with 99).  

## Anchors and escapes

  
If we want to make sure that we match a thing made *entirely* out of word characters, we can use:  

```perl
/^\w+$/;
```

  
The `^` means 'beginning of the string' and `$` means 'end of the string', (beginning and end of the string you `=~` bind to the regex). So this regex will only match strings composed *purely* of word characters.

Another useful escape sequence is `\s`, which matches a space character (including both literal spaces, and `\n` newlines, `\r` carriage returns, `\f` form feeds, `\t` tabs and a few other obscure things). To match a space only, you can just use:  

```perl
/ /;
```

  
and to match a newline:  

```perl
/\n/;
```

  
`\d` will similarly match a single digit `[0-9]`.  

## Capturing parentheses

  
An extremely important thing you can do with a regex is to capture what `perl` actually matched. To do this, you use `( )` parentheses within the regex:  

```perl
/^(\w+)$/;
```

  
If the regex matches `$_`, which it will if `$_` is composed entirely of 'word' characters, then the thing that `\w+` matched will now be squirrelled away by perl for your perusal. How do we get at these stored goodies? Well, there are two ways. The first is to use the pattern match variables, `$1`, `$2`, `$3`, `$4` … Whatever was captured by the first set of parentheses will appear in `$1`, the second set in `$2`, and so on. So:  

```perl
/(\w(\s+)(\w+))/;
```

  
If this actually matches `$_`, then the entire match `\w\s+\w+` will be found in `$1`, the space characters `\s+` will be found in `$2`, and the last word characters `\w+` will be found in `$3`. Another way to do this is to assign the results of the regex to a list outside the regex:  

```perl
my ( $wholething, $space, $word ) = $test =~ /(\w+(\s+)(\w+))/;
```

  
Here, if the regex matches, the values of `$1`, `$2` and `$3` will be dumped into `$wholething`, `$space` and `$word` respectively. You may have just noticed that a regex is a context sensitive thing: in list context it returns the match variables, in scalar context, it returns TRUE or FALSE.  

## Regex modifiers

  
If the regex:  

```perl
/(\w(\s+)(\w+))/;
```

  
makes you eyes hurt, you can use the `/x` *e**x**tended* modifier, thus:  

```perl
/
    (
      this in $1
        \w    # a word character
        (\s+) # some spaces, capture into $2
        (\w+) # some more word characters, capture into $3
    )
/x;
```

  
perl ignores whitespace in a `/x` modified regex. Another very useful modifier is `/i`, which makes a regex case **i**nsensitive:  

```perl
/^hello, world$/i;
```

  
will match "Hello, World", "hello, world" and indeed "HEllO, WoRLd". Note that in regexes, unescaped letters and numbers mean just what you type: it's only escaped alphanumeric characters (`\w` word character, `\d` digit) and punctuation (`+` one or more, `^` start of string) that mean something special.  

## Greediness and quantification of regex atoms

  
Regexes are 'greedy' and 'lazy' by nature. If you have this situation:  

```perl
$_ = "hello everybody";
/(\w+)/;
print $1;
```

  

```text
hello
```

  
`$1` will end up with "hello" in it. This shows that regexes are lazy (they match at the first place in the string they can, so "hello", not "everybody"), and that they are greedy (the regex has matched the maximum possible number of letters, "hello", not just "h" or "hell"). The modifier `+` always tries to greedily slurp up as many characters as it can and still match the whole sequence. The same applies to `*`, which is zero or more of the preceding character:  

```perl
/^\w*$/;
```

  
will match any alpha_num3ric string, and also the empty string "". Another quantifier is the `?`, which indicates you want to match zero or one of the preceeding character:  

```perl
/Steven?/;
```

  
Will match Steve or Steven.

The second most pointless regex in the world is this:  

```perl
/.*/;
```

  
The `.` is a special metacharacter that means 'any character except `\n`', so this regex will match pretty much anything as long as it's not entirely a string of newlines. The *most* pointless regex of *all* is:  

```perl
/.*/s;
```

  
The `/s` modifier makes `.` match `\n` too (it treats a multi-line string with embedded `\n` as a **s**ingle line). So this regex matches zero or more of anything, so it will always match regardless of what `$_` is!

You can specify *exactly* how many of a character you want using `{n,m}` braces:  

```perl
/\w{3}/;   # matches exactly 3 alpha_num3rics
/\w{3,8}/; # matches 3 to 8 alpha_num3rics
/\w{3,}/;  # matches 3 or more alpha_num3rics
/\w{1,}/;  # pedant's version of /\w+/;
/\w{0,}/;  # pedant's version of /\w*/;
/\w{0,1}/; # pedant's version of /\w?/;
```

  
Sometimes, greedy regexes are not what you are after. You can stop regexes being greedy using the `?` modifier on any of the quantifying metacharacters, *i.e.* `* ? {n,m}` and `+` . So:  

```perl
$_ = "hello everybody";
/(\w+?)/;
print $1;
```

  

```text
h
```

  
This code returns the smallest possible match, rather than the greediest.  

## Character classes and Unicode characters

  
As I said earlier, `\w` is (as far as basic ASCII is concerned) equivalent to the 'character class':  

```perl
[A-Za-z0-9_]
```

  
Brackets are used to surround a list of characters that comprise the class. Here are some useful(?) classes:  

```perl
[aeiouAEIOU] # English vowels
[10]         # binary digits
[OIWAHMVX]   # bilaterally symmetrical capital letters
```

  
Any quantifier appearing after a character class applies to the whole character class: one or more of any of the characters in the braces:  

```perl
/[A-Z]+/
```

  
Matches one or more capital letters. You can define your own character classes using this notation, but please have a care for those who live outside the comfy world of 7 bits:  

```perl
$_="El niño";
/(\x{00F1})/ and print "Yep, matched an n-tilde: $1";
```

  
The `\x{00F1}` (which can be abbreviated to `\xF1` if this isn't ambiguous) is the Unicode code point of the ñ character. You can also use named characters with the 'charnames' pragma...  

```perl
use charnames ':full';
$_="á é í ü or even ñ";
/(\N{LATIN SMALL LETTER N WITH TILDE})/ and print "Yep, matched an n-tilde: $1";
```

  
To save yourself even more time, you can `use utf8`:  

```perl
use utf8;
my word = "λόγος";
print "It's all Greek to me\n" if $word =~ /^\w+$/;
```

  
This changes the sematics of `\w` so that it'll match Greek, Arabic, hiragana, hangul, and maybe - one day - even  Tengwar. If this pragma is loaded, it will also allow you to create subroutines with non-ASCII names:  

```perl
use utf8;
λόγος();
sub λόγος
{
    print "You'll be lucky if 'λόγος' prints correctly in your terminal!\n";
}
```

  
Most of the punctuation *metacharacters* (the characters like `+` and `.` and `*` that mean something special in a regex) lose their meta-nature inside a character class. Usually, you have to escape these metacharacters in a regex:  

```perl
/\*/;
/ \+ \? /x;
```

  
The first will match a literal \* character, the second a literal string of +?. But inside a character class, you don't need to bother:  

```perl
/[*+.]+/;
```

  
will match one or more asterisks, periods or pluses  there's no need to escape them, because only a few characters mean something special inside a character class. The characters that *do* mean something special *inside* a character class include `-`, which makes a natural range, as you saw in the definition of `\w` (hence `[A-Z]`, `[a-f]`, `[1-6]`, `[0-9A-Fa-f]`, *etc*.), and `^`, which means 'anything except…' **iff it's the first item in the brackets**. So:  

```perl
/[^U]/;          # anything but the capital letter U
/[^A-Z0-9]/;     # anything but capital letters and numbers
/[A-Z^]/;        # capital letter or caret
/[^A-Z^]/;       # anything but a capital letter or caret
/[^A-Za-z0-9_]/; # anything but a word character.
```

  
Now, that last one could be written more easily as `/[^\w]/` or even better as `/\W/`, the `\W` being Perl's shorthand for 'anything but an alpha_numeric'. Likewise `\S` is anything but whitespace, and `\D` is anything but a digit.  

## Leaning toothpick syndrome

  
If you *do* want to include a special character like `-` or `^` in a character class, you'll need to escape it:  

```perl
/[ \\ \/ \- \] ]/x; # note the x so I can pad them nicely with spaces
```

  
This will match a single backslash `\` (which you *always* need to escape in Perl, whether in plain code, regex or in a character class). It will also match a forward slash `/`, a `]` close-bracket (this needs escaping, else it'll be prematurely interpreted as the end of the character class) or a hyphen `-`. You may be wondering about why you also have to escape the `/`. This is for similar reasons [escaping quotes in strings](/2012/10/perl-not-a-hello-world-script/ "Not a hello world script"). If you don't escape the regex delimiter `/`, `perl` will think the regex finishes in the wrong place. Fortunately for matching path names under Unix, like `qq()` and `q()`, you can specify your own regex quotes with `m()` (for **m**atch):  

```perl
m(\w+?);
m{[\\ / \- \] ]}x;
```

  
See that with the second, you no longer need to escape the `/`. This is very useful in situations where otherwise you'd be writing:  

```perl
/C:\/perl\/bin\/perl\.exe/;
```

  
which is called leaning toothpick syndrome:  

```perl
m{C:/perl/bin/perl\.exe};
```

  
is rather better. As with quoting strings, avoid clever and cute delimiters: stick to slashes, parentheses or braces unless you want the maintainer of your code to come calling with a machete.  

## Alternation and grouping without capturing

  
What else can you do with regexes? Well, you can specify alternatives:  

```perl
/foo|bar/;
```

  
which will match both foo and bar, using the `|` or pipe-character. One problem with this is sometimes you'll need to group things using parentheses:  

```perl
/([Cc]ornelia|my ex-snake) eats (\w+)/;
```

  
but now the interesting thing you're trying to capture (what `[Cc]ornelia` eats) is in `$2`, not `$1`, which may be OK, but if you'd rather not have spurious pattern match variables to ignore, you can use the grouping-but-not-capturing `(?: )` regex extension:  

```perl
( $food ) = /(?:[Cc]ornelia|my ex-snake) eats (\w+)/;
```

  
The `(?: )` allows grouping, but doesn't squirrel away a value into `$1` or its friends, so it doesn't interfere with assigning captures to lists. There are dozens of other regex extensions looking like `(?...)` in Perl regexes, which you can explore yourself (they also make Perl's regular expression highly *ir*regular to computer scientists).  

## Match variables

  
Perl has three special regex punctuation variables. `` $` $& `` and `$'` . These are the pre, actual, and post match variables:  

```perl
my $string =  "Cornelia ate mice that I'd thawed on the radiator";
$string    =~ /mice|mouse/;
print "PRE $`\nMATCH $&\nPOST $'\n";
```

  

```text
PRE Cornelia ate
MATCH mice
POST that I'd thawed on the radiator
```

  
Using these three variables will slow down your program, and are almost unreadable, but use them if you must.  

## Back-references

  
One last thing to do is to use what you've already matched, *i.e.* back-reference within a regex. Say you want to find the first bold or italic word in an HTML document:  

```perl
my $html_input_file = shift @ARGV;
local $/ = undef; 
    # this sets the local 'input separator' to nothing, so that
open my $HTML, $html_input_file
    or die "Bugger: can't open $html_input_file for reading: $!";
$_ = <$HTML>;
    # this will slurp in an entire file, rather than a line at a time
m{
    <(i|b)>
        # an <i> or <b> tag, captured into $1
    (.*?)
        # minimum number of any characters captured into $2
    </\1>
        # an </i> or </b>, depending on the opening tag
}sxi;
        # . matches \n, extended, case insensitive
print "$2\n";
```

  
The `\1` allows the pattern to match *the same* something that would end up in `$1`, here 'b' or 'i'. This isn't written `$1` like you'd expect (there is a good but technical reason). This regex (or some variation on it) looks like it will parse HTML. However, it is actually impossible to parse nested languages like [HTML](lesson13.html#htmlparser) or [XML](lesson17.html) without a more complex sort of grammar than can be provided by regexes. Getting around this problem can wait until a later post.  

## Quote-regex operator

  
Regexes can be used both directly, and stored for later use using the `qr()` operator. This q(uote) r(egex) operator is a simple way of keeping regexes and passing them around like strings:  

```perl
my $regex = qr/(?:milli|centi)pedes?/i;
my $text  = "Millipedes are cute. No really.";
print "Found something interesting\n" if $text =~ /$regex/;
```

  
You can use `$regex` wherever you'd usually use a regex (in a match, or a substitution), and you can pass it to subroutines, or use it as part of a larger regex. Note that any modifiers, like `/i`, are internally incorporated into the string and honoured. You can even print out the `$regex` as a string. How useful.  

## Regex summary

  

- Atoms of regexes: alpha_numeric characters, character class escapes (`\w` word, `\W` not-word, `\s` space, `\S` not-space, `\d` digit, `\D` not-digit), character classes `[blah1-9] and negated classes [^blah1-9]`, escaped metacharacters (`\.` a literal . period), metacharacters ( `.` anything but `\n`).
- Alternatives : use the `|` for alternatives.
- Quantifiers for the atoms: `*` (0 or more), `+` (1 or more), `?` (0 or 1), `{n,m}` (between n and m).
- Greediness : can be turned off with a `?` following the `+ ? * {n,m}` quantifiers.
- Capturing : use `()` parentheses, and grab `$1`, `$2`, *etc*. Use `(?: )` to avoid captures if you just want to use the parentheses to group, not capture.
- Backreferences : use `\1`, `\2`, inside the match instead of `$1`, `$2`, *etc.*
- Modifiers: `/x` ignores whitespace and comments, `/s` makes . match `\n`, and `/i` make the regex case-insensitive. These are usually called the `/X` modifiers, even though the / is actually part of the regex quoting mechanism. There is also a `/m` modifier that changes the semantics of the start and end of string markers (`^ $ \A \Z \z`). `perldoc perlre` for details.

  
Next up...[substitutions, splitting and joining](/2012/10/perl-substitute-split-join/ "Substitutions, splitting and joining").
