from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify([i for i in range (100)])

@app.route('/api')
def api_route():
    return render_template('index.html')

@app.route('/api/<year>')
def api_year(year):
    date=dt.datetime(int(year), 1, 1)
    return jsonify([date])

if __name__ == '__main__':
    app.run(debug=True)