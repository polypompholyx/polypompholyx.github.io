---
title: References and data structures
date: '2012-10-04T14:06:40Z'
lastmod: '2013-04-12T10:32:05Z'
url: /2012/10/perl-refs-data-structures/
slug: perl-refs-data-structures
draft: false
wp_id: 451
categories:
- Perl
---

## References

Arrays and hashes and lists and [the manipulation thereof](/2012/10/perl-substitute-split-join/ "Substitutions, splitting and joining") are very useful, but sometimes you want something a bit less flat; a little more multidimensional. Perl does indeed allow for multidimensional arrays (of a sort), but the syntax is a little odd. Let us enter the world of the *reference*.

References are like signposts to other data. To create a multidimensional array, what you actually need to do is create a normal 1-dimensional array whose elements are these signposts to other arrays. In this way, we can fake a multidimensional array. So, how do we create a reference? There are two ways. The first is to use the `\` operator, which creates references to bits of data you have *named* and defined previously:  

```perl
$scalar     = "hello";
$scalar_ref = \$scalar;
@array      = ( 'q', 'w', 'e', 'r', 't', 'y' );
$array_ref  = \@array;
%hash       = ( key => "value", lemon => "curd" );
$hash_ref   = \%hash;
```

  
Because references are just a single signpost saying "the thing I'm referring to is just over *there*", they are \$ingular data, hence they are always \$calars. Creating arrayrefs and hashrefs is such a common thing to do, there is a shorthand, which allows you to create them directly, and without naming them:  

```perl
$array_ref  = [ "q", "w", "e", "r", "t", "y" ];
$array_ref2 = [ qw{ you can use qw to save time } ];
$hash_ref   = { key => "value", lemon => "curd" };
```

  
These create references to *anonymous* arrays and *anonymous* hashes. In the first example, we created references to named arrays and hashes, like `@array` and `%hash`. In this example, there is no named array or named hash, only the **`[ ]`** brackets or **`{ }`** braces, which are never named.

You can also create references to anonymous subroutines:  

```perl
$code_ref = sub { return 2**$_[0] };
```

  
Which is very, very useful, as we shall see.  

## Dereferencing

  
*Creating* references is easy then: you just need the right mix of `\`, and `{ } [ ]` braces and brackets. How do we get back to the contents? This is *dereferencing*. To see how this works, let's take an example of the multidimensional array we wanted in the first place:  

```perl
@unidimensional = (
    ( "this is just a one dimensional array", "even though"),
    ( "we have nested", "parentheses" )
);
    # parentheses don't nest in perl:
    # everything gets flattened to a single list
@multidimensional = (
    [ "but this one", "really is multidimensional" ],
    [ "two by", "two" ]
);
    # brackets mean create references to anonymous arrays
    # and put them in @multidimensional
