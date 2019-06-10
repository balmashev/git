from flask import json, Flask, request, render_template
from flask.ext.mysql import MySQL
from werkzeug import check_password_hash, generate_password_hash

mysql = MySQL()
app = Flask(__testapp__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwerty123'
app.config['MYSQL_DATABASE_DB'] = 'PortalDB'
app.config['MYSQL_DATABASE_HOST'] = '94.233.224.222'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        # проверка
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Пользователь зарегистрирован!'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Заполните все поля</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __testapp__ == "__main__":
    app.run(port=5002)
