from flask import Flask, render_template, request, send_file
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm

app = Flask(__name__)

W, H = 58*mm, 40*mm

def make_barcode(value):
    cls = barcode.get_barcode_class("code128")
    obj = cls(value, writer=ImageWriter())
    buf = BytesIO()
    obj.write(buf, options={
        "module_width": 0.32,
        "module_height": 14,
        "quiet_zone": 2,
        "font_size": 0,
        "text_distance": 0,
        "write_text": False,
        "dpi": 300,
    })
    buf.seek(0)
    return buf

def make_pdf(values):
    pdf_buf = BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=(W,H))
    for value in values:
        img = make_barcode(value)
        c.drawImage(ImageReader(img), 5*mm, 11*mm, width=48*mm, height=20*mm,
                    preserveAspectRatio=True, anchor='c', mask='auto')
        c.setFont("Helvetica", 10)
        c.drawCentredString(W/2, 6*mm, value)
        c.showPage()
    c.save()
    pdf_buf.seek(0)
    return pdf_buf

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    raw = request.form.get("codes", "")
    values = [x.strip() for x in raw.splitlines() if x.strip()]
    if not values:
        return "Введите хотя бы один номер.", 400
    pdf = make_pdf(values)
    return send_file(pdf, mimetype="application/pdf",
                     as_attachment=True,
                     download_name="barcodes_58x40.pdf")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
