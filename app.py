from flask import Flask, request, jsonify, render_template_string
import time

app = Flask(__name__)

# Lưu giá trị hiện tại (mặc định)
current_value = "00000000"
last_updated = time.strftime("%H:%M:%S")

# Giao diện trang web
HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTTP Transmitter Control</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .card {
            background: #1e293b;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            width: 100%;
            max-width: 420px;
        }
        h1 {
            margin: 0 0 0.5rem 0;
            font-size: 1.5rem;
        }
        .status {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 1.5rem;
        }
        input {
            width: 100%;
            padding: 12px 16px;
            font-size: 1.1rem;
            border: 2px solid #334155;
            border-radius: 10px;
            background: #0f172a;
            color: #f8fafc;
            box-sizing: border-box;
            margin-bottom: 1rem;
        }
        input:focus {
            outline: none;
            border-color: #3b82f6;
        }
        button {
            width: 100%;
            padding: 12px;
            font-size: 1rem;
            font-weight: 600;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #2563eb;
        }
        .current {
            margin-top: 1.5rem;
            padding: 12px;
            background: #0f172a;
            border-radius: 10px;
            font-family: monospace;
            word-break: break-all;
        }
        .success {
            color: #4ade80;
            margin-top: 0.8rem;
            display: none;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>HTTP Transmitter</h1>
        <div class="status">Giá trị sẽ được Build Logic đọc qua GET</div>

        <form id="form">
            <input type="text" id="value" placeholder="Nhập giá trị (ví dụ: 00000000)" 
                   value="{{ value }}" maxlength="64" required>
            <button type="submit">Send</button>
        </form>

        <div class="success" id="success">Đã gửi thành công!</div>

        <div class="current">
            <div style="color:#94a3b8; font-size:0.85rem;">Giá trị hiện tại:</div>
            <div id="display">{{ value }}</div>
            <div style="color:#64748b; font-size:0.8rem; margin-top:6px;">
                Cập nhật lúc: {{ updated }}
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('form');
        const success = document.getElementById('success');
        const display = document.getElementById('display');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const value = document.getElementById('value').value.trim();
            
            const res = await fetch('/set', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({value: value})
            });
            
            if (res.ok) {
                const data = await res.json();
                display.textContent = data.value;
                success.style.display = 'block';
                setTimeout(() => success.style.display = 'none', 2000);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, value=current_value, updated=last_updated)

@app.route('/set', methods=['POST'])
def set_value():
    global current_value, last_updated
    data = request.get_json(silent=True) or {}
    value = str(data.get("value", "")).strip()
    
    if value:
        current_value = value
        last_updated = time.strftime("%H:%M:%S")
    
    return jsonify({"value": current_value, "status": "ok"})

# Endpoint quan trọng cho HTTP Transmitter
@app.route('/get', methods=['GET', 'POST'])
@app.route('/value', methods=['GET', 'POST'])
def get_value():
    # Trả về đúng format mà Build Logic thường đọc
    return jsonify({"value": current_value})

# Endpoint gốc cũng trả về value (tiện lợi)
@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        # Nếu Transmitter gửi POST, có thể xử lý thêm ở đây
        pass
    return jsonify({"value": current_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
