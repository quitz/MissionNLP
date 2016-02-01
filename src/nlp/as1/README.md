**Overview**

There are two problems in this homework. In Problem 1, you will write a program that computes all the anagrams of a word. In Problem 2, you will write a small converter from UTF-16 to UTF-8. This is primarily a chance for you to install and check your setup with the required tools for the class (Python and Vocareum) and make sure you are comfortable with basic programming.

Note: Solutions to Problem 1 can be easily found on the web. You may not consult these solutions (nor solutions to Problem 2). You may however look up general Python documentation.

Problem 1

You will write a Python program which will take a string as the first parameter, and write an output file called anagram_out.txt which contains of all the anagrams (permutations) of the string, one per line, sorted alphabetically. If you use Python 2.7, name your program anagram.py; if you use Python 3.4, name your program anagram3.py. For example, your program will be expected to handle:

> python anagram.py 'ron'

This program will output a file with the following 6 lines, in this order:

nor
nro
onr
orn
rno
ron

You can also test your program by comparing the output on the string ramesh to the test file (anagram_ramesh.txt). The actual test will be done with different strings.

Reading:

The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)
UTF-8, a transformation format of ISO 10646 (You only need to refer to section 3, “UTF-8 definition”).

You will write a Python program which will take a path to an input file (absolute path name) as the first parameter. It will read the file as a binary file, and assume that it contains characters from Unicode's Basic Multilingual Plane (U+0000 to U+FFFF) in UTF-16 encoding (big endian), that is every 2 bytes correspond to one character and directly encode that character's Unicode code point. The program will encode each character in UTF-8 (between 1 and 3 bytes), and write the encoded bytes to a file called utf8encoder_out.txt. If you use Python 2.7, name your program utf8encoder.py; if you use Python 3.4, name your program utf8encoder3.py. For example, your program will be expected to handle:

> python utf8encoder.py /path/to/input

You can test your program by running it on the following input files and comparing the program output to the corresponding output files.

english_in.txt , english_out.txt
arabic_in.txt , arabic_out.txt
gujarati_in.txt , gujarati_out.txt
japanese_in.txt , japanese_out.txt
The actual test will be done with similar files.
