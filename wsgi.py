from app import app

# Vercel 需要一个名为 app 的 WSGI 应用对象
if __name__ == "__main__":
    app.run()
