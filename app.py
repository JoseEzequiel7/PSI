from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/atividade', methods=['GET', 'POST'])
def somar():
    resultado = ''
    if request.method == 'POST':
        num1 = int(request.form['numero1'])
        num2 = int(request.form['numero2'])
        resultado = num1 + num2
    return render_template('form.html', resultado=resultado)

