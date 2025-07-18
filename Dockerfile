FROM python:3.13-slim

# SQL_DIR is automatically set in settings.py to:
# /remommender/db.sqlite3
# Those two are required by settings,
# but not if the image is isolated and cozy
ENV MEDIA_URL="/media/"
ENV MEDIA_ROOT="/srv/media/"
# The last thing that is required and cannot be set by default
# is the SECRET_KEY

WORKDIR /remommender

COPY . /remommender

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./runserver.sh"]
CMD []