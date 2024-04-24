from flask import Flask, render_template, request, send_file
import PyPDF2
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(_name_) 

@app.route('/')
def index():
    return 'Hola, mundo!'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Procesar el archivo PDF y obtener la información
            pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
            text = ''
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()

            # Generar el nuevo PDF
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.drawString(100, 750, text)  # Aquí puedes personalizar el contenido del nuevo PDF
            pdf.save()

            buffer.seek(0)
            return send_file(buffer, as_attachment=True, attachment_filename='nuevo_pdf.pdf')
    return render_template('upload.html')

if _name_ == '_main_':
    app.run(debug=True)