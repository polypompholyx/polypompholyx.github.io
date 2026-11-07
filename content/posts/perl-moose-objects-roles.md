---
title: Moose objects and roles
date: '2013-04-12T15:48:41Z'
lastmod: '2013-04-12T17:22:24Z'
url: /2013/04/perl-moose-objects-roles/
slug: perl-moose-objects-roles
draft: false
wp_id: 738
categories:
- Perl
wp_comments:
- id: 4859
  author: apatsche
  url: ''
  date: '2013-05-07T08:17:44Z'
  kind: comment
  html: '<p>no need  to use strict/warnings<br/>

    use Moose; # automatically turns on strict and warnings</p>

    <p>https://metacpan.org/module/Moose#SYNOPSIS</p>'
  depth: 0
- id: 4869
  author: polypompholyx
  url: http://www.polypompholyx.com
  date: '2013-05-07T11:11:57Z'
  kind: comment
  html: '<p>Thanks for this: I didn''t notice that bit of the perldoc!</p>'
  depth: 1
- id: 5345
  author: jjap
  url: ''
  date: '2013-05-29T14:07:52Z'
  kind: comment
  html: <p>Very understandable explanation of Roles in Moose, thanks!</p>
  depth: 0
---

## Mr Moose's Newfangled Object Framework

[Creating objects from scratch by hand-rolling them](/2013/02/classes-and-objects/ "Classes and objects") is somewhat fragile, and you end up drowning in the writing of endless boilerplate accessor methods. I would strongly suggest that rather than doing objects the hard way, you use the `Moose` object framework unless there's some particular constraint (speed, memory footprint) on your code that would make it inappropriate.

`Moose` is simply a module, so to do stuff with it, you'll need to load it.  

```perl
use 5.12.0;
use strict;
use warnings;
use Moose;
```

  
The first three lines are optional, but if you're using Perl's modern object framework, you might as well take advantage of its other more recent features.

From a coding standpoint, a `Moose` object is still a blessed [hashref](/2012/10/perl-refs-data-structures/ "References and data structures") instantiated with `new`, but the module imports some syntactic-sugar functions that allow you to create objects by declaration, rather than having to hand-code most of their methods.

Creation of the `Cat` class from the previous post is so simple we can afford to give it an extra attribute and an extra method for the same quantity of RSI:  

```perl
package Cat;
use strict;
use warnings;
use 5.12.0;
use Moose;

has( 'stomach_contents',
      is      => 'rw', 
      isa     => 'Str', 
      default => 'nothing',
);

has( 'balance',
      is      => 'ro', 
      isa     => 'Str', 
      default => 'perfect',
);

sub feed {
    my ( $self, $food ) = @_;
    $self->stomach_contents( $food ) if defined $food;
    return $self->stomach_contents();
}

sub vomit {
    my ( $self ) = @_;
    my $vomit = $self->stomach_contents();
        # we could still use feed() instead, but this is more intuitive
        # given Moose has created the accessor method for us for free
    $self->feed( 'nothing' );
    return $vomit;
}

sub fetch {
    say "I don't bloody think so";
}

1;
```

  
The `has` declaration is used to create an attribute called `stomach_contents` with an associated getter/setter method called  `stomach_contents`. The other items passed to `has` set restrictions on the attribute and what its getter/setter can do, and what the value of the attribute can be.  

