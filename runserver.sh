#!/bin/bash

RESET_DB=false

for arg in "$@"; do
    case $arg in
        -r|--reset)
        RESET_DB=true
        shift
        ;;
    esac
done

if [ "$RESET_DB" = true ]; then
    echo "!! Resetting the database !!"
    rm -rf $MEDIA_ROOT*
    python manage.py flush --no-input
fi

echo "<< Updating the database schema >>"
python manage.py makemigrations --no-input
python manage.py migrate --no-input

echo "<< Starting the Django development server >>"
python manage.py runserver
