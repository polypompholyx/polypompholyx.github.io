---
title: Bondage, discipline and subroutines
date: '2012-10-03T14:46:29Z'
lastmod: '2013-04-12T09:59:49Z'
url: /2012/10/perl-bondage-discipline-subs/
slug: perl-bondage-discipline-subs
draft: false
wp_id: 360
categories:
- Perl
---

## Lexical `my` variables and `use strict;`

You may have noticed [a little thing I slipped in the last script](/2012/10/perl-pretty-loops-nicer-code/ "Prettier loops and nicer code"): the keyword `my` in the `chomp`. `my` is a very important keyword, although you'll note that it doesn't seem to make any difference if you delete it and run the program. What `my` does is pin a variable to a particular part of your program, so that it can't be seen from elsewhere. This may not seem very useful at the moment, but is exceedingly important as your programs get bigger. Such as here:

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

Many new things, we'll take it a bit at a time. Most Perl tutorials I've read leave `my` until the very end, but it's not really very difficult, and in the interests of getting you into good habits early, we'll take it on now. The first step to writing well behaved scripts is to bung this at the top:

```perl
use strict;
use warnings;
```

The first line turns on Perl's bondage and discipline mode. The second line enables ~~safe words~~ warnings. In `strict` mode, if you do not use `my` (or its big brother, `our`) on *every *variable and therefore safely pin them down to particular bits of your code, your program will barf.

It's a ridiculous question, but why should you want bondage and discipline? Why should you want to hogtie variables down to specific places in your code? Well, on little throwaway scripts, you might not, and it's fine not to bother. But on big things, with lots of user defined functions (subroutines), it's essential, as we shall see.

The next part of the code goes:  

```perl
my @peas = qw/chick mushy split/;
```

  
*i.e.* create an array called `@peas` containing the obvious items. Note the ugly and unwise choice of quoting characters. Then:  

```perl
while ( my $type = pop @peas ) {
    print "$type peas are ", flavour( $type ), ".\n";
}
```

  

## `while` loops

  
Three new things here, the `while` loop, the `pop` and the `flavour()`. We'll take these in turn.

`while` is another loop control, like [`for`](/2012/10/perl-simple-loops/ "Simple loops") and [`foreach`](/2012/10/perl-pretty-loops-nicer-code/ "Prettier loops and nicer code"). It has the general form:  

```perl
while ( THIS_IS_TRUE ) { DO_SOMETHING; }
```

  
So when is:  

```perl
my $type = pop @peas
```

  
"TRUE" then? Perl considers anything apart from `undef`ined variables, empty strings, and the number zero as TRUE. `pop` pulls the last member out of an array and returns it (shortening the array by one). Here the popped member is captured each time into the variable `$type`. Since `"chick"`, `"mushy"` and `"split"` are not the number zero, and are most clearly `defined` as something, `$type` is TRUE until you try to `pop` a non-existent, `undef`ined, fourth item out of the array, whereupon the loop exits. Which is all very obvious really:  

```perl
while ( there are still things to pop out of the array ) { DO_SOMETHING; }
```

  
So all this loop does is iterate over the array, just like `foreach`, but empties the array from the end in so doing. Perl has several other sorts of loop, in addition to `while`, `for` and `foreach` loops. This one should be fairly obvious too:  

```perl
until ( THIS_IS_TRUE ) { DO_SOMETHING; }
```

  

## Array functions: `pop`, `push`, `shift`, `unshift`, `splice`, `reverse`

  
Perl also has plenty of other array manipulators. `pop` will pull out the *last* member of an array. If you want to pull values out of the *front* end, you'll need `shift`, which returns the first member of an array, shortening the array by one from the front. If you want to add things to an array, you'll want to use `push` or `unshift`, which add things to the end or beginning of an array respectively. For example:  

```perl
@peas = ( "chick", "mushy", "split" );
print "\@peas contains ( @peas )\n";

$foo = pop @peas;
# $foo contains "split", @peas now contains ("chick", "mushy")
print "$foo was popped, ( @peas ) are left in \@peas\n";

$bar = shift @peas;
# $bar contains "chick", @peas now contains just ("mushy")
print "$bar was shifted, ( @peas ) is left in \@peas\n";

push @peas, "garbanzo";
# @peas now contains ("mushy", "garbanzo")
print "garbanzo was pushed, now \@peas contains ( @peas )\n";

unshift @peas, "marrowfat";
# @peas now contains ("marrowfat", "mushy", "garbanzo")
print "marrowfat was unshifted, now \@peas contains ( @peas )\n";

push @peas, $foo, $bar;
# @peans now contains ("marrowfat", "mushy", "garbanzo", "split", "chick")
print "( $foo $bar ) were pushed, now \@peas contains ( @peas )\n";
```

  

