FROM python:3.11-slim
RUN apt-get update -y \
    && apt-get install -y python3 python3-pip python-is-python3
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "chess_agent_openai.py"]