```

  
The multidimensional array is really a one-dimensional array that contains pointers (references) to the location of other arrays. So Perl doesn't *really* have multidimensional arrays, but you can fake them using references. Getting at the data is a little complex:  

```perl
my @multidimensional = (
    [ "but this one", "really is multidimensional" ],
    [ "two by", "two" ]
);
my $element_1_1 = $multidimensional[1]->[1]; # gets 'two'
print $element_1_1;
```

  

```text
two
```

  
The `$multidimensional[1]` bit is obvious: we're just using the usual (counting from **zero**) syntax for pulling out the 2<sup>nd</sup> element of the array. If we actually captured this:  

```perl
my @multidimensional = (
    [ "but this one", "really is multidimensional" ],
    [ "two by", "two" ]
);
$element_1 = $multidimensional[1];
print ref $element_1;
print $element_1;
```

  
the scalar `$element_1` would contain the reference itself. We can use the `ref` operator to find out what the scalar points to:  

```perl
print ref $element_1;
```

  

```text
ARRAY
```

  
We can also find out what `perl` calls the reference:  

```perl
print $element_1;
```

  

```text
ARRAY(0x183f1dc)
```

  
or similar, which isn't very informative! The `0x...` is a hexadecimal code to the array's location in memory, basically the 'map reference' where the array has been stored. So although:  

```perl
$multidimensional[1]
```

  
returns a reference to an array (`'0x183f1dc'`):  

```perl
->[1]
```

  
is the bit that actually 'dereferences' the reference, chasing the pointer to the array at `0x183f1dc`. You could think of the `->` as 'follow this signpost to the real data'. The `->` dereferencing arrow can also be used to pull out bits of multidimensional hashes:  

```perl
my %multi_hash = (
    name => {
        fore => "Steve",
        sur  => "Cook",
    },
    age => 26 # fucking hell, this tutorial is 10 years old
);
my $forename = $multi_hash{name}->{'fore'};
my $age      = $multi_hash{'age'};
print "name $forename, age $age\n";
```

  

```text
name Steve, age 26
```

  

## HoH, AoA and other Thingies

  
You can see here that a multidimensional structure needn't be a boring rectangular matrix (an array of arrays, AoA), exactly 2 by 2 or 4 by 4 by 3. Not does it need to be a hash of hashes (HoH). It can be an unbalanced and weird Thingy: you can have anything you like:  

```perl
my @complex = ( # is an array at the top-level, containing...
    "a scalar",
    { and => "an internal hashref" },
    "another scalar",
    [ # element 3 of the @complex is this big arrayref
        [
            "a two deep arrayref",
            "with two elements"
        ],
        { # element 1 of this arrayref is a little hashref
            lemon => "curd" # key lemon of this hashref is curd
        }
    ]
);
print my $wanted = $complex[3]->[1]->{'lemon'};
```

  
Hopefully the syntax should be OK now: if you wanted the words "curd", you need:  

```perl
my $wanted = $complex[3]->[1]->{'lemon'};
```

  
*i.e.* take the third element of `@complex` (don't forget we count from 0!), that is the big arrayref at the end, dereference it to get the first element (the little hashref inside the arrayref), then dereference the hashref with the key lemon.

When we do objects later, we'll find that they are usually *anonymous hashrefs*:  

```perl
$anonymous_hashref = { name => "Cornelia", species => "Elaphe guttata" };
```

  
to get at the name this time, we need the syntax:  

```perl
$name = $anonymous_hashref->{'name'};
```

  
Note that because we are starting with a scalar (not an array as in the last example), the very *first* thing we need to do is dereference it with an arrow: the scalar `$anonymous_hashref` points to an (anonymous) hash, so you can't just look at its keys, because a scalar *doesn't* have keys. If this doesn't make sense, compare these:  

```perl
@array    = ( qw/ some elements/ );
$zeroeth_element_of_array    = $array[0];
$arrayref = [ qw/some elements/ ];
$zeroeth_element_of_arrayref = $arrayref->[0];
```

  
There is a certain shortcut you can take when dealing with multidimensional arrays and hashes (and mixtures, like arrays of arrayrefs of hashrefs). Since an array or hash can only contain a single 1 dimensional list, we know that:  

```perl
@array = ( [ "two", "by" ], [ "two", "elements" ] );
$element_0_1 = $element[0][1];
```

  
can only mean:  

```perl
$element_0_1 = $array[0]->[1];
```

  
So, in general, if you're dealing with something that is a *real* array or hash at the highest level, you can miss off the `->` arrows completely unambiguously, so our earlier example:  

```perl
$wanted = $complex[3]->[1]->{'lemon'};
```

  
could be written with less line noise as:  

```perl
$wanted = $complex[3][1]{'lemon'};
```

  
However, you must be careful with this syntax if you're dealing with something that is a *scalar* at the highest level (*i.e.* an anonymous hashref or arrayref):  

```perl
$arrayref    = [ [ "two", "by" ], [ "two", "elements" ] ];
    # note this is scalar (an arrayref), not an array
