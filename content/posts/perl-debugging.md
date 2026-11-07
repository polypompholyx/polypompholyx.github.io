---
title: Debugging
date: '2012-10-04T15:30:16Z'
lastmod: '2013-04-25T11:49:31Z'
url: /2012/10/perl-debugging/
slug: perl-debugging
draft: false
wp_id: 466
aliases:
- /2012/10/perlesign-and-debugging/
categories:
- Perl
---

## Debuggering

So now you know how Perl works, and how to use it both for scripts and [one-liners](/2012/10/perlcommand-line/ "Command line"). But what do you do when it doesn't? And how do you use it for larger projects?

Perl has [some bugs](https://rt.perl.org/rt3/Public/Search/Simple.html?Query=Queue%20=%20'perl5'%20AND%20(Status%20=%20'open'%20OR%20Status%20=%20'new'%20OR%20Status%20=%20'stalled') "Perl bug tracker") and misfeatures, but it's extremely unlikely that you've found a new one that's not in the docs, so if a program fails to run as you expect, the chances are it's you that's buggered up. How can you find out where you've inserted a problem?  

## Planning

  
The zeroth thing to do is make sure you don't make life difficult for yourself in the first place: plan your code before you start. Work out what you want to do, how you plan to achieve it, and then write bare-bones prototype code:  

```perl
#!/usr/bin/perl
use strict;
use warnings;

my ( $input_file, $output_file ) = @ARGV;
my @fields = parse ( $input_file );
open my $OUTPUT, ">", $output_file or die "Cannot open '$output_file' for writing:$!\n";
foreach ( @fields ) {
    print $OUTPUT "$_\n";
}

sub parse { 
    print "Got to the parser\n";
}
```

  
You can flesh out these bare bones later, testing each new bit of functionality as you go. This is especially useful if you have many largely independent subroutines to write. It's easier to debug code when you know which block the mistake is in.  

## Modularisation

  
If you ever find yourself repeating a piece of code, it's very likely you should be putting it in a subroutine. Which would you rather: debugging one occurrence of a possible bug (and all code is a possible bug), or debugging eighty? The same applies to subroutines themselves. If you ever use a subroutine across more than one script, perhaps you should be putting it in a [module](/2013/02/perl-packages-modules/ "Packages and writing modules").  

## CPAN

  
Don't reinvent the wheel: check out [CPAN](http://www.cpan.org "CPAN") before you write a program that copies files (`File::Copy`), interfaces with a database (`DBI::`), or traverses directory trees (`File::Find`). It's extremely unlikely you will do a better job of hand-rolling of these functions yourself.  

## Style

  
The other important thing is to make your code clean. Check out `perldoc perlstyle`, but - most importantly - be consistent no matter how you choose to write your code. Comment your code with `#comments`, but bear in mind that explaining the bigger picture, weird gotchas, and *why* you are doing things are all much more important than explaining the minutiae of *how*.  

## Documentation

  
Document your code and your API with POD. This will make life easier for anyone using or modifying your code later, which will probably include your own good self at some point. Although TIMTOWTDI, choose the most appropriate way. Which of these would you prefer to debug?  

```perl
(open A,"<$ARGV[0]")||die($!);
($a,$b,$c,$d,$e)=split/\//,<A>;
print "$_\n" for($a,$b,$c,$d,$e);
```

  
or:  

```perl
use strict;
use warnings;
my $input = shift;
open my $INPUT, '<', $input or die "Can't open '$input' for reading: $!\n";
print "$_\n" foreach split m{ / }x, <$INPUT>;
```

  
or:  

```perl
#!/usr/bin/perl
use strict;
use warnings;
use diagnostics;
my $input = shift; 
    # get the input file
open my $INPUT, '<', $input or die "Can't open '$input': $!\n";
    # open the input file
my $line = <$INPUT>; 
    # read a line from the input file
my @records = split m{ / }x, $line; 
    # split the records on colons
foreach my $record ( @records ) { print "$record\n"; }
    # print them out \n delimited
```

  
These all do the same thing: the first is horrible: ugly formatting, leaning toothpicks `/\//`, no `strict`, `$a, $b`…where you really need an array (not to mention that using `$a` and `$b` is a bad idea because of `sort`), a nondescript `A` for a filehandle, `(blah)||` instead of low precedence `blah or`.

The third buries its intent in spurious commentary: it's obvious what it does, but I've used ten lines of wankingly self-indulgent verbosity when the second shows you can do the same thing much more clearly in just three. Well written code shouldn't need many comments: it's obvious already what the third code does without echoing every line in English. Reserve comments for nasty things like regexes, ugly-but-necessary constructs, and commenting the gist of paragraphs of code. Verbosity isn't necessarily a good thing. It's quite obvious what this does (read it backwards from `split` to `foreach`):  

```perl
print "$_\n"
  foreach
    reverse
      sort { lc $a cmp lc $b }
        grep { ! /^#/ }
          split m{ / }x,
            ( "usr/bin/perl/#comment/blah" );
```

  
whereas:  

```perl
my $string   = "usr/bin/perl/#comment/blah";
my @splat    = split m{ / }x, $string;
my @grepped  = grep { ! /^#/ } @splat;
my @sorted   = sort { lc $a cmp lc $b } @grepped;
my @reversed = reverse @sorted;
foreach my $item ( @reversed ) { print "$item\n"; }
```

  
Has rather more chances of bugging up, if only from misspellings.  

## `use strict` and `use warnings`

  
Ensure the first lines of any code you write contain:  

```perl
use strict;
use warnings;
```

  
These will catch some of the commonest mistakes, like trying to write to read-only filehandles, variables you only use once (probably misspellings), and so on. You may also find `use diagnostics;` helpful: it translates warnings into something more descriptive and gives you ideas on how to fix stuff.  

## Check your variables

  
OK, so you've not made life difficult for yourself in the first place. And it's still not working. What next? Well, in general, you will know roughly where the cock up is: it's probably close to the last bit of code you typed (or in a subroutine/modules used by that code you just typed). Sprinkling some `print` statements around liberally in the general area is a dirty but extremely effective way of debugging:  

```perl
my $var = "this";
if ( $var = "that" ) { print "TRUE\n"; }
```

  

```text
TRUE
```

  
Oops. Add `print $suspect_variables`:  

```perl
my $var = "this";
if ( $var = "that" ) { print "$var\n"; print "TRUE\n"; }
```

  

```text
that
TRUE
```

  

## Assignment != equality

  
Ah. We have commited Perl goof number 1: getting `=` (assignment) and `==` (numerical equality) mixed up:  

```perl
$a = 20;
if ( $a = 2 ) { print "TRUE\n"; }
```

  
`$a` is assigned the value `2`, which returns the value 2, which isn't `undef` or `0`, so it's TRUE. D'oh! In a similar vein, don't get `eq` and `==` mixed up, and don't get `=` and `=~` mixed up in regexes.  

## Dump your data

  
Sprinkling about `print` statements may be augmented by the use of any of the following.

For things nastier than a single string, like objects or hashrefs:  

```perl
use Data::Dumper;
print Dumper( \$very_complex_data_structure );
```

  
For redirecting output:  

```perl
open STDOUT, '>', "stdout.txt" or die $!;
open STDERR, '>', "stderr.txt" or die $!;
print "output this";
warn "whinge about this";
```

  
For avoiding `Error 500: You can't write Perl` when playing with CGI applications (if anyone actually does that any more!):  

```perl
use CGI::Carp qw( fatalsToBrowser );
```

  

## \[{("Balance")}\]

  
Besides messing up `=` and `==`, some other frequent cock-ups include...

Messing up pairs and semicolons. It's very easy to lose track of paired things like `{} [] <>` and `()`. Most text editors have a brace-matching function that will help you find missing braces and parentheses. Whether or not you've remembered to put a `;` at the end of every line is also a common source of problems.

Quotes are even better at this; quotes in the general sense of `" "`, `<<"HEREDOC"; HEREDOC\n`, `/ /`, `s##!!` , `qx@@` , and `tr|||` . Don't forget to escape quotes if you have to embed them. Furthermore, be warned: the 'wrong' line may be reported when an uncompilable program complains about things like this:  

```perl
$string = "forgot the quote at the end,;
# so perl thinks the remaining lines are still string
print qq:$_\n: for ( 1.. 10 ) # and forgot the semicolon here too
print " and only now does it realise something bad has happened";
```

  

```text
String found where operator expected at D:\Steve\perl\t.pl line 4, 
    at end of line (Missing semicolon on previous line?)
Can't find string terminator ' " ' anywhere before EOF at D:\Steve\perl\t.pl line 4.
```

  

## Miscellaneous gotchas

  
Arrays and lists index from `0`, not `1`. Don't forget many Perl operators will return different things in list or scalar context too: `splice`, `localtime`, `each` and arrays being common cases in point.

Printing to a closed filehandle is a silent error unless you `use warnings;` and it's very easy to forget the `>` in:  

```perl
open my $FH, '>', $f; # for writing
```

  
As far as modules go, bugs in your own modules are your problem, deal with them in the same way as using a script: write a small script that uses a bit of functionality from the module, and make sure each bit works individually. Other people's modules are usually quite well tested, but beware that some modules don't work on all systems (they'll warn you when you install them), and beware of using old scripts that may use old versions of modules, and *vice versa.*

Exponents are written like Fortran-esque `**`, not like Excel-esque `^`, and are more closely associated than unary minus, hence `-2**2` is `-4`, despite what maths might say about the matter (I have never understood this myself). Precedence issues are also sometimes a problem: if in doubt, add parentheses.  

## RTFM, STFW

  
If all else fails, you still have `perldoc` or the HTML that comes with the ActiveState distribution. The literature that comes with `perl` is extensive to a fault, so use it.  

```perl
perldoc -f function_you_may_be_using_the_wrong_syntax_for
perldoc perltrap
```

  
`perltrap` is the 'Traps for the unwary' documentation: the above are the commonest problems for people such as me who came with no idea about other programming languages. If you are a C programmer or Python hacker, your problems (how do I take an address? What're all these braces for?) your gotchas may be different.

The [perlmonks](http://www.perlmonks.org)' website is lovely: it has a FAQ for common 'how do I do this', a tutorial, and trawling through the archives is a good way of picking up tips. You can also post requests for help, which are almost always answered with grace and helpfulness, but RTFM before you waste someone's time with a spurious question about why this:  

```perl
$a = "foo"; print "TRUE" if $a = "bar";
```

  
doesn't work.  

## Line-noise is a bug not a feature

  
Perl is a language for dirty little hacks, shell scripts and for confusing maintenance staff with all `Th@t_L!Ne_\n0i$e`, or so I'm told. Hopefully, all the nagging about `use strict;` POD, comments, the `/x` modifier for regexes and the importance of modules, classes and debugging means that your dirtier hacks are not something you'd want to release onto the world. Here are some tips that may help if you move from writing little scripts to programming bigger, portable applications. Note that I've only really developed scripts where the customer is me, so I have nothing useful to say about dealing with projects where the biggest problem is working out what the fuck the customer actually wants, rather than how to implement it.

Write the code, the tests and the documentation as you go along, rather than leaving one or other until the end. Without documentation you will end up squandering hours trying to understand the code you yourself wrote not a few months ago. Without tests, you will  end up breaking old features in the same breath as adding new ones.

Keep an eye on the future extensibility and portability of your code. Don't code in obvious portability flaws: `use File::Spec` rather than concatenating together file-paths with backslashes (which won't work under Unix); don't shell out with `system` to call programs that may not exist on another OS (and which you could probably emulate perfectly well using your own code, or someone else's modules) .

Be strict and well-formed in your output, but be forgiving to your input.

If your script has options, give them sensible defaults, and document them.

It's much better to write clean, consistent, nicely formatted scripts that people like using and don't mind maintaining, rather than writing twisty, messy guff that eventually ends up as some unmaintainable but irremovable [ball of mud](http://www.laputan.org/mud/) with a cargo-cult built up around it ("we know it works, we just don't know *how* it works").

Use `$variables_that_mean_something`, don't call everything `$file`, `$variable`, `$thing` and `@data`.

Modularise your code, *i.e.* use loosely coupled modules and classes (do not create [God objects](http://en.wikipedia.org/wiki/God_object "God object at Wikipedia")), avoid global variables, and if there are a load of configurations, put them in a separate file, especially if they are accessed by many scripts, *etc.*  

## Time and memory

  
Even if you don't have a Computing Science degree, don't forget that computing is a form of engineering, and therefore of applied maths. Algorithms have memory and time costs, and algorithms *O(\>N<sup>2</sup>)* do not scale: an algorithm whose time of execution or memory footprint (*O*)  increases more rapidly than the square of the amount of input data (*N*)  is unusable for anything but tiny, trivial cases. The thing to look out for here is embedded loops: if you have anything that looks like:  

```perl
for my $first ( @all_the_data_items ) {
    for my $second ( @all_the_data_items ) {
        print "Match!\n" if $first eq $second;
    }
}
```

  
you are skirting the borders of unusability: for every (`$first`) item in `@all_the_items`, you make a comparison to every (`$second`) item in `@all_the_items`. Hence you will make *N<sup>2</sup>* comparisons, where *N* is `scalar @all_the_items`. Hence, the script's time of execution will increase with the square of *N*. Whatever you do, don't put another loop in the inner loop that goes over all the data, or you'll likely be dead by the time the script has dealt with more than ten thousand items (seriously: if it takes 1 ms to do the innermost loop thing, it will take (10000\*\*3)/(1000\*60\*60\*24\*365) = 32 years). The `Benchmark` module may help you decide on issues of speed and optimisation, but 'make it work, make it right, then make it fast' is a traditional warning against the dangers of premature optimisation.  

## Testing

  
When you create a module `Blah` with [standard tools](/2013/02/perl-packages-modules/ "Packages and writing modules"), it will provide you with a boilerplate test script `Blah.t`. Inside a test script, you can probe outputs for known inputs and check that your module is working correctly. For example, if `Blah` exports a function called `greet`, you might well like to check that:  

```perl
use Test::More tests => 2;
    # Note that you need to tell Test::More how many tests you intend on running
BEGIN { use_ok('Blah') };
    # Checks that the module compiles correctly
ok( greet( "Einstein" ) eq "Hello, Mr. Einstein" );
    # ok checks that the comparison made is TRUE.
```

  
The `ok` function from `Test::More` checks whether the argument it is given is true or not. If you ever have to refactor a module, it's essential to know whether or not your new version behaves in the same way as the previous version. If you write tests that cover the code sufficiently well (checking every branch in the logic), then you will have a much better idea of whether your refactored module will be a drop-in replacement. Even better, you will be told immediately which tests are failing (and hopefully, therefore, where the code is still broken). Computer programs are largely black boxes to their users, and the main thing they are interested in is not the neatness of the box's contents (which they'll never look at), but the fact that no matter what's in the box, when you give it input A, it always produces output B, and not a recipe for cheesecake or a segfault.
