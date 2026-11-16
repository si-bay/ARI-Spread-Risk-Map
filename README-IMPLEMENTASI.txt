ERI MVP update

Files included:
- backend/app.py
- pages/risk-map.html
- js/generator.js
- css/generator.css

Before copying:
1. Open a terminal in the project root.
2. Make a backup of the four files before replacing them.
3. Copy the four files from this package into the matching folders.

Backend requirements:
- Flask
- flask-cors

The backend uses Python's standard library for HTTP requests. It does not need requests, NumPy, joblib, or scikit-learn for this MVP.

Run from the project root with the project's Python environment:
python backend/app.py

Then open the frontend using your local web server. The JavaScript requests:
http://127.0.0.1:5000/api/regions

Important:
- Existing point coordinates are retained as reference locations.
- Environmental values come from Open-Meteo APIs; they are model estimates, not local station measurements.
- If the provider is unavailable, the app displays unavailable/error status rather than substituting invented values.
- The legacy model file is not deleted; it is simply not used by this MVP.
- Open-Meteo API terms and attribution should be reviewed before public deployment, especially for commercial use.
