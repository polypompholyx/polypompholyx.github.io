---
title: Packages and writing modules
date: '2013-02-20T12:34:56Z'
lastmod: '2013-04-12T10:41:36Z'
url: /2013/02/perl-packages-modules/
slug: perl-packages-modules
draft: false
wp_id: 517
aliases:
- /2013/02/perl-packages-module/
- /2013/02/perl-package-module/
categories:
- Perl
---

## Modularisation is a virtue

The previous post showed you [how to install and use other people's modules](/2012/10/perl-install-modules/ "Installing modules"); this post will address how to write your own.

At some point, you will probably find yourself copying-and-pasting code from one script to another. When you find yourself doing that, you should consider what would happen if it later turns out there is a bug in that pasted code. Ten copy-and-pastes down the line, you're going to wish like hell you'd put that bit of code into a module, so you only needed to fix the bug in one place rather than ten.  

- If you ever use the same bit of code two or more times in a single script, you should probably put it in a subroutine.
- If you ever find yourself using the same subroutine in more than one script, you should definitely put it into a module.

  
If you've not seen [CPAN](http://search.cpan.org) yet, now is a good time to do so. It's always a good idea (if not essential!), to have a look on CPAN before you start any significant project, as the chances are, someone else will have been there before you, written the code, worried about it, debugged it, put fifteen bells and twelve whistles onto it, and released it for all and sundry to use.  

## Creating a module

  
There're many things you can mess up if you're writing a module from scratch, so the best way to do it, even for 'personal' modules you have no intention of unleashing on the world, is to use a module-building command-line utility. There are two types of these in common usage; the older is a utility called `h2xs`; the newer is exemplified by the `module-starter` utility that comes with `Module::Starter`.

Change to a directory you don't mind creating a directory called `MyModule` in, and type:  

``` input
h2xs -AXn MyModule
```

  
at the command prompt. The `A` and `X` switches create a vanilla module, not an XS C-extension (don't ask). The `n` switch names your module. The equivalent for `module-starter` requires you to supply a little bit of extra information, which you'll have to edit manually later if you use `h2xs`:  

``` input
module-starter --module MyModule --author="Some One" --email="someone@example.org"
```

  
If all goes well, you will now have a directory called `MyModule` containing the files:  

```text
Changes
Makefile.PL  or  Build.PL
MANIFEST
lib/MyModule.pm
README
t/MyModule.t
```

  
These files will be slightly different if you use `module-starter` but the same main items will be there:  

- `Changes` lists the changes since your previous release, *i.e.* none so far!
- `Makefile.PL` is a script that uses the module `ExtUtils::MakeMaker` to create a makefile suitable for installing your module with the Unix utility `make`. It also details the modules and versions upon which your own module depends in the `PREREQ_PM` hashref. The use of `ExtUtils::MakeMaker` and `make` to install modules is on its way to deprecation: if you are planning on distributing the module, you may want to pass the additional `--builder=Module::Build` switch to `module-starter` to specifies the use of a more modern building system, such as `Module::Build`. This will generate a file called `Build.PL` (rather than `Makefile.PL`) in which prerequisites can be defined using the `requires` hashref.
- `MANIFEST` is a list of the files in the distribution
- `README` explains what the module does
- `t/MyModule.t` is a script using the module Test::More to ensure the module works.

  
The most important part of the module distribution is `MyModule.pm` (`pm` is 'perl module'), which will contain a template something along the lines of:  

```perl
package MyModule;

use 5.012001;
use strict;
use warnings;

require Exporter;
our @ISA         = qw(Exporter);
our %EXPORT_TAGS = ( 'all' => [ qw( ) ] );
our @EXPORT_OK   = ( @{ $EXPORT_TAGS{'all'} } );
our @EXPORT      = qw( );

our $VERSION = '0.01';

# Preloaded methods go here.

1;
__END__

=head1 NAME

MyModule - Perl extension for blah blah blah

=head1 SYNOPSIS

use MyModule;
blah blah blah

=head1 DESCRIPTION

Stub documentation for MyModule, created by h2xs.

=head2 EXPORT

None by default.

=head1 AUTHOR

A. U. Thor, E<lt>a.u.thor@a.galaxy.far.far.awayE<gt>

=head1 SEE ALSO

Mention other useful documentation...

=cut
```

  

## Packages

  
Let's take this a bit at a time:  

```perl
package MyModule;
```

  
The first thing that should be at the top of any module is a `package` statement. A `package` is a name-space, which is a way of letting you use the same names for variables and subroutines in different parts of a program. For example:  

```perl
package Foo;
$e = "hello";
print "In package Foo, \$e is $e\n";

package Bar;
$e = "goodbye";
print "But in package Bar, \$e is $e\n";
print "You can still see \$e in package Foo if you fully qualify it...\n";
print "\$Foo::e is still $Foo::e\n";
```

  

```text
In package Foo, $e is hello
But in package Bar, $e is goodbye
But you can still see $e in package Foo if you fully qualify it...
$Foo::e is still hello
```

  
In the same way that a command shell will assume you mean the `file.ext` in the current working directory, `perl` assumes you mean the variable called `$e` in the current `package`. The reason you've not seen the word `package` at the top of every script so far is that `perl` automatically assumes you are working in `package main;` unless you tell it otherwise explicitly. Think of `main` as your home package. If you want to fiddle with things from other `package`s, you'll need to fully qualify their names with `::` double colons, which are similar to the `/` delimiter in the shell. Think of `package` like `chdir`, and `::` as the `/` path delimiter. So the package variable:  

```perl
$e
```

  
in `package Foo` is called:  

```perl
$Foo::e
```

  
and the subroutine:  

```perl
function()
```

  
in `package Foo::Parp` is called:  

```perl
Foo::Parp::function()
```

  
if you have to fully qualify them. Note in the second case that you can have sub-packages (of a sort - there is no *real *hierarchy here) with more than one `::` double colon. The reason we create modules in new packages is that if we wrote this:  

```perl
# my module
$x = "blah";

# my script
$x = "bobble";
```

  
then when we used the module, our script would overwrite the module's definition of `$x`, because they would share the same namespace. When you create modules, you create a new namespace where you can make and manipulate variables to your heart's content without having to worry about trashing other people's variables and subroutines of the same name in other `package`s. Note that lexical `my` variables don't suffer from this problem, which is another reason to `use strict.`

That's pretty largely all there is to `package`s. You can define several in one file, or spread one over several files, but the 'natural' size of one `package` is one file, *i.e.* if you create a file called `MyModule.pm`, it should generally contain the `package MyModule`.  

## Pragmata

  
The next few lines specify the version of `perl` you're using and turn on some sensible restrictions:  

```perl
use 5.012001;
use strict;
use warnings;
```

  
`use 5.012001;` means '`die` if the version of `perl` you're running is less than 5.012001'. This is particularly important if you're using something new, like `say` or `given/when`, that old versions of `perl` don't support. `use strict; use warnings;` is something you ought to have been doing for a while now. If you hadn't realised, every time you've written `use strict;` or `use ANYTHING;` at the top of a script, you've been using other people's modules. Modules written with lowercase names like `strict` are called *pragmata* or pragma modules: they generally affect how `perl` deals with your script itself, rather than giving you extra functionality.  

## Exporting functions

  
Onward...  

```perl
require Exporter;
```

  
Now we get into the slightly more complex stuff. `Exporter` is simply a module that helps exports symbols, particularly subroutines, from one `package` to another. `require` is very similar to `use` in that it loads in the contents of a module, so that you have access to its functions from your scripts.

A difference between `require` and `use` is that `require` doesn't import any functions into your `package`. If you were writing a script (which by default would define itself in `package main`), and you wanted to use the function `parse()` from `package MyModule`, you have two ways of doing it. You can **`require`**` MyModule;` and then call the function with 'fully qualified' names (the `::` double colon syntax):  

```perl
# we're in package main if we don't say we're not
require MyModule;
my ( @parsed ) = MyModule::parse( @things_to_parse );
```

  
Alternatively, you can **`use`**` MyModule;` which (if suitably set up) will automatically *export* the function `parse()` from `package MyModule` into `package main` (or wherever you're working), so you can use it more easily:  

```perl
# use exports the functions from package MyModule to package main
use MyModule;
my ( @parsed ) = parse( @things_to_parse );
```

  
without any need to fully qualify the function name. When you `require Exporter;` you are asking `perl` to read in the `Exporter` module, but not to import any functions from it. As we don't actually want to import functions from the `Exporter` module, we `require`, not `use` it.

The other thing about `use` its that it does its thing at compile-time, rather than at run-time: this means that when your script is compiled by `perl`, it will check to see if you have all the requisite modules before executing anything, and if you don't have them all, it will `die`. `require` doesn't do this compile-time checking.

`use MyModule;` is exactly equivalent to:  

```perl
BEGIN { require MyModule; import( MyModule ) }
```

  
where `BEGIN{}` is a special block that is automatically called by `perl` when it starts: it makes things happen at the very beginning of compiling a script.

`import()` is just a subroutine in the `MyModule.pm` file that tells `perl` which functions to import into the caller's namespace (*i.e.* the `package`, probably `main`, that the script `use`-ing the module is working in).

Now it's all very well saying `perl` will import functions from one package to another, but where does it 'physically' look for these packages in the first place? When you create a module, you need to save it somewhere it can be found:  

```perl
print "$_\n" foreach @INC;
```

  
will list the places in your computer's file-system that are searched for modules in. `@INC` is therefore rather like the `PATH` environmental variable but for modules. You'll notice that `"."`, the current working directory (CWD), is one of the places on this list. So if you put `MyModule.pm` in your CWD, it will be found and used when a script says `use MyModule;`. What about that `Package::Subpackage` business? If you create a directory called `MyModule` in the CWD (say `D:/flapdoodle/`), then create a file called `Subpackage.pm`, perl would look for the package `MyModule::Subpackage` in `D:/flapdoodle/MyModule/Subpackage.pm`.

Writing a simple module, which contains some utility subroutines that are to be used by several scripts, is simple a matter of writing those subroutines , and then writing *another* subroutine called `import` that exports these functions from one package to another.

The latter is a simple matter of setting a typeglob in the caller's symbol table to a reference to the subroutine you wish to export.

Erm, yeah. Almost no-one rolls their own `import` function. Almost everyone just borrows the one in `Exporter`, which is what:  

```perl
our @ISA = qw( Exporter );
```

  
is for. `@ISA` (that's @rray 'is a') is where you can put the names of modules that you want  `perl` to search in, to find functions *you* can't be bothered to define. So, if you can't be bothered to define `import()` yourself, you can tell  `perl` to look for this function in `Exporter.pm` instead, hence:  

```perl
our @ISA = qw( Exporter );
# MyModule IS A Exporter
# It inherits functions that I can't be bothered to define from Exporter
```

  
So now, when a script `use`-s `MyModule`, it will use the `import()` method from the `Exporter` module to furnish the script with whatever functions you chose to export from `MyModule.pm`.  

## Global variables

  
The final bit to understand here is the `our` which is - as you may have guessed - related to `my`. When you `use strict;` all variables have to be nailed down to a particular lexical scope with `my`, and will disappear from the symbol table, making them inaccessible from other scopes and packages. However, what happens if you do want someone to be able to see the value of a variable in your module? For example, in the module [`File::Find`](lesson09.html#file), the variable `$dir` contains the current directory being processed, which is a useful bit of information for scripts using the module. But if you make `$dir` a lexically scoped `my` variable, it will be invisible outside of the scope in which it is created. For modules, this means *invisible outside of the module itself*.

This is what `our` is for. `our` *explicitly* allows you to share global variables, which is exactly what `strict` doesn't usually allow. `our` allows you to circumvent `strict` for variables you *really do* want to be accessible from anywhere using the `$Package::variable` or `@MyModule::ISA` notation. Since `@ISA` needs to be visible outside the scope in which it is defined (`Exporter` uses it), we must `our` it, not `my` it.  

## Defining an interface

  
That's the worst bit over. The rest of it is just defining the interface:  

```perl
our %EXPORT_TAGS = ( 'all' => [ qw( ) ] );
our @EXPORT_OK   = ( @{ $EXPORT_TAGS{'all'} } );
our @EXPORT      = qw( );
our $VERSION     = '0.01';
```

  
`$VERSION` is obvious. Like `use 5.012001;` you can also `use MyModule 0.02;` This makes your script `die` if the version of `MyModule` you have is older than the version you want to use.

`@EXPORT` is the easiest way of exporting functions. If your module contained three functions `sublime()`, `boil()` and `melt()`, and you wanted to export all of them to the caller's namespace:  

```perl
our @EXPORT = qw( sublime boil melt );
```

  
would do just that. However, people usually prefer to selectively import functions, and the use of `@EXPORT` is discouraged unless your module *is* just one or two functions (like `File::Find` or `File::Path`). This is what `@EXPORT_OK` is for. If you wanted people to be able to import these three functions selectively, you could do this:  

```perl
our @EXPORT_OK = qw( sublime boil melt );
```

  
Then users of your module could:  

```perl
use MyModule "sublime", "boil";  # or
use MyModule qw( sublime boil ); # avoid all those quotes
```

  
if they had no interest in importing the `melt()` function and polluting their namespace.

Finally, `%EXPORT_TAGS` allows you to define groups of functions to export. Say you want people to be able to import your three functions as a lump without having to go to all the trouble of writing three whole things:  

```perl
use MyModule qw( sublime boil melt );
```

  
you can create an export tag called `all`, which contains all three functions. `%EXPORT_TAGS` is just a hash of key/value pairs. The `keys` are the names of the tags you want to define, and the `values` are an arrayref of the functions you want to dump in the tag:  

```perl
our %EXPORT_TAGS = ( 'all' => [ qw( sublime boil melt ) ]   ); # or
our %EXPORT_TAGS = ( 'all' => [ "sublime", "boil", "melt" ] );
```

  
With this defined, you can:  

```perl
use MyModule qw( :all );
```

  
and `Exporter` will conveniently translate the tag `:all` into the list of three functions you have defined with the `all` key in the `%EXPORT_TAGS` hash. If you do define an `:all` tag, which is good practice, you can then use it in `@EXPORT_OK`:  

```perl
our @EXPORT_OK = ( @{ $EXPORT_TAGS{'all'} } );
```

  
Finally, after all the `package`, exportation and global variables nonsense, we finally get onto the non-boilerplate stuff:  

```perl
# Preloaded methods go here.
1;
__END__
```

  
This bit is just a program. Go write it in the space `# Preloaded methods go here`. Mostly, you'll only be defining subroutines here, since these are what you usually want to export. The `1;` is needed because all modules have to return TRUE when they load: this ensures they do. The `__END__` token is a signal to `perl` to stop parsing, since after this comes the documentation for the module, and this is of interest only to `perldoc`, not to `perl` itself.  

## Documentation with POD

  
Talking of which:  

```perl
=head1 NAME

MyModule - Perl extension for blah blah blah

=head1 SYNOPSIS

use MyModule;
blah blah blah

=head1 DESCRIPTION

Stub documentation for MyModule, created by h2xs.

=head2 EXPORT

None by default.

=head1 AUTHOR

A. U. Thor, E<lt>a.u.thor@a.galaxy.far.far.awayE<gt>

=head1 SEE ALSO

Mention other useful documentation...

=cut
```

  
Perl documentation is written in POD (plain old documentation) format, which is a markup language like HTML, but simpler. `perldoc` can read and display the POD embedded in a module, which makes it the perfect tool for documenting your module so you don't forget how it works, and so others can use it without getting up close and personal with the source code. Things starting `=` are processing directives. I think you can guess what `head1` and `head2` do. `=cut` is the signal for the end of the POD. Some other useful directives are:  

```perl
=over 4
```

  
and  

```perl
=back
```

  
`=over` indents the text by some amount (here 4 spaces), and `=back` restores the indent to 0. You'll notice that if you want a newline in your POD, you need a blank line: POD is otherwise newline-insensitive.  

```perl
=item * function()
```

  
is used to create itemised lists, with a pretty `*` as a bullet point. Like HTML, POD uses angle brackets to mark up certain bits of text, but unlike HTML/XML (with its `<open-tag> </close-tag>` syntax), the thing you want to italicise, or whatever, goes inside the brackets:  

```perl
I<text>
```

  
will put `text` in italics. `B<text>` does bold, `C<blah>` does code, `L<foobar>` does links (`L<perl>` links to the perl manpages), and `E<>` does escapes like `E<lt>` and `E<gt>` for `<` and `>`. Documenting your code is essential if you want people to use it: don't fall into the trap of assuming a) everyone's stupid and you're going to let them wallow in it or b) everyone will know how to use your code by osmosing it in. If you have a memory like mine, you won't remember how to use your own scripts in six month's time, so write the documentation now, so you don't have to labouriously re-learn your own code later. The easiest way to learn POD documentation is to use `perldoc` to read some prettily formatted, then look at the module itself to see what it looks like in code.

So, here's the inevitable hello world module. I think this should all be very obvious (`srand` seeds a random number generator, `rand(NUMBER)` generates a random number between 0 and NUMBER, and `||=` is an assignment operator for `||`, which is an idiom for 'default': `A ||= B` is the shorthand for `A = A || B`, which means 'A equals B unless A already equals something other than 0 or `undef`'):  

```perl
package Hello;
use 5.012001;
use strict;
use warnings;
require Exporter;
our @ISA = qw( Exporter );
our @EXPORT = qw( hello ); # no need for :tags, only one function!
our $VERSION = '0.01';
srand;
sub hello {
    my $name = shift;
    $name ||= "you";
    my $message = rand(1) > 0.5 ? "a waste of time" : "a lot of fun";
    return "Hello, $name, isn't this $message?\n";
}
1;
__END__

=head1 NAME

Hello - Perl extension for printing a stupid message      

=head1 SYNOPSIS
  use Hello;
  $msg = hello( "Steve" );
  print $msg;

=head1 DESCRIPTION

Stub documentation for MyModule, created by h2xs. It looks like the author 
of the module took careful note of the importance of documentation, 
and here it is:

=head2 EXPORTED FUNCTIONS

=item * hello( $arg )

=over 4

Randomly prints one of two stupid message for $arg, which should be a name,
but will default to 'you'.

=back

=head1 AUTHOR

Steve Cook

=head1 SEE ALSO

L<perl>.

=cut
```

  
Then all we need to do is save the module in the root of one of the directories in `@INC` (*i.e.* the CWD, or similar) and:  

```perl
#!/usr/bin/perl
use strict;
use warnings;
use Hello;
hello( "Perl novice" );
```

  
Next up...[classes and objects](/2013/02/classes-and-objects/ "Classes and objects")
