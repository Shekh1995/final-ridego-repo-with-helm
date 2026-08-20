FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN mkdir -p /data && chown -R 10001:10001 /data
USER 10001
EXPOSE 5003
CMD ["python","app.py"]
