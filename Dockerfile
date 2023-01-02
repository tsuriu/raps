FROM python:3.10-alpine

RUN mkdir /api
WORKDIR /api

COPY requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /api/

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]

#EXPOSE 8000