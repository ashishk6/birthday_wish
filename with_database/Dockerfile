FROM python:3.6

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY birthday.py .
ENV FLASK_APP=birthday.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]