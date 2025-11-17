from flask import send_file
from app import app

@app.route('/preview/short-answer')
def short_answer_preview():
    return send_file('misc/short_answer_preview.html')

if __name__ == '__main__':
    app.run(debug=True)
