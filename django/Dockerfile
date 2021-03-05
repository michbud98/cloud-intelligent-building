FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD Pipfile /app
ADD Pipfile.lock /app
ADD ./control_web_app /app/
RUN pip install pipenv
RUN pipenv install --system --skip-lock 
CMD python manage.py runserver 0.0.0.0:$PORT
