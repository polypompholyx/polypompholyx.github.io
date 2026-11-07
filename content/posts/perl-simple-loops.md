---
title: Simple loops
date: '2012-10-03T13:55:29Z'
lastmod: '2013-04-12T09:49:53Z'
url: /2012/10/perl-simple-loops/
slug: perl-simple-loops
draft: false
wp_id: 347
aliases:
- /2012/10/perl-loops/
categories:
- Perl
---

## Loops

Hopefully you're now happy with the fundamental data types in Perl: scalars, [arrays](/2012/10/arrays-and-slices/ "Arrays and slices") and [hashes](/2012/10/perl-hashes/ "Hashes"), so most of the script below shouldn't be too mysterious:

```perl
#!/usr/bin/perl
print "What is your name?\n";
$name = <STDIN>;
chomp $name;
@beans = ( "adzuki", "haricot", "mung" );
print( "\@beans contains ", scalar @beans, " members: @beans\n" );
for ( $i = 0; $i < scalar @beans; $i++ ) {
    print "$name likes $beans[$i] beans.\n";
}
```

```text
@beans contains 3 members: adzuki haricot mung
Steve likes adzuki beans.
Steve likes haricot beans.
Steve likes mung beans.
```

Don't get scared by the line-noise (*i.e.* all the punctuation): if you do, [regexes](/2012/10/perl-regexes/ "Regexes") will probably be fatal. The very beginning should be quite obvious now:

```perl
print "What is your name?\n";
$name = <STDIN>;
chomp $name;
```

means something like, "read in someone's name from a command prompt, get rid of the trailing newline from the input, and stick the result in the scalar variable  `$name`", whilst:

```perl
@beans = ( "adzuki", "haricot", "mung" );
```

means "create a list of the strings 'adzuki', 'haricot' and 'mung', and store the list in the array variable `@beans`". Note that `@beans` and a hypothetical `$beans` (and an even more hypothetical `%beans`) would be completely *different* variables: mucking about with one would have no effect on the other.

## Context

The next line prints out some stuff about the beans:

```perl
print( "\@beans contains ", scalar @beans, " members, @beans\n" );
```

You may have some difficulty with exactly what is going on here, but all we're doing is feeding `print` a list of three items:

```perl
print( "a string", something to do with @beans, "another string" );
```

Let's consider the three items in the list separately:

```perl
"\@beans contains "
```

is responsible for the bit of the output that looks like

```text
@beans contains
```

