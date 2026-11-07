---
title: Prettier loops and nicer code
date: '2012-10-03T14:12:43Z'
lastmod: '2013-04-12T09:53:30Z'
url: /2012/10/perl-pretty-loops-nicer-code/
slug: perl-pretty-loops-nicer-code
draft: false
wp_id: 352
categories:
- Perl
---

## Idiomatic Perl

[The original code we were studying is very ugly](/2012/10/perl-simple-loops/ "Simple loops"), and Perl makes writing short, diabetogenic code easy. It also makes writing shoddy, abominable code easy too, but I wouldn't recommend this as a course of action. A much more attractive way of writing the [horrible code from the last page](/2012/10/perl-simple-loops/ "Simple loops") is:

```perl
#!/usr/bin/perl
print "What is your name?";
chomp( $name = <STDIN> );
@beans = qw( adzuki haricot mung );
print "\@beans contains ", scalar @beans, " members, @beans\n";
foreach ( @beans ) {
    print "$name likes $_ beans.\n";
}
```

This is much tidier, and probably more readable even without any further explanation. There are a few new things though. The assignment of `<STDIN>` ("`Steve\n`" or whatever) to `$name` actually *returns* the variable `$name`, which is exactly what `chomp` needs to work on. So those two lines can be combined:

```perl
$name = <STDIN>;
chomp $name;
```

is exactly the same as:

```perl
chomp( $name = <STDIN> );
```

This is a typical bit of idiomatic Perl.

## Quote operators

The `qw( )` is a simpler way of making a list of variables. It stands for "quote words". To save you the effort of all those:

```perl
('X', 'Y', 'Z');
```

quotes and commas, you can just write:

```perl
qw(X Y Z);
```

which is much easier on the eye, although - of course - it's unsuitable if any of `X`, `Y` or `Z` contain spaces. You can mix and match quoting systems, so:

```perl
@bits = ( "hello, sailor", "1", "mung", "adzuki", "haricot", 
    "dal\n", "\t", $thing );
```

could also be written:

```perl
@bits = ( 'hello, sailor', 1, qw( mung adzuki haricot ), 
    "dal\n", "\t", $thing );
```

`1` is a number, not a string, so it doesn't need quotes, and I've only used double quotes for things that really need them (strings with escapes like `\t` in them). Written like this, it's not really any more readable, but it gives you the idea. Incidentally, it doesn't matter which (non-alphanumeric) character you use around a `qw` list:

```perl
qw(X Y Z);
qw{X Y Z};
qw/X Y Z/;
qw[X Y Z];
qw^X Y Z^;
```

are all equivalent. As long as you use the same character, or pairs of naturally paired characters like `( )`, `[ ]` and `{ }` then this'll work. I'd prsonally avoid anything but parentheses and braces though, unless you're deliberately trying to make your code unreadable.

Perl also has the quote operators `qq( )` and `q( )`, which are equivalent to `" "` and ' `' '` respectively, but you get to chose your own quote characters, which can be useful if your string contains lots of some character you'd rather not have to keep escaping:  

```perl
q(Exploding 'chocolate' cake and an awful 'lot' of 'quotes');
```

  
and:  

```perl
'Exploding \'chocolate\' cake and an awful \'lot\' of '\quotes\'';
```

  
are equivalent, but the first doesn't make your eyes bleed. Just because you *can* do something doesn't mean you *should*: anyone using `qq' '` and `q" "` is clearly ill. If you need to include the quote character itself in a string, whether you use conventional double quotes, or the `qq( )` or `q( )` operators, you'll have to escape it, just as you did with single quotes in single-quoted strings:  

```perl
"This is "wrong" ";
# because of the embedded, unescaped " characters
"This is \"OK\" ";
# properly escaped
qq!This is overexcited! and wrong! not to mention unreadbly awful!;
# because the second and third !s are unescaped
qq!This is OK\! though!;
# properly escaped !
```

  
Please don't even think of using exclamation marks as delimiters: it's cute until the maintainer of your code has you killed.  

```perl
qq{This uses a choice of "delimiter" that's (very) well chosen};
```

  
The next bit of the shortened code:  

