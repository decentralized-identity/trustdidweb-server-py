FROM python:3.11

WORKDIR /flask

# Install debugging tools
RUN apt update && apt install -y \
    curl

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app ./app
COPY config.py main.py ./

CMD ["gunicorn", "--bind=0.0.0.0:5000", "main:app"]