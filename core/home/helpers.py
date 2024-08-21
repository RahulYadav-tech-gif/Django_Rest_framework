from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
import os
from django.conf import settings

def save_pdf(params: dict):
    template = get_template("pdf.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)

    file_name = f'{uuid.uuid4()}.pdf'
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write the PDF to a file
        with open(file_path, 'wb') as output:
            output.write(response.getvalue())
        
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return '', False

    if pdf.err:
        return '', False

    return file_name, True
