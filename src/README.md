# Part 10 — Technical Proof of Concept

This small Flask prototype demonstrates two technical risks in the proposed Local Service Problem Diagnosis and Matching System:
1. Whether a text-classification component can map a problem description to a service category.
2. Whether the web application can save the description and prediction in SQLite.

## Requirements
- Python 3.10 or newer recommended
- pip

## Run in VS Code terminal
```bash
python -m venv .venv
```
Windows:
```bash
.venv\Scripts\activate
```
macOS/Linux:
```bash
source .venv/bin/activate
```
Then:
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 in a browser.

## Test the API
With the application running, send a POST request to `/api/classify` with JSON:
```json
{"description":"The kitchen sink pipe is leaking"}
```
Expected response fields: `request_id`, `predicted_category`, and `confidence`. The exact predicted category and confidence are produced by the model at runtime.

Health check: open http://127.0.0.1:5000/health.

## Database
The app creates `service_requests.db` automatically and stores each submitted problem in `poc_requests`.

## Important limitation
The included CSV is a small illustrative dataset created for proof-of-concept testing. The model's confidence is not a calibrated probability and the sample is not representative of real-world requests. Do not report this prototype as production-ready or claim validated accuracy. Before making an accuracy claim, create a larger labeled dataset, split it into training and test sets, and report test metrics.

## Suggested evidence to capture
1. VS Code terminal showing the app started successfully.
2. Browser result after submitting a sample problem, showing predicted category and request ID.
3. SQLite table contents showing the saved description and predicted category.
4. Optional API test response from `/api/classify`.
