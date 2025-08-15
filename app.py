HTML_FORM = """
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>RPM 멀티툴 로그인</title>
  <style>
    body {
      background: #f5f7fa;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .login-container {
      background: #fff;
      padding: 32px 38px 28px 38px;
      border-radius: 10px;
      box-shadow: 0 6px 32px rgba(0,0,0,0.12);
      text-align: center;
      width: 360px;
    }
    .login-title { font-size: 2rem; font-weight:bold; margin-bottom:24px; }
    .login-input {
      font-size: 1.25rem;
      width: 90%;
      margin: 10px 0;
      padding: 12px;
      border-radius: 6px;
      border: 1px solid #BBC4D1;
    }
    .login-btn {
      font-size: 1.3rem;
      padding: 10px 0;
      width: 80%;
      margin: 18px 0 8px 0;
      border: none;
      border-radius:6px;
      background: #3d76e2;
      color:#fff;
      cursor:pointer;
    }
    .pw-toggle {
      font-size:1rem;
      margin-top:-5px;
      margin-bottom:10px;
      background: none;
      border: none;
      color: #3d76e2;
      cursor:pointer;
    }
    ul {color:red; font-size:1rem;}
  </style>
</head>
<body>
  <div class="login-container">
    <div class="login-title">RPM 멀티툴 웹 로그인</div>
    <form method="post">
      <input class="login-input" type="text" name="username" placeholder="RPM ID" required><br>
      <input class="login-input" type="password" name="password" id="pw_input" placeholder="RPM PW" required>
      <br>
      <button type="button" class="pw-toggle" onclick="togglePW()">PW 보기</button><br>
      <input type="submit" class="login-btn" value="로그인">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li><b>{{ message }}</b></li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
  </div>
  <script>
    let pwShown = false;
    function togglePW() {
      var pwInput = document.getElementById('pw_input');
      var btn = document.querySelector('.pw-toggle');
      if (pwInput.type === "password") {
        pwInput.type = "text";
        btn.innerText = "PW 숨기기";
        pwShown = true;
      } else {
        pwInput.type = "password";
        btn.innerText = "PW 보기";
        pwShown = false;
      }
    }
  </script>
</body>
</html>
"""
