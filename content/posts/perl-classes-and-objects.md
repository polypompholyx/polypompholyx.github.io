---
title: Classes and objects
date: '2013-02-20T15:14:28Z'
lastmod: '2013-04-12T15:50:11Z'
url: /2013/02/perl-classes-and-objects/
slug: perl-classes-and-objects
draft: false
wp_id: 519
aliases:
- /2013/02/classes-and-objects/
categories:
- Perl
---

## Mr Wall's Olde Fashioned Objeckts

*Caveat lector*. Despite some cosmetic surgery, this post, [like the previous one on writing modules](/2013/02/perl-packages-modules/ "Packages and writing modules"), may show its age. It was originally written when Perl 5 wasn't even 10 years old, and things have moved on substantially since then (and no, I don't mean Perl 6). However, there's a lot of code out there using blessed hashref objects, so before I post something about using the [`Moose`](http://search.cpan.org/dist/Moose/) object framework ([quick-ref guide](http://users.ox.ac.uk/~oliver/data/files/moose-quick-ref.pdf)), this post will explain how to use objects, and how to hand-roll "traditional" Perl 5 hashref objects.

From a usage standpoint, a Perl object is simply a variable that contains some data, and which has some associated methods, which do something with that data when you invoke them. From a coding standpoint, a Perl object is usually just a [reference](/2012/10/perl-refs-data-structures/ "References and data structures") to a data structure (often a [hash](/2012/10/perl-hashes/ "Hashes")) that has been "blessed" into a class (which is just a [package](/2013/02/perl-packages-module/ "Packages and writing modules")), in which the methods are defined as simple [subroutines](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines").  

## Instantiating an object and invoking methods on it

  
By convention, Perl objects are created (instantiated) with a 'class method' called `new`:  

```perl
my $kitty = Cat->new(); # create new object $kitty of class Cat
```

  
and then manipulated by invoking "object methods" on them, such as `feed`:  

```perl
$kitty->feed( "Mechanically recovered meat sludge" );
```

  
If you were writing this in procedural  Perl, you might create a hashref called `$kitty`:  

```perl
$kitty= { stomach_contents => "nothing" };
```

  
and write a function called `feed()`:  

```perl
sub feed {
    my ( $cat, $food ) = @_;
    $cat->{ 'stomach_contents' } = $food;
}
```

  
so you could call:  

```perl
feed( $kitty, "Mechanically recovered meat sludge" );
```

  
to feed the cat.

Although the procedural program above with `$kitty` and `sub feed` works perfectly well, you have to worry about the internal structure of the `$kitty`, what its keys and values are, what the return value of `sub feed` is, and know that the cat is a hashref (not an arrayref), and so on. The same would apply to anyone else trying to write new functions for the cat such as `worm` and `spay`. Furthermore, if you had a  `$puppy` hashref too, which inconveniently had an attribute called `last_meal` rather than `stomach_contents`, you'd need a specific `feed_dog` function to avoid a name-space clash with the `feed` function you've written for the cat.  

## Encapsulation

  
In object-oriented code, the object encapsulates all the details of what is going on, so the user of the object need not care about the `$kitty`'s innards, it just need to know which button buttons (methods) are available to press.

As a user of the code anyway. If you want to *write* the code, you'll have to know the guts intimately. Objects are implemented in the following way:  

- A class is just a package.
- An object is just a reference (usually a hashref).
- A method is just a subroutine.

  
Here is the start of an simple `Cat` class:  

```perl
package Cat;
use strict;
use warnings;
# We'll fill in the gaps here presently
1;
__END__
```

  
There's no need to worry about exporting subroutines, as the whole point of objects is that objects look after their own subroutines (methods). Hence, no `@EXPORT`, *etc*.  

## Classes and objects and methods

  
As you may have gathered, `Cat` is a *class*, not an object. An object is a particular *instance* of a class. The class provides the code to instantiate new objects, so the package that defines a class needs to supply a subroutine that makes and returns new objects, *i.e.* a constructor that instantiates new objects. You *can* call this method anything you like, but it's generally best to call it `new` like everyone else does:  

```perl
sub new {
    my $class = shift;
    my $self = { };
    bless $self, $class;
    $self->feed('nothing');
    return $self;
}
```

  
This method can be called in two ways in a script:  

```perl
use Cat;
my $mr_tibbles  = new Cat; # avoid
my $mrs_tibbles = Cat->new();
```

  
You should always use the latter, as the former can lead to some nasty syntactic ambiguities. The `new` method is just a subroutine, a factory for making objects of class `Cat`. When you invoke a class method, the name of the class is the first thing in the `@_` of the subroutine that implements it. Similarly, when you invoke an object method, the object upon which the method is invoked is the first thing in the `@_` of the subroutine that implements it. So:  

```perl
Cat->new();
```

  
will do something along the lines of calling the function `new( "Cat" )` in `package Cat`. The `new()` method we wrote above therefore gets "Cat" when it it called and it `shift`s this into `$class`. So it will know what sort of an object it should make. Do not be tempted to hard-code the class, as in:  

```perl
$class = "Cat"; # b0rken
```

  
because this will break should anyone want to subclass your class: if someone wants to implement a class called `Tabby` and borrow ('inherit') your `new()` constructor, the hard-coded `new()` will make objects of the wrong class (*i.e.* `Cat`, not `Tabby`). This is a Bad Thing.

Next, the constructor creates the data structure the object needs. This is conventionally called `$self`, but doesn't have to be. This is conventionally a hashref, but doesn't have to be.

Then comes the important bit. We know our class. We have our (empty) data structure. We need to glue these together to form an object. `bless` does this:  

```perl
bless $self, $class;
```

  
makes the data in `$self` an instance of class `$class`.

Now the data structure has been blessed into the appropriate class, you can invoke methods upon it. Here, we invoke the object method `feed` to fill the cat's stomach with nothing:  

```perl
$self->feed('nothing');
```

  
Obviously, for this to work out, we also need to define that object method in our package:  

```perl
sub feed {
    my ( $self, $food ) = @_;
    $self->{ 'stomach_contents' } = $food if defined $food;
    return $self->{ 'stomach_contents' };
}
```

  
The constructor then returns this blessed hashref, to be captured by our user's script in `$mr_tibbles`. That is all there is to constructing an object.  
If you want to see what `$mr_tibbles` actually looks like on the inside, you can investigate him using the arrow de-referencing operator, so:  

```perl
$contents = $mr_tibbles->{ 'stomach_contents' };
```

  
will get you 'nothing', and ...  

```perl
use Data::Dumper;
Dumper( $mr_tibbles );
```

  
...will spray `$mr_tibbles` 's guts out all over the screen. However, such direct dissection of object is generally considered bad form (although it is useful when debugging). The only way to investigate `$mr_tibbles` should be *via* his object methods. `feed()` is just such a method. You call the method with a `->` (which is the same as `.` for most other programming languages that support object-orientation):  

```perl
$mr_tibbles->feed( "Mechanically recovered meat sludge" );
```

  
The `->` here is being used *not* to dereference a reference, but to call a method on `$mr_tibbles`. This dual use for `->` confused the life out of me at first, but if you're careful to note the brackets, you'll be OK:  

```perl
$thing->{ key };
    # hashref dereference, note the {}
$thing->[ index ];
    # arrayref dereference, note the []
$thing->( args );
    #coderef dereference, note the ()
$thing->method( args );
    # method call on object $thing, optional arguments in ()
```

  
The object (`$mr_tibbles`) upon which you invoke a method is the first item put into `@_`. So for the method `feed`, the `@_` is `( $mr_tibbles, "Mechanically recovered meat sludge" )`. These are assigned to `$self` and `$food` respectively. Then, if the `$food` is defined, it's put into `$mr_tibbles` 's stomach with `$self->{ 'stomach_contents' } = $food;`

If no food is passed:  

```perl
$contents = $mr_tibbles->feed();
```

  
does nothing to `$mr_tibbles`: the stomach contents are unchanged. However, *via* `return $self->{ 'stomach_contents' };` the method can both alter (*mutate*) `$mr_tibbles`'s stomach contents and just report (*access*) what he ate last.

The `ref` operator will usually return what a reference refers to (ARRAY, SCALAR, HASH, *etc*.), as you know. However, if we call it on an object, it will return the class the object belongs to:  

```perl
ref( $mr_tibbles );
```

  
This can be useful for debugging. We will now add some more object methods:  

```perl
sub vomit {
    my ( $self ) = @_;
    my $vomit = $self->feed(); # returns whatever he last ate
    $self->feed( 'nothing' );
    return $vomit;
}
```

  
This demonstrates that you can (and should) use methods even within the class. You could've written:  

```perl
sub vomit {
    my ( $self ) = @_;
    my $vomit = $self->{ 'stomach_contents' };
    $self->{ 'stomach_contents'} = 'empty';
    return $vomit;
}
```

  
and manipulated the cat's innards directly, but using the first version protects you from your *own* changes to your *own* code: let your methods do everything for you and it will save you a lot of grief when you decide to rearrange the innards of the cat later.  

## Cat class

  
So here is our `Cat` class, which we should save to a file called `Cat.pm` somewhere in the `@INC` path.  

```perl
package Cat;
use strict;
use warnings;

sub new {
    my $class = shift;
    my $self = { };
    bless $self, $class;
    $self->feed('nothing');
    return $self;
}

sub feed {
    my ( $self, $food ) = @_;
    $self->{ 'stomach_contents' } = $food if defined $food;
    return $self->{ 'stomach_contents' };
}

sub vomit {
    my ( $self ) = @_;
    my $vomit = $self->feed();
    $self->feed( 'nothing' );
    return $vomit;
}

1;
```

  

## Inheritance

  
Let's now implement a rudimentary `Manx` class that inherits from `Cat`, which we should save to a file called `Manx.pm` somewhere in the `@INC` path.  

```perl
package Manx;
use strict;
use warnings;
use base 'Cat';

sub new {
    my $class = shift;
        # This will be 'Manx' unless this constructor itself is inherited by a subclass!
    my $self = $class->SUPER::new( @_ );
        # This will call the constructor of the Cat class, generating a Manx object,
        # but only adding the attributes of the generic Cat, as that's all the parent
        # class knows how to do
    $self->tail_type( 'stumpy' );
    $self->_secret_name( time % 2 ? 'Odette' : 'Evelyn' );
        # Now we add the Manx-specific attributes
    return $self;
}

sub tail_type {
    my( $self, $tail_type ) = @_;
    $self->{ 'tail_type' } = $tail_type;
}

sub miaow {
    my( $self ) = @_;
    print "Miaow\n";
}

sub _secret_name {
    my( $self, $name ) = @_;
    $self->{ '_secret_name' } = $name if defined $name;
    return $self->{ '_secret_name' };
}

1;
```

  
The `@ISA` array takes on a special importance in classes. `@ISA` contains places to look if you can't find a function in the module itself. In object oriented programming, looking somewhere else is called inheritance. The:  

```perl
package Manx;
use base( 'Cat' );
```

  
is a shorthand for:  

```perl
package Manx;
BEGIN {
    our @ISA = ( 'Cat' );
    require Cat;
}
```

  
So when you:  

```perl
use Manx;
my $tabitha = Manx->new();
$tabitha->vomit();
$tabitha->miaow();
```

  
you'll get a new `Manx` cat that can puke and vocalise. Even though there's no method called `vomit()` in `package Manx`, `$tabitha` can still `vomit` because this method is defined in the `Cat` class from which it inherits: a `Manx` IS A `Cat`, and if the relevant method can't be found in `Manx`, the packages in `@ISA` will be searched to find the method instead.

You will note that this subclass defines its own new constructor, because it wants to set the `tail_type` attribute at the time the object is instantiated. The proper way to do this is to call the constructor of the Manx's superclass using the `SUPER::` pseudoclass:  

```perl
sub new {
    my $class = shift;
        # This will be 'Manx' unless this constructor itself is inherited by a subclass!
    my $self = $class->SUPER::new( @_ );
        # This will call the constructor of the Cat class, generating a Manx object,
        # but only adding the attributes of the generic Cat, as that's all the parent
        # class knows how to do
    $self->tail_type( 'stumpy' );
    $self->_secret_name( time % 2 ? 'Odette' : 'Evelyn' );
        # Now we add the Manx-specific attributes
    return $self;
}
```

  
You may also be wondering why the underscore in `_secret_name`. The reason for the underscore is that `_hashkeys` and `_methods` look special to C++ programmers, since they indicate that the data or method are private to the class and should not be used outside of it (*i.e.* they are for internal use only, and do not comprise part of the class's API). In Perl, it's considered bad form for a script to mess with the insides of an object (like the `$self->{ 'stomach_contents' })` directly. It's not expressly forbidden, but it *is* considered unforgivably bad form to mess with a private `$self->{ '_secret_name' }` attribute.

As you can see, there is a great deal of boilerplate here, and much that you might get wrong by accident. Consequently, I would recommend that you use an object framework such as [`Moose`](http://search.cpan.org/dist/Moose/) to create objects by declaration, rather than hand-rolling them as you have see here. And that's what will be...

Next up...[Moose objects and roles](/2013/04/perl-moose-objects-roles/ "Moose objects and roles").