```text
@peas contains ( chick mushy split )
split was popped, ( chick mushy ) are left in @peas
chick was shifted, ( mushy ) is left in @peas
garbanzo was pushed, now @peas contains ( mushy garbanzo )
marrowfat was unshifted, now @peas contains ( marrowfat mushy garbanzo )
( split chick ) were pushed, now @peas contains ( marrowfat mushy garbanzo split chick )
```

  
`push` and `unshift` are list operators, and canadd an entire list of things to the array. Bearing in mind an array is just a list with delusions of grandeur:  

```perl
@peas  = ( "chick",  "mushy",   "split" );
@beans = ( "adzuki", "haricot", "mung"  );
push @peas, @beans, "and this too";
print "@peas\n";
```

  

```text
chick mushy split adzuki haricot mung and this too
```

  
will shove the entire contents of `@beans` onto the end of `@peas`, followed by the string `"and this too"`.

The least popular array operator is `splice`. Although `splice` can do everything `pop`, `push`, `shift` and `unshift` can do and more, it has a rather difficult syntax:  

```perl
splice @ARRAY, START_INDEX, THIS_MANY, LIST;
```

  
will remove THIS_MANY items starting from START_INDEX, and replace them with the contents of LIST. Incidentally, `splice` is one of the context sensitive operators: in list context, it will return all the spliced out items, but if you call it in scalar context, it returns just the last item removed from the array, rather than the whole list of them. So:  

```perl
@all_removed = splice ...;
#list context, because there's an @rray to capture what splice returns
$last_one_removed = splice ...;
#scalar context, because there's only a $calar to capture the output of splice
```

  
THIS_MANY and LIST are optional, defaulting to 1 and undefined (`undef`) respectively.  

```perl
pop @things;
```

  
and  

```perl
splice( @things, -1, 1, undef );
```

  
mean the same thing: both remove a single item (`1`): the last (`-1`) member of an array (`@things`), and replace it with nothing (which is called `undef` in Perl). `pop` is more intuitive though.

Another useful array operator is `reverse`:  

```perl
@backward_peas = reverse @peas;
```

  
`reverse` leaves `@peas` *itself* unchanged, but returns the array in reversed order, here to be captured in `@reversed`. If you want to `reverse` an array *in situ*, use:  

```perl
@array = reverse @array.
```

  
The distinction between an array and a list is similar to that between a scalar and a value: an array is something you can name, like `@bits`, whereas a list is just a comma-separated list of values in a script. Likewise, `$that` is a scalar, but `'this'` is just a value.

You can slice lists in the same way as you slice arrays:  

```perl
my @bits = ( 'this', 'is', 'a', 'list', 'not', 'an', 'array' )[ 0 .. 1, 5 .. 6 ];
print "@bits";
```

  
However, you cannot `pop` a list:  

```perl
my $word = pop ( 'this', 'is', 'a', 'list', 'not', 'an', 'array' );
print $word;
```

  

```text
Type of arg 1 to pop must be array (not list).
Execution aborted due to compilation errors.
```

  
The reason for this is that although it makes sense that you can slice, or even `reverse` a list:  

```perl
print reverse ( qw( t s i l ) );
```

  
you cannot remove the last item from a list, because a list is not a variable: to `pop` a value from the list would be equivalent to taking an eraser to the text of your script, and that is nonsensical.  

## Subroutines (functions)

  
Anyway, back to the point. The only other new thing in the code we were examining above:  

```perl
while ( my $type = pop @peas )
    { print "$type peas are ", flavour( $type ), ".\n"; }
```

  
is the function `flavour()`. Although Perl has some bizarrely named operators (like `chomp`, `pop`, `getgrent` and `dump`), `flavour` is not amongst them. `flavour()` is a user defined function, or *subroutine*. To create a subroutine you need to write something like:  

```perl
sub NAME { DO_SOMETHING; }
```

  
And to call it, you simply need to write  

```perl
NAME( ARGUMENT_LIST );
```

  
The `flavour` subroutine is called by the body of the program to determine how the three peas of interest taste. Subroutines frequently need to `return` things to the main part of the program: in this case, `flavour()` returns what the subroutine thinks about certain sorts of pea. So let's look at how `flavour()` does this:  

