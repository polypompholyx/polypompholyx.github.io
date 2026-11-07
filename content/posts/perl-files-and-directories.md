---
title: Files and directories
date: '2012-10-03T20:34:09Z'
lastmod: '2013-04-12T10:15:28Z'
url: /2012/10/perl-files-and-directories/
slug: perl-files-and-directories
draft: false
wp_id: 401
categories:
- Perl
---

## Reading and writing to files

The [symbol table](/2012/10/perlsymbol-table/ "Symbol table") is a little esoteric, so let's get back to practicalities. How do you mess about with files and directories in Perl? A simple example:

```perl
#!/usr/bin/perl
use strict;
use warnings;

open my $INPUT, "<", "C:/autoexec.bat"
    or die "Can't open C:/autoexec.bat for reading $!\n";

open my $OUTPUT, ">", "C:/copied.bat"
    or die "Can't open C:/copied.bat for writing $!\n";

while ( <$INPUT> ) {
    print "Writing line $_";
    print $OUTPUT "$_";
}
```

Here we open two files, one to read from, one to write to. The `$INPUT` and `$OUTPUT` are *filehandles*, just like `STDIN` was, only we have created these two ourselves with `open`. It's a good idea to give filehandles uppercase names, as these are less likely to conflict with Perl keywords (we don't want to try reading from a filehandle called `print` for example).

Note that it's also possible to write the above in the following way:  

```perl
open INPUT, "C:/autoexec.bat"
    or die "Can't open C:/autoexec.bat for reading $!\n";

open OUTPUT, ">C:/copied.bat"
    or die "Can't open C:/copied.bat for writing $!\n";

while ( <INPUT> ) {
    print "Writing line $_";
    print OUTPUT "$_";
}
```

  

