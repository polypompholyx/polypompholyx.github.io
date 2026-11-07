---
title: Hashes
date: '2012-10-03T13:20:52Z'
lastmod: '2013-04-12T09:43:25Z'
url: /2012/10/perl-hashes/
slug: perl-hashes
draft: false
wp_id: 340
categories:
- Perl
---

## Hashes

Perl actually has two sorts of array. Simple arrays like [those we've already discussed](/2012/10/arrays-and-slices/ "Arrays and slices") are simply called arrays. The second sort of array is called an *associative array*, or *hash.* They're very similar to dictionaries, if you're a Python programmer. Hashes are created with a `%` for `%we_ran_out_of_sensible_symbols`, and contain pairs of data (ah, maybe it was for the two blobs in a `%` sign) called `keys` and `values`. Here are some typical hash creations:

```perl
%hash = ( key1 => 'value1', key2 => 'value2', key3 => 'value3' );
%dictionary = (
    aardvark  => "first",
    name      => "Steve",
    age       => 35, # that was 25 in the original version of this tutorial. fuck.
    zebedee   => "character in The Magic Roundabout",
);
```

The syntax is nearly the same as for normal arrays: the only difference is the `=>`. The `=>` is just a "fat comma", and in fact, if you replaced the `=>` with a real comma, and surrounded each of `aardvark`, `Steve`, `age` and `zebedee` with quotes, it would still work. Hashes are simply created from lists, and they're not fussy about their commas. However, `=>` has two advantages: it makes the fact you're creating pairs of data more explicit, and it also means you don't have to quote the string that forms the key (this is done automagically for you): note it's `aardvark`, not `'aardvark'`. You might also note that I've neatly lined up the fat commas: pretty code is readable code.

The first member of each pair in a hash is called the key, and the second is called the value. To access the individual members of a hash, you use a similar syntax to accessing array members, but rather than `[INDEX]` brackets, you use `{KEY}` braces:  

```perl
$value = $hash{ 'key' };
```

  
So:  

```perl
%fruit_trees = (
    apple => "Malus", 
    pear  => "Pyrus",
    plum  => "Prunus"
);
```

  

```perl
$latin_name_of_apple = $fruit_trees{ 'apple' };
print $latin_name_of_apple;
```

  
Again, like the funny syntax for normal arrays, you need a `$`, because you're accessing \$ingle bits of data from the hash. Hashes are stupendously useful, since it is far easier to use a hash than an array in a situation like:  

```perl
$personal_details{ 'name' };
```

  
since if you used an array:  

```perl
$personal_details[ 2 ];
```

  
you'd have to remember whatever arbitrary index you stored that the person's name at (`2` here). It's far easier to use a hash in these circumstances, and just ask for what you want with a key.  

## Hash slices

  
As with arrays, you can also take slices of hashes, but the syntax will make you do a double take:  

```perl
%trees = (
    apple =>  "Malus",
    pear  =>  "Pyrus",
    plum  =>  "Prunus",
    oak   =>  "Quercus",
    ash   =>  "Fraxinus",
    yew   =>  "Taxus",
);
@latin_names_of_fruit_trees 
    = @trees{ 'apple', 'pear', 'plum' }; # hash slice
print "@latin_names_of_fruit_trees\n";
```

  
What's with the `@` for the slice syntax? Remember that `$`, `@` and `%` aren't really part of the name of a variable, they are ways of accessing or creating data of a specific type. When we take a slice of a hash, we are accessing a *list* of `values`, just as when we are slicing an array, so we need a `@`. If it's any consolation, I think this is horrible too. Again, note the pretty arrangement of the tree hash: Perl is largely whitespace-insensitive, so you can largely get away with writing your code in whatever creative way you want.

So, to summarise. Perl has three fundamental data types: [scalars](/2012/10/perl-not-a-hello-world-script/ "Not a hello world script"), [arrays](/2012/10/arrays-and-slices/ "Arrays and slices") and hashes. When creating them, you'll need to use `$`, `@` and `%` respectively. When accessing them, you'll need to use `$` to access \$ingle bits of data, and `@` to access plur@l slices of data, with the appropriate parentheses: `[INDEX]` for arrays, `{KEY}` for hashes.

Next up...[simple loops](/2012/10/perl-simple-loops/ "Simple loops").
