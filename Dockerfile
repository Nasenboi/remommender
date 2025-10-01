FROM python:3.9-slim

# SQL_PATH is automatically set in settings.py to:
# /remommender/db.sqlite3
# Those two are required by settings,
# but not if the image is isolated and cozy
ENV MEDIA_URL="/media/"
ENV MEDIA_ROOT="/srv/media/"
# The last thing that is required and cannot be set by default
# is the SECRET_KEY

WORKDIR /remommender

COPY . /remommender

#RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install --no-cache-dir tensorflow librosa django-ninja scikit-learn dotenv welford typing annoy transformers pandas torch essentia matplotlib django-cors-headers tempocnn

EXPOSE 8000

#ENTRYPOINT ["./runserver.sh"]
ENTRYPOINT ["/bin/bash"]
CMD []