- You *can* miss off the `$` sigil on the filehandles. However, modern Perl usage is to use a lexically scoped filehandle (except for the standard input, output and error handles that are opened automatically for you). You *will* see the old style filehandles in code, but you should avoid them if you are running under `perl` versions \> 5.8, as they rely on global variables, and are subject to the same sort of clobbering that [we saw earlier](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines").
- You *can* miss off the `<` on calls to `open`, and perl will assume you mean 'to read'. However, it's better practice to explicitly state what you mean with the three argument form.
- You *can* combine the read/write/append token into the filename. However, both this and missing out the `<` on opening to read can be the cause of subtle bugs, so you'd be better to avoid them.

  

## `die`

  
The `open` command always needs at least two arguments: a filehandle, an optional read/write/append token, and a string containing the name of a file to open. So the first line:  

```perl
open my $INPUT, "<", "C:/autoexec.bat"
    or die "Can't open C:/autoexec.bat for reading $!\n";
```

  
means '`open` the file `C:/autoexec.bat` for reading, and attach it to filehandle `$INPUT`'. Now, if this works, the `open` function will return TRUE, and the stuff after `or` will never be executed. However, if something *does* go wrong (like the file doesn't exist, as it won't if you're running on Linux or MacOS), the `open` function will return FALSE, and the statement after the `or` *will* be executed.

`die` causes a Perl program to terminate, with the message you give it (think of it as a lethal `print`). When something goes wrong, like problems opening files, the Perl special variable `$!` is set with an error message, which will tell you *what* went wrong. So this `die` tells you what you couldn't do, followed by `$!`, which'll probably contain 'No such file or directory' or similar.

A word of advice before we go any further. On Windows, paths are delimited using the \\ backslash. On Unix and MacOSX, paths are delimited using the / forward-slash. Perl will happily accept either of these when running under Windows, but bear in mind \\ is an escape, so to write it in a string, you'll have to escape it, thusly:  

```perl
$file = "C:/autoexec.bat";
$file = "C:\\autoexec.bat";
```

  
I'd go with the first one in the name of portability and legibility, although if you ever need to call an external program (using `system`, which we'll cover later), you'll probably have to convert the / to \\ with a [regex substitution](/2012/10/perl-substitute-split-join/ "Substitutions, splitting and joining").

The second line:  

```perl
open $OUTPUT, ">", "C:/copied.bat"
    or die "Can't open C:/copied.bat for writing $!\n";
```

  
is very similar to the first, but here we are opening a file for writing. The difference is the `>`:  

```perl
open my $READ, "<C:/autoexec.bat";           # explicit < for reading
open my $READ, "<", "C:/autoexec.bat";       # three argument version is safer
open my $WRITE, ">C:/autoexec.bat";          # open for writing with >
open my $WRITE, ">", "C:/autoexec.bat";      # safer
open my $APPEND, ">>C:/autoexec.bat";        # open for appending with >>
open my $APPEND, ">>", "C:/autoexec.bat";    # safer
open my $READ, "C:/autoexec.bat";            # perl will assume you 'read'
```

  
The `>` means open the file for writing. If you do this *the file will be erased and then written to*. If you *don't* want to wipe the file first, use `>>`, which opens the file for writing, but doesn't clobber the contents first. The three argument versions are generally safer: consider whether you want this to work:  

```perl
chomp( my $file_name = <STDIN> );
    # user types ">important_file"
open my $FILE, $file_name;
    # you assume for reading, but the > that the user enters overrides this. Oops.
```

  

## Reading lines from a file

  
The next bit is easy:  

```perl
while ( <$INPUT> ) {
    print "Writing line $_";
    print $OUTPUT "$_";
}
```

  
Remember [the line reading angle brackets](/2012/10/perl-input-and-output/ "Input and output") `<>` ? As in:  

```perl
chomp ( my $name = <STDIN> );
```

  
This is the same, but here we are reading lines from our own filehandle, `$INPUT`. A line is defined as stuff up to and including a newline character, just as it was when you were reading things from the keyboard (and you also know this is strictly a fib, `<>` and `chomp` deal with lines delimited by whatever is in `$/` currently). Conveniently:  

```perl
while ( <$INPUT> )
```

  
is a shorthand for:  

```perl
while ( defined ( $_ = <$INPUT> ) )
```

  
*i.e.* while there are lines to read, read them into `$_`. The `defined` will eventually return FALSE when it gets to the end of the file (don't test for `eof` explicitly!), and then the `while` loop will terminate. However, while there really *is* stuff to read, the script will `print` to the command line "writing line blah…", then `print` it to the `$OUTPUT` filehandle too using:  

```perl
print $OUTPUT "$_";
```

  
Note that there *is no comma between the filehandle and the thing to print.* A normal `print`:  

```perl
print "Hello\n";
```

  
is actually shorthand for:  

```perl
print STDOUT "Hello\n";
```

  
where `STDOUT` is the standard output (*i.e.* the screen), like `STDIN` was the standard input (*i.e.* the keyboard). To print to a filehandle other than the default `STDOUT`, you need to tell `print` the filehandle name explicitly. If you want to make the filehandle stand out better, you can surround it with braces:  

    print { $OUTPUT } "$_";

  

## Pipes and running external programs with `system`

  
What else can we do with filehandles? As well as opening them to read and write files, we can also open them as *pipes* to external programs, using the `|` symbol, rather than `>` or `<`.  

```perl
open my $PIPE_FROM_ENV, "-|", "env" or die $!;
print "$_\n" while ( <$PIPE_FROM_ENV> );
```

  
This should (as long as your operating system has a program called `env`) print out your environmental variables. The `open` command:  

```perl
open my $PIPE_FROM_ENV, "-|", "env" or die $!;
```

  
means '`open` a filehandle called `PIPE_FROM_ENV`, and attach it to the *output* of the command `env` run from the command line'. You can then read lines from the output of '`env`' using the `<>` as usual.

You can also pipe stuff *into* an external program like this:  

```perl
open my $PIPE_TO_X, "|-", "some_program" or die $!;
print $PIPE_TO_X "Something that means something useful to some_program";
```

  
Note the `or die $!` : it's always important to check the return value of external commands, like `open`, to make sure something funny isn't going on. Get into the habit early: it's surprising how often the file that can't possible be missing actually is…

An even more common way of executing external programs is to use `system`. `system` is useful for running external programs that do something with some data that you have just created, and for running other external programs:  

```perl
system "DIR";
```

  
Will run the program `DIR` from the shell, should it exist. Given it doesn't exist on anything but Windows, there's no point in running it unless the OS is correct. Perl has the OS name (sort of) in a punctuation variable, `$^O`. Try running:  

```perl
print $^O;
```

  

```text
MSWin32
```

  
to find out what `perl` thinks your OS is called.

`system` is a weird command: it generally returns FALSE when it works. Hence:  

```perl
if ( $^O eq "MSWin32") { system "dir" or warn "Couldn't run dir $!\n" }
else                   { print "Not a Windows machine.\n"             }
```

  
will give spurious warnings. Here we have used `warn` instead of `die`: `warn` does largely the same thing as `die`, but doesn't actually `exit`: it just prints a warning. As you may guess from my 'coding' the word `exit`, if you want to kill a `perl` program happily (rather than unhappily, with `die`), use `exit`.  

```perl
print "Message to STDOUT\n";
warn  "Message to STDERR\n";
exit 0;                   # exits program gracefully with return code 0
die "Whinge to STDERR\n"; # exits program with an error message
```

  
What you actually need for `system` is the bizarre:  

```perl
system "dir" and warn "Couldn't run dir $!\n";
```

  
a (historically explicable, but still bizarre) wart.

`perl` opens three filehandles when it starts up: `STDIN`, `STDOUT` and `STDERR`. [You've met the first two already](/2012/10/perl-input-and-output/ "Input and output"). `STDERR` is the filehandle warnings, dyings and other whingings are printed to: it is also connected to the terminal by default, just like `STDOUT`, but is actually a different filehandle:  

```perl
warn "bugger";
```

  
and  

```perl
print STDERR "bugger";
```

  
have largely the same effect. There's no reason why you can't close and re-open a filehandle, even one of the three default ones:  

```perl
#!/usr/bin/perl
use strict;
use warnings;
close STDERR;
open STDERR, ">>errors.log";
warn "You won't see this on the screen, but you'll find it in the error log";
```

  

## Logical operators

  
You have now met two of Perl's logical operators, `or` and `and`. Perl has several others, including `not` and `xor`. It also has a set stolen from C that look like line-noise: `||`, `&&` and `!`, which also mean 'or', 'and' and 'not', but bind more tightly to their operands. Hence:  

```perl
open my $FILE, "<", "C:/file.txt" or die "oops: $!";
```

  
will work fine, because the *precedence* of `or` (and all the wordy logic operators) is *very* low, *i.e.* perl thinks this means:  

```perl
open( my $FILE, "<", "C:/file.txt" ) or die "oops: $!";
```

  
because `or` has an even *lower* precedence than the comma that separates the items of the list. However, `perl` thinks that:  

```perl
open my $FILE, "<", "C:/file.txt" || die "oops: $!";
```

  
means  

```perl
open my $FILE, "<", ( "C:/file.txt" || die "oops" );
```

  
because `||` has a much *higher* precedence than the comma. Since `"C:/file.txt"` is TRUE (it's `defined`, and not the number 0), `perl` will never see '`die "oops"`'. The logical operators like `&&`, `or` and `||` return whatever they last evaluated, here `C:/file.txt`, so `perl` will try and open this file, *but if it doesn't exist, there is nothing more to do and you will get no warning that something has gone wrong*. The upshot: don't use `||` when you should use `or`, or make sure you put in the brackets yourself:  

```perl
open( FILE, "<", "C:/file.txt" ) || die "oops";
```

  
Operator precedence is a little dull, but it is important. If you are worried, bung in parentheses to ensure it does what you mean. Generally `perl` DWIMs (particularly if you're a C programmer), but don't count on it.  

## Backticks

  
One last way of executing things from the shell is to use `` ` ` `` backticks. These work just like the quote operators, and will interpolate variables (as will `system "$blah @args"` for that matter), but they capture the output into a variable:  

```perl
my $output = `ls`;
print $output;
```

  
Like `qq()` and `q()` and `qw()`, there is also a `qx()` (quote execute) operator, which is just like backticks, only you chose your own quotes:  

```perl
my @output = qx:ls:;
```

  

## Directories

  
Handling directories is similar to handling files:  

```perl
opendir my $DIR, ".";
while ( defined( $_ = readdir $DIR ) ) {
    print "$_\n";
}
```

  
The `opendir` command takes a directory handle, and a directory to open, which can be something absolute, like `C:/windows`, or something relative, like `.` the current working directory (CWD) or `../parp` the directory `parp` in the parent directory of the CWD.

Rather than using the `<>` line reader, you must use the command `readdir` to read the contents of a directory. I've used the `defined` explicitly, as you never know what idiot is going to create a file or directory called `0` in the directory you're reading.

When you get to the end of a directory listing using `readdir`, you will need to use `rewinddir` to get back to the beginning, should you need to read the contents in again.

To change the current working directory, you use the command `chdir`.

Here's a program that changes to a new directory, and spews out stuff about the contents to a file called `ls.txt` in the new directory.  

```perl
#!/usr/bin/perl
use strict;
use warnings;

my $dir = shift @ARGV;
chdir $dir or die "Can't change to $dir: $!";
opendir my $DIR, "."
    or die "Can't opendir $dir: $!\n"; # the new CWD, to which we changed
open my $OUTPUT, ">", "ls.txt" or die "Can't open ls.txt for writing: $!";

while ( defined ( $_ = readdir $DIR ) ) {
    if    ( -d $_ ) { print $OUTPUT "directory $_\n" }
    elsif ( -f $_ ) { print $OUTPUT "file $_\n" }
}
close $OUTPUT or die "Can't close ls.txt: $!\n";
    # pedants will want to use an 'or die' here
closedir $DIR or die "Can't closedir $dir: $!";
    # perl will close things itself, but it doesn't hurt to be explicit
```

  
There are a few new things here. `@ARGV` you may recognise from the [symbol table](/2012/10/perlsymbol-table/ "Symbol table") programs. This is another special Perl variable, like `$_` and `$a`. It contains the arguments you passed to the program on the command line. Hence to run this program you will need to type:  

``` input
perl thing.pl d:/some/directory/or/other
```

  
`@ARGV` will contain a list of the single value `d:/some/directory/or/other`, which you can get out using any array operator of your choice. In fact, `pop` and `shift` will automatically assume `@ARGV` in the body of the program, so you could equally well write..  

```perl
my $dir = shift;
```

  
and get the same effect. This should [remind you of subroutines](/2012/10/perl-bondage-discipline-subs/ "Bondage, discipline and subroutines"), the only difference is that array operators default to `@ARGV` in the body, and `@_` in a sub. The V stands for 'vector' if you're interested, it's a hangover from C.  

## File-test operators

  
The rest of the program is self explanatory, except for the `-f` and `-d`. Not too surprisingly, these are 'file test' operators. `-f` tests to see if a file is a file, and `-d` tests to see if a file is a directory. So:  

```perl
-f "C:/autoexec.bat"
```

  
will return TRUE, as will:  

```perl
-d "C:/windows"
```

  
as long as they exist! Perl has a variety of other file test operators, such as `-T`, which tests to see if a file is a plain text file, `-B`, which tests for binary-ness, and `-M`, which returns the age of a file in days at the time the script started. The others can be found using `perldoc`.  

## `perldoc`

  
`perldoc` is perl's own command line manual: if you type:  

``` input
perldoc -f sort
```

  
at the command prompt, `perldoc` will get all the documentation for the function `sort` (the `-f` is a switch for f(unction) documentation), and display it for you. Likewise:  

``` input
perldoc -f -x
```

  
will get you information on file test operators (generically called '`-x`' functions). For really general stuff:  

``` input
perldoc perl
```

  
will get you general information on perl itself, and:  

``` input
perldoc MODULE_NAME
```

  
*e.g.*:  

``` input
perldoc strict
```

  
will extract internal documentation from modules (including *pragma* modules like `strict`) to tell you how to use them. This internal documentation is written in POD (plain old documentation) format, which we'll cover when we get onto writing modules. Lastly:  

``` input
perldoc -h
```

  
or amusingly:  

``` input
perldoc perldoc
```

  
will tell you how to use `perldoc` itself, which contains all the other information for its correct use I can't be bothered to write out here.  

## Files and directories summary

  
A quick summary. Opening files looks like:  

```perl
open my $FILEHANDLE, $RW, $file_to_open; # note the commas
```

  
If `$RW` is "`<`", it'll be opened for reading, if "`>`", for writing, if "`>>`", for appending, if "`-|`", opened as a pipe from an external command called blah, and if "`|-`" as a pipe to an external program.

You should always check return values of `open` to make sure the file exists, with `or die $!` or similar, which prints to the `STDERR` filehandle, as does `warn`. External commands can also be run with `system` (don't forget the counterintuitive '`and die $!`'), backticks, or the `qx()` quotes. Read from files with the `<$FILEHANDLE>` angle brackets, print to them with:  

```perl
print $FILEHANDLE "parp"; # note the lack of comma
```

  
and close them with `close`.

Use `opendir`, `readdir`, `rewinddir`, `chdir` and `closedir` to investigate directories (with `or die` as appropriate), and the file-test operators `-x` to investigate files and directories. And if in doubt, use the `perldoc`.

Next up...[regexes](/2012/10/perl-regexes/ "Regexes").
