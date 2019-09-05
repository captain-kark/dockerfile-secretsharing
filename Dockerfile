FROM python:2.7
WORKDIR /app/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY default.py .
VOLUME /tmp/split/ # secret to split (by default.py)
VOLUME /tmp/recover/ # secret to recover (by default.py)
ENTRYPOINT ["python", "default.py"]  # /tmp/split/${filename}, /tmp/recover/
