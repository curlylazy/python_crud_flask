from flask import Flask, render_template, json, request, redirect, url_for
import pymysql.cursors, os

app = Flask(__name__)

# mysql = MySQL()

# # MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'db_pyhton'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

conn = cursor = None
#fungsi koneksi database
def openDb():
   global conn, cursor
   conn = pymysql.connect("localhost", "root", "", "db_python", cursorclass=pymysql.cursors.DictCursor )
    # conn = pymysql.connect(
    #     host='localhost',
    #     user='root',
    #     password='',
    #     db='db_python',
    #     charset='utf8mb4',
    #     cursorclass=pymysql.cursors.DictCursor)
   cursor = conn.cursor()

#fungsi untuk menutup koneksi
def closeDb():
   global conn, cursor
   cursor.close()
   conn.close()

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/additem')
def additem():
    return render_template('additem.html')

@app.route('/actadditem', methods=['POST','GET'])
def actadditem():
    try:

        _kodeitem = request.form['kodeitem']
        _namaitem = request.form['namaitem']
        _kategori = request.form['kategori']
        _keterangan = request.form['keterangan']
        _jumlah = request.form['jumlah']

        openDb()
        sql = "INSERT INTO tbl_item (kodeitem, namaitem, jumlah, keterangan, kategori) VALUES (%s, %s, %s, %s, %s)"
        val = (_kodeitem, _namaitem, _jumlah, _keterangan, _kategori)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()

        return json.dumps({'message':'Data berhasil disimpan !'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/listitem')
def listitem():
    openDb()
    sql = "SELECT * FROM tbl_item"
    cursor.execute(sql)
    rows = cursor.fetchall()
    closeDb()
    return render_template('listitem.html', rows=rows)

@app.route('/edititem/<kodeitem>', methods=['GET'])
def edit(kodeitem):
    openDb()
    cursor.execute('SELECT * FROM tbl_item WHERE kodeitem=%s', (kodeitem))
    row = cursor.fetchone()
    closeDb()
    return render_template('edititem.html', row=row)

@app.route('/actedititem', methods=['POST','GET'])
def actedititem():
    try:

        _kodeitem = request.form['kodeitem']
        _namaitem = request.form['namaitem']
        _kategori = request.form['kategori']
        _keterangan = request.form['keterangan']
        _jumlah = request.form['jumlah']

        openDb()
        sql = "UPDATE tbl_item SET namaitem=%s, kategori=%s, keterangan=%s, jumlah=%s WHERE kodeitem=%s"
        val = (_namaitem, _kategori, _keterangan, _jumlah, _kodeitem)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()

        return json.dumps({'message':'Data berhasil diupdate !'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/acthapusitem/<kodeitem>', methods=['GET'])
def acthapusitem(kodeitem):
    openDb()
    cursor.execute('DELETE FROM tbl_item WHERE kodeitem=%s', (kodeitem,))
    conn.commit()
    closeDb()

    return redirect(url_for('listitem'))

if __name__ == "__main__":
    app.run(debug=True)