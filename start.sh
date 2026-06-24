#!/bin/bash
echo "Ingesting PDF..."
python src/ingest.py
echo "Starting API..."
uvicorn api:app --host 0.0.0.0 --port 8000 &
echo "Starting UI..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0