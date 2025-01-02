FROM python:3.10-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

WORKDIR /code/backend

# RUN cd backend/

EXPOSE 11251

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "11251", "--workers", "4"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "11251", "--workers", "12"]
# uvicorn main:app --host 0.0.0.0 --port 11253 --workers 4