```perl
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

  

## The default subroutine array `@_`

  
The first new thing here is another of the infamous punctuation variables, **`@_`**. `@_` contains a list of all the arguments passed to the subroutine, in this case, whatever the value of `$type` was when the subroutine was called in the body of the program.

For the sake of argument, let's say this is `"chick"`. `@_` is just an array, so `shift` will pull the first member out as it would with any array. So `$query` will end up containing `"chick"`. Like `$_`, `@_` is assumed by certain operators: in a subroutine, `shift` will assume `@_` if you don't tell it otherwise:  

```perl
sub blah {   $arg   = shift @_;  }
sub blah {   $arg   = shift;     }
sub blah { ( $arg ) =        @_; }
```

  
are more-or-less equivalent, although note that the last onme doesn't actually modify `@_`. I almost always use the last one, since it's easier to add extra arguments later. In the last one, we have assigned `@_` to a \[one item long\] list (in parentheses):  

```perl
( $name, $date, $error, @other_things ) = @_;
( $arg )                                = @_;
```

  
which allows you to refer to the arguments with pretty names, rather than the perfectly valid, but rather painful:  

```perl
$_[0];
$_[1];
...
```

  
Note that you can't just say:  

```perl
$arg = @_;
```

  
if there's only one argument, since the `$arg` forces scalar context and arrays tell you how big they are, **not** what's in them in this context. The parentheses are required, unless (of course), you actually *want* to know *how many* arguments were passed, rather than *what* arguments were passed. Which is unlikely.  

## Lexical scope

  
The subroutine `flavour()` defines a list of peas (`"chick"` and `"garbanzo"`), called `@peas`. And **this** is where `my` comes in. `flavour`'s `@peas` has *exactly* the same name as the `@peas` in the main body of the program. How is `perl` supposed to know the difference? What **`my`** does is prevent the `@peas` in the subroutine from trashing the `@peas` in the main body of the program.

Try this out:  

```perl
@peas = qw/chick mushy/;
    # The body of the program contains an array called @peas
print "In the body of the program, \@peas contains @peas.\n";
trasher();
    # Call the subroutine, no need for arguments
print "Oh dear, it appears that \@peas in the body of the program has been trashed.\n";
print "Now it contains @peas.\n";
print "This is because \@peas in the subroutine overwrites the \@peas in main.\n";

sub trasher {
    @peas = qw/petit-pois yellow-gram/;
        # Because we haven't pinned  this @peas down with 'my',
        # it refers to the same @peas array as that in the body of the program
    print "In the subroutine trasher, \@peas contains @peas.\n";
}
```

  

```text
In the body of the program, @peas contains chick mushy.
In the subroutine trasher, @peas contains petit-pois yellow-gram.
Oh dear, it appears that @peas in the body of the program has been trashed.
Now it contains petit-pois yellow-gram.
```

  
Without the `my` to pin down the two separate `@peas` to their proper places, subroutines can overwrite variables in the body of the program. This is usually a Bad Thing: subroutines *can* change the value of variables in the body of the program, but that doesn't mean they *should* be allowed to!

In general, a good subroutine is a black box: you feed it values, and it feeds values back. That way, people can use your subroutines and functions without worrying what they might do to the variables in their program, or indeed, what their program might do to yours. Sometimes, you really *will* want a subroutine to change a 'global' variable, that is one in the body of a program, but more often than not, you don't, and `my` is the way to stop it, thus:  

```perl
@peas = qw/chick mushy/;
print "In the body of the program, \@peas contains @peas.\n";
well_behaved( );
print "Using my, we have avoided trashing \@peas in the body of the program\n";
print "\tIt still contains @peas.\n";

sub well_behaved {
    my @peas = qw/petit-pois yellow-gram/;
    print "In the subroutine well_behaved, \@peas contains its own values, @peas.\n";
}
```

  

```text
In the body of the program, @peas contains chick mushy.
In the subroutine well_behaved, @peas contains its own values, petit-pois yellow-gram.
Using my, we have avoided trashing @peas in the body of the program
    It still contains chick mushy.
