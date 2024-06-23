from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from webscraping import perform_web_scraping
from models.modelo import predict_new_entry

app = Flask(__name__, template_folder='.')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-link', methods=['POST'])
def process_link():
    try:
        url = request.form['jobLinkInput']
        data = perform_web_scraping(url)
        
        # Llamar a la función predict_new_entry desde el archivo modelo.py
        prediction = predict_new_entry(data['title'], data['location'], data['company_profile'], data['description'],
                                       data['employment_type'], data['required_experience'], data['function'])
        
        return jsonify({'prediction': prediction})
    
    except Exception as e:
        # Manejar errores y devolver un mensaje de error en JSON
        return jsonify({'error': str(e)}), 500  # Devuelve el error con un código de estado 500

if __name__ == '__main__':
    app.run(debug=True)
