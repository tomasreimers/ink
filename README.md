# Ink

## About

Ink allows people to add strings to PDFs programmatically, for example, when filling out PDF forms.

## Installation

Download the repository, and include ink.py (i.e. 'import ink')

## Usage

Ink exposes one function, fill_pdf, which:

Modifies the PDF of the input stream by inserting the strings in modifications,
and then writes the new PDF out to the output stream

```
input_stream - a stream of the file to modify (i.e. open('./example.pdf', 'r'))
output_stream - a stream to write the file out to (i.e. open('./example_output.pdf', 'w'))
modifications - an array of modifications to make, a modification is a dictionary
                with the following properties:
                    page - index of page to modify
                    x - x coordinate to write string to (from bottom left)
                    y - y coordinate to write string to (from bottom left)
                    value - the string to write
                    [font, default: Helvetica] - which font to use
                    [font_size, default: 20] - which font_size to use
                    [align, default: ALIGN.LEFT] - one of ALIGN.LEFT, .RIGHT, .CENTER, for how to align text
@return - void
```

For an example, see `example.py`.

## Author

(C) Tomas Reimers, 2016

## License

MIT License, also included in license.txt
