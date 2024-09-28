import PyPDF2
from docx import Document

def pdf_to_word(pdf_file, word_file):
    # Open the PDF file
    with open(pdf_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Create a new Word document
        doc = Document()
        
        # Loop through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page_num].extract_text()
            
            # Add the text from the PDF page to the Word document
            doc.add_paragraph(text)
        
        # Save the Word document
        doc.save(word_file)

if __name__ == "__main__":
    pdf_file = 'audit.pdf'
    word_file = 'output.docx'
    pdf_to_word(pdf_file, word_file)
    print(f'PDF {pdf_file} has been successfully converted to Word {word_file}')
