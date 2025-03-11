from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_1234"

# Configuración de la conexión a MySQL
def conectar_bd():
    try:
        # Verifica si está en producción (PythonAnywhere) o en local
        if "PYTHONANYWHERE_DOMAIN" in os.environ:
            conexion = mysql.connector.connect(
                host="MonseLopez216.mysql.pythonanywhere-services.com",  # Servidor de MySQL en PythonAnywhere
                user="MonseLopez216",
                password=os.getenv('DB_PASSWORD', '123456789'),  # Se recomienda definirlo en variables de entorno
                database="MonseLopez216$gestion_empleados"
            )
        else:
            # Configuración para desarrollo local
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456789",
                database="gestion_empleados"
            )

        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return None

# Ruta principal - Listar todos los empleados
@app.route('/')
def index():
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleado")
        empleados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('index.html', empleados=empleados)
    return "Error de conexión a la base de datos"

# Ruta para mostrar el formulario de agregar empleado
@app.route('/agregar', methods=['GET'])
def mostrar_agregar():
    return render_template('agregar.html')

# Ruta para procesar el formulario de agregar empleado
@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        puesto = request.form['puesto']
        salario = request.form['salario']
        
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            sql = "INSERT INTO empleado (nombre, apellido, email, puesto, salario) VALUES (%s, %s, %s, %s, %s)"
            datos = (nombre, apellido, email, puesto, salario)
            cursor.execute(sql, datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            flash("Empleado agregado correctamente")
            return redirect(url_for('index'))
    return "Error al agregar empleado"

# Ruta para mostrar el formulario de editar empleado
@app.route('/editar/<int:id>', methods=['GET'])
def mostrar_editar(id):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleado WHERE id = %s", (id,))
        empleado = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if empleado:
            return render_template('editar.html', empleado=empleado)
        else:
            flash("Empleado no encontrado", "error")
            return redirect(url_for('index'))
    
    flash("Error de conexión a la base de datos", "error")
    return redirect(url_for('index'))

# Ruta para procesar el formulario de editar empleado
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        puesto = request.form['puesto']
        salario = request.form['salario']
        
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            sql = "UPDATE empleado SET nombre = %s, apellido = %s, email = %s, puesto = %s, salario = %s WHERE id = %s"
            datos = (nombre, apellido, email, puesto, salario, id)
            cursor.execute(sql, datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            flash("Empleado actualizado correctamente")
            return redirect(url_for('index'))
    return "Error al actualizar empleado"

# Ruta para eliminar empleado
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM empleado WHERE id = %s", (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("Empleado eliminado correctamente")
        return redirect(url_for('index'))
    return "Error al eliminar empleado"

if __name__ == '__main__':
    app.run(debug=True)
