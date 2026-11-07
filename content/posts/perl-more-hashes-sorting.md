---
title: More hashes and sorting
date: '2012-10-03T19:21:03Z'
lastmod: '2013-04-22T16:10:16Z'
url: /2012/10/perl-more-hashes-sorting/
slug: perl-more-hashes-sorting
draft: false
wp_id: 384
categories:
- Perl
---

## Hash manipulation: `each`, `delete`, `exists`

Before we got side-tracked with [subroutines](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines") and [conditionals](/2012/10/perl-conditionals/ "Conditionals"), [we covered arrays](/2012/10/arrays-and-slices/ "Arrays and slices") in some detail, and saw [the various functions](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines"), like `push` and `pop` that you can torture them with. The functions for torturing [hashes](/2012/10/perl-hashes/ "Hashes") are our next port of call. Perl stores the `key => value` pairs of a hash in essentially random order (well, unhelpful, if not actually random), so operations like `push`ing and `pop`ping don't make any sense, as hash items are not ordered in a useful fashion. We've already seen how to extract single items and slices of hash:

```perl
my %bits          = ( soy => 'sauce', sesame => 'oil', garlic => 'clove' );
my $one_item      = $bits{ 'soy' };
my @several_items = @bits{ 'sesame', 'garlic' };
```

However, to create a new member of the hash, you can't use `push`, as it doesn't make any sense, so you need to write:

```perl
$hash{ 'new_key' } = 'new_value';
```

You don't actually need the quotes around the key when you access or create hashes or their elements:

```perl
$hash{ newkey } = 'new_value';
```

but I prefer to use them as I am anal. If you want to find out if a particular hash entry exists, you can use the `exists` function:

```perl
print "yep, it's there\n" if exists $bits{ 'soy' };
if ( exists $bits{ 'soy' } ) {
    print "yep it's there\n";
}
```

