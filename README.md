# Tkinter File Renaming GUI

## Getting Started

Clone the repo and run `Sam's File Renaming GUI.py`


## Workflow
- Paste a folder path or browse to a folder.
- Edit file names manually, or apply global operations to all files.
- When ready, click the 'Rename' button to rename the files.
- Successful renames will be highlighted green, and unsuccessful ones will be colour coded based on the error type.
- Detailed information will be printed to the console.


## Current Global Rename Operations:

Operations are as follows:
- Uppercase
- Lowercase
- Title case
- Sentence case
- TV download fixer (performs numerous operations including find & repace, snipping superfulous information, fixing casing, and regex stuff)
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

### Improved window resizing

This will improve the UX

### Sub folders check box

Allow the choice of whether or not to search in a folder's sub folders
