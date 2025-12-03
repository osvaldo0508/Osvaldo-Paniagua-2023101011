# Comercial Ganadera - Página Web de Venta Informativa

Página web desarrollada en Flask para una empresa que vende ganados bovinos. Muestra lotes de animales con información detallada y permite a los clientes solicitar más información mediante un formulario.

## Características

- Dashboard con 6 tipos de ganado (Ternero/a, Novilito, Novillo, Vaquillona, Vaca, Toro)
- Formulario de contacto que guarda datos en MySQL
- Respaldo automático en CSV si la BD no está disponible
- Accesible desde cualquier IPv4 del equipo en puerto 5000
- Diseño responsive con CSS
- Base de datos MySQL con script de creación

## Requisitos Previos

- Python 3.7 o superior
- MySQL Server instalado y ejecutándose
- Git (opcional)

## Instalación

### 1. Descargar o clonar el repositorio

```bash
git clone https://github.com/osvaldo0508/Osvaldo-Paniagua-2023101011.git
cd "Ejercicio 2"
```

### 2. Crear la base de datos MySQL

Abre PowerShell o cmd y ejecuta:

```bash
mysql -u root -p < create_db.sql
```

Si no tienes contraseña:

```bash
mysql -u root < create_db.sql
```

### 3. Instalar dependencias Python

```bash
pip install flask pymysql
```

### 4. Configurar variables de entorno (Opcional)

Si tu MySQL tiene usuario/contraseña diferentes, edita `db_connection.py` o configura en PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("DB_USER", "tu_usuario", "User")
[Environment]::SetEnvironmentVariable("DB_PASS", "tu_contraseña", "User")
```

## Ejecución

Desde la carpeta del proyecto:

```bash
python app.py
```

Luego abre en tu navegador:

- Desde el mismo equipo: http://localhost:5000
- Desde otro equipo: http://<IP_DE_TU_EQUIPO>:5000

Para obtener tu IP, ejecuta en PowerShell:

```bash
ipconfig
```

Busca "IPv4 Address" (ej: 192.168.1.100)

## Estructura del Proyecto

```
Ejercicio 2/
├── app.py                    # Aplicación Flask
├── db_connection.py          # Conexión a MySQL
├── create_db.sql             # Script para crear BD
├── contactos_backup.csv      # Respaldo de contactos (generado)
├── templates/
│   └── dashboard.html        # Página principal
├── static/
│   └── css/
│       └── style.css         # Estilos
└── README.md                 # Este archivo
```

## Base de Datos

Tabla: contactos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | ID único |
| nombre | VARCHAR(100) | Nombre del cliente |
| apellido | VARCHAR(100) | Apellido |
| correo | VARCHAR(150) | Email |
| celular | VARCHAR(50) | Celular |
| horario | VARCHAR(100) | Horario preferido |
| creado_en | DATETIME | Fecha de registro |

## Uso

1. Abre el navegador en http://localhost:5000
2. Visualiza los lotes de ganado disponibles
3. Haz clic en "Pedir más info" en cualquier lote
4. Completa el formulario con: nombre, apellido, correo, celular y horario
5. Envía el formulario
6. Los datos se guardan en MySQL (o en contactos_backup.csv si la BD no responde)

## Solución de Problemas

**Error: "No module named 'flask'"**

```bash
pip install flask
```

**Error: "No module named 'pymysql'"**

```bash
pip install pymysql
```

**Error: "Access denied for user 'root'"**

Verifica que MySQL esté ejecutándose y ajusta usuario/contraseña en `db_connection.py`.

**Error: "Table 'ganados_db.contactos' doesn't exist"**

Ejecuta nuevamente:

```bash
mysql -u root -p < create_db.sql
```

**El formulario no guarda datos**

- Verifica que MySQL esté corriendo: `mysql -u root -p -e "SELECT 1;"`
- Revisa que se cree automáticamente `contactos_backup.csv` como respaldo

## Subir a GitHub

```bash
git add .
git commit -m "Comercial Ganadera - Página Web"
git push origin main
```

## Notas

- No se envían notificaciones aún, solo se guardan los datos
- La página es informativa, no realiza compras
- Las imágenes se cargan desde Unsplash (requiere internet)

## Autor

Osvaldo Paniagua - 2023101011
