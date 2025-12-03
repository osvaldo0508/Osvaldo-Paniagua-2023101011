# ...existing code...
from flask import Flask, render_template, request, redirect, url_for
from db_connection import get_db_connection
import pymysql
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Datos de lotes (informativo; puede reemplazarse por consulta a BD si se desea)
LOTES = [
    {
        "tipo": "Ternero/a",
        "titulo": "Ternero/a (al pie de la madre)",
        "descripcion": "Bovino joven, ideal para recría.",
        "cantidad": 12,
        "precio": "USD 120",
        "imagen": "https://www.google.com/imgres?q=fotos%20de%20ganados%20ternero%20bobina%20joven&imgurl=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F1413061082%2Fes%2Ffoto%2Fretrato-de-un-peque%25C3%25B1o-ternero-en-el-campo-de-hierba.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3DnsP9mlL3XpTHo71Tit1dymWLgP7WMZLAWs7wFqW_Aas%3D&imgrefurl=https%3A%2F%2Fwww.istockphoto.com%2Fes%2Ffotos%2Fternero&docid=yFBmmHWjM4zp5M&tbnid=9TM_kqjZhabm3M&vet=12ahUKEwid_rXkk6CRAxVzErkGHdXBJ7sQM3oECCMQAA..i&w=612&h=408&hcb=2&ved=2ahUKEwid_rXkk6CRAxVzErkGHdXBJ7sQM3oECCMQAA"
    },
    {
        "tipo": "Novilito",
        "titulo": "Novilito (castrado, destete - 2 años)",
        "descripcion": "Animal castrado, buena adaptación y peso.",
        "cantidad": 8,
        "precio": "USD 350",
        "imagen": "https://www.google.com/imgres?q=novillito%20macho&imgurl=https%3A%2F%2Fnews.agrofystatic.com%2Fnovillito_19.jpg%3Fd%3D620x375&imgrefurl=https%3A%2F%2Fnews.agrofy.com.ar%2Fnoticia%2F178726%2Fnovillo-consumo-resiste-ingresos-abultados&docid=VZt7fBSPjV-2NM&tbnid=O6dsx8_ffVTk6M&vet=12ahUKEwia2LvYiqCRAxWwEbkGHcpWKuIQM3oECBYQAA..i&w=620&h=375&hcb=2&ved=2ahUKEwia2LvYiqCRAxWwEbkGHcpWKuIQM3oECBYQAA"
    },
    {
        "tipo": "Novillo",
        "titulo": "Novillo (castrado, >2 años)",
        "descripcion": "Novillo de más de dos años, listo para faena.",
        "cantidad": 5,
        "precio": "USD 480",
        "imagen": "https://www.google.com/imgres?q=novillito%20macho&imgurl=https%3A%2F%2Fnews.agrofystatic.com%2Fnovillito_19.jpg%3Fd%3D620x375&imgrefurl=https%3A%2F%2Fnews.agrofy.com.ar%2Fnoticia%2F178726%2Fnovillo-consumo-resiste-ingresos-abultados&docid=VZt7fBSPjV-2NM&tbnid=O6dsx8_ffVTk6M&vet=12ahUKEwia2LvYiqCRAxWwEbkGHcpWKuIQM3oECBYQAA..i&w=620&h=375&hcb=2&ved=2ahUKEwia2LvYiqCRAxWwEbkGHcpWKuIQM3oECBYQAA"
    },
    {
        "tipo": "Vaquillona",
        "titulo": "Vaquillona (destete - 1ra parición)",
        "descripcion": "Hembra joven, buena genética para reproducción.",
        "cantidad": 10,
        "precio": "USD 420",
        "imagen": "https://www.google.com/imgres?q=vaquillona%20hembra&imgurl=https%3A%2F%2Flookaside.instagram.com%2Fseo%2Fgoogle_widget%2Fcrawler%2F%3Fmedia_id%3D3400000603232167388&imgrefurl=https%3A%2F%2Fwww.instagram.com%2Fp%2FC8vOojfxGXc%2F&docid=1_bVm5QvtH4jPM&tbnid=IGwRgWwyTCgQ9M&vet=12ahUKEwj_5fnAk6CRAxV0ILkGHfGdOawQM3oECBsQAA..i&w=2160&h=1440&hcb=2&ved=2ahUKEwj_5fnAk6CRAxV0ILkGHfGdOawQM3oECBsQAA"
    },
    {
        "tipo": "Vaca",
        "titulo": "Vaca (hembra adulta)",
        "descripcion": "Hembra adulta, puede estar en producción.",
        "cantidad": 7,
        "precio": "USD 600",
        "imagen": "https://www.google.com/imgres?q=vaca%20hembra&imgurl=https%3A%2F%2Ftaxonomiaanimal.wordpress.com%2Fwp-content%2Fuploads%2F2018%2F03%2Fvaca.png&imgrefurl=https%3A%2F%2Ftaxonomiaanimal.wordpress.com%2F2018%2F03%2F28%2Fvaca%2F&docid=sXfMJyNstz3oAM&tbnid=YqrwxnmIH2_1iM&vet=12ahUKEwjznoeEi6CRAxVWHLkGHXc8CisQM3oECBMQAA..i&w=636&h=360&hcb=2&ved=2ahUKEwjznoeEi6CRAxVWHLkGHXc8CisQM3oECBMQAA"
    },
    {
        "tipo": "Toro",
        "titulo": "Toro (macho entero)",
        "descripcion": "Toro entero de alta calidad genética.",
        "cantidad": 3,
        "precio": "USD 1200",
        "imagen": "https://www.google.com/imgres?q=Toromacho%20entero&imgurl=https%3A%2F%2Fstatic7.depositphotos.com%2F1279189%2F757%2Fi%2F450%2Fdepositphotos_7570409-stock-photo-limousine-bull.jpg&imgrefurl=https%3A%2F%2Fdepositphotos.com%2Fes%2Fphotos%2Ftoro-macho.html&docid=Msi_63Xa51keoM&tbnid=sMeEmJBxjBMpPM&vet=12ahUKEwiQ_PeOi6CRAxVoKLkGHeRfDqwQM3oECBMQAA..i&w=600&h=412&hcb=2&ved=2ahUKEwiQ_PeOi6CRAxVoKLkGHeRfDqwQM3oECBMQAA"
    }
]

