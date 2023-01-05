FROM python:3.9-slim

EXPOSE 8501

COPY . /app

WORKDIR /app

RUN pip3 install -r requirments.txt

ENTRYPOINT ["streamlit", "run", "streamlit_app.py"]