Both of these do the same thing, the first just shows you that you can append a conditional `if` statement modifier in just the same way you can append [`foreach`](lesson02.html#foreach). The same applies to `for`, `while`, `unless`, and `until`.

If you want to remove a hash key, use `delete`:  

```perl
delete $bits{ 'soy' };
```

  
will remove the pair `( soy => 'sauce' )` from the hash. These functions are all very useful, but the most common thing you'll want to do with is iterate over the pairs in the hash, in much the same way `foreach ( @array )` iterates over the members of an array. There are no less than three variations on this theme.

The first is `each`, which will return a pair from a hash. You'll most often see this in constructs using `while`, like:  

```perl
my %bits = ( soy => 'sauce', sesame => 'oil', garlic => 'clove' );
while ( my ( $key, $value ) = each %bits ) {
    print "$key has value $value\n";
}
```

  

```text
sesame has value oil
garlic has value clove
soy has value sauce
```

  
This iterates over the items in the hash, assigning the key value pairs to `$key` and `$value` in turn. Note the parentheses around `$key` and `$value`. You need these because `each` returns a two-item-long list. Slinging about lists is one of Perl's strengths:  

```perl
my @things = ( 1, 2, 'three' );
    # assign a list to an array

my ( $one, $two, $three ) = ( 1, 2, 'three' );
    # assign a list of values to a list of variables

($x, $y) = ($y, $x);
    # swap two scalars
```

  
Note the brackets around the `($one, $two, $three)`. You need these to make `perl` realise it's a list, just as when you create arrays. If you miss them off, `perl` will try to evaluate `$one`, `$two` and `$three` *separately* (*i.e.* in scalar context), and therefore come up with the last thing it evaluated, which is `$three`. It will then do exactly the same to the other side, come up with `'three'`, then go " `$three = 'three'` ", and *nothing else*. `$one` and `$two` will never be assigned anything. You *need* brackets to force list context, in the same way as you sometimes need `scalar` to force scalar context. One important thing to note is that if you put an `@array` in something like this, it will be *greedy*:  

```perl
my ( @greedy, $starved ) =
    ( 'some', 'other', qw/things using the qw operator/ );
print "\@greedy : @greedy\n\$starved : $starved\n";
```

  

```text
@greedy : some other things using the qw operator
$starved :
```

  
`$starved` will never get anything: arrays will slurp up everything from a list. There are various ways around this: here's just one (if you know how many items you want to put in the array):  

```perl
my( @greedy, $satiated );
( @greedy[ 0 .. 5 ], $satiated ) =
    ( 'some', 'other', qw/things using the qw operator/ );
print "\@greedy : @greedy\n\$satiated : $satiated\n";
```

  

```text
@greedy : some other things using the qw
$satiated : operator
```

  
The use of a slice assignment:  

```perl
@greedy[ 0 .. 5 ]
```

  
should be fairy self-explanatory: it is a slice of the array, using the `..` range operator, so this is just shorthand for:  

```perl
@greedy[ 0, 1, 2, 3, 4, 5 ]
```

  
and will work just fine: the array will only get stuff up to and including the word '`quotewords`', and `$satiated` will get '`operator`'. Bear this in mind when you mess with `@_` in subroutines:  

```perl
( @gets_everything, $gets_nothing ) = @_;
```

  
Getting round this array flattening and greediness will be covered when we get around to discussing references. Anyway, getting back to hashes:  

```perl
while ( my ( $key, $value ) = each %bits ) {
    print "$key has value $value\n";
}
```

  
`each` generates a two item long list, which is captured into `$key` and `$value`, and this is repeated over the entire hash using a `while` loop. Note I've bunged in a `my` too, as I'll always be using `strict` from now on, in the interests of getting you into good habits.  

## Hash `keys` and `values`

  
The other two ways of torturing a hash are to pull out just its `keys` or its `values`:  

```perl
my %trees = (
    acorn      => "Quercus",
    oak        => "Quercus",
    beech      => "Fagus",
    yew        => "Taxus",
    maidenhair => "Ginkgo",
);

foreach ( keys %trees ) {
    print "\%trees contains the Latin name for $_.\n";
}
foreach ( values %trees ) {
    print "\%trees knows some English names for $_.\n";
}
```

  

```text
%trees contains the Latin name for maidenhair.
%trees contains the Latin name for beech.
%trees contains the Latin name for yew.
%trees contains the Latin name for acorn.
%trees contains the Latin name for oak.
%trees knows some English names for Ginkgo.
%trees knows some English names for Fagus.
%trees knows some English names for Taxus.
%trees knows some English names for Quercus.
%trees knows some English names for Quercus.
```

  
I've escaped the `%` in the double quoted strings: you don't need to do this, as unlike arrays and scalars, hashes don't interpolate their contents in a double quoted string. However, it doesn't hurt, and may be easier for you to remember. Note that hashes can have several *values* that are the same (*Quercus* twice): only *keys* have to be unique. If both your keys and your values are unique, you can make a bilingual dictionary with `reverse`...  

```perl
my %Eng_to_Esp = (
    one   => 'unu',
    two   => 'du',
    three => 'tri',
    four  => 'kvar',
    five  => 'kvin'
);

my %Esp_to_Eng = reverse %Eng_to_Esp;
print "The Esperanto for two is $Eng_to_Esp{'two'}.\n";
print "And the English for kvar is $Esp_to_Eng{'kvar'}.\n";
```

  

```text
The Esperanto for two is du.
And the English for kvar is four.
```

  
You can also see that although a hash itself won't interpolate in a double quoted string, its members (and items from a normal array) will.  

## Sorting: `sort` and `<=>`

  
Something you'll often want to do is `sort` a list, especially with hashes: as the `keys`, `values` and `each` pairs are in an unhelpful order, you'll often want to torture them into something more ordered. Perl has a function called `sort` for just these occasions:  

```perl
my %trees = (
    oak        => "Quercus",
    beech      => "Fagus",
    yew        =>"Taxus",
    maidenhair => "Ginkgo",
);

print "$_.\n" foreach ( sort keys %trees );
```

  

```text
beech.
maidenhair.
oak.
yew.
```

  
By default, `sort` sorts things 'ASCIIbetically':  

```perl
#!/usr/bin/perl
use strict;
use warnings;

my %trees = (
    Oak        => "Quercus", # capital O
    beech      => "Fagus",
    yew        =>"Taxus",
    maidenhair => "Ginkgo",
);

print "$_.\n" foreach ( sort keys %trees );
```

  

```text
Oak.
beech.
maidenhair.
yew.
```

  
It sorts strings by the ASCII values of their characters, hence O comes before b, because the ASCIIbet goes something like 0, 1, 2 .. 9, (some other things), A, B, C .. Z, (few bits), a, b, c .. z. As here:  

```perl
print "The ASCII value of O is ", ord "O", "\n";
print "The ASCII value of b is ", ord "b", "\n";
```

  

```text
The ASCII value of O is 79
The ASCII value of b is 98
```

  
This also demonstrates the use of `ord`, which tells you the ASCII value of a letter. `chr` does the opposite, converting ASCII numbers to characters.  

```perl
print chr( $_ ) foreach ( 74, 117, 115, 116, 32,
97, 110, 111, 116, 104, 101, 114, 32, 112, 101,
114, 108, 32, 104, 97, 99, 107, 101, 114, 46);
```

  

```text
Just another perl hacker.
```

  
Anyway, the point is, if you want your data sorted numerically, or properly alphabetically, rather than ASCIIbetically, you'll need to twiddle with `sort`. `sort` can take an optional extra argument that tells it how to sort:  

```perl
my @numbers            = ( 1, 2, 3, 4, 100, 101, 102, 6); # 6 is out of order
my @default_sorted     = sort @numbers;
my @numerically_sorted = sort { $a <=> $b } @numbers;

print " DEFAULT: @default_sorted\n NUMERICALLY: @numerically_sorted\n";
```

  

```text
DEFAULT: 1 100 101 102 2 3 4 6
NUMERICALLY: 1 2 3 4 6 100 101 102
```

  
Note the default output: 100 comes before 2, because the first character of 100, '1', comes before the first character of 2, '2'. So how does the numerical sort work? The extra bit `sort` needs is a *block* squashed between the keyword `sort` and the things to sort, surrounded by braces `{ }`:  

```perl
sort { $a <=> $b } @numbers;
```

  
The *spaceship operator*, `<=>` compares two numbers and returns certain values depending on which is larger. The values it compares are `$a` and `$b`, which are `sort`'s default variables, and stand for *pairs of things taken from `@numbers`*. `perl` does the actual *sorting* itself: all *you* need to tell `perl` is, given a pair of numbers (`$a` and `$b`), which one is bigger *i.e.* should come later in the sorted list?  

- If `$a` is bigger, you need to tell `perl` '1'.
- If `$b` is bigger, you need to tell `perl` '-1'.
- If they are both equal, you should tell `perl` '0'.

  
The spaceship operator is a built-in comparison thingummy that does just this for numbers. For strings, the equivalent is `cmp` ([remember `==` *vs.* `eq`](/2012/10/perl-conditionals/ "Conditionals")), which compares strings character by character according to their ASCII values. Hence:  

```perl
sort { $a cmp $b } @strings;
```

  
is the same as just plain old:  

```perl
sort @strings;
```

  
To sort things properly alphabetically, you might try:  

```perl
my @trees = qw/oak ash Ginkgo Quercus linden Fraxinus lychee/;
print "$_\n" foreach ( sort { lc( $a ) cmp lc( $b ) } @trees );
```

  

```text
ash
Fraxinus
Ginkgo
linden
lychee
oak
Quercus
```

  
`lc` stands for 'lower case': it returns strings it is given in lowercase, here so they can be compared without worrying that A-Z comes before a-z in the ASCIIbet. You'll never guess what `uc` does.

You can define much more complicated and arbitrary sorting schemes than these, using the '1', '-1', '0' technique. In many of these cases, it's more convenient to define a subroutine to do the comparisons, such as `in_my_arbitrary_way`, then call it using:  

```perl
@weird_sorted = sort in_my_arbitrary_way @things;
```

  
Say you'd prefer it if the first word in the dictionary was 'xenon', but then afterwards, carried on as normally:  

```perl
my @strings      = qw( zebedee blob aardvark xenon shark cat dog );
my @funny_sorted = sort funny_sort @strings;
print "@funny_sorted\n";

sub funny_sort {
    if    ( $a eq 'xenon' ) {
        return -1; 
            # if $a is xenon, $a should come earlier, so -1
    }
    elsif ( $b eq 'xenon' ) {
        return 1; 
            # if $b is xenon, $a must come later, so 1
    }
    else {
        return ( lc( $a ) cmp lc ( $b ) ); 
            # otherwise sort alphabetically
    }
}
```

  

```text
xenon aardvark blob cat dog shark zebedee
```

  
This will run under `use strict;` even though we've not 'scoped' the `$a` and `$b` in the subroutine using `my`. This is because `$a` and `$b`, as well as all the funny punctuation variables like `$_`, are special-cased and you don't need to scope them.

That's `sort` pretty much sorted: you can use it in any of these ways:  

```perl
@sorted = sort @unsorted;
    # use the default ASCIIbetical sort

@sorted = sort { DO_SOMETHING_WITH_$a_AND_$b } @unsorted;
    # use your own sort

@sorted = sort my_sorting_subroutine @unsorted;
    # define your own sort sub elsewhere
```

  

## Orcish manoeuvre and Schwartzian transform

  
A common problem when performing sorts is that the internal implementation of `sort` has to access the data on which the sort is performed several times for each item in the unsorted list. If accessing this data is time consuming (if you have to use a system call for example), the `sort` can take rather a long time. The canonical example is trying to sort a list of filenames by their age:  

```perl
my @filenames = glob "data/bacteria/sequences/*.seq";
# glob calls a C-shell style globbing function
sub brute_force { -M $a <=> -M $b }
@sorted = sort brute_force @filenames;
```

  
There are several ways to get around this expensive look-up: the Orcish manoeuvre and the Schwartzian transform are two. Both cache the key you are sorting on so that you only need to look it up once. The Orcish manoeuvre is the simpler of the two:  

```perl
my @filenames = glob "data/bacteria/sequences/*.seq";
{
    my %cached; # lexically scoped in a bare block to keep things tidy
    sub orcish {
        ( $cached{$a} ||= -M $a )
                  <=>
        ( $cached{$b} ||= -M $b )
    }
}
@sorted = sort orcish @filenames;
```

  
In the Orcish manoeuvre, we check to see if we have already looked up the value of `-M $a` or `-M $b` by requesting the value of `$cached{$a}` or `$cached{$b}`. If we haven't previously cached them, we store the age in the cache, so that next time we don't have to do the expensive system call to get the age. If we have previously cached them, we just get the value from the cache anyway. The name is derived from the `||=`, which could be read "Or-Cache" if you like.

You can compare the Orcish and brute force techniques using the `Benchmark` module:  

```perl
use Benchmark;
my @filenames = glob "data/bacteria/sequences/*.seq";
sub brute_force { -M $a <=> -M $b }
{
    my %cached;
    sub orcish   {
        ( $cached{$a} ||= -M $a )
               <=>
        ( $cached{$b} ||= -M $b )
    }
}
timethese(
    10000, # 10 000 iterations of each
    {
        "Brute force" => 
            sub { my @sorted = sort brute_force @filenames },
        "Orcish" => 
            sub { my @sorted = sort orcish @filenames },
    }
);
```

  

```text
Benchmark: timing 10000 iterations of Brute force, Orcish...
Brute force: 133 wallclock secs 
  (30.02 usr + 102.50 sys = 132.52 CPU) @ 75.46/s (n=10000)
Orcish: 1 wallclock secs 
  ( 1.43 usr + 0.00 sys = 1.43 CPU) @ 6983.24/s (n=10000)
```

  
`Benchmark`'s function `timethese()` takes a number of iterations (10 000 here) and a hashref of `name => coderef` pairs as arguments, and times how long the coderefs take to run. The Orcish manoeuvre is much faster.

The Schwartzian transform (named after Randal L. Schwartz) is even faster, but rather more complex at first glance:  

```perl
my @filenames = glob "data/bacteria/sequences/*.seq";
my @sorted =
map {
    $_->[0]
    # 4. Construct the list of names by extracting 
    # them from the sorted arrayrefs
}
(
    sort {
        $a->[1] <=> $b->[1]
        # 3. Sort this list of arrayrefs based on their file ages
    }
    (
        map {
            [$_, -M]
            # 2. Convert them into list of [ filename, age ] arrayrefs
        }
        (
            @filenames
            # 1. Take a list of filenames
        )
    )
);
print "$_\n" for @sorted;
```

  
Read it "upwards": first we take `@filenames`, and create a list of `[ filename, age ]` arrayrefs using `map`. Then we `sort` based on the age ( `$a->[1] <=> $b->[0]` ), to create an ordered list of these `[ filename, age ]` arrayrefs. Finally, we grab the filenames `$_->[0]` and create a final list of sorted filenames using `map` again. This `map-sort-map` is elegant and fast as the array lookups are quicker than the hash lookups in the Orcish manoeuvre.  

## Hashes summary

  
Hashes are as simple to use as arrays too: you can use any of the following for hash torture:  

```perl
my %hash = (
    telephone   => "Bell",
    television  => "Baird, no Farnsworth, no Baird",
    lightbulb   => "Insert argument here",
    JesusChrist => "Paul of Tarsus",
);

print $hash{ 'lightbulb' };                 # access
print @hash{ 'lightbulb', 'television' };   # slice
$hash{ www } = "Berners Lee";               # append
print "Yes" if exists $hash{ 'telephone' }; # exist
delete $hash{ 'JesusChrist' };              # remove

while ( my( $k, $v ) = each %hash ) {
    print "$v invented $k\n";               # iterate
} 

print keys %hash;                           # keys
print sort values %hash;                    # values
```

  
Next up...[symbol table](/2012/10/perlsymbol-table/ "Symbol table").
