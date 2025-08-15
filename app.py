from flask import Flask, render_template, request, redirect, url_for, session, flash
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import gspread

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_whitelist(filename='whitelist.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()

ALLOWED_IDS = load_whitelist()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username in ALLOWED_IDS:
            session['user'] = username
            session['pw'] = password
            return redirect(url_for('main'))
        else:
            flash("권한 없음❌ / 담당자에게 권한 요청 필요")
    return render_template('login.html')

@app.route('/main', methods=['GET'])
def main():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('main.html',
                           checker_result=None,
                           inputter_result=None,
                           segment_result=None)

def create_new_driver():
    driver_path = ChromeDriverManager().install()
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=opts)

@app.route('/run_checker', methods=['POST'])
def run_checker():
    if 'user' not in session:
        return redirect(url_for('login'))
    promo_ids = request.form.get('promo_ids', '')
    id_list = [x.strip() for x in promo_ids.replace('\n', ',').split(',') if x.strip()]
    username = session.get('user')
    password = session.get('pw')
    result_out = ""
    driver = None
    try:
        driver = create_new_driver()
        driver.get("https://auth-web.woowa.in/login?targetUrl=http://rpm.woowa.in")
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "btnSubmit").click()
        WebDriverWait(driver, 7).until(EC.url_contains("rpm.woowa.in"))
        for pid in id_list:
            # 여기에 기존 자동 검토 기능 구현
            result_out += f"ID: {pid} 검토 결과: (여기에 결과 출력)\n"
    except Exception as e:
        result_out += f"오류 발생: {str(e)}"
    finally:
        if driver:
            driver.quit()
    return render_template('main.html',
                           checker_result=result_out,
                           inputter_result=None,
                           segment_result=None)

@app.route('/run_inputter', methods=['POST'])
def run_inputter():
    if 'user' not in session:
        return redirect(url_for('login'))
    mission_ids = request.form.get('mission_ids', '')
    id_list = [x.strip() for x in mission_ids.replace('\n', ',').split(',') if x.strip()]
    username = session.get('user')
    password = session.get('pw')
    result_out = ""
    # 여기에 기존 결과 자동입력 기능 구현
    result_out = "결과 자동입력 기능 실행 완료 (예시)"
    return render_template('main.html',
                           checker_result=None,
                           inputter_result=result_out,
                           segment_result=None)

@app.route('/run_segment_clicker', methods=['POST'])
def run_segment_clicker():
    if 'user' not in session:
        return redirect(url_for('login'))
    segment_ids = request.form.get('segment_ids', '')
    id_list = [x.strip() for x in segment_ids.replace('\n', ',').split(',') if x.strip()]
    username = session.get('user')
    password = session.get('pw')
    result_out = ""
    # 여기에 기존 세그먼트 자동 클릭 기능 구현
    result_out = "세그먼트 자동 클릭 기능 실행 완료 (예시)"
    return render_template('main.html',
                           checker_result=None,
                           inputter_result=None,
                           segment_result=result_out)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
