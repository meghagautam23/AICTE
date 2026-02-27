import os

from mindease import create_app


app = create_app()


if __name__ == "__main__":
    server_port = int(os.getenv("PORT", "5050"))
    app.run(host="127.0.0.1", port=server_port, debug=True)
