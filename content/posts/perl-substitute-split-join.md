---
title: Substitutions, splitting and joining
date: '2012-10-04T12:31:11Z'
lastmod: '2013-04-12T10:26:26Z'
url: /2012/10/perl-substitute-split-join/
slug: perl-substitute-split-join
draft: false
wp_id: 446
categories:
- Perl
---

## Substitution and transliteration

[Matching patterns](/2012/10/perl-regexes/ "Regexes") is very useful, but often we want to do something more than just match things. What if you want to replace every occurrence of a certain thing with something else? This is the domain of the `s///` and `tr///` operators. `s///` is the substitution operator, and `tr///` is the transliteration operator. `tr///` is useful for simple things:

```perl
my $string =  "all lowercase with 5ome num8er5";
$string    =~ tr/a-z/A-Z/;
print $string;
```

```text
ALL LOWERCASE WITH 5OME NUM8ER5
```

You just make a list on one side of the `tr///`, and a list on the other side (hyphens can be used to create natural ranges), and perl will map one lot to the other. The substitution operator is even more powerful and useful:

```perl
$_ = "old M\$ dross";
s/old/new/i; # substitute any occurrence of old with new, case insensitively
s/M\$/Microsoft/i;
s/dross/loveliness/i;
print; # did you forget print defaults to $_ ?
```

```text
new Microsoft loveliness
```

## Interpolation in regexes

In the second one, note you have to escape the `$`. This is because both pattern matching and substitution can interpolate variables:

```perl
my $name   = "Cornelia";
my $string = "Cornelia is a corn-snake.";
print "Matched $name\n" if $string =~ /$name/;
$string =~ s{is}{was}; # *sniff*
print $string;
```

```text
Matched Cornelia
Cornelia was a corn-snake.
```

Note that like `m//`, `s///` and `tr///` can use the usual 'any quotes you fancy', although avoid `?` and `'` , as they have a special significance. So:

```perl
s|A|B|;  # three the same
s(A){B}; # two pairs
s{A}|B|; # one pair, two the same
```

all work, although I'd only recommend the middle one.

## Substitution modifiers

The `s///` can take all the modifiers (`/s`, `/x`, `/i`) that matching `m//` can take, but it has another two of its own, `/g` and `/e`. `/e` is like a little `eval` (which we will discuss later) that evaluates the substitution's right hand side, and `/g` means 'globally', *i.e.* do it to every match you find:

```perl
my $string =  "2 3 4 5 6";
$string    =~ s/ (\d+) / 2 * $1 /xge; # double every number you match
print $string;
```

```text
4 6 8 10 12
```

If you hadn't noticed, when you use a substitution with capture parentheses, the captures are in `$1`, *etc*., as usual, and you can use these on the right hand side of the `s///`. Of course, you can also use `/g` and `/e` separately. In fact, you can use `/g` on `m//` as well:

```perl
$_ = "2 3 4 5 6";
while ( /(\d+)/g ) { print "$1 times 2 is ", $1 * 2, "\n"; }
```

```text
2 times 2 is 4
3 times 2 is 6
4 times 2 is 8
5 times 2 is 10
6 times 2 is 12
```

Here, the `/g` means 'keep matching till you run out of string'.

## Splitting and joining strings

There are several operators that use pattern matching of one sort or another. The first is `split`. `split` expects a list. The first argument is the regex you want to `split` the string on, the rest of the arguments are things to `split`. You can capture the `split` bits in an array:

```perl
my $string   = "A : colon:delimited: file: with: some : random :spaces";
my ( @bits ) = split /\s*:\s*/, $string;
    # splits on colons surrounded by optional spaces
print "$_\n" foreach @bits;
```

```text
A
colon
delimited
file
with
some
random
spaces
```

The opposite of `split` is `join`, which has a similar syntax, only it expects not a regex as its first argument, but a string. So:

```perl
my $joined = join "|", qw/one two three four five six/;
print $joined;
```

```text
one|two|three|four|five|six
```

How about this:

```perl
print join "|", reverse split /\s*:\s*/, 
    "A: colon: delimited  : file: with  :    spaces";
```

```text
spaces|with|file|delimited|colon|A
```

Running list operators into each other like this a) is clever, but b) easily becomes unreadable. *Caveat scriptor*.

## Grepping

Another useful tool for regex is `grep`. This operator takes a regex as its first argument too, and a list of things to '`grep`' as the rest. What is `grep`ping? Well, `grep`ping means 'returning the things that match from a list':

```perl
my ( @names )     = qw/ Cornelia Atropos Lachetis Amber /;
my ( @match )     = grep   /^A/, @names;
my ( @not_match ) = grep ! /^A/, @names;
print "Start with A @match\nDon't @not_match\n";
```

```text
Start with A Atropos Amber
Don't Cornelia Lachetis
```

