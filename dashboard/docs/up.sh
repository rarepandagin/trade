#!/bin/sh

sudo systemctl stop collector.service
sudo systemctl stop pulse_maker.service


rm -rf trade/
git clone git@github.com:rarepandagin/trade.git
cp -rf trade/* ./myprojectdir/
rm -rf trade/

rm -rf trade_beats/
git clone git@github.com:rarepandagin/trade_beats.git


# mysite.settings.py
sed -i '1s/.*/DEBUG = False/' /home/sammy/myprojectdir/mysite/settings.py
sed -i '2s/.*/SITE_ID=1/' /home/sammy/myprojectdir/mysite/settings.py

# mysite.wsgi.py
sed -i '1s/.*/PRODUCTION = True/' /home/sammy/myprojectdir/mysite/wsgi.py


# trade_beats.toolkit.py
sed -i '1s/.*/PRODUCTION = True/' /home/sammy/trade_beats/toolkit.py


rm /home/sammy/myprojectdir/logs.txt
rm /home/sammy/trade_beats/logs.txt





source ~/myprojectdir/myprojectenv/bin/activate


rm -rf /home/sammy/myprojectdir/static

python ~/myprojectdir/manage.py collectstatic


python /home/sammy/myprojectdir/manage.py migrate



# echo "Daemon Reload"
sudo systemctl daemon-reload

echo "Postgres"
sudo systemctl restart postgresql

echo "Gunicorn"
sudo systemctl restart gunicorn
sudo systemctl restart gunicorn.socket

sudo systemctl restart gunicorn.service


# echo "Gunicorn"
# sudo systemctl start daphne.service

echo "Nginx"
sudo systemctl restart nginx


echo "Gunicorn"
sudo systemctl restart daphne.service


echo "Collector"
sudo systemctl restart collector.service
echo "Pulse Maker"
sudo systemctl restart pulse_maker.service


# cd /home/sammy/trade_beats/
# chmod +x ./collector.py
# nohup python ./collector.py  > script1.log 2>&1 & 

# chmod +x ./pulse_maker.py
# nohup python ./pulse_maker.py > script2.log 2>&1 &

# tail -f /home/sammy/trade_beats/logs.txt