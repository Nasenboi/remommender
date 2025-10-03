#!/bin/bash

RESET_DB=false
DELETE_FILES=false

for arg in "$@"; do
    case $arg in
        -r|--reset)
        RESET_DB=true
        shift
        ;;
        -d|--delete)
        DELETE_FILES=true
        shift
        ;;
    esac
done

if [ "$DELETE_FILES" = true ]; then
    echo "!! Deleting media files !!"
    read -p "Are you sure you want to delete all media files? This will remove all files in MEDIA_ROOT. [y/N]: " confirm
    confirm=${confirm:-N}
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Aborting file deletion."
        DELETE_FILES=false
    fi
fi

if [ "$DELETE_FILES" = true ]; then
    rm -rf $MEDIA_ROOT*
fi

if [ "$RESET_DB" = true ]; then
    python manage.py flush --no-input
fi

echo "<< Updating the database schema >>"
# Make migrations best done manually ^^"
# python manage.py makemigrations --no-input
python manage.py migrate --no-input

echo "<< Starting the Django development server >>"
python manage.py runserver 0.0.0.0:8000
