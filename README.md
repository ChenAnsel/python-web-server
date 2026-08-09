# Python Web Server

A lightweight Python web server with a built-in Python template engine, inspired by the way PHP can embed server-side code in HTML files.

## ✨ Features

- **Pure Python** — built with Python's standard library; no external web framework is required.
- **HTTP server** — accepts TCP connections and handles basic HTTP requests.
- **Python template execution** — execute Python code inside `<?py ... ?>` blocks in `.py.html` files.
- **Session support** — creates a `session_id` cookie and keeps per-session data in memory.
- **GET parameters** — query-string parameters are available through the `GET` context.
- **Include support** — include another file from a template with `include(...)`.
- **Request logging** — requests are written to `python_server.log`.
- **Path protection** — prevents requested paths and includes from escaping the server's working directory.
- **Simple to learn** — the entire server is contained in `web_server_main.py`.

## 📁 Project Structure

```text
python-web-server/
├── web_server_main.py
├── example file/
│   └── index.py.html
└── README.md
```

## 🧰 Requirements

- Python 3.x
- No third-party Python packages are required.

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/ChenAnsel/python-web-server.git
cd python-web-server
```

Start the server:

```bash
python web_server_main.py
```

The server asks for a host and port when it starts. If you press Enter without entering a value, it uses:

```text
Host: 0.0.0.0
Port: 8080
```

Then open the server address in a web browser.

For local testing, you can use:

```text
http://127.0.0.1:8080/
```

The root path `/` loads `index.py.html`.

## 🧪 Template Syntax

The server recognizes Python blocks in the following form:

```html
<?py
print("Hello World")
?>
```

The Python code is executed on the server and its standard output is inserted into the generated response.

### GET Parameters

Query parameters are available through the `GET` variable:

```html
<?py
print(GET)
?>
```

For example:

```text
http://127.0.0.1:8080/?name=Ansel
```

### Sessions

Session data is available through the `session` variable:

```html
<?py
session["username"] = "Ansel"
print(session["username"])
?>
```

### Include Files

Another template file can be included with:

```html
<?py
include("header.py.html")
?>
```

See the files in `example file/` for a working example.

## ⚠️ Security Notes

This project executes Python code from template files with `exec()`. Template files therefore have the ability to execute Python code with the permissions of the server process.

**Do not use this server to host untrusted templates or expose it to the public Internet without understanding and improving its security model.**

The current implementation includes basic path checks, but it is intended primarily as a learning/experimental project rather than a production-ready web server.

## 📝 Logging

Requests are written to:

```text
python_server.log
```

The log file is recreated when the server starts.

## 🎯 Project Goal

The goal of this project is to experiment with how a small web server and server-side template system can be implemented using Python's standard library.

It is also intended to make Python-based server-side pages feel somewhat similar to PHP-style embedded server code, while keeping the implementation small and easy to inspect.

## 🤝 Contributing

Ideas, bug reports, and improvements are welcome. Fork the repository, make your changes, and open a pull request.

## 📄 License

No license has been specified for this repository yet. If you plan to allow others to freely reuse and modify the code, consider adding an open-source license such as MIT.
