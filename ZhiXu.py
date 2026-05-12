from flask import Flask,request,redirect,session,send_from_directory,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from flask_cors import CORS # 解决跨域问题
# redirect 重定向 页面跳转
# session 保持登录


import pymysql

app = Flask(__name__)
app.secret_key = '999999999'

CORS(app, supports_credentials=True)


def get_db():
    return pymysql.connect(
        host = '127.0.0.1',
        port= 3306,
        user = 'root',
        password = '123456',
        db = 'user_system',
        charset = 'utf8mb4'
    )

@app.route('/')
def home():
    if 'user'  in session and session['user'] is not None:
        return redirect('/index2') # 跳路由而非直接跳HTML文件
    else: # 未登录
        return redirect('enter.html')  # 跳登录页

# 首页
@app.route('/index2')
def index2():
    # 未登录强制跳登录页
    if 'user' not in session or session['user'] is None:
        return redirect('enter.html')
    # 已登录返回index2.html
    return send_from_directory(directory='.', path='index2.html')

# 登录处理
@app.route('/login', methods=['POST'])
def login():
    # 先清空旧的session，避免残留导致误判
    session.clear()

    if not request.is_json:
        return 'failed'

    data = request.get_json() or {}  # 非JSON请求直接返回空字典
    username = data.get('username', '').strip()  # 强制去空格
    password = data.get('password', '').strip()

    if username == '' or password == '':
        return 'failed'

    user_pwd = None

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT password FROM users WHERE username=%s', (username,))
        result = cursor.fetchone()  # 未查询到则返回None
        if result and len(result) > 0:
            user_pwd = result[0]  # 只赋值有效密码
        db.close()
    except Exception as e:
        print(f"数据库查询错误：{e}")
        return 'failed'

    login_success = False
    if user_pwd and check_password_hash(user_pwd, password):
        session['user'] = username
        login_success = True

        # 任何不满足的情况都返回失败
    return 'success' if login_success else 'failed'

# 注册处理
@app.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm = request.form.get('confirm')
    if password != confirm:
        print('注册失败，两次输入的密码不一致')
        return 'failed'
    db = get_db()
    cursor = db.cursor()
    try:
        # 检查用户名是否重复
        cursor.execute('SELECT*FROM users WHERE username=%s',(username,))
        if cursor.fetchone():
            print('注册失败，用户名已存在')
            return 'failed'
        # 密码加密
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users(username,password) VALUES(%s,%s)', (username, hashed_password))
        db.commit()
        print(f'注册成功，用户名{ username}')
        return 'success'
    except Exception as e:
        print(f"注册失败，数据库错误：{e}")
        db.rollback()
        return 'failed'
    finally:
        db.close()

# 登出
@app.route('/logout')
def logout():
    session.clear()
    return redirect('enter.html')

# 静态文件处理 拦截index2.html的逻辑
@app.route('/<path:path>')
def static_file(path):
    # 禁止直接访问index2.html，强制走/login校验的路由
    if path == 'index2.html':
        return redirect('/index2')
    return send_from_directory(directory='.',path=path)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7777)

