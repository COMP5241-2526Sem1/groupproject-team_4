from app import app

# Vercel需要一个名为'app'的WSGI应用
if __name__ == "__main__":
    app.run()
