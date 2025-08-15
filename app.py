from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_whitelist(filename='whitelist.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()

ALLOWED_IDS = load_whitelist()

LOGIN_PAGE = """
<!doctype html>
<title>RPM 멀티툴 웹 로그인</title>
<style>
body { background: #f5f7fa; height:90vh; display:flex; align-items:center; justify-content:center;}
.container {background: #fff; padding: 32px 38px; border-radius: 10px; text-align: center; box-shadow: 0 6px 32px rgba(0,0,0,0.12); width: 360px;}
input {font-size:1.2rem;margin:8px 0; padding:10px; width:80%; border-radius:5px; border:1px solid #AAA;}
button {font-size:1.2rem;margin:12px 0; padding:10px;width:86%; border-radius:5px;border:none;background:#3d76e2;color:#fff;cursor:pointer;}
.pw-toggle {font-size:1rem;background:none;border:none;color:#357;}
</style>
<div class="container">
  <h2>RPM 멀티툴 웹 로그인</h2>
  <form method="POST">
    <input type="text" name="username" placeholder="RPM ID" required><br>
    <input type="password" name="password" id="pw_input" placeholder="RPM PW" required>
    <br>
    <button type="button" class="pw-toggle" onclick="togglePW()">PW 보기</button><br>
    <button type="submit">로그인</button>
  </form>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul style="color:red;">
      {% for message in messages %}
        <li><b>{{ message }}</b></li>
      {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
</div>
<script>
function togglePW() {
  var pwInput = document.getElementById('pw_input');
  var btn = document.querySelector('.pw-toggle');
  if (pwInput.type === "password") {
    pwInput.type = "text";
    btn.innerText = "PW 숨기기";
  } else {
    pwInput.type = "password";
    btn.innerText = "PW 보기";
  }
}
</script>
"""

MAIN_PAGE = """
<!doctype html>
<title>자동 검토</title>
<style>
body {background:#f5f7fa; height:90vh; display:flex; align-items:center; justify-content:center;}
.box {background:#fff; padding:32px 38px; border-radius:10px; text-align:center; box-shadow:0 6px 32px rgba(0,0,0,0.12); width:420px;}
input, textarea {width:88%; margin:10px 0; font-size:1.1rem; padding:7px;}
button {font-size:1.1rem;margin:15px 0; padding:9px 0;width:90%;border-radius:5px;border:none;background:#3d76e2;color:#fff;}
.result {background:#f8f8ff;padding:15px;border-radius:7px;margin-top:15px;white-space:pre-wrap;font-size:1rem;}
</style>
<div class="box">
  <h2>자동 검토 (Selenium)</h2>
  <form method="POST" action="/run">
    <div>프로모션 ID (여러개면 콤마 또는 줄바꿈)</div>
    <textarea name="promo_ids" rows="4" placeholder="예: 12345,23456"></textarea><br>
    <button type="submit">자동 검토 실행</button>
  </form>
  {% if result %}
  <div class="result">{{ result }}</div>
  {% endif %}
  <div style="margin-top:10px;">
    <a href="/logout">로그아웃</a>
  </div>
</div>
"""

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in ALLOWED_IDS:
            session['user'] = username
            session['pw'] = password
            return redirect(url_for('main'))
        else:
            flash("권한 없음❌ / 담당자에게 권한 요청 필요")
    return render_template_string(LOGIN_PAGE)

@app.route('/main', methods=["GET"])
def main():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template_string(MAIN_PAGE, result=None)

@app.route('/run', methods=["POST"])
def run():
    if not session.get('user'):
        return redirect(url_for('login'))
    promo_ids = request.form.get("promo_ids", "")
    id_list = [x.strip() for x in promo_ids.replace('\n',',').split(',') if x.strip()]
    username = session.get('user')
    password = session.get('pw')
    result_out = ""
    try:
        driver_path = ChromeDriverManager().install()
        opts = webdriver.ChromeOptions()
        opts.page_load_strategy = "eager"
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=opts)
        driver.get("https://auth-web.woowa.in/login?targetUrl=http://rpm.woowa.in")
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "btnSubmit").click()
        WebDriverWait(driver, 7).until(EC.url_contains("rpm.woowa.in"))
        for promo_id in id_list:
            result_out += f"ID: {promo_id} 검토 결과: (여기서 구현)\\n"
        driver.quit()
    except Exception as e:
        result_out += f"작업 중 오류: {str(e)}"
    return render_template_string(MAIN_PAGE, result=result_out)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