You need to escape (use a `\` on) the `@` of `@beans`. If you put a Perl variable into a double-quoted string, the variable name will be replaced with the actual contents of that variable. So, if you don't escape the `@`, `perl` will interpolate the entire contents of `@beans` ("adzuki haricot mung") into what it's going to print, a fact that we'll take advantage of in a minute. With the `\`, it prints a literal `@` symbol instead, followed by the string 'beans' (no pun intended). So, `\$` and `\@` are two more escape characters like `\"` and `\n`.

`print` is a *list operator*, that is, it will print out any stuff you put in a list after it. In just the same way as array variables, a list is some stuff between `( )` parentheses, separated by commas, so the stuff we're feeding `print` *is* a list (just look at the code), and the next item is:  

```perl
scalar @beans
```

  
Perl is a helpfully (well, *usually* helpfully) context sensitive language. Unsurprisingly, the two main contexts it recognises are scalar (singular) context, and list (plural) context, which you've already met in passing when we discussed array and hash access and slicing. `print` *forces* list context on the things that follow it. So, if you simply put this:  

```perl
@beans
```

  
you'd get a mess, because *the usual behaviour of an array in list context is to interpolate all its members*. `perl` would squadge the contents of `@beans` ("adzukiharicotmung") into the output, not even padding it with spaces like it does between double quotes. That's not what we're after here. What we actually want is the *number* of items in the array. *In scalar context, an array will return the number of members it contains*, which is just what we want. Scalar context can be *forced* using the `scalar` operator, hence the upshot of:  

```perl
scalar @beans
```

  
is to give the size of the array, rather than its contents, to `print`, which it duly does:  

```text
3
```

  
List/scalar context is one of Perl's more esoteric, but more useful features, and we'll come across more as we go along. For now, remember that if you assign stuff to an array:  

```perl
@holes = ( "nostril", "meatus", "bumhole");
```

  
or use an operator that expects a list, like `print`:  

```perl
print( "nostril", "meatus", "bumhole");
```

  
the arguments ("nostril", and so on) will be interpreted in list context unless you explicitly use the `scalar` keyword. Many Perl functions, and some sorts of variable, return different values in scalar and list contexts. Most importantly for the present moment, an array will be interpreted as a *list of its members* in list context, but will be interpreted as the *number of its members* in scalar context. Hence:  

```perl
@holes = ( "nostril", "meatus", "bumhole");
print @holes, "\n";
    # print forces list context on what it's given
$number = @holes;
    # $number forces scalar context so perl assigns the size of
    # array @holes to $number
print $number;
print scalar @holes;
    # scalar also forces scalar context, overriding print's
    # preference for lists
```

  

```text
nostrilmeatusbumhole
3
3
```

  
Finally, the last item given to `print` in our original program is:  

```perl
" members, @beans\n"
```

  
which is responsible for the output of  

```text
members, adzuki haricot mung
```

  
Double quote interpolate the contents of the array into the string, padding the members with spaces, hence the output of:  

```text
adzuki haricot mung
```

  
rather than:  

```text
adzukiharicotmung
```

  

## `for` loops

  
The very last bit of the code:  

```perl
for ( $i = 0; $i < scalar @beans; $i++ ) {
    print "$name likes $beans[$i] beans.\n";
}
```

  
is a `for` loop. `for` loops take a bit of explanation, and mercifully, Perl has a cute shortcut for loops which we'll investigate in a minute. But first, let's learn it the hard, C-style way, which is occasionally useful. A `for` loop, as you may know/have guessed, looks like:  

```perl
for ( LOOP_VAR = START_VALUE; TEST_LOOP_VAR; INCREMENT_LOOP_VAR ) {
    DO_SOMETHING;
}
```

  
The `( )` and `{ }` are required, but you can write this with non-K&R style bracing:  

```perl
for ( LOOP_VAR = START_VALUE; TEST_LOOP_VAR; INCREMENT_LOOP_VAR )
{
    DO_SOMETHING;
}
```

  
or with hideous bracing like this:  

```perl
for 
( LOOP_VAR = START_VALUE; TEST_LOOP_VAR; INCREMENT_LOOP_VAR ) 
{ DO_SOMETHING; }
```

  
if you'd rather, whatever looks best to you: Perl is largely space and newline insensitive as mentioned above. It's fairly obvious from the output that the loop in the program prints:  

```text
Steve likes XXXXX beans.
```

  
for each member of the array `@beans`. How exactly does it do this? First it sets the *loop variable*, `$i`, to a starting value of 0. Then it tests the loop variable to see if it's smaller than the `scalar` size of `@beans` (which is 3). On each passage of the loop, it does the INCREMENT_LOOP_VARIABLE thing: `$i++` means 'add 1 to `$i`'. So the upshot of all this is simply that `$i` is a counter that ticks 0, 1, 2. Immediately upon hitting 3 the loop will terminate, as 3 is not \< 3). Hopefully the `for` loop should now be crystal clear. Hence:  

```perl
for ( $i = 0; $i < scalar @beans; $i++ ) {
    print "$name likes $beans[$i] beans.\n";
}
```

  
means:  

```perl
for
(
    set $i to 0;
    keep looping while $i is less than 3;
    increment $i by 1 on each pass of the loop
)
{
    print out Steve likes the $i'th member of @beans
}
```

  

## Operators

  
The increment operator, `++` , can be used in two ways: you can either write:  

```perl
$i++
```

  
or  

```perl
++$i
```

  
In this particular case, it doesn't matter which you use, but in fact `$i++` increments `$i` *after* returning it (post-increment), whereas `++$i` increments it *before* returning it (pre-increment). So:  

```perl
$i = 1;
print "At the start, \$i is $i.\n";

print "\$i still returns ",
    $i++, 
    " when you post-increment it, but its value is now $i\n";
$i = 1;
print 
   "But if you pre-increment it, \$i's value will be incremented by one to ",
   ++$i,
   "before its value is actually printed.\n";
```

  

```text
At the start, $i is 1.
$i still returns 1 when you post-increment it, but its value is now 2.
But if you pre-increment it, $i's value will be incremented by one to 2 before its value is actually printed.
```

  
Note the escaped (backslashed) `$` on some of the `$i`'s. You already know you need to escape a `@` in a double-quoted string to print a literal @ character. The exact same thing applies to `$`.

There's no reason why you shouldn't write  

```perl
$i++;
```

  
as  

```perl
$i = $i + 1;
```

  
but the former is much more concise. It is probably painfully obvious what  `--$i` and `$i--` do by extrapolation, but there is more than one way to decrement a variable too (an unofficial Perl motto is TIMTOWTDI: there is more than one way to do it, although very often, one of the possible ways is markedly less disgusting):  

```perl
--$i;
```

  
is shorthand for:  

```perl
$i -= 1;
```

  
which itself is shorthand for:  

```perl
$i = $i - 1;
```

  
The middle version is something which you may find useful. The `-=` *subtraction assignment operator* is one of a whole class of similar operators, like `+=` (so `$i++` is short for `$i += 1` which is itself short for `$i = $i + 1`).

Perl has all the usual mathematical operators, like `+`, `-`, `*`, `/`, `%` (modulus), and `**` (raise-to-the-power-of), and any of these may be used like `-=` or `+=` too, so:  

```perl
$a = $a ** 2;
# square $a and bung the result back into $a
```

  
is the same as:  

```perl
$a **= 2;
```

  
One operator lacking in most other languages is the `x` operator (that's just a little "x" character), which will 'multiply' strings:  

```perl
$string = "hello";
$three_copies_of_string = $string x 3;
print $three_copies_of_string;
```

  

```text
hellohellohello
```

  
You can of course also use the `x` in a `x=` construction too:  

```perl
$string = "hello";
$string x= 3; # put "hellohellohello" into $string
```

  
One final useful operator is `.` which *concatenates* two strings together:  

```perl
my $world = ", world\n";
my $cat   = "This is the concatenation operator in action";
my $msg   = "hello" . $world . $cat . "\n";
print $msg;
```

  

```text
hello, world
This is the concatenation operator in action
```

  
Next up...[prettier loops and nicer code](/2012/10/perl-pretty-loops-nicer-code/ "Prettier loops and nicer code").
