#!/bin/sh

rm -rf trade/
git clone git@github.com:rarepandagin/trade.git
cp -rf trade/* ./myprojectdir/

rm -rf trade_beats/
git clone git@github.com:rarepandagin/trade_beats.git

#sed -i '1s/.*/DEBUG = False/' /home/sammy/myprojectdir/mysite/settings.py
sed -i '2s/.*/SITE_ID=1/' /home/sammy/myprojectdir/mysite/settings.py



source ~/myprojectdir/myprojectenv/bin/activate
python ~/myprojectdir/manage.py collectstatic

python /home/sammy/myprojectdir/manage.py makemigrations
python /home/sammy/myprojectdir/manage.py migrate



echo "Daemon Reload"
sudo systemctl daemon-reload

#echo "Postgres"
sudo systemctl restart postgresql

echo "Gunicorn"
sudo systemctl restart gunicorn
sudo systemctl restart gunicorn.socket

sudo systemctl restart gunicorn.service
sudo systemctl start daphne.service

echo "Nginx"
sudo systemctl restart nginx


sudo systemctl restart daphne.service