$element_0_1 = $arrayref->[0]->[1];
$element_0_1 = $arrayref->[0][1];
```

  
The last two are equivalent, but note you can't dispense with the first `->` , which is actually obvious, as:  

```perl
$element[0][1];
```

  
means the first element of the zeroeth arrayref contained in ***@*element**, which doesn't exist (or if it does, you'll get the value from that, which isn't what you're after).

You've now seen that constructing references can be done in many ways. TIMTOWTDI. Some examples:  

```perl
$arrayref  = [ 0, 1, 2, 3 ];
    # create a scalar that is an anonymous arrayref
@array     = ( 0, 1, 2, 3 );
$arrayref  = \@array;
    # create a reference to a real named array
@multi     = ( \@one, \@two, \@three );
    # multidimensional array constructed from references to named arrays
@multi2    = ( [ 1, 2 ], [ 3, 4 ], [ 5, 6 ] );
    # multidimensional array constructed from anonymous arrayrefs
$arrayref2 = [ [ 1, 2 ], [ 3, 4 ], [ 5, 6 ] ];
    # multidimensional: arrayref constructed from anonymous arrayrefs
```

  

## Slicing thingies

  
Often you won't want to play with just a single element of a **thingy** (which is the not very descriptive term for a Perl data structure composed of some gungy mass of references). You'll want a slice of a thingy, or to iterate over the whole array pointed to by an arrayref. How do we do this? Well, both need the same sort of dereferencing syntax:  

```perl
$arrayref = [ 0, 1, 2, 3, 4 ];
@slice    = @{ $arrayref }[ 0, 2 ];
@anonymous_array_pointed_to_by_arrayref = @{ $arrayref };
```

  
The way to read **`@{ $arrayref }`** is 'the array referred to by `$arrayref`'. If you want a hash, you use a similar syntax:  

```perl
$hashref = {
    lemon      => "curd", 
    strawberry => "jam", 
    orange     => "marmalade",
};
@hashslice     = @{ $hashref }{ lemon, orange };
    # don't forget slices are plur@l data
%anonymous_hash_pointed_to_by_hashref = %{ $hashref };
```

  
This (of course?) produces yet another way of accessing the individual elements of a reference:  

```perl
$hashref = {
    lemon      => "curd", 
    strawberry => "jam", 
    orange     => "marmalade",
};
$hashelement  = ${ $hashref }{ "lemon" };
    # the pairs inside the hash referred to by $hashref are $calar data
$arrayref     = [ 0, 1, 2, 3, 4 ];
$arrayelement = ${ $arrayref }[2];
    #the elements inside the array referred to by $arrayref are $calar too
