---
title: Installing modules
date: '2012-10-05T19:35:08Z'
lastmod: '2013-04-12T10:37:20Z'
url: /2012/10/perl-install-modules/
slug: perl-install-modules
draft: false
wp_id: 481
categories:
- Perl
---

## CPAN

With [bits and bobs](/2012/10/perl-bits-and-bobs/ "Bits and bobs"), we've covered much of the core functionality of Perl, but `perl` also comes with dozens of useful modules in its standard distribution. [CPAN](http://www.cpan.org "CPAN") expands this with an enormous wealth of other contributed modules that you can install. There are three ways of doing this:

The most direct method is to go directly to [CPAN](http://search.cpan.org/search?query=parse-recdescent&mode=all "Parse::RecDescent on CPAN"), download the module you want (as a zipped tarball), unzip it and untar it, change directory to the folder you've just unzipped, and build the module with `dmake` or whatever `make` program you have available. So, if we wanted to install the `Parse::RecDescent` module, you'd download the `Parse-RecDescent-1.967009.tar.gz` tarball from CPAN, and then:  

``` input
gzip -d Parse-RecDescent-1.967009.tar.gz
tar -xf Parse-RecDescent-1.967009.tar
cd Parse-RecDescent-1.967009
perl Makefile.pl
dmake
dmake test
dmake install
```

  
However, this relies on a number of Unix utilities that you may not have if you're on Windows (but [can easily obtain](http://sourceforge.net/projects/unxutils/ "UnxUtils at Sourceforge")), and will fail if the module has any dependencies.

The other two ways are much easier. The first is to use the `CPAN.pm` module, which comes with the core `perl` distribution. If you type:  

``` input
perl -MCPAN -e shell
```

  
at a command prompt, it will open a CPAN shell that can install modules for you. Accept the default configuration options. To install a module, all you then need type into the CPAN shell is:  

``` input
install Parse::RecDescent
```

  
and this will be done automatically.

The alternative for those using the ActiveState port of `perl` on Window is to use the Perl package manager, `ppm`. If you type:  

``` input
ppm install Parse-RecDescent
```

  
at a command prompt, `ppm` will do it's best to install the module for you. This technique relies on the fact that someone else has done the equivalent of the the `Makefile.pl/dmake` dance on `Parse::RecDescent` and uploaded the result to the ActiveState `ppm` repository as a file named `Parse-RecDescent.ppd` (note the hyphen replacing the double-colons). YMMV as the coverage of CPAN by the ActiveState repository is not 100%.

Some Perl modules contain extensions written in C (so called XS modules), usually to increase the speed with which they are able to run. When these modules are built with `make`, the C is compiled and linked, for which you need a C compiler. If you *are* on Windows and using the ActiveState distribution, you will find it useful to install the C-compiler `MinGW` so that you can compile such modules. This is a simply matter of typing:  

``` input
ppm install MinGW
```

  
at a command prompt.

Some modules I could not do without...  

## Command line option processing

  
The **`Getopt::Long`** module allows you to easily modify the behaviour of a script according to the switches you pass it:  

```perl
use Getopt::Long;
GetOptions (
    # takes a hash of ( switch => reference in which to put its value ) pairs
    'help' => \ my $help,
        # simple boolean switch, sets $help to 0 or 1 
        # depending on whether the --help switch was present
    'verbose!' => \ my $verbose,
        # the ! indicates that --verbose and --noverbose are both valid switches
    'source=s' => \ my $source,
        # =s indicates that the source option requires
        # a string argument, --source=c:/temp
    'number:i' => \ my $number,
        # :i indicates that the number option
        # takes an optional integer argument, --number=3
);
$number ||= 666;
    # $number  is set to 666 if it's not been set to this by the switches
    # note that this would overwrite a switch of -n 0
$number = 666 unless defined $number;
    # if you would like -n 0 to not be ignored!
```

  
Note the direct use of references to lexically scoped variables (`\ my $var`) to save you having to declare the switch-recording variables before calling `GetOptions()` . Note also the use of `||=` and `unless defined` to default the values of unset switch variables.

You can then run your script with the switches:  

``` input
script.pl --verbose
script.pl --noverbose
script.pl --verbose --source="C:/temp/in.txt" --number=9
script.pl --help
```

  
to enable variations on a theme. You can also get away with shortening these to unambiguous strings, leaving out the equals signs and just using a single dash:  

``` input
script.pl --verbose --number=9 --source="C:/temp/in.txt"
```

  

``` input
script.pl -v -n 9 -s "C:/temp/in.txt"
```

  
`perldoc Getopt::Long` for details.  

## Interacting with databases

  
The **`DBI`** (database interface) module allows you to talk with a database server, like MySQL, Oracle, *etc*. To use it, you `use DBI;` then tell the DBI module which driver (`DBD::` module) you want to use to talk to the database server, *e.g.* `DBD::mysql` for MySQL. Here's a brief foray:  

```perl
use DBI;
my $sql_query_string = 
    "SELECT Genus, Species FROM Plants WHERE Genus = 'Drosera'";
my $dsn = "DBI:mysql:database=plants;host=localhost;port=3306";
    # $dsn contains the configurations for MySQL,
    # such as the server and database to use
my $dbh = DBI->connect( $dsn, "Username", "Password1" )
    or die "Can't connect to server\n";
    # create a database handle and connect it to the database
my $sth = $dbh->prepare( $sql_query_string );
$sth->execute();
while ( my $row = $sth->fetchrow_hashref() ) {
    print "$row\n" ;
}
$dbh->disconnect();
```

  
Again, for more details, `perldoc DBI`.  

## Handling files portably

  
The `File::` modules have various utilities for messing with files. Although Perl has the `rename` command, which can be used to both rename and *move* files about:  

```perl
rename "C:/flunge.log", "D:/piffle.log";
```

  
It *doesn't* have a native copy function (although it's quite easy to roll your own badly):  

