# pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf(text: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    textobject = c.beginText(40, 750)
    textobject.setFont("Helvetica", 12)

    for line in text.split("\n"):
        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