See that you can make an anti-`grep` using the `!` 'not' before a regex. The way `grep` actually works is by running through the list you give it, setting `$_` to each item in turn. It then uses the regex to pattern match on `$_`, as usual. Only things that match are returned. `grep` is useful for finding lines in a file that match a certain pattern. It's another of those Perl operators that returns different values in scalar and list context. In list context (previous example) it return the list of matches, but in scalar context:

```perl
my $number = grep /^A/, @names;
```

it returns the number of matches. `grep` can be heavily abused, syntactically speaking:

```perl
grep /regex/, LIST;
grep { /regex/ } ( LIST );
```

Both work the same, although I always use the latter, as it makes the condition more obvious. [This may vaguely remind you of `sort`](lesson04.html#sort). I prefer the second version, even though it's line noise for its own sake.

## Mapping

One final operator before we leave regexes. `map` has nothing to do with regexes, but it has a similar syntax to `grep` (and to `sort` for that matter). I love `map`. There's nothing like it for bringing out the mathematician in you. `map` needs a block of code that does something to `$_`, followed by a list, just like `grep`. `map` then runs though the list, using `$_` to cache each value, so you can torture it with the block of code:

```perl
@mapped = map { DO_SOMETHING_TO $_ } ( LIST );
```

So:

```perl
@doubled = map { 2 * $_ } ( qw/ 2 4 6 8 10 / );
print "@doubled";
```

```text
4 8 12 16 20
```

This is shorthand for:

```perl
@doubled = map { return 2 * $_ } ( qw/ 2 4 6 8 10 / );
print "@doubled";
```

in case you were wondering: blocks return the last thing they evaluated in the absence of an explicit `return` statement.

Dull? Yes. But how about:  

```perl
@selective_doubles = 
    map { /[24680]$/ ? ( 2 * $_ ) : $_ } ( qw/ 1 2 3 4 5 6 7 8 / );
print "@selective_doubles";
```

  

```text
1 4 3 8 5 12 7 16
```

  
which returns a list of numbers that have been doubled *iff* (if and only if) they are even.

One word of warning for both `grep` and `map`. `$_` is not a *copy* of the data in the list you feed to these functions, it's an *alias* to the actual values of the list. That means that **if you modify `$_` itself, rather than just returning it, you will alter the items in the list** *fed to* `grep` or `map`, not just the items in the returned list. This may be what you want, but probably isn't:  

```perl
my @original = qw/Abacus chocolate sprite/;
print "original: @original\n";
my @returns = map { s/A//gi; } ( @original );
print "afterward: @original\nreturned: @returns\n";
```

  

```text
original: Abacus chocolate sprite
afterward: bcus chocolte sprite
returned: 2 1
```

  
You may be wondering what the hell has happened. Well, firstly, the actual members of `@original` have been altered, because `s///` messes with `$_` directly. Hence all the A characters have been stripped. The `s///` operator returns the *number* of substitutions in scalar context, hence `@returns` contains 2 (**A**b**a**cus), 1 (chocol**a**te) and `undef` (since sprite contains no `/A/i`). If you remember that a `map` is basically a `foreach` loop:  

```perl
my @mapped = map { DO_SOMETHING_TO $_ } ( LIST );
```

  
and  

```perl
my @mapped;
foreach ( LIST ) {
    my $return_value = DO_SOMETHING_TO $_;
    push @mapped, $return_value;
}
```

  
are the same thing, you'll be fine. As long as you [remember that altering the value of `$_` in a `foreach` loop](lesson02.html#foreach) indirectly alters the original value in the `LIST`, that is! Go on, try writing the `s///` `map` as a `foreach` loop, and you'll see what I mean.  

```perl
my @original = qw/Abacus chocolate sprite/;
print "original: @original\n";
my @returns;
foreach ( @original )
       {
    my $return_value = s/A//gi;
    push @returns, $return_value;
}
print "afterward: @original\nreturned: @returns\n";
```

  
Told you so. What you probably need in this case is a temporary variable:  

```perl
my @original = qw/Abacus chocolate sprite/;
print "original: @original\n";
my @returns = map { my $tmp = $_; $tmp =~ s/A//gi; $tmp; } ( @original );
print "afterward: @original\nreturned: @returns\n";
```

  

```text
original: Abacus chocolate sprite
afterward: Abacus chocolate sprite
returned: bcus chocolte sprite
```

  
So, to summarise:

The `s///` operator acts like the `m//` operator, but selectively substitutes text. The `tr///` operator is quicker and easier for simple substitutions. The syntax of the new list operators is:  

```perl
@splat = split /\s/, @splitees;
@junt  = join '+', @joinees;
@mup   = map { $_ * 2 } @mappees;
@grap  = grep { /\d+/ } @grepees;
@argh  = map { "IP: $_" } 
           join '.', split /\:/, 
             grep { /^\d{1,3}:\d{1,3}:\d{1,3}:\d{1,3}$/ } 
               ( @ip );
```

  
Next up...[references and data-structures](/2012/10/perl-refs-data-structures/ "References and data structures").