```perl
local $/ = undef;          # set the input delimiter to nothing, so...
$whole_file = <$IN>;       # this slurps in the whole file from the IN filehandle
print $OUT $whole_file;    # print it to another filehandle OUT
```

  
`File::Copy` allows you to copy files about with ease and without worry:  

```perl
use File::Copy;
copy( "D:/index.html", "F:/backup/index.html");
```

  
**`File::Find`** allows you to traverse a directory tree recursively, and do stuff to files in it:  

```perl
use File::Find;
find( \&wanted, "D:/perl" );
    # find takes a list of arguments
    # the first is a reference to a subroutine to run each time a file is found
    # the rest are the directories to search, here just one item, D:/steve
sub wanted {
    # the name of the file found is put in $_
    # the current directory path and file is put in $File::Find::name
    if ( /\.(htm|html)$/ ) { print "Found an htmlfile $File::Find::name\n"; }
}
```

  
You'll also want to look in the `File` and `Cwd` namespaces if you ever find yourself wanting to create a temporary file, or concatenate file and directory names in a platform-independent way, or parsing a filename into drive, path and file:  

```perl
use 5.14.1;
use File::Spec;
use Cwd;

my $cwd = getcwd;
    # imported from Cwd
say File::Spec->catfile( $cwd, 'subdirectory', 'filename.log' );
    # catfile concatenates a list of directories and a filename with appropriate / or \\
    # catdir does similar but for a list of directories

my $absolute_path = File::Spec->rel2abs( '..\Python' );
say $absolute_path;

my ($drive, $directories, $file ) =
    File::Spec->splitpath( 'H:\\Perl\\bin\\h2xs.bat' );
say "# $_" for $drive, $directories, $file;
```

  

```text
H:\Perl\subdirectory\filename.log
H:\Python
# H:
# \Perl\bin\
# h2xs.bat
```

  

## Using internet protocols through Perl

  
The **`Net`** modules are Perl implementations of Internet protocols like FTP:  

```perl
use Net::FTP;
my $ftp = Net::FTP->new( "ftp.myhost.com" );
    # connect to server, note this is an OO module
$ftp->login( "Bob", "Password1" );
$ftp->cwd( "/files" );
$ftp->get( "the_one_i_want.txt" );
$ftp->quit();
```

  
Similar implementations of all the other Internet protocols are available, `perldoc Net::`*`blah`* for each's documentation.  

## Manipulating lists

  
**`List::Util`** is a good place to look to avoid wheel reimplementations:  

```perl
use List::Util qw(first max min reduce shuffle sum);
my @list     = ( 1, 32, 8, 4, 16 );
my $max      = max @list;
my $min      = min @list;
my $sum      = sum @list;
my $first    = first { $_ > 10 } @list;
my @shuffled = shuffle @list;
my $product  = reduce { $a * $b } @list;
print <<"__REPORT__";
Max:      $max
Min:      $min
Sum:      $sum
First:    $first
Shuffled: @shuffled
Product:  $product
__REPORT__
```

  

```text
Max:      32
Min:      1
Sum:      61
First:    32
Shuffled: 8 4 32 16 1
Product:  16384
```

  
`reduce` calls the block you pass it repeatedly (much like `sort`), so can be used to perform various map to scalar conversions, although the module already comes with five of the most useful, and **`List::MoreUtils`** has even more.  

## Graphical user interfaces

  
I wouldn't necessarily recommend **`Tk`** these days (I'd probably suggest **`Wx`**, but have not actually used this), but sometimes you want something a little easier on the eye than black box with a prompt in it:  

```perl
use Tk;
my $mw = new MainWindow; # Make a new window
$mw->title( "My first little GUI" );
my $button = $mw->Button(
    # Create a button, configure it with a (-key => value) hash
    -text    => "Hello world",
    -command => sub { exit(0) },
        # the -command key takes a coderef as its value, here to exit
);
$button->pack();
    # The button needs to be packed by the geometry manager into
    # the MainWindow to be visible
MainLoop();
    # Start the main event loop that handles the button clicks, etc.
```

  

