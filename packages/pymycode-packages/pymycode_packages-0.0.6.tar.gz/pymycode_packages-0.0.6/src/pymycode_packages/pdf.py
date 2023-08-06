from PyPDF2 import PdfWriter, PdfReader

def remove_pages(input_file_path, pages*, out_file_path):
    pages_to_keep = pages # page numbering starts from 0
    infile = PdfReader(input_file_path, 'rb')
    output = PdfWriter()

    for i in pages_to_keep:
        p = infile.pages[i] 
        output.add_page(p)

    with open(out_file_path, 'wb') as f:
        output.write(f)