```

  
So what exactly does `my` do? It stops a variable being visible outside the *block* in which it is *declared*. Blocks are things enclosed in `{ }` braces:  

```perl
BODY OF PROGRAM HERE
START OF OUTER BLOCK {
    OUTER BLOCK'S SCOPE EXTENDS FROM HERE
      start of inner block {
      inner block's scope
      } end of inner block
    TO HERE AND INCLUDES THE INNER BLOCK'S SCOPE TOO
} END OF OUTER BLOCK
```

  
The 'scope' is basically what is enclosed in a block. If you created a `my` variable in the inner block, only things in the scope of the inner block could see it. The outer block would **not** be able to see it (or trash it) at all. If you created a `my` variable in the outer block, only things in the outer block's scope could see it (*but* this *does* include the inner block!). The BODY OF PROGRAM couldn't see either. A subroutine is just a particular case of this:  

```perl
BODY OF PROGRAM HERE
START OF SUBROUTINE BLOCK {
    SUBROUTINE'S SCOPE EXTENDS FROM HERE
      start of inner block {
      inner block's scope
      } end of inner block
    TO HERE AND INCLUDES THE INNER BLOCK'S SCOPE TOO
} END OF SUBROUTINE BLOCK
```

  
So the `@peas` declared in the subroutine `well_behaved()` is only visible (and is the first variable of that name that *is* visible) within the braces that surround the subroutine:  

```perl
sub well_behaved {
    my @peas = qw/petit-pois yellow-gram/;
    print "In the subroutine thing, \@peas contains @peas.\n";
}
```

  
Outside this italic 'scope', `my @peas` is invisible, to both the body of the program, and to any other subroutines you might create. **A `my` variable is only visible from the place it is created to the end of the innermost enclosing block**.

There a few quasi-exceptions to this:  

```perl
foreach my $pea ( @peas ) { print $pea; }
```

  
DWIMs ("does what I/you mean"): the `$pea` is scoped to the inner block (and the rest of the program can't see it) even though it seems to be declared in the scope of the program, not of the `foreach` block. This is a Good Thing.

One thing to be careful of is if you want to use a loop to stuff things into a `my` variable:  

```perl
foreach ( @a ) { my @b; push @b, $_; } # WRONG
my @b; foreach ( @a ) { push @b, $_; } # RIGHT
```

  
The first one will create a new `@b` on each pass of the loop, and when the loop exits, `@b` goes out of scope and is destroyed! Waste of time. Use the second one. While we're on the subject of `foreach` loops, you should know that the loop variable stands for the *actual* variable from the list you're looping over, so mucking with it will muck with the original list:  

```perl
#!/usr/bin/perl
my @bits = qw/ b c m t /;
print "@bits\n";
foreach my $bit ( @bits ) { $bit .= "ap" };
print "@bits\n";
```

  

```text
b c m cr
bap cap map crap
```

  
To allow a program to run under `use strict;` we must declare every variable in the program (both the main body and the subroutines) with `my`. Variables declared with `my` in the main body of the program are still be visible to subroutines (since the scope of the body includes all its subroutines), and subroutines *can* still change them.

The penultimate bit of the program:  

```perl
    foreach ( @peas ) {
        if ( $query eq $_ ) {
            return "delicious";
        }
    }
```

  
simply determines whether the type of pea that `flavour()` gets passed matches anything in `flavour()`'s own `@peas`. If it does, it will return "delicious", using:  

```perl
return "delicious";
```

  
`return` sends back the list of things you give it (here the list is just one item long) to the main body of the program. So if we pass `flavour()` the value 'chick', which is in `flavour()`'s list of delicious peas, `flavour('chick')` will be 'delicious' and this is exactly what is printed out by the body of the program. However, if what we pass doesn't match any of `flavour()`'s preferences, the `foreach` loop will end naturally, and we come across:  

```perl
return "disgusting";
```

  
which it duly does.  

## Subroutines summary

  
We've rather glossed over the `if` *conditional* but that is the topic of the next post. To summarise subroutines:

create (declare) them with:  

```perl
sub blah { DO_SOMETHING; }
```

  
use (call) them with:  

```perl
blah( LIST_OF_ARGUMENTS );
blah( $calar, @nd_an_array_too, @nd_another_array );
blah(); # if blah doesn't need telling what to do
```

  
All the arguments - including any items from arrays passed as arguments - will be flattened into a single long list, which is passed to the subroutine, and available for manipulation within the subroutine inside the default array:  

```perl
@_
```

  
which you can get at using any array operator (or assigning it to a list).  

```perl
my $arg1 = shift @_;
my $arg2 = pop @_;
my $arg3 = shift;
my( $arg4, @args5 ) = @_;
```

  
Exit the subroutine with:  

```perl
return ( "something\n", 'and maybe another', $thing, @or_things );
return; # or just exit without returning anything at all
```

  
Subroutines will `return` without an explicit `return` with the value they last evaluated. I always use `return` as I like to be explicit. You can capture what is returned in the usual way: if `blah()` takes a list of arguments, and returns just one thing:  

```perl
$thing_returned_by_blah = blah( $argument, @other_arguments );
```

  
or if `blah` takes no arguments at all but returns a list:  

```perl
@lot_of_things = blah();
```

  
*etc., etc.*

Finally, be warned that:  

```perl
use strict;
if ( $you_do_not_use eq "my variables" ) {
    my @variables;
    my $pinned_down;
    print "you'll trash variables of the same name in the program body.\n";
    print "and strict will kill you";
}
```

  
Next up...[conditionals](/2012/10/perl-conditionals/ "Conditionals").
