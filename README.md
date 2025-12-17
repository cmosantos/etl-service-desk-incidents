# ETL Service Desk Incidents

Rodar:
- python -m venv .venv
- .venv\Scripts\activate
- pip install -r requirements.txt
- python -m src.generate_sample_data
- python -m src.pipeline --input data/raw/incidents.csv

