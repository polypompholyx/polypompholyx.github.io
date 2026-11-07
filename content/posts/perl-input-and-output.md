---
title: Input and output
date: '2012-10-03T12:27:14Z'
lastmod: '2013-04-12T09:45:28Z'
url: /2012/10/perl-input-and-output/
slug: perl-input-and-output
draft: false
wp_id: 313
categories:
- Perl
---

## Input

The "[not a hello world script](/2012/10/perl-not-a-hello-world-script/ "Not a hello world script")" script is a little dull. Let's try something a more useful:

```perl
#!/usr/bin/perl
print "What is your name?\n";
$name = <STDIN>;
chomp( $name );
print "$name likes beans.\n";
```

Don't forget the semicolons at the end of each statement.

The first line of this program should be obvious now, but the others may need a little explaining. The second line contains the line-reading operator `< >` and the `STDIN` *filehandle*. `STDIN` (the "standard input filehandle") is automatically opened whenever you run `perl`, and is where things inputted through pressing buttons on the keyboard live. If you surround a filehandle like `STDIN` with the `< >` line reading angle brackets, you will read a line from that filehandle. A line to `perl` is some text followed by a newline character, hence:  

```perl
<STDIN>
```

  
means "read a line from the keyboard". Which it duly does, grabbing `Grumblepuss\n` or suchlike: whatever you type in followed by the enter key (which appends a `\n` newline). The `=` is an assignment operator, and `$name` is the name of a Perl *variable*. Hence,  

```perl
$name = <STDIN>;
```

  
means, "read a line in from the keyboard and store it in the variable `$name`".

If you are from a Java or C background, you may be wondering what the `$` is for, although anyone sufficiently elderly to remember BBC Micro BASIC may feel slightly more at home. The `$` at the front of `$name` means that `$name` is a "scalar" variable (think `$` for `$calar`), *i.e.* a  `$ingle`, flat item of data, *not* a list. Scalar variables are Perl's bread and butter, and they can hold anything: an integer, a floating point number, a string, or even more esoteric things like objects and filehandles.  

## Cleaning up input

  
Next up in our script is our second Perl function ([we've already met `print`](/2012/10/perl-not-a-hello-world-script/ "Not a hello world script")). This goes by the peculiar name of `chomp`:  

```perl
chomp( $name );
```

  
When you read data in from the keyboard, you will have to press the Enter key. In addition to ending your line of input, this will also add a newline character to whatever you just typed. Hence `$name` will actually contain `Grumblepuss\n`,with the newline at the end, not just `Grumblepuss` on its own. The `chomp` function removes the newline from the variable it is given, so after chomping, `$name` will just contain `Grumblepuss`. The parentheses aren't really necessary here: they're just a matter of taste. My personal taste is to leave parentheses off most Perl built-ins, so we'll immediately change that script to...  

```perl
#!/usr/bin/perl
print "What is your name?\n";
$name = <STDIN>;
chomp $name;
print "$name likes beans.\n";
```

  

## Output

  
Finally, the last line  

```perl
print "$name likes beans.\n";
```

  
prints out  

```text
Grumblepuss likes beans
```

  
or similar. Because we have used `" "` double quotes, the contents of variables like `$name` will be *interpolated* into what is output automagically. If you'd used `' '` single quotes on the `print` statement, you'd have got:  

```perl
$name likes beans.\n
```

  
which isn't what we want here. As we saw earlier, double quotes interpolate escape sequences like `\n`; now you have seen that they *also* interpolate the values of scalar variables too. This is extremely useful, and saves you the effort of writing something like:  

```perl
print $name, "likes beans.\n";
```

  
This *would* also work, as `print` will print out a comma-separated list of values just as happily as a single item, but it's rather more effort. Single quotes neither interpolate escapes (except `\\` and `\'`) nor interpolate variables.

Versions of `perl` equal to or higher than 5.10.0 (I'm using 5.16.1 at the instant of writing this) have a new built-in called `say`, which automatically adds a newline to the end of the outputted data:  

```perl
#!/usr/bin/perl
use 5.16.1;
say "We don't need no stinking newlines";
```

  

```text
We don't need no stinking newlines
```

  
The `say` function is not available automatically for backwards-compatibility reasons, but if you include a `use 5.10.0;` line to require a version of `perl` greater than or equal to 5.10.0 then `say` will be made available.

Next up...[arrays and slices](/2012/10/arrays-and-slices/ "Arrays and slices").