## Templating

  
**`HTML::Template`** is useful for creating HTML files from templates (\*surprise\*), but it also useful grounding for other, more complex templating engines. The module allows three main constructs in the HTML template: variables, loops and conditionals, which is about as complex as you can embed into HTML without severely entangling the design with the technology. Here is a simple template for a list of species in a genus of plants:  

```perl
<html>
  <head>
    <title><TMPL_VAR NAME="GENUS"></title>
  </head>
  <body>
    <h1>Genus <TMPL_VAR NAME="GENUS"></h1>
    <p>Species:</p>
    <ul>
      <TMPL_LOOP NAME="SPECIES">
      <li><TMPL_VAR NAME="EPITHET"> <TMPL_VAR NAME="AUTHORITY">
      <TMPL_IF NAME="COMMON_NAME">
        [<TMPL_VAR NAME="COMMON_NAME">]
      </TMPL_IF>
      <TMPL_IF NAME="IUCN"> - IUCN status <TMPL_VAR NAME="IUCN">
        <TMPL_ELSE> - Conservation status unknown
      </TMPL_IF>
      </li>
    </TMPL_LOOP>
    </ul>
  </body>
</html>
```

  
Filling in the template is a straightforward matter:  

```perl
use strict;
use HTML::Template;

my $template = HTML::Template->new( filename => "monograph.html" );
$template->param( GENUS => 'Sarracenia' );
my @species;
while ( <DATA> ) {
    chomp;
    next if /^\s*$/;
    my ( $epithet, $authority, $common_name, $iucn ) = split /\s*:\s*/;
    push @species, {
        EPITHET     => $epithet,
        AUTHORITY   => $authority,
        COMMON_NAME => $common_name,
        IUCN        => $iucn,
    };
}
@species = sort { $a->{'epithet'} cmp $b->{'epithet'} } @species;
$template->param( SPECIES => \@species );
print $template->output;

__DATA__
alata : Alph.Wood : Pale pitcher plant : NT
flava : L. : Yellow pitcher plant : LC
leucophylla : Raf. : White pitcher plant : VU
minor Walt. : Hooded pitcher plant : LC
oreophila : (Kearney) Wherry : Green pitcher plant : CR
psittacina : Michx. : Parrot pitcher plant : LC
purpurea : L. : Purple pitcher plant :
rubra : Walt. : Sweet pitcher plant :
```

  
`HTML::Template` has three important methods. The first is `new()`:  

```perl
my $template = HTML::Template->new( filename => "monograph.html" );
```

  
This creates a templating object which will fill in the gaps in a file called `monograph.html`, which is the HTML-ish file shown above. The second important method is `param()`, which takes a hash of `name => value` pairs:  

```perl
$template->param( TMPL_VARIABLE_NAME => "value to substitute in" );
$template->param( GENUS => 'Sarracenia' );
```

  
Any occurrence of the tag:  

```perl
<TMPL_VAR NAME="GENUS">
```

  
in the template will be replaced with the value `Sarracenia` when you come to use `output`,  

```perl
print $template->output;
```

  

the template object will duly fill in the gap:

``` out
<h1>Genus Sarracenia</h1>
```

The module also allows for conditionals and loops. To create loops, rather than using a simple hash, you use a reference to an array of hashrefs instead:

```perl
my @species;
while ( <DATA> ) {
    my ( $epithet, $authority, $common_name, $iucn ) = split /\s*:\s*/;
    push @species, {
        EPITHET     => $epithet,
        AUTHORITY   => $authority,
        COMMON_NAME => $common_name,
        IUCN        => $iucn,
    };
}
$template->param( SPECIES => \@species );
```

which generates something like this in the output::

```text
<li>alata Alph.Wood [Pale pitcher plant] - IUCN status NT</li>
<li>flava L. [Yellow pitcher plant] - IUCN status LC</li>
<li>...
```

If you pass the `param()` method a `( SPECIES =>\@array_of_hashrefs )` pair, the module will look for a corresponding `<TMPL_LOOP NAME="SPECIES"></TMPL_LOOP>` pair in the template. So in this case, we define an arrayref called `SPECIES`, which contains a number of `{ EPITHET => "flava", AUTHORITY => "L.", `*`etc`*` }` hashrefs in the script. When we send this data to the template, it sets `<TMPL_VAR NAME="EPITHET">` and `<TMPL_VAR NAME="AUTHORITY">` to each of the corresponding values from the loop variable.

You'll also notice that testing for conditionals is just as easy:  

```perl
<TMPL_IF NAME="IUCN">
    IUCN status <TMPL_VAR NAME="IUCN">
<TMPL_ELSE>
    Conservation status unknown
</TMPL_IF>
```

  
We set a parameter in the template object called `IUCN` in the script. In the template, if this is TRUE, then the HTML between the `<TMPL_IF NAME="IUCN"></TMPL_IF>` will be filled in appropriately and outputted. You can also (as we have done here), specify a `<TMPL_ELSE>` within this structure to be filled in and outputted if `IUCN` is FALSE.

I also use **`Win32::OLE`** and **`Parse::RecDescent`** a huge amount, but they will be posts all of their very own.

Next up...[packages and writing modules](/2013/02/perl-packages-module/ "Packages and modules").