@app.route('/')
def dashboard():
    mensaje = request.args.get('mensaje')
    return render_template('dashboard.html', lotes=LOTES, mensaje=mensaje)

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    correo = request.form.get('correo', '').strip()
    cel = request.form.get('cel', '').strip()
    horario = request.form.get('horario', '').strip()
    created_at = datetime.utcnow()

    conn = None
    cursor = None
    mensaje = ""

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, apellido, correo, celular, horario, creado_en) VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, apellido, correo, cel, horario, created_at)
        )
        conn.commit()
        mensaje = "Información enviada. Nos pondremos en contacto."
    except Exception as e:
        # Respaldo local si falla la BD
        backup_file = os.path.join(os.path.dirname(__file__), 'contactos_backup.csv')
        header_needed = not os.path.exists(backup_file)
        try:
            with open(backup_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if header_needed:
                    writer.writerow(['nombre','apellido','correo','celular','horario','creado_en'])
                writer.writerow([nombre, apellido, correo, cel, horario, created_at.isoformat()])
            mensaje = "No se pudo conectar a la base de datos. Datos guardados localmente."
        except Exception:
            mensaje = "Error al guardar la información."
    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except Exception:
            pass

    return redirect(url_for('dashboard', mensaje=mensaje))

@app.route('/suscribirse', methods=['GET', 'POST'])
def suscribirse():
    """
    Endpoint añadido para resolver referencias en plantillas.
    POST: recibe 'email' y guarda en archivo de respaldo (o en BD si se desea).
    GET: redirige al dashboard.
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        creado_en = datetime.utcnow().isoformat()
        backup = os.path.join(os.path.dirname(__file__), 'suscripciones_backup.csv')
        header_needed = not os.path.exists(backup)
        try:
            with open(backup, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if header_needed:
                    writer.writerow(['email','creado_en'])
                writer.writerow([email, creado_en])
            mensaje = "Gracias por suscribirte."
        except Exception:
            mensaje = "No se pudo guardar la suscripción. Intente más tarde."
        return redirect(url_for('dashboard', mensaje=mensaje))
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    # Accesible desde cualquier IPv4 del equipo en el puerto estándar de Flask (5000)
    app.run(host='0.0.0.0', port=5000, debug=True)
# ...existing code...