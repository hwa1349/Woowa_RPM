from flask import Flask, request, render_template_string, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 보안용 키 반드시 설정하세요

def load_whitelist(filename='whitelist.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

ALLOWED_IDS = load_whitelist()

HTML_FORM = """
<!doctype html>
<title>RPM 멀티툴 로그인</title>
<h2>RPM 멀티툴 웹 로그인</h2>
<form method="post">
  <input type="text" name="username" placeholder="RPM ID" required>
  <input type="password" name="password" placeholder="RPM PW" required>
  <input type="submit" value="로그인">
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
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in ALLOWED_IDS:
            return f"<h3>로그인 성공! 환영합니다, {username} 님</h3>"
        else:
            flash("권한 없음❌ / 담당자에게 권한 요청 필요")
    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
