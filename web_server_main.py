import socket
import re
import io
import contextlib
import os
import uuid
import urllib.parse

HOST = input('start host(or 0.0.0.0):') or "0.0.0.0"
PORT = input("server port(or 8080)") or 8080
LOG_FILE="python_server.log"

sessions = {}  # session_id -> data

# 儲存log
#先清空log
with open(LOG_FILE,"w") as create_file:
    create_file.close()
def save_log(content):
    with open(LOG_FILE,"a") as log_file:
        log_file.writelines(content)
        log_file.close()

# 🍪 解析 Cookie
def parse_cookies(request):
    cookies = {}
    lines = request.split("\r\n")
    for line in lines:
        if line.startswith("Cookie:"):
            cookie_line = line.split(":", 1)[1].strip()
            for pair in cookie_line.split(";"):
                if "=" in pair:
                    k, v = pair.strip().split("=", 1)
                    cookies[k] = v
    return cookies


# 🔥 include 功能
def include_file(filename, context):
    try:
        file_path = os.path.normpath(os.getcwd() +'/' + filename)

        if not file_path.startswith(os.getcwd()):
            return "[Forbidden include]"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return render_py_with_context(content, context)

    except Exception as e:
        return f"[Include Error: {e}]"


# 🔥 Template Engine（支援 context + include）
def render_py_with_context(html, context):
    pattern = r"<\?py(.*?)\?>"

    def execute_code(match):
        code = match.group(1).strip()

        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(code, context)
        except Exception as e:
            return f"[ERROR: {e}]"

        return output.getvalue()

    return re.sub(pattern, execute_code, html, flags=re.DOTALL)


def handle_request(client_socket,ip):
    request = client_socket.recv(4096).decode(errors="ignore")
    log=str(ip)+"\n"+request
    save_log(log)

    try:
        # 📌 解析路徑 & GET
        first_line = request.split("\r\n")[0]
        method, full_path, _ = first_line.split()

        parsed_url = urllib.parse.urlparse(full_path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if path == "/":
            path = "/index.py.html"

        # 🍪 Session
        cookies = parse_cookies(request)
        session_id = cookies.get("session_id")

        new_session = False
        if not session_id or session_id not in sessions:
            session_id = str(uuid.uuid4())
            sessions[session_id] = {}
            new_session = True

        session = sessions[session_id]

        # 📁 路徑安全
        file_path = os.path.normpath(os.getcwd() + path)

        if not file_path.startswith(os.getcwd()):
            response = "HTTP/1.1 403 Forbidden\r\n\r\nForbidden"

        elif not os.path.exists(file_path):
            response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"

        else:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 🧠 建立 context（像 PHP request scope）
            context = {
                "session": session,
                "GET": query_params,
            }

            # 🔥 加 include 函數
            context["include"] = lambda filename: print(
                include_file(filename, context)
            )

            # 🔥 執行模板
            content = render_py_with_context(content, context)

            headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n"

            if new_session:
                headers += f"Set-Cookie: session_id={session_id}; Path=/\r\n"

            response = headers + "\r\n" + content

    except Exception as e:
        response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n{e}"

    client_socket.send(response.encode())
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"🔥 Server running at http://{HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            handle_request(client_socket,addr)
    except KeyboardInterrupt:
        print("Web server stop")
        server.close()


if __name__ == "__main__":
    start_server()
