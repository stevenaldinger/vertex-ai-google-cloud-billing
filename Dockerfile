FROM python:3.11

EXPOSE 8080

WORKDIR /app

COPY app/requirements.txt ./

RUN pip install -r requirements.txt

COPY app ./

COPY modules /root/modules

ENV PYTHONPATH="/root/modules"

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
