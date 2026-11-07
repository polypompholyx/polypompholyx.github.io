---
title: Command line
date: '2012-10-05T09:24:25Z'
lastmod: '2013-04-12T15:52:23Z'
url: /2012/10/perlcommand-line/
slug: perlcommand-line
draft: false
wp_id: 473
categories:
- Perl
---

## Command line Perl

Despite being a suitable for [large projects](/2013/04/perl-moose-objects-roles/ "Moose objects and roles"), Perl grew out of Unix shell scripting, so it allows you to run it from the command line directly:

``` input
perl -e "print 'Hello'; print 2 + 2;"
```

if you're on Windows, or:

``` input
perl -e 'print q:Hello:; print 2 + 2;'
```

if you're on Unix. The quotes matter. The `-e` is the execute switch, and there are several others:

``` input
perl -v
```

will get you information on the version of `perl` you're running.

``` input
perl -h
```

will tell you all the switches you can use.

``` input
perl -w
```

turns on warnings, (and note that all these switches can also be bunged on the shebang line of a normal script if you'd rather).

``` input
perl -c programfile.pl
```

checks the syntax of a perl script `programfile.pl` without actually executing it.

## Taint

``` input
perl -T
```

turns on taint mode. When running under taint, `perl` will not allow you to do certain unsafe things. In particular, anything entered by users of the script will be considered tainted, and you will not be allowed to use it in potentially dangerous things like:

```perl
system( $x );
```

To untaint data, you need to run any externally sources strings through pattern-match-and-capture, which `perl` assumes you're sensible enough to write so as to preclude the possibility of letting bad things through.

## Loading modules on the command line

``` input
perl -MFile::Find -e "find( sub{ print qq($_\n) if /\.jpg/ }, shift )" D:/pictures
```

The `-M` switch allows you to use a module from the command line, here `File::Find`. This one-liner just prints every JPEG file found in `D:/pictures`.

## Text manipulation from the command line

Here's a little one-liner that prints out the palindromes found in a dictionary file, using the fact that `reverse` will reverse a string in scalar context:

``` input
perl -l -n -e "print if $_ eq reverse" custom.dic
```

This one has two new switches, `-n` and `-l`. The `-n` switch assumes a:

```perl
while ( <> ) { ... }
```

loop around the program. The filehandle-less `<>` diamond operator is a shorthand for opening and reading in every file that follows on the command line, line-by-line. The `-l` switch does line-end processing (*i.e.* `chomp`): it's quite clever, in that it removes trailing newlines from lines read in from these files, but it adds them back on again if you print them. So:

``` input
perl -lne "print if $_ eq reverse" custom.dic
```

is shorthand for something like:

```perl
$\= $/;
for my $file ( @ARGV ) {
    open my $FILE, "<$file";
    while ( defined ( $_ = <$FILE> ) ) {
        chomp;
        print if $_ eq reverse $_;
    }
}
```

Only much more convenient. The first line, `$\= $/;` sets the output record separator `$\` to the input record separator `$/` . You have met the second of these before: it contains the character that `chomp` will remove from strings, and that delimits lines when reading from a `<FILEHANDLE>`. It is ordinarily set to `\n`. The `$\` variable is the mirror image of `$/` : it's what `perl` will append to every call to `print`. It is ordinarily set to `undef`. By setting the output record delimiter to the input record delimiter, our chomped newlines will be re-appended when we print `$_`.

## File manipulation from the command line

Another useful switch is `-i` (also accessible by setting the special variable `$^I`). It does an in-place edit of the files on the command line, so whenever you are thinking "Oh, I want to do *blah* to files foo, bar and baz, but want to back them up first", look no further than:

``` input
perl -i.bak -p -e "blah" foo bar baz
```

The `-i.bak` switch tells `perl` to copy each file it opens to a back-up file with `.bak` appended to it (or whatever you specify). This effects our backing-up. We then use the `-p` and execute switches to manipulate the original files.

The `-p` switch is the same as `-n`, only it `print`s the result of the manipulation at the end. Not only this, but when you are doing in-place editing, it prints the result to a special filehandle called `ARGVOUT`, which is opened for writing on each file on the command-line. Under normal circumstances, a plain `print;` statement will `print STDOUT $_;`, but when you are in-place editing, the `-p` will do an implicit `print ARGVOUT $_;` instead.

So to replace every vowel in a file called `abjadify.txt` with x's, we can use:  

``` input
perl -i.bak -p -e "tr/aeiouAEIOU/xxxxxXXXXX/" abjadify.txt
```

  
Which will back up our original file to `abjadify.txt.bak`, transliterate all the vowels to x's, then write the result to the file, producing something like:  

```text
Xt's qxxtx xxsy tx rxxd x lxngxxgx yxx knxw wxll whxn yxx rxplxcx xll thx vxwxls
wxth x's, xs lxngxxgxs xrx vxry rxdxndxnt xnd thxrx xrx xsxxlly lxts xf clxxs 
tx dxstxngxxsh bxtwxxn wxrds lxkx bxxts xnd bxxts, bxt nxt hxrx xbvxxxsly!
```

  
Next up...[Debugging](/2012/10/perl-debugging/ "Debugging")
