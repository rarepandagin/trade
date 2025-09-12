#!/bin/sh

rm -rf trade/
git clone git@github.com:rarepandagin/trade.git
cp -rf trade/* ./myprojectdir/
rm -rf trade/

# mysite.settings.py
sed -i '1s/.*/DEBUG = False/' /home/sammy/myprojectdir/mysite/settings.py
sed -i '2s/.*/SITE_ID=1/' /home/sammy/myprojectdir/mysite/settings.py

# mysite.wsgi.py
sed -i '1s/.*/PRODUCTION = True/' /home/sammy/myprojectdir/mysite/wsgi.py

rm /home/sammy/myprojectdir/logs.txt

source ~/myprojectdir/myprojectenv/bin/activate

rm -rf /home/sammy/myprojectdir/static

python ~/myprojectdir/manage.py collectstatic

python /home/sammy/myprojectdir/manage.py migrate

echo "Daemon Reload"
sudo systemctl daemon-reload
echo "Postgres"
sudo systemctl restart postgresql
echo "Gunicorn"
sudo systemctl restart gunicorn
sudo systemctl restart gunicorn.socket
sudo systemctl restart gunicorn.service
echo "Nginx"
sudo systemctl restart nginx
echo "Daphne"
sudo systemctl restart daphne.service

