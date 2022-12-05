FROM python:3.10

WORKDIR /usr/src/gang_bang_music

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]