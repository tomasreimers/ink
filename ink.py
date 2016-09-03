from enum import Enum
from PyPDF2 import PdfFileWriter, PdfFileReader
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as canvas_lib
import StringIO

DEFAULT_FONT = 'Helvetica'
DEFAULT_FONT_SIZE = 20

class ALIGN(Enum):
    LEFT = 'drawString'
    CENTER = 'drawCentredString'
    RIGHT = 'drawRightString'

# Modifies the PDF of the input stream by inserting the strings in modifications,
# and then writes the new PDF out to the output stream
#
# input_stream - a stream of the file to modify (i.e. open('./example.pdf', 'r'))
# output_stream - a stream to write the file out to (i.e. open('./example_output.pdf', 'w'))
# modifications - an array of modifications to make, a modification is a dictionary
#                 with the following properties:
#                     page - index of page to modify
#                     x - x coordinate to write string to (from bottom left)
#                     y - y coordinate to write string to (from bottom left)
#                     value - the string to write
#                     [font, default: Helvetica] - which font to use
#                     [font_size, default: 20] - which font_size to use
#                     [align, default: ALIGN.LEFT] - one of ALIGN.LEFT, .RIGHT, .CENTER, for how to align text
#
# @return - void

def fill_pdf(input_stream, output_stream, modifications):
        # open file handles
        to_close = []
        input_pdf = PdfFileReader(input_stream)
        output_pdf = PdfFileWriter()

        # iterate over pages
        for page_idx in range(input_pdf.getNumPages()):
            # get page dimensions
            page = input_pdf.getPage(page_idx)
            assert page.trimBox.lowerLeft == (0, 0), "trimbox not anchored at origin"
            (width, height) = page.trimBox.upperRight

            # create a input page
            new_buf = StringIO.StringIO()
            canvas = canvas_lib.Canvas(
                new_buf,
                pagesize=(width, height),
            )

            # make any modifications
            edits = False
            for modification in modifications:
                if modification['page'] == page_idx:
                    canvas.setFont(
                        modification.get('font', DEFAULT_FONT),
                        modification.get('font_size', DEFAULT_FONT_SIZE)
                    )
                    getattr(canvas, modification.get('align', ALIGN.LEFT))(
                        modification['x'],
                        modification['y'],
                        modification['value'],
                    )
                    edits = True
            canvas.save()

            # merge into original page
            new_pdf = PdfFileReader(
                new_buf
            )
            if edits:
                page.mergePage(new_pdf.getPage(0))
            output_pdf.addPage(page)

            # cannot close until we've written out the output PDF
            to_close.append(new_buf)

        # finally, write "output" to a real file
        output_pdf.write(output_stream)

        for to_close_file in to_close:
            to_close_file.close()
