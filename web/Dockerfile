FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install ./models/en_core_web_sm-3.0.0.tar.gz
CMD [ "python", "app.py" ]