```perl
print "\@beans contains ", scalar @beans, " members, @beans\n";
```

  
is virtually the same as before, but you'll note that list operators like `print` don't really need the `( )` parentheses, although feel free to leave them in if it prevents ambiguity. Some languages distinguish between functions (which need parentheses) and operators, which don't. In Perl they're by-and-large the same thing, and parentheses are only *required* for creating lists, or for mathematical (precedence) reasons: `2+(8*3)` is different from `(2+8)*3`.  

## `foreach` loops and the default variable `$_`

  
The C-style `for` loop is mercifully replaced with something much, much tidier:  

```perl
foreach ( @beans ) {
    print "$name likes $_ beans.\n";
}
```

  
Which is hugely more intuitive than the `for(;;){}` loop, and it runs more quickly too. The only difficult thing here is the infamous **`$_`** variable.

**`$_` is the 'default' variable**. It is automagically set, and automagically assumed by many functions. A more explicit way of writing this loop is:  

```perl
foreach $bean ( @beans ) { print "$name likes $bean beans.\n" }
```

  
The  

```perl
foreach $bean ( @beans )
```

  
means "set `$bean` to the value of each member of `@beans` in turn". If you don't supply a loop variable (here, `$bean`), it will be conveniently assumed you wanted to put each bean into `$_`. We'll be seeing a lot more of `$_` as we go on.

You may be wondering what characters you can get away with in the name of a Perl variable: they should start with a letter (upper or lower case), and thereafter can contain any of A to Z, a to z, 0 to 9 and the underscore \_. YMMV with alphanumerics from other scripts (Perl supports Unicode, but that's a whole other post).  

## Other punctuation variables

  
However, Perl is also liberally sprinkled with "punctuation variables", which you will need to learn as you go along. Rather than starting '`$`letter', they generally start '`$`punctuation', like `$_` , `$!` , `$@` and `$/`, to name four of the most useful ones. These variables are special, and are often set or assumed by certain functions. Earlier you learnt that `chomp` will remove newlines from variables. This is actually a fib: it will remove whatever is in `$/` from the end of the string if it's present, it just happens that `$/` (the "input record separator") is set to `\n` by default:  

```perl
$string = "hello:";
chomp $string;
print "$string\n";
    # chomp does nothing, as $/ is \n and $string doesn't end in \n
$/ = ":";
chomp $string;
print "$string\n";
    # chomp will now remove : from the end of strings, which it duly does
```

  

```text
hello:
hello
```

  
Of these punctuation variables, `$_` is particularly infamous: the following do the same thing:  

```perl
foreach $bean ( @beans ) { print $bean; }
foreach ( @beans ) { print; }
```

  
`perl` assumes `$_` as the loop variable in the `foreach`, and also assumes `$_` if no other arguments are given to `print`. Some criticise Perl scripts for having the invisible thread of `$_` running through them, but there's nothing to stop you being more explicit if you want.  

## Statement modifiers

  
Back to the program. There are a few more short-cuts that are instructive, if we ignore the middle bit:  

```perl
print "What is your name?";
chomp( $name = <STDIN> );
@beans = qw( adzuki haricot mung );
foreach ( @beans ) {
    print "$name likes $_ beans.\n";
}
```

  
can also be written:  

```perl
print "What is your name?";
chomp( $name = <STDIN> );
@beans = qw( adzuki haricot mung );
print "$name likes $_ beans.\n" foreach @beans;
```

  
For simple, **single** statements like the last one, you can append the loopy bit and avoid all those braces in this pleasantly readable style. Beware using this on long lines though, as the loopy bit (*statement modifier*) at the end can get lost. You should always have a care for the future readers of your code: well written code can read like prose if you're careful, which makes understanding it much easier. Perl gives you 'more than one way to do it', but that doesn't mean you should chose the first appalling way that comes into your head. However, if you want serious brevity:  

```perl
print "What is your name?";
chomp( my $name = <STDIN> );
print "$name likes $_ beans.\n" foreach qw( adzuki haricot mung );
```

  
There is little distinction between a list and a *bona fide* array, so if you just put a list where a real array is expected, it'll generally still do what you mean.

Next up...[bondage, discipline and subroutines](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines").
