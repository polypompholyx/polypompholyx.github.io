---
title: Arrays and slices
date: '2012-10-03T13:06:13Z'
lastmod: '2013-04-12T09:45:49Z'
url: /2012/10/arrays-and-slices/
slug: arrays-and-slices
draft: false
wp_id: 333
categories:
- Perl
---

## Types

You [should now be able to](/2012/10/perl-input-and-output/ "Input and output") create very simple scripts that can take input from the keyboard, assign it to scalar variables, and echo it back to the screen with `print`. Time for some technicalities.

Perl is often (and wrongly!) termed a *weakly typed* language. For those of you coming from bondage and discipline languages like C or Java, this means Perl does not require you to explicitly point out what kind of variable your variables are: `float`s, `double`s, `int`egers, `char`acters, `bool`eans, `string`s, *etc*.

For those of you who are learning programming here, this means you don't have to worry about what you put into a variable like `$name`, in particular, you don't need to worry if its a little integral number, a big fat floating point number, a single character, a string, or anything else, and you are free to assign different values, and different *kinds* of value dynamically as the program runs.

Perl *does* have data types though. However, what `perl` worries about is not the distinctions a computer might like to make (in terms of how big a chunk of data is in memory), but the distinction between singular and plural, much like many human languages. In Perl, singular data is called scalar data, and comes in variables starting with a `$`. Plural data is called *array* (or list) data, and is stored in variables starting with a `@`.  

## Scalars

  
Scalar data is \$ingular data. Scalar variables always start with a `$` for \$calar, and can contain **one** of pretty much anything. `$name` could contain an integer (`2`), a floating point number `(12.045e+89`), a character (`"K"`) or a string (`"or Pretty much anything else"`). They can even contain pointers to other sorts of data ("references", but we're getting ahead of ourselves). To create a scalar variable, you just write:  

```perl
$string = "Some string or other";
$number = 12453;
```

  
You don't need to, and indeed should *not*, put quotes around numbers.  

## Arrays

  
In contrast to scalar data, array data is `plur@l` data. Array variables start with a `@` for `@rray`, and store a **list** of scalars. Creating an array could look like any of the following:  

```perl
@numbers  = ( 1, 3.05, 4, 2e-10, 23 );
@strings  = ( "Hello", 'everybody', "I'm Dr. Nick Riviera\n" );
@allsorts = ( 12.5, 'plop', "some tabs\t\t\t\t", $chocolate, 56, "C" );
```

  
When you create an array, you need to put the (suitably quoted, scalar) values in a *list* between parentheses, separated by commas, *i.e.* arrays are created like this:  

```perl
@array = ( $scalar1, $scalar2, $scalar3 );
```

  
To access the individual members of an array, imaginatively called `@array`, we need to use square brackets. The syntax is:  

```perl
@array = ( 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22 );
$the_9th_member_of_the_array = $array[8];
print $the_9th_member_of_the_array;
```

  
And `$the_9th_member_of_the_array` will print out '16'. There are two gotchas here.

Firstly, what has happened to the `@` of `@array`?

And secondly, why `8`, not `9`?

The `$` and `@` 'sigils' aren't *really* part of the name of the variable. They are more a way of telling `perl` whether the thing you're talking about is a **single** thing or a **list** of things. When you *create* an array, you use a `@` sign, because you want  `perl` to put a *list* into it. However, when you want to access an *individual member* of an array, you're trying to get a singular piece of data, a scalar, so this gets an `$`.

This syntax is a little weird, but you're currently stuck with it: when you're talking about a list of data, you need a `@`, as in `@array = ( `*`blah...`*` );` but to access a single bit of array data, you need to a `$`, as in `$array[index_number];`

Which brings me to the second point. In Perl, arrays index from the number 0, so the 9<sup>th</sup> element in an array is at index number 8: `$array[8]`. If you just put your brain into perl/C gear and think of the 1<sup>st</sup> element of an array as being the 'zeroth', 0<sup>th</sup>, member, you may find this easier. So:  

```perl
#!/usr/bin/perl
@beans = ( "adzuki", "haricot", "mung" );
    # anything following a '#' is a comment
    # perl will ignore everything from the '#' to the end of the line
print "$beans[0]\n";  # this is adzuki
print "$beans[1]\n";  # this is haricot
print "$beans[2]\n";  # this is mung
print "$beans[-1]\n"; # this is also mung
```

  

```text
adzuki
haricot
mung
mung
```

  
Negative indices are counted back from the end of the array, so the last item is the minus-1<sup>th</sup>.  

## Slices

  
Another useful way to access pieces of arrays is to take *slices* of them:  

```perl
@cake = ( "flour", "eggs", "milk", "sugar", "butter", "sultanas", "water" );
@slice_of_cake = @cake[ 3, 6 ];
print "@slice_of_cake\n";
```

  

```text
sugar water
```

  
`@slice_of_cake` will contain the list ( "sugar", "water" ). Note that the slice syntax `@slice_of_cake` needs a `@`, because you are creating a list. Likewise, `@cake` also gets a `@`, because you're creating plur@l data, not a \$ingle piece of data. Slices are useful for getting at multiple bits of data simultaneously, without tediously having to write single accesses for each bit. You can also *assign* things to a slice:  

```perl
@array = ( "hello", "everybody", "I'm", "Dr.", "Nick", "Riviera" );
print "@array\n";
@array[ 3, 4, 5 ] = ( "a", "complete", "charlatan" );
print "@array\n";
```

  
You can see from the previous few scripts that, like scalar variables, arrays also interpolate their values when put in double quotes. Furthermore, the items will be helpfully padded with spaces too.

Next up...[hashes](/2012/10/perl-hashes/ "Hashes").
