from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import ContentStream, NameObject, TextStringObject

wm_text = "Sample"
replace_with = ""

reader = PdfFileReader("/Users/pasha/Downloads/pettersson-rimgard-belinda-proton-coupled-energy.pdf")
writer = PdfFileWriter()

all_ops = set()
for page in reader.pages[:1]:
    print(page.keys())
    content_object = page["/Contents"].getObject()
    content = ContentStream(content_object, reader)
    for operands, operator in content.operations:
        all_ops.add(operator)
        if operator == b'TJ':
            text = operands[0][0]
            if isinstance(text, TextStringObject) and text.startswith('Downloaded'):
                print(text)
print(list(sorted(all_ops)))