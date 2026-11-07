---
title: Formatting data
date: '2014-01-13T14:03:50Z'
lastmod: '2014-01-20T10:14:59Z'
url: /2014/01/r-formatting-data/
slug: r-formatting-data
draft: false
wp_id: 1286
categories:
- R
---

Although you will occasionally type data directly into R, more often than not, you will have a spread-sheet containing data which you want to import. R can easily import data from a **comma-separated variable** (CSV) file. If you open a CSV file using a text-editor, you will see that they look something like this inside (this is [dose_response.csv](/wp-content/uploads/2014/01/dose_response.csv)):  

```r
C,mu
0.125,0.69
0.25,0.68
0.5,0.687
1,0.63
2,0.467
4,0.252
8,0.091
16,0.021
```

  
The first row contains labels for the columns, and the remaining rows contain the data. The pair of labels, and the pairs of data, are each separated by a comma.

R can import CSV files directly using the `read.csv()` function. Functions in R always have their **arguments** (*i.e.* the numbers, vectors, *etc.*, they act upon) enclosed by a pair of **(** **parentheses** **)**. Here we assign the contents of the file to a variable called `dose.response.data`:  

```r
dose.response.data<-read.csv( "H:/dose_response.csv")
print( dose.response.data )
```

  

```text
       C    mu
1  0.125 0.690
2  0.250 0.680
3  0.500 0.687
4  1.000 0.630
5  2.000 0.467
6  4.000 0.252
7  8.000 0.091
8 16.000 0.021
```

  
Note the paired `"` quotes `"` around the file-path: in R, **strings** of characters like this must always be enclosed in quotes.

I will conventionally assume you have created a folder called `R` or similar in your home-directory, in which you save and store all of your R data and scripts:  

