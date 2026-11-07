---
title: Conditionals
date: '2012-10-03T15:33:33Z'
lastmod: '2013-04-12T10:02:26Z'
url: /2012/10/perl-conditionals/
slug: perl-conditionals
draft: false
wp_id: 363
aliases:
- /2012/10/perlconditionals/
categories:
- Perl
---

## Conditionals: `if` and `unless`

We're on the home-straight in [understanding the code from the last post](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines") now:

```perl
#!/usr/bin/perl

use strict;
use warnings;

my @peas = qw/chick mushy split/;
while ( my $type = pop @peas ) {
    print "$type peas are ", flavour( $type ), ".\n";
}

sub flavour {
    my $query = shift @_;
    my @peas = qw/chick garbanzo/;
    foreach ( @peas ) {
        if ( $query eq $_ ) {
            return "delicious";
        }
    }
    return "disgusting";
}
```

The very last bit is the *conditional* statement in the `flavour()` subroutine. This part compares the type of pea the subroutine was passed with all the peas in its own `@peas`, and if it matches any of them, the subroutine returns 'delicious'. The `if` conditional has the general form:

```perl
if     ( THIS_IS_TRUE ) { DO_SOMETHING; }
```

which is analogous to:

```perl
while  ( THIS_IS_TRUE ) { DO_SOMETHING; }
```

The equivalent of:

```perl
until  ( THIS_IS_TRUE ) { DO_SOMETHING; }
```

is:

```perl
unless ( THIS_IS_TRUE ) { DO_SOMETHING; }
```

## Comparison operators: `eq` and `==`

The actual comparison the `if` statement makes is:

```perl
$query eq $_
```

The `eq` tests to see if two strings are identical. Perl has two sets of comparisons: numerical and string. The 'equal to' test is `eq` for strings, and `==` for numbers (that's *two* = signs). Perl goof number one is getting `==` comparison and `=` assignment mixed up.

In addition to 'equal to' comparisons, Perl also has greater than, less than, greater than or equal to, less than or equal to, and not equal to comparisons. For numbers these are `>`, `<`, `<=`, `>=`, and `!=` respectively. The equivalents for strings are `gt`, `lt`, `ge`, `le`, and `ne`.

The reason Perl makes a distinction between numerical and string comparisons is because "2" and "2.0" are numerically equal, but not stringily equal : `"2" == "2.0"` is TRUE because 2 and 2.0 are the same numerically (mathematicians: shush). However, `"2" eq "2.0"` is FALSE, because they are clearly *not* the same string of characters. You want the maths symbols to compare things as numbers, and the language symbols to compare them as strings.

`if` statements can be optionally followed by any number of `elsif` statements, and an optional `else` statement, so:  

```perl
if    ( THIS_IS_TRUE ) {
    DO_THIS_THING;
}
elsif ( THIS_OTHER_THING_IS_TRUE ) {
    DO_THIS_OTHER_THING;
}
else {
    DO_THE_DEFAULT_THING;
}
```

  
Which is all very simple and obvious. You can also nest `if`'s inside other `if`'s to a gazillion degrees, which is a perfect way of making code unreadable, but will be necessary from time to time.  

## Switch statements: `given` and `when`

  
If you come from a C background, you may be wondering if Perl has a switch statement, which, if you don't, is basically a shorthand for a very long `if...elsif...elsif...elsif...else` statement. As of Perl 5.10.0, it does, but you need to explicitly enable it:  

```perl
use 5.14.1;
given ( $arg ) {
    when ( $_ eq 'quit' )  { exit;               }
    when ( $_ eq 'squit' ) { say "Norovirus";    }
    default                { system "perldoc Math::Complex" }
}
```

  
`given` sets `$_` to the argument you give it (`$arg`), and you can then test  `$_` against various values using  `when`. If one of the  `when` cases succeeds, control leaves the `given` switch structure. If none of the cases succeed, an optional  `default` block can be called.  The new keyword `exit` simply causes a Perl program to stop. `system` [we'll come across later](/2012/10/perl-files-and-directories/ "Files and directories"), but for the moment, just see what happens if you enter neither 'quit' nor 'squit' when you run this script.

Next up...[More hashes and sorting](/2012/10/perl-more-hashes-sorting/ "More hashes and sorting")
