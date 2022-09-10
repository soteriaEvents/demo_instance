#!/usr/bin/bash

# fetching data files
rm /tmp/base_data.json
rm /tmp/ticketing_data.json
curl -o /tmp/base_data.json https://raw.githubusercontent.com/soteriaEvents/demo_instance/master/data/base_data.json
curl -o /tmp/ticketing_data.json https://raw.githubusercontent.com/soteriaEvents/demo_instance/master/data/ticketing_data.json
echo "fetched data json files"


# resetting database
cd ~
python manage.py flush --no-input
python manage.py loaddata /tmp/base_data.json
python manage.py loaddata /tmp/ticketing_data.json
echo "resetted database data"


# setting up for fetching images
cd /tmp
echo "setting up for fetching images"
curl -o load_images.py https://raw.githubusercontent.com/soteriaEvents/demo_instance/master/script/load_images.py
curl -o requirements.txt https://raw.githubusercontent.com/soteriaEvents/demo_instance/master/requirements.txt
python -m pip install -r requirements.txt
echo "CLOUDINARY_URL=${CLOUDINARY_URL}" > .env


# start fetching images
python /tmp/load_images.py
echo "images fetched & uploaded"


mkdir -p ~/crontab
cd ~/crontab
date >> reset_database_log.txt
echo "updated ~/crontab/reset_database_log.txt"
cat ~/crontab/reset_database_log.txt
