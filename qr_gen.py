"""QR code generation using the qrcode library."""

import io

import qrcode


def generate_qr(text: str) -> io.BytesIO:
    """Generate a QR code PNG image for *text* and return as a BytesIO buffer."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
