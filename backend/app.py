from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

model = joblib.load('model_ispa_rf.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        regions = data.get('regions', [])
        
        if not regions:
            return jsonify({'error': 'Data wilayah kosong'}), 400

        features = []
        for r in regions:
            density_val = float(str(r['density']).replace('.', '').replace('/km²', '').strip())
            features.append([
                float(r['aqi']),
                float(r['cases']),
                density_val,
                float(r['humidity'])
            ])

        X_input = np.array(features)

        predictions = model.predict(X_input)
        probabilities = model.predict_proba(X_input)
        classes = list(model.classes_)

        results = []
        for i, r in enumerate(regions):
            pred_label = str(predictions[i])
            
            prob_high = probabilities[i][classes.index('high')] if 'high' in classes else 0.0
            prob_med = probabilities[i][classes.index('medium')] if 'medium' in classes else 0.0
            
            risk_score = int(round((prob_high * 100) + (prob_med * 50)))
            risk_score = max(10, min(risk_score, 99))

            r['level'] = pred_label
            r['riskScore'] = risk_score
            results.append(r)

        return jsonify({'status': 'success', 'data': results})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("Server Model Random Forest ISPA berjalan di http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)