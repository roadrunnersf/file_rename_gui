# Tkinter File Renaming GUI

## Introduction

First, the user pastes in or browses to a folder. The program searches that folder and its child folders for files, and displays the file names as entry boxes in a Tkinter GUI. File names can be edited manually, or operations can be globally performed on them, such as upper case or applying a prefix. Once the files are named to the user's liking, they can be bulk renamed with one click.


## Current Global Rename Operations:

Operations are as follows:
- Uppercase
- Lowercase
- Title case
- Sentence case
- TV download fixer (performs numerous operations including replacing periods with spaces, snipping superfulous information and proper casing.)
- Movie year fixer (adds brackets to a 4 digit year on the end of a file name)
- Snip text before and including input string
- Snip text after and including input string
- Snip x characters from start of name
- Snip x characters from end of name
- Replace x with y
- Prefix
- Suffix

More operations can easily be added to the program by passing in any function that takes a string as its input and returns a string.
Dialog boxes can also be included in the operation with just a few extra lines of code.


## Future Functionality
### Scrolling
The program currently only allows up to 100 files to be displayed at once, as more than this would cause the excess fles to be pushed off the bottom of the screen. Functionality is currently being tested to add a scroll bar to allow more items to be displayed at once.
###Improved window resizing
This will drastically imporove the UX
###Sub folders check box
Allow the choice of whether or not to search in a folder's sub folders
