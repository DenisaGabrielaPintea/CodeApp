from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Calculator Docker</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; margin-top: 50px; background-color: #f0f2f5; }
        .box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { padding: 8px; margin: 5px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 8px 15px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Calculator Flask & Docker</h2>
        <form method="POST">
            <input type="number" step="any" name="n1" placeholder="Număr 1" required>
            <span>+</span>
            <input type="number" step="any" name="n2" placeholder="Număr 2" required>
            <button type="submit">Adună</button>
        </form>
        {% if rezultat is not none %}
            <h3>Rezultat!: {{ rezultat }}</h3>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    suma = None
    if request.method == 'POST':
        try:
            n1 = float(request.form.get('n1', 0))
            n2 = float(request.form.get('n2', 0))
            suma = n1 + n2
        except:
            suma = "Eroare"
    return render_template_string(HTML_TEMPLATE, rezultat=suma)

if __name__ == '__main__':
    # Important pentru Docker: host='0.0.0.0'
    app.run(host='0.0.0.0', port=5050)