- If you pass `is => 'rw'`, the method will act as a read/write getter/setter accessor method. If you pass `is => 'ro'`, the attribute can only be set at the time of instantiation, and the associated method will a **r**ead **o**nly getter accessor thereafter.
- If you pass `isa => 'Str'`, the attribute must be (something interpretable as) a string. `Bool`, `Num`, `ArrayRef`, *etc.* are some of the alternative [restrictions on the attribute's type](http://search.cpan.org/dist/Moose/lib/Moose/Manual/Types.pod "Moose Types on CPAN").
- The value of the attribute can be set to a default at instantiation by `default => `*`blah`* where *blah* can be a value, or a coderef like `sub { time % 2 ? 'empty' : 'fish-heads' } ` that returns a default value.

  
You then create a `Cat` in the same way as before:  

```perl
my $kitty = Cat->new(); # create new object $kitty of class Cat
```

  
and manipulate it by invoking methods on it as before:  

```perl
$kitty->feed( "Mechanically recovered meat sludge" );
```

  
You can *still* even violate encapsulation and look at its innards:  

```perl
use Data::Dumper;
Dumper( $kitty );
```

  

## Inheritance (if you must)

  
To implement the `Manx` class that inherits from `Cat`, you use `extends`:  

```perl
package Manx;
use strict;
use warnings;
use 5.12.0;
use Moose;
extends 'Cat';

has( 'tail_type',
      is      => 'rw', 
      isa     => 'Str', 
      default => 'stumpy',
);

# We can override the default value of the 'balance' attribute of the parent Cat class
# using a plus sign to indicate we're extending/modifying a pre-existing attribute
has( '+balance', default => 'issues' );
has( '_secret_name',
      is      => 'ro', 
      isa     => 'Str', 
      default => sub { time % 2 ? 'Odette' : 'Evelyn' },
);

sub miaow {
    my( $self ) = @_;
    print "Miaow\n";
}

# We can override the 'fetch' method too by passing a coderef to 'override',
# and we can invoke the parent's 'fetch' method by calling 'super'

override 'fetch' => sub {
    my $self = shift;
    say "Hm, thinking about it...";
    $self->_secret_name eq 'Odette' ? super() : say "Oh, alright then";
};
1;
```

  

## Roles

  
Although inheritance is a very common feature in programming languages that have classes, when you create subclasses that *inherit* from base classes and then extend them with additional functionality, there's a good chance you might be better off composing the class from its *roles* instead.

Some classes *genuinely* extend their base classes. `3DPoint` extends `2DPoint` by the addition of a `z` attribute.  `Bird` extends `Vertebrate` by overriding the default 'skin' value of the `integument` attribute with 'feathers'.

If a piece of code uses a generic `Vertebrate` object, you should be able to replace it with a `Bird` and see no ill effects, because all the things a `Vertebrate` can do should be a subset of the things a `Bird` can do.

However, what happens when we try to make a `Bird` `fly?` When we come to implement `Bat`, we realise that a lot of the aerial assault code in `Bird` should also be in `Bat` too. It doesn't make sense to factor `fly` out into `Vertebrate` otherwise you'd be able to make a generic `Vertebrate->fly`, which - in general - it shouldn't be able to do.

The problem is that our two classes are trying both to model the hierarchy of our organisms, and also to avoid code duplication. These two aims are incompatible. We want only one copy of the `fly` method to avoid code duplication in `Bird` and `Bat`, but we also want `Vertebrate` to contain only the methods applicable to all vertebrates. Similarly, we'd want only one copy of `lay` and `roll` to avoid duplication of `EggLayer` code across `Bird` and `Bee`.

One way to work around this clash is to allow a class to have multiple parents. We could create classes called `Aircraft` and `EggLayer` and allow `Bird` to inherit from `Vertebrate` and `Aircraft` and `EggLayer`. This would certainly make sense if we'd already written the `Aircraft` class for some other previous project. Such multiple inheritance is possible in Perl, but it simply opens a new can of worms.

The most important of these problems is that `Bird` will inherit all the methods and attributes of all its base classes, and there may well be clashes. It is not possible to resolve these clashes automatically *and* correctly. Perhaps you want `Bird` to inherit the `squawk` method from `Vertebrate` (overriding `Aircraft`'s irrelevant radio transponder version). But maybe you also want some sort of disambiguation so you can use `Aircraft`'s `roll` method and the egg-`roll`-ing method that is supplied by `EggLayer`. Most languages (including Perl's default method resolution order) do not give you this flexibility.

`Moose` allows you to compose a class from roles, and to allow fine-grained control over what happens when roles have conflicting methods.  

```perl
use strict;
use warnings;
use 5.12.0;

{
  package Vertebrate;
  use Moose;
  has( 'integument', is => 'ro', default => 'skin' );
  sub squawk { 
    my ( $self, $what ) = @_;
    say uc "$what!!!"
  };
}

{
  package Aircraft;
  use Moose::Role;
  has( 'wings',      is => 'ro', default => 'flap', );
  sub fly {
    my ( $self ) = @_;
    print "My wings " . $self->wings . "\n";
  }
  sub roll {
    say "Are you sure you wouldn't rather I yawed or pitched?";
  }
  sub squawk { 
    say "7700! 7700! 7700!"
  };
  requires 'wingspan';
}

{
  package EggLayer;
  use Moose::Role;
  has( 'clutch',      is => 'rw', default => 0, );
  sub lay {
    my ( $self ) = @_;
    print "Clutch-size now " . $self->clutch( 1 + $self->clutch ) . "\n";
  }
  sub roll {
    say "Inverting my eggs";
  }
  requires 'wingspan';
}

{
  package Bird;
  use Moose;
  extends 'Vertebrate';
  has( '+integument',             default => 'feathers' );
  has( 'wingspan',    is => 'ro', default => 0 );
  with
    'Aircraft' => { -alias => { squawk => 'transponder_squawk'}, -excludes => 'squawk' },
    'EggLayer' => { -alias => { roll => 'roll_eggs' }, -excludes => 'roll' };
}

my $bird = Bird->new( wingspan => 20 );
print "Bird has ". $bird->integument . "\n";
$bird->fly;
$bird->squawk( "Tweet" );
$bird->transponder_squawk;
$bird->roll;
$bird->lay;
$bird->lay;
$bird->roll_eggs;
```

  

```text
Bird has feathers
My wings flap
TWEET!!!
7700! 7700! 7700!
Are you sure you wouldn't rather I yawed or pitched?
Clutch-size now 1
Clutch-size now 2
Inverting my eggs
```

  
Rather than inheriting `EggLayer` and `Aircraft` base classes using `extends`, we consume `EggLayer` and `Aircraft` roles using `with`.

The packages that define the `EggLayer` and `Aircraft` roles look very similar to the packages implementing the `Vertebrate` and `Bird` classes; the main difference is that they `use Moose::Role` rather than `use Moose`. Roles cannot be instantiated, so you cannot create a stand-alone `Aircraft` or `EggLayer` object, but you could certainly consume these roles into `Cessna` and `Platypus` classes.

The `Aircraft` role shows an additional feature. It implements `fly`, `roll` and `wings` itself, but it does not implement `wingspan`. However, it `requires` that `wingspan` be implemented *somehow* by any class consuming the `Aircraft` role. This allows you to use roles to create interfaces.  

```perl
{
  package Aircraft;
  use Moose::Role;
  has( 'wings',      is => 'ro', default => 'flap', );
  sub fly {
    my ( $self ) = @_;
    print "My wings " . $self->wings . "\n";
  }
  sub roll {
    say "Are you sure you wouldn't rather I yawed or pitched?";
  }
  sub squawk { 
    say "7700! 7700! 7700!"
  };
  requires 'wingspan';
}
```

  
If you delete the line in `Bird` that defines wingspan as an attribute, you'll get an exception:  

```text
'Aircraft|EggLayer' requires the method 'wingspan' to be implemented by 'Bird'
```

  
The `Bird` class has to deal explicitly with any naming conflicts arising from its consumption of roles. This is a good thing: better to deal with this clearly and make it do what you want, than to rely on some One Size Fits None automated resolution.

Either the `Bird` class has to define its own `roll` method directly, or it needs to exclude and/or alias the `roll` methods it has consumed. Here, we exclude consumption of `EggLayer`'s `roll` method, but also alias it to `roll_eggs` so that we can still access it is we need to. We could also have excluded and aliased the `Aircraft` version to `roll_fuselage` or similar, but that would leave the class without any `roll` method at all. Although this is allowed, it's probably to be discouraged, as naïve coders using your `Bird` class will expect it to have a `roll` method, and it's best not to disappoint them.  

```perl
{
  package Bird;
  use Moose;
  extends 'Vertebrate';
  has( '+integument',             default => 'feathers' );
  has( 'wingspan',    is => 'ro', default => 0 );
  with
    'Aircraft', => { -alias => { squawk => 'transponder_squawk'}, -excludes => 'squawk' },
    'EggLayer'  => { -alias => { roll => 'roll_eggs' }, -excludes => 'roll' };
}
```

  
Similarly, we have a conflict between the `squawk` *inherited* from the `Vertebrate` class, and the `squawk` *consumed* from the `Aircraft` role. Note this is subtly different from the case above, which was a conflict between roles, rather than between a role and a class. Here, we exclude consumption of the irrelevant `Aircraft` version, but again alias it so we can access it as `transponder_squawk` if we wish. If we did not do this, the `squawk` consumed from the `Aircraft` role would **silently** override the `squawk` inherited from the `Vertebrate` class.

Roles provide a convenient way of packaging behaviours up into reusable chunks, without having to create a (possibly, even probably) spurious hierarchy of classes and subclasses and inheritance. If you find yourself using inheritance, think carefully about whether the subclass you propose is truly extending its parent, or whether it's simply adding new behaviours that other classes might need too. If the answer is the latter, you probably want roles not inheritance.

Next up...[command line](/2012/10/perlcommand-line/ "Command line")
