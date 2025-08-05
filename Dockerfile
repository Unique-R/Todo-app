FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wget \
    && wget -O /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /wait-for-it.sh \
    && apt-get remove -y wget && apt-get autoremove -y
COPY . .
CMD ["/wait-for-it.sh", "db:5432", "--", "python", "main.py"]
