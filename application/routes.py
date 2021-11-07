from flask import render_template, redirect, url_for, request, flash, session
from application import app
from flask_mysqldb import MySQL
import MySQLdb
import os


app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASS")
app.config['MYSQL_DB'] = os.getenv("DB_NAME")
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM testimoni")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',testimoni=data)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checklogin', methods=['POST'])
def checklogin():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
 
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session["username"] = request.form.get("username")
            return redirect(url_for('dashboard'))
        else:

            return 'Incorrect username/password!'

@app.route('/logout')
def logout():
    session["username"] = None
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM kontak_pesan")
    data = cur.fetchall()
    cur.close()
    return render_template('dashboard.html',kontak_pesan=data)

@app.route('/kirim_pesan',methods=["POST"])
def kirim_pesan():
    nama = request.form['nama']
    email = request.form['email']
    pesan = request.form['pesan']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO kontak_pesan (nama,email,pesan) VALUES (%s,%s,%s)",(nama,email,pesan))
    mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/hapus_pesan/<string:id_data>', methods=["GET"])
def hapus_pesan(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM kontak_pesan WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('dashboard'))


#  CRUD

@app.route('/testimoni')
def testimoni():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM testimoni")
    data = cur.fetchall()
    cur.close()
    return render_template('testimoni.html',testimoni=data)

@app.route('/simpan',methods=["POST"])
def simpan():
    nama = request.form['nama']
    pesan = request.form['pesan']
    pekerjaan = request.form['pekerjaan']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO testimoni (nama,pesan,pekerjaan) VALUES (%s,%s,%s)",(nama,pesan,pekerjaan))
    mysql.connection.commit()
    return redirect(url_for('testimoni'))


@app.route('/update', methods=["POST"])
def update():
    id_data = request.form['id']
    nama = request.form['nama']
    pesan = request.form['pesan']
    pekerjaan = request.form['pekerjaan']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE testimoni SET nama=%s,pesan=%s,pekerjaan=%s WHERE id=%s", (nama,pesan,pekerjaan,id_data,))
    mysql.connection.commit()
    return redirect(url_for('testimoni'))

@app.route('/hapus_testimoni/<string:id_data>', methods=["GET"])
def hapus_testimoni(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM testimoni WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('testimoni'))



