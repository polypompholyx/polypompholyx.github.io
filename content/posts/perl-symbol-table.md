---
title: Symbol table
date: '2012-10-03T19:47:55Z'
lastmod: '2013-04-12T10:08:58Z'
url: /2012/10/perl-symbol-table/
slug: perl-symbol-table
draft: false
wp_id: 393
aliases:
- /2012/10/perlsymbol-table/
categories:
- Perl
---

## Symbols

That's pretty much [everything for hashes](/2012/10/perl-more-hashes-sorting/ "More hashes and sorting"), except for one topic usually missed out from introductory tutorials (possibly rightly!) This post will tell you a little about the innards of what you've been doing when you create variables. It's not really necessary to know this stuff to be able to use Perl for day-to-day stuff, so do feel free to skip to the [next post](/2012/10/perl-files-and-directories/ "Files and directories") if this one becomes too esoteric.

`perl` maintains its own *internal* hash, called the *symbol table*, or `%main::` (that's 'hash main double colon'), which you also have access to:  

```perl
#!/usr/bin/perl
# use strict; # turn off strictures, for reasons we'll come to in a minute
use warnings;

$pibble = 2;
@foo    = ( 1, 4 );
%bits   = ( me => 'tired' );
sub my_sort { return ( $a cmp $b ) }

foreach ( sort keys %main:: ) {
    print "This perl program has a symbol called $_.\n";
}
```

  

```text
This perl program has a symbol called STDIN.
This perl program has a symbol called pibble.
...
```

  
This program will print stuff about the 'symbols' `perl` has defined for you, and the symbols you have created. Somewhere you will find `pibble`, `foo`, `bits` and `my_sort`. You'll also find a lot of other things, including `STDIN`, the name of the standard input filehandle, and `a` and `b` (as in `$a` and `$b`).  

## Typeglobs

  
The symbol table is just a hash, with the rather atypical name `%main::`, and that program simply printed out the keys of that hash. If you want to see the `values`, you'll have to be acquainted with Perl's final, and most esoteric data type, the *typeglob*, and another type of scoping besides `my`. Arrays have `@`, scalars have `$`, and *typeglobs* have `*`. The typeglob `*foo`, *contains* the definitions of `$foo`, `@foo`, `%foo`, and the subroutine `sub foo` (which is called *`&foo`* : subs get `&` as their sigil) all rolled into one. Try this program out:  

```perl
#!/usr/bin/perl
# use strict;
# use warnings; # turn warnings off too

# define some things
$pibble = 2;
@foo    = ( 1, 4 );
$foo    = 'bar';
%foo    = ( key => 'value' );
%bits   = ( me => 'tired' );
sub my_sort { return ( $a cmp $b ) }

print "This program contains...\n";

while ( my ( $key, $value ) = each %main:: ) {
    # iterate over the key/value pairs of the symbol table hash

    local *symbol = $value;
    # this assigns the value from the symbol table to a typeglob

    # the following lines look to see if the typeglob contains 
    # a $, %, @ or & definition

    if ( defined $symbol ) {
        print "a scalar called \$$key\n";
            # remember \$ is just an escaped $ ...
            # followed by the contents of variable $key
    }
    if ( defined @symbol ) {
        print "an array called \@$key\n";
    }
    if ( defined %symbol ) {
        print "a hash called \%$key\n";
    }
    if ( defined &symbol ) {
        print "a subroutine called $key\n";
    }
}
```

  

```text
a hash called %ENV
a scalar called $pibble
a scalar called $_
a hash called %UNIVERSAL::
a scalar called $foo
an array called @foo
a hash called %foo
a scalar called $$
...
```

  
The `values` from the symbol table hash are typeglobs, looking something like `*main::foo`, `*main::ENV`, `*main::_` *, etc*. If you create your own `local` typeglob, `*symbol`, to contain one of these values from the symbol table, you can look to see if the various sub-types (scalar, array, *etc*.) are defined using `$symbol`, `@``symbol`, `%symbol` and `&symbol`. So, as the loop runs through the `$key`, `$value` pairs from the symbol table, `$value` will at some point contain `*main::foo`. So:  

```perl
local *symbol = $value;
```

  
creates a typeglob `*symbol` containing the definitions of symbols called `main::foo`, and  

```perl
if ( defined %symbol )
```

  
will ask 'is there a hash in the symbol table called `%main::foo`?'.

The `main::` bit means that we're looking at symbols from the 'main' symbol table. A program can use more than one symbol table: we'll get onto this when we talk about packages and modules later: the *main* `package` and symbol table is simply the one that `perl` assumes your program is using if you don't set it explicitly.  

## `local` variables

  
There is one final complication. Try sticking a `my` on any of the variables you've defined, like `$foo`, and run the program. You'll find they suddenly disappear from the symbol table. What on earth is happening? Well, the dirty secret is that `perl` actually has *two* completely independent sets of variables: one set introduced with Perl 5, and a legacy set that harks back to the days of Perl 4. Those that you create *without* a `my`, are Perl's old-style *global* or *`package`* variables, which live in the symbol table, and are extractable with typeglobs. This always includes all subroutine definitions anywhere, as you can't use `my` on these. These variables are global, and any program using your code can access them. Even if they're defined somewhere other than `main`, *e.g.* in a different `package` like [`File::Find`](/2012/10/perl-install-modules/ "Installing modules"), all you need to mess with them is to know the `package` to which they belong (here `File::Find`), the name of the variable (`$dir`) and you can modify them:  

```perl
$File::Find::dir = "plopsy";
```

  
to probably fatal effect. The reason these package variables were supplemented with `my` variables in Perl 5 was because there was no way to make package variables truly private to a subroutine. There was no `my` in Perl 4, and you had to use a thing called `local`, which you've seen above with a typeglob, to create temporary *dynamically* scoped (as opposed to *lexically* scoped `my`) variables:  

```perl
#!/usr/bin/perl
use strict;
use warnings;

$variable = "hello";
print "\$variable is $variable in the body.\n";
temporary();
print "\$variable is still $variable in the body.\n";

sub temporary {
    local $variable = "goodbye";
    print "\$variable is $variable in the temporary sub.\n";
}
```

  

```text
$variable is hello in the body.
$variable is goodbye in the temporary sub.
$variable is still hello in the body.
```

  
This looks to have exactly the same effect as `my` would, but in fact we're still talking about the **same** `$variable`, it just so happens that `perl` stashes away the original value when it hits the `local`, and replaces it when it returns to the body of the program. The symbol table entry is temporarily changed to its new value. In contrast, `my` creates a completely separate, fresh and unsullied variable with no relationship whatsoever to variables of the same name elsewhere in the program. To see the difference, if you called another subroutine from within `temporary()`, `$variable` would still be set to its temporary value of 'goodbye':  

```perl
#!/usr/bin/perl
use strict;
use warnings;

$variable = "hello";
print "\$variable is $variable in the body.\n";
temporary();
print "\$variable is still $variable in the body.\n";

sub temporary {
    local $variable = "goodbye";
    print "\$variable is $variable in the temporary sub.\n";
    inner();
}

sub inner {
    print "\$variable is $variable in the inner sub.\n";
}
```

  

```text
$variable is hello in the body.
$variable is goodbye in the temporary sub.
$variable is goodbye in the inner sub.
$variable is still hello in the body
```

  
In contrast, '*lexically* scoped', `my` variables live in only a particular part (scope) of the program, and are completely inaccessible outside of it. Each new `my` `$variable` is a completely different `$variable`. They do **not** appear in any symbol table. If you were to put `my` instead of `local`:  

```perl
#!/usr/bin/perl
use strict;
use warnings;

$variable = "hello";
print "\$variable is $variable in the body.\n";
temporary();
print "\$variable is still $variable in the body.\n";

sub temporary {
    my $variable = "goodbye";
    print "\$variable is $variable in the temporary sub.\n";
    inner();
}

sub inner {
    print "\$variable is $variable in the inner sub.\n";
}
```

  

```text
$variable is hello in the body.
$variable is goodbye in the temporary sub.
$variable is hello in the inner sub.
$variable is still hello in the body.
```

  
You'll see that the `$variable` in `temporary()` is now a completely **different** variable, isolated from the rest of the program, unrelated to the `$variable` in the body of the program, and certainly not accessible from `inner()` any more. `inner()` prints out the only `$variable` visible in its scope, which is the one in the body of the program.

You may well never have to use typeglobs, or the symbol table, or `local` in anger, but it's nice to know how stuff works, rather than merely how to use stuff, hence this digression. Normal service will now be resumed.

Next up...[files and directories](/2012/10/perl-files-and-directories/ "Files and directories").
