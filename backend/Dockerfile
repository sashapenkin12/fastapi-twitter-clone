FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY . backend/

EXPOSE 8000

CMD ["/wait-for-it.sh", "db:5432", "--", "uvicorn", "backend.api.app:init_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