```

  
So that if we have a dereferenced arrayref:  

```perl
@{ $arrayref }
```

  
we access its elements with the usual Perl syntax:  

```perl
${ $arrayref }[ INDEX ]
```

  
In simple cases, the `{ }` braces can be omitted, although I personally never miss them off, as I get easily confused:  

```perl
@array = @{ $arrayref };
@array = @$arrayref;
```

  
are equivalent nonetheless.  

## Creating reference structures at run-time

  
All the examples so far have relied on you knowing the structure of the thingy at compile time. Although there will be times when you will create huge perl thingies in your code, more often than not, you will be building them at run time from data entered by users or from other files. In fact, a great deal of programming parsing is to do with converting data from one format to another. Data stored in flat files is called 'serialised' data. Data stored within a script will usually be more tree-like. Conversion from serialised input (such as XML files, text files or user input) to serialised output (such as an HTML file, or an email) *via* an internal parse tree of some sort is often a job for [modules from CPAN](http://www.cpan.org "CPAN"), but you'll frequently need to create a quick and dirty converter for a simple format such as the one below. Here, we use simple array and hash manipulation operators (like `push`, `for`, and hash assignment) to create a Thingy on the fly. Since references are just pointers to hash and array structures, building and manipulating them is a simple matter of getting up close and personal to these functions.  

```perl
#!/usr/bin/perl
use strict;
use warnings;
my $record;
my @people;
while ( <DATA> ) {
    chomp;
    if ( /\*\*\*/ ) {  # start of record marker
        $record = {};  # create an empty hashref
    }
    elsif ( my ( $field, $data ) = / (\w+) \s* = \s* (.*) /x ) {
        if ( $field eq "pets" ) {
            $data = [ split /\s*,\s*/, $data ];
            # create an anonymous arrayref:
            # you can wrap things that return lists in []
            # and create arrayrefs as simply as this. Good, isn't it?
        }
        $record->{ $field } =  $data;
        # add key/value pair to the anonymous hashref $record
    }
    elsif ( /---/ ) { # end of record marker
        push @people, $record; # add the hashref to the @people array
    }
    else {
        next;
    }
}
# we have now created a tree in memory, looking something like:
# @people = (
#    { name=>'alice', age=>37, pets=>[] }, 
#    { name=>'bob',   age=>23, pets=>[ 'dog' ] },
#    { name=>'eve',   age=>26, pets=>[ 'millipede', 'snake' ] },
# );
for my $person ( @people ) {
    print ucfirst "$person->{'name'} is $person->{'age'} years old ";
    # ucfirst capitalises the first letter of a string
    if ( my @pets = @{ $person->{'pets'} } ) {
        # assignment is neatest here, as we use @pets in a minutes
        local $" = ', ';
        # the $" is a special perl variable, containing 
        # the thing used to separate array elements in quoted strings:
        # usually it's a space, but we make it a comma and space for
        # our output here
        print "and has the following pets: @pets.\n";
    }
    else {
        print "and has no pets.\n";
    }
}
# everything after a __DATA__ token is available to a perl script and
# can be read automagically via the DATA filehandle, which is opened
# on running your script
__DATA__
***
name = alice
age = 37
pets =
---
***
name = bob
age = 23
pets = dog
---
***
name = eve
age = 26
pets = millipede, snake
---
```

  

```text
Alice is 37 years old and has no pets.
Bob is 23 years old and has the following pets: dog.
Eve is 26 years old and has the following pets: millipede, snake.
```

  
So we take one serial format (our `__DATA__` section), convert it into an internal thingy, then dump the thingy in our own chosen format.  

## Passing by value and passing by reference

  
What other practical uses are there for references? Well, if you've tried to `return` arrays from subroutines, you'll find that it doesn't work how you expected:  

```perl
my ( @one, @two ) = fruits();
print "one @one\ntwo @two\n";
sub fruits {
    my @first  = qw/ lemon orange lime/;
    my @second = qw/ apple pear medlar/;
    return @first, @second;
}
```

  

```text
one lemon orange lime apple pear medlar
two
```

  
The problem is that arrays in list context (such that `return` gives its arguments) interpolate their members. That is, `return` flattens `@first` and `@second` into one big list. The second problem is that arrays are greedy, so when we return this flattened list from the subroutine, `@one` slurps up *all* the return values, and `@two` gets nothing. There is a kludge to get around this:  

```perl
my ( @one, @two );
( @one[ 0 .. 2 ], @two[ 0 .. 2 ] ) = thingy();
```

  
but this is obviously dependent on knowing how many elements are returned: this will break if the two arrays have variable lengths. What we really need to do is pass the arrays by reference:  

```perl
my ( $one, $two ) = fruits();
print "one @{$one}\ntwo @{$two}\n";
sub fruits {
    my @first  = qw/ lemon orange lime/;
    my @second = qw/ apple pear medlar/;
    return \@first, \@second;
}
```

  
The subroutine returns a list of arrayrefs (effectively an array of arrays), which the body of the program then plays with using the `@{ $ref }` dereferencing syntax. You can be explicit if you want, and dereference the arrayrefs back to real arrays if you'd rather:  

```perl
my ( $one, $two ) = fruits();
my @one = @{ $one };
my @two = @{ $two };
```

  
There's something rather important to note about *passing things by reference* instead of by value, as we have done here:  

```perl
my @spices = qw( ginger kratchai galangal );
by_value( @spices );
print "@spices\n";
sub by_value {
    my @spices = @_;
    push @spices, "turmeric";
}
```

  

```text
ginger kratchai galangal
```

  
When you pass things by value, you are passing *copies* of the data, so manipulating these data in the sub does nothing interesting to the original data. To do that, you'd have to return the altered array, and capture it in `@spices` to change the original data. However, when you pass *by reference*, you are passing pointers to the *original* data, so if you manipulate *what the references point to*, you are modifying the *original data*:  

```perl
my @spices = qw( ginger kratchai galangal );
by_reference( \@spices );
print "@spices\n";
sub by_reference {
    my $spices = shift;
    push @{ $spices }, "turmeric";
}
```

  

```text
ginger kratchai galangal turmeric
```

  
Another source of subtle bugs is directly messing with the elements of `@_`:  

```perl
my @spices = qw( ginger kratchai galangal );
by_value( @spices );
print "@spices\n";
sub by_value {
    $_[0] = 'cardamom';
}
```

  

```text
cardamom kratchai galangal
```

  
Like `$_` in a `foreach` loop, the items in `@_` are aliased to the items in the list of arguments passed to the subroutine. Modifing them will modify the data in the body of the program, which is generally something you *don't* want to do. It's always best to be explicit if you want the subroutine to modify its arguments. If you don't want it to, pass by value, and immediately copy the contents of `@_` into some nice lexically scoped variables.  

## `Data::Dumper`

  
References can get quite complicated, which is where the module `Data::Dumper` comes in very handy. Modules can be `use`d, like you have seen with `strict`: they imports some extra functionality to your program, in this case, a function called `Dumper()`.  

```perl
#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
my @complex = (
    "a scalar",
    { and => "a internal hashref" },
    "another scalar",
    [
        [
            "a two deep arrayref",
            "with two elements"
        ],
        {
            lemon => "curd"
        }
    ]
);
print Dumper( \@complex );
```

  

```text
$VAR1 =
[
  'an array',
  {
    'containing' => 'a hashref'
  },
  'a scalar',
  [
    [
      'a two deep arrayref',
      'with two elements'
    ],
    {
      'lemon' => 'curd'
    }
  ]
];
```

  
`Data::Dumper` takes a *reference* to any perl data structure and spits out the contents in a) a pretty printed format, and b) in a format that you can actually `print` to a file:  

```perl
open my $FILE, $file;
print $FILE Dumper( \@complex );
```

  
to save it for later (*serialisation*). You can then recover the data with:  

```perl
do $file;
```

  
Although don't  `do` this if you do not trust the data!  

## Anonymous functions and closures

  
You may remember a while ago that I said you can create anonymous subroutines:  

```perl
$coderef = sub { return 2*$_[0] };
```

  
To use these, you can dereference them like normal, using `()` parentheses, as you might have guessed:  

```perl
print $coderef->(3);
```

  

```text
6
```

  
This is very powerful: it means you can actually return bits of code from subroutines:  

```perl
#!/usr/bin/perl
use strict;
use warnings;
my $multiply = <STDIN>;
my $coderef  = construct( $multiply );
print $coderef->( 2 );
sub construct {
    my $number  = shift;
    my $coderef = sub { return $number * $_[0] };
    return $coderef;
}
```

  
This creates coderefs on the fly which will multiply by whatever number you decide *via* `STDIN`. The technical term for such things is *closures*: the weird thing about them is that the `$number` in `sub construct` is a lexically scoped `my` variable, and ought to disappear forever (go out of scope) when you leave the subroutine. However, when you use:  

```perl
$coderef->( 2 ); # or equivalently
&{ $coderef }( 2 ); 
    # & is the sigil for subroutines, like arrays get @ and hashes get %
```

  
the value of `$number` you entered when you constructed the coderef is still there, deeply bound into the coderef, even though it 'shouldn't' really exist outside the scope of `sub construct`. Magic.

So far we have only talked about so called *hard* references. There are also such things as soft references, which if you try to use when `strict` is on will barf. In the interests of hygiene, I'll not tell you about them, they're not much used, for good reason, and you can always find out about them yourself. If you ever think you need one, it's almost certain what you actually need is a hash.

Next up...[bits and bobs](/2012/10/perl-bits-and-bobs/ "Bits and bobs").
