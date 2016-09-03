import ink

# A quick example of how to write modifications to a PDF

if __name__ == "__main__":
    # open PDFs
    input_pdf = open('./example.pdf', 'rb')
    output_pdf = open('./example_output.pdf', 'wb')

    # modify PDFs
    ink.fill_pdf(
        input_pdf,
        output_pdf,
        [
            {
                'page': 0,
                # center of page, b/c dimensions of letter paper are 595x842
                'x': 595/2,
                'y': 842/2,
                'value': 'Hello, world!',
                'align': ink.ALIGN.CENTER,
            },
        ],
    )

    # close PDFs
    input_pdf.close()
    output_pdf.close()
