FROM python:3.12-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY myinference.py /app/

ENTRYPOINT ["python"]

CMD ["/app/myinference.py"]
