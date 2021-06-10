FROM python:rc-buster
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=api.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1
EXPOSE 5000
CMD ["flask", "run"]