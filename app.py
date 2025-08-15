from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

LOGIN_URL = "https://auth-web.woowa.in/login"  # 실제 로그인 요청 URL
PROTECTED_URL = "http://rpm.woowa.in"          # 로그인 후 접근할 페이지

def login_and_get_session(user_id, user_pw):
    session_requests = requests.Session()
    payload = {
        "username": user_id,
        "password": user_pw,
    }
    response = session_requests.post(LOGIN_URL, data=payload)
    if response.ok and "로그인 후 확인할 특정 키워드" in response.text:
        return session_requests
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('username')
        user_pw = request.form.get('password')
        sess = login_and_get_session(user_id, user_pw)
        if sess:
            session['user'] = user_id
            # requests 세션 객체는 Flask 세션에 저장 불가능하니 별도 처리 필요
            flash("로그인 성공")
            return redirect(url_for('main'))
        else:
            flash("로그인 실패")
    return render_template('login.html')

@app.route('/main')
def main():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
