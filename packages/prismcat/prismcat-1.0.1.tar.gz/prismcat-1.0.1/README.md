# PrismCat

## Explanation
PrismCat reads a file (or stdin) and highlights lines based on regex supplied in arguments. 

Colors follow the rainbow in priority e.g. (Error)>Red>Yellow>Green>Blue>Purple and are specified as arguments with their initial letter: -e -r -y -g -b -p, each taking a quoted regular expression as input. 

PrismCat can output to stdin, or to an html file (using the -o option) for future reference retaining the coloring. 

the -a flag eliminates all lines that aren't currently highlighted, filtering output to only the important lines. 

## Future
Eventually, PrismCat should be a full drop-in replacement for cat with the additional features provided in the current version