from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dữ liệu người dùng lưu tạm
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Tên người dùng đã tồn tại, vui lòng chọn tên khác.', 'danger')
            return redirect(url_for('register'))

        users[username] = generate_password_hash(password)
        flash('Đăng ký thành công! Bạn có thể đăng nhập.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))

        flash('Tên đăng nhập hoặc mật khẩu không chính xác.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    flash('Bạn cần đăng nhập để truy cập trang này.', 'warning')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Đã đăng xuất thành công.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