```r
dose.response <-read.csv( "H:/R/dose_response.csv")
```

  
R uses the UNIX convention of a forward-slash `/` (rather than the Windows convention of a backwards slash `\`) to navigate down through folders in the file-system.

If for some reason you forget where you have stored a CSV file, you can browse to it by passing the function `file.choose()` to `read.csv()`:  

```r
dose.response <-read.csv( file.choose() )
```

  
N.B. Under Windows, the `.csv` part of the file-name (the file-extension) will usually be 'helpfully' hidden. You can (and *should*) unhide them for all files (in Win7 Explorer: Organize→ Folder and Search Options→View→uncheck 'Hide extensions for known file types').

The `read.csv()` function will import the data from the CSV file into an object called a **data frame**. This contains several named vectors (*i.e.* the columns). Although you will usually import them, you can create data frames manually by grouping vectors together using the `data.frame()` function:  

```r
conc.vector<-c( 0.125, 0.25, 0.5, 1, 2, 4, 8, 16 )
mu.vector<-c( 0.69,0.68,0.687,0.63,0.467,0.252,0.091,0.021)
manual.dose.response <-data.frame( C=conc.vector, mu=mu.vector )
print( manual.dose.response )
```

  
Note the `option.name=option.value` syntax: this is the standard way to pass **named arguments** to an R function.

To create an importable CSV file from your own data in an Excel spread-sheet, you need to:  

- Lay the data out in an otherwise empty workbook. If you are using a European version of Excel, you should change the options to use a full stop as the decimal separator, not a comma (in Excel, press F1 and search for "decimal separator" to find out how to do this).
- Use the top row to give meaningful labels to the columns. Avoid spaces, commas and other punctuation characters in these labels, as these will be used as the column names in R, and these should follow the same conventions as for variables. If you need to use anything other than letters, you can use a full-stop or underscore for clarity *e.g.* `conc.mM` or `mu_perhour`.
- Use "Save As" to save the file as a sensibly named "CSV (Comma delimited) (`*.csv`) file" (I'll assume you're saving to and loading from `H:/R` ).  Don't just call it `data.csv` or you'll rapidly get confused about what "data" it contains! Again, avoid spaces and similar punctuation: you can use a full-stop or an underscore instead.
- A CSV file is a single list of plain-text values, so Excel will probably moan about incompatible things because your spread-sheet may contain multiple worksheets, formulae, bold text, *etc*. It's usually fine to just click 'OK'.
- Close Excel, and you should now be able to import the new CSV file into R directly.
- Once you've imported the data, check the column headings and the data have imported and appear as you expect:

  

```r
names( dose.response.or.whatever.the.data.frame.is.called)
print( dose.response.or.whatever.the.data.frame.is.called)
```

  
In the table below, each row corresponds to a person whose height and mass you have measured. Data of the sort in the table below is [continuous](/2014/01/r-kinds-of-data/ "Kinds of data"): both the height and mass values are numeric, and the values they can take are not restricted to integer values. The correct way to arrange such data in a spread-sheet for import into R is the 'intuitive' way, where each row corresponds to a datum.  

  

  

  

Height / m

  

Mass / kg

  

  

  

1.60

  

65

  

  

  

1.69

  

70

  

  

  

1.54

  

72

  

  

  

1.81

  

85

  

  

  

  
However, the 'intuitive' way of arranging categorical data is generally *not* how R needs it arranged:

*Heights of smokers and non-smokers (m)*  

  

  

  

Smokers

  

Non-smokers

  

  

  

1.60

  

1.61

  

  

  

1.69

  

1.90

  

  

  

1.54

  

1.42

  

  

  

1.81

  

1.55

  

  

  

  
Each row contains data from two different individuals, and there is no particular reason that the smoker who is 1.60 m tall should be paired with the non-smoker who is 1.61 m tall. There's also no particular reason why the columns should be the same length either. This is not an appropriate way to lay out categorised data for import into R. In R, you need to tabulate the data as shown below with **one row for each 'individual' record**. The levels (here, `Y` or `N`, but they could be called `Smoker` and `Non.Smoker` or whatever you prefer) of each factor (just one here: `Smokes`) are listed in the same way as you would if they were continuous data.  

  

  

  

Height

  

Smokes

  

  

  

1.60

  

Y

  

  

  

1.69

  

Y

  

  

  

1.54

  

Y

  

  

  

1.81

  

Y

  

  

  

1.61

  

N

  

  

  

1.90

  

N

  

  

  

1.42

  

N

  

  

  

1.55

  

N

  

  

  

  
The same applies even if the data set is entirely categorical: each row should be an 'individual', not a count. A **contingency table** of count data like this is not generally what you want to import into R:  

  

  

  

  

Male

  

Female

  

Genderqueer

  

  

  

Left-handed

  

1

  

2

  

0

  

  

  

Ambidextrous

  

0

  

1

  

0

  

  

  

Right-handed

  

2

  

3

  

1

  

  

  

  
R can *produce* a contingency table from the raw data (we'll see this later), but if you're importing the raw data, there should be a single row for each 'individual', as shown below:  

  

  

  

Gender

  

Handedness

  

*Height*

  

  

  

Female

  

L

  

…

  

  

  

Female

  

L

  

  

  

  

Female

  

A

  

  

  

  

Female

  

R

  

  

  

  

Female

  

R

  

  

  

  

Female

  

R

  

  

  

  

Genderqueer

  

R

  

  

  

  

Male

  

L

  

  

  

  

Male

  

R

  

  

  

  

Male

  

R

  

  

  

  

  
If you ever get stuck wondering how to format categorical data, imagine that for each 'individual' you have measured, there is an extra item of continuous data to add too (*e.g.* the height of the people in the table above, as shown by the italicised column heading and empty cells). Adding that extra data to the table must be simple matter of pasting it into a new column of the same length, otherwise the format of the table you have produced is wrong.  

## Exercises

  
Perform the following data import in R.  

1.  Edit and save the file [sycamore_seeds.xlsx](/wp-content/uploads/2014/01/sycamore_seeds.xlsx) into a form in R can import (call it `sycamore_seeds.csv`). This shows the length of a sycamore seed's wing compared to the speed with which it descends when dropped. Read the data into R, and check it has imported correctly.
2.  R contains a lot of example data sets, which you can obtain a list of using `data()`. R is also capable of writing CSV files just as easily as it can read them: try `help(write)`. Output the DNAse ELISA assay data to a file called `dnase_elisa.csv`.
3.  Edit and save the file [dog_whelks.xlsx](/wp-content/uploads/2014/01/dog_whelks.xlsx) into a form in R can import (call it `dog_whelks.csv`). The data shows the shell-height of dog-whelks on sheltered *vs*. exposed shores. Read the data into R, and check it has imported correctly.

  

## Answers

  

1.  Your XLSX file should look something like this before you save it as [sycamore_seeds.csv](/wp-content/uploads/2014/01/sycamore_seeds.csv):

  

  

  

  

wing.length

  

descent.speed

  

  

  

25

  

1.38

  

  

  

41

  

0.67

  

  

  

27

  

1.28

  

  

  

35

  

0.95

  

  

  

36

  

1.03

  

  

  

31

  

1.15

  

  

  

34

  

1.02

  

  

  

29

  

1.17

  

  

  

33

  

1.17

  

  

  

  

2.  Save the ELISA data:

  

```r
write.csv( DNase, file="H:/R/dnase_elisa.csv" )
```

  

3.  Your dog whelk XLSX file should look something like this before you save it as [dog_whelks.csv](/wp-content/uploads/2014/01/dog_whelks.csv):

  

  

  

  

Height

  

Exposure

  

  

  

22

  

Sheltered

  

  

  

23

  

Sheltered

  

  

  

26

  

Sheltered

  

  

  

…

  

…

  

  

  

15

  

Exposed

  

  

  

17

  

Exposed

  

  

  

19

  

Exposed

  

  

  

…

  

…

  

  

  

  
Next up... [Plotting data](/2014/01/r-plotting-data/ "Plotting  data").
