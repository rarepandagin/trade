https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu






### reseting Django DB (removes all data except super users)

delete all migration files
drop all tables starting with dashboard_
python manage.py migrate --fake dashboard zero
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --fake dashboard zero
python manage.py makemigrations
python manage.py migrate

first thing, you need to recreate the stats object
goto admin and create a new stats object.


### frontend update_code.sh:

#!/bin/sh

rm -rf ParnianFrontend/
git clone git@github.com:ParnianAI/ParnianFrontend.git
cp -rf ParnianFrontend/* ./myprojectdir/
sed -i '1s/.*/DEBUG = True/' /home/sammy/myprojectdir/mysite/settings.py
sed -i '2s/.*/SITE_ID=3/' /home/sammy/myprojectdir/mysite/settings.py
source ~/myprojectdir/myprojectenv/bin/activate
python ~/myprojectdir/manage.py collectstatic

python ~/myprojectdir/manage.py makemigrations
python ~/myprojectdir/manage.py migrate


### backend update_code.sh:

#!/bin/sh

rm -rf ParnianBackend/
git clone git@github.com:ParnianAI/ParnianBackend.git
cp -rf ParnianBackend/src/parnian_backend/* ./myproject/
sudo shutdown -r now 'System maintenance'


### exports update_code.sh:

#!/bin/sh

rm -rf ParnianExports/
git clone git@github.com:ParnianAI/ParnianExports.git
cp -rf ParnianExports/* ./myproject/
sudo shutdown -r now 'System maintenance'


## Error 413 on Export Server
large amounts of data are sent to this server. You need to increase nginx upload file size to avoid error 413.
```
sudo nano /etc/nginx/sites-available/myproject
```
add this line:
```
client_max_body_size 100M;
```
for more info see:
https://ashwin.cloud/tutorials/nginx-fix-413-request-entity-too-large/#:~:text=Here's%20what%20the%20error%20might,for%20nginx%20is%201%20megabyte.
---


### Proxy

Django can provide a proxy server on `/proxy/`
this is used by ESRI SDK to avoid errors caused by CORS policy
ESRI falls back to using this proxy if the remote server does not support CORS
to run this proxy on your Django server install this library:
```pip install django-proxy```
that's it. you won't need to add it as an app in the settings.py.

### PDAL

you don't need to install PDAL on conda
just install it on Ubuntu and call it from command line

install laspy like this or you would not be able to read laz
pip install "laspy[lazrs,laszip]"
conda install conda-forge::pdal
---

502 gateway error:
/etc/nginx/nginx.conf change user from www-data to root


### IPOPT

Windows:
pyomo needs ipopt.exe in windows path.
install the binaries from https://www.coin-or.org/download/binary/Ipopt/
specificly download https://www.coin-or.org/download/binary/Ipopt/Ipopt-3.11.1-win64-intel13.1.zip
extract it to C:\ and include its bin dir to windows path

Ubuntu:

first open:
`https://coin-or.github.io/Ipopt/INSTALL.html`
and install the requirements:
`sudo apt-get install gcc g++ gfortran git patch wget pkg-config liblapack-dev libmetis-dev
`
just be aware that this page exist. you won't need it if the method below works.
we follow the method described in `https://coin-or.github.io/Ipopt/INSTALL.html#COINBREW`
just do the steps below:

use `coinbrew` tool to install ipopt on ubuntu.
it is just a script. download it from here.
https://coin-or.github.io/coinbrew/

then create a folder called: `ipopt_installed`
```
cd
wget https://raw.githubusercontent.com/coin-or/coinbrew/master/coinbrew
chmod u+x coinbrew
mkdir ipopt_installed
sudo nano ipop_installer_batch.sh
```

within `ipop_installer_batch.sh` wirte:
```
./coinbrew fetch Ipopt --no-prompt
./coinbrew build Ipopt --prefix=/home/sammy/ipopt_installed --test --no-prompt --verbosity=3
./coinbrew install Ipopt --no-prompt
```

save and exit.
then run it: `sudo bash ipop_installer_batch.sh`
it will install ipopt in here:
`/home/sammy/ipopt_installed/bin`

this path should also go in the system path
`sudo nano ~/.bashrc`

the last line in the file:
`export PATH=/home/sammy/ipopt_installed/bin:$PATH`

you will need to provide `executable` argument in pyomo.solve function anyway.
this might be because the app is running is API mode and paths become relative.
but pyomo needs absolute paths. so you do need to provide aboslute path it pyomo.
so not sure if adding ipopt path to the system path would be required at all.
```
opt = pyo.SolverFactory('ipopt', executable="/home/sammy/ipopt_installed/bin/ipopt")
```



---
# mathutils
to use the hip-roof generator algorithm called `bpypolyskel` you need to install `mathutils`.
this library installs on ubuntu with no problem.
but for windows you need to do this:

First you need to download and install Microsoft VS Build tools for C++ etc.
go to microsoft website, download their exe tool and install on Windows.


Next you need to download a path file and apply to the python package before installing it.
here are the steps:

!!!!
make sure you install WINDOWS SDK

download this path file:
https://gitlab.com/ideasman42/blender-mathutils/uploads/aebb580ffe731f0d0b56d9dc7463b5c6/Py39-PyNoArgsFucntion-20210809.patch

then:

cd ..
git clone https://gitlab.com/ideasman42/blender-mathutils.git
cd - && cd ../blender-mathutils
git apply {directory_of_patch}/Py39-PyNoArgsFucntion-20210809.patch
python setup.py build
python setup.py install

this will install the library on any python version.



---
# Django allauth

install this for social media log in capability

```
python -m pip install django-allauth
pip install django-allauth[socialaccount]
```

---
# Django upload/post size

you need to increase the upload and post size in a Django server

open:

```envs\p311\Lib\site-packages\django\conf\global_settings.py```

change ```FILE_UPLOAD_MAX_MEMORY_SIZE``` and ```DATA_UPLOAD_MAX_MEMORY_SIZE``` like this:
```
# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
FILE_UPLOAD_MAX_MEMORY_SIZE = 262144000  # i.e. 250 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 262144000  # i.e. 250 MB
```
more info:
https://stackoverflow.com/questions/41408359/requestdatatoobig-request-body-exceeded-settings-data-upload-max-memory-size

---

# Django Production Setup:

pip install -U 'channels[daphne]' channels-redis



issue of failing to connect to WSS:
make sure that the asgi lines are invoked
in debug mode, the lines in consumer have to be invoked when launching
if they are not then you need to install these:
pip install channels==3.0.4 daphne==3.0.2


initially follow this for wgsi (no wss)
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04

then you need to install Daphne:
https://plainenglish.io/blog/how-deploy-an-asgi-django-application-with-nginx-gunicorn-daphne-and-supervisor-on-ubuntu-server

you may need to have this script as boot.sh the way it is described in the document 
```
#!/bin/sh
sudo systemctl restart gunicorn.service
sudo systemctl start daphne.service
```

to get this root.sh run at startup:
```sudo nano /etc/systemd/system/on_boot.service```

the reason is that neither the gunicorn nor daphne would start on their own at the start up

this problem did not happen with AWS. only with DO.

also make sure to always update the static files mamunally with

`python ~/myprojectdir/manage.py collectstatic`


# WSS and Daphne

For windows:
make sure you use an onlder version of Channels
pip install channels==3.0.5 


For Ubuntu:

you need `Daphne` to properly serve WSS.

#### Notes:
- you can't do WS on HTTPS. only WSS.)
- you don't need anything on the client side to make WSS calls. only python is enough.

Step 1:
Follow steps in:
https://plainenglish.io/blog/how-deploy-an-asgi-django-application-with-nginx-gunicorn-daphne-and-supervisor-on-ubuntu-server

but you do not need Administrator or Celery


### Diagnosis:


```journalctl -u daphne.service```
first check if your Daphne is running. check Daphne status:

```systemctl status daphne.service```


if Daphne is not running properly, its status says that it is `dead`.

in this case you won't be able to properly set up a WSS on Django ASGI.
first make sure your Daphne status file is configured correctly. see the example.
next make sure that Daphne Service is running at boot.
see `daphne.service` file in the examples.

```sudo nano /etc/systemd/system/daphne.service```

once you made sure that the `daphne.service` file is correct,
then you need to make sure that your `boot.sh` file has proper permission
and that it is run at boot.

```chmod u+x boot.sh```

one way to make `boot.sh` is described in the article (modyfiing `/etc/systemd/system`).
but this did not work on EC2. Another way to run it at boot is to copy it to `/etc/rc.local`:
```
cp boot.sh /etc/rc.local
```
this worked on EC2.



# Final Django Setup
make sure to change user-group to sammy in all config files
sudo nano /etc/nginx/nginx.conf




### caching:
you need to disable caching at least when doing heavy dev:
follow this article:

```https://ubiq.co/tech-blog/disable-nginx-cache/```

---

### commonly used links:
```
sudo nano /etc/nginx/nginx.conf
        - first line: make sure to change user to sammy, otherwise your statics can't be read
        - add     client_max_body_size 20M;     to http to allow for larger uploads


Django:
    sudo nano /etc/nginx/sites-available/mysite
Flask:
    sudo nano /etc/nginx/sites-available/myproject


sudo certbot --nginx -d your_domain -d www.your_domain
sudo certbot --nginx -d parnian.app -d www.parnian.app


sudo nginx -t

sudo nano /etc/systemd/system/gunicorn.service


sudo tail -F /var/log/nginx/error.log

sudo tail -F /var/log/nginx/access.log

sudo journalctl -u gunicorn


sudo systemctl restart gunicorn.service

sudo systemctl start daphne.service

```

---
### Postgres

### install python client
on windows:

```
pip install psycopg2 --user
```

on ubuntu:

```
sudo apt install python3-dev libpq-dev
pip install psycopg2
```

#### to install on Ubuntu 22:
```sudo apt update 
sudo apt install postgresql postgresql-contrib 
sudo systemctl start postgresql.service
```

### DJango set up:
```
CREATE DATABASE django;
GRANT ALL PRIVILEGES ON DATABASE django TO postgres;
ALTER ROLE postgres WITH PASSWORD 'f4I8H2C0U40X104jwVUSKW38F4X23894j2938429jz';
```


#### to make Postgres accessible remotely
```
sudo nano /etc/postgresql/16/main/postgresql.conf
```
Add the following line to the end:
```listen_addresses = '*'```
then:
```
sudo nano /etc/postgresql/16/main/pg_hba.conf
```
Add the following line to the end:
```host    all             all             0.0.0.0/0               md5```

sudo ufw allow 5432/tcp   



# if you want a non-django postgres db:
#### to run:
```
sudo -i -u postgres     # to activate the role
createdb parnian_backend;


psql                    # to run
ALTER ROLE postgres WITH PASSWORD '!iB4V*#8t';
\conninfo               # to know where you are
\c parnian_backend         # to connect to db
```
#### to set up a DB
```

CREATE TABLE parcels (
    id serial PRIMARY KEY,
    project_uuid varchar (1000),
    project_uuid bigint,
    datetime varchar (1000), 
    user_id bigint,
    user_ip varchar (1000),
    pickle bytea
);

```


```

Resize in AWS:

- take and image from the existing instance. it will go into to AMIs.
- create a new instance from this AMI. it will have a new IP
- in Route 53 change the IP of the A record to this new IP

```

# RE for between text
<svg(.*?)</svg>

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAusH8DTCH4f4KpqzKI/BNlmRXZOzhYeq92OHSqKSZNr
/home/sammy/myprojectdir/myprojectenv/lib/python3.12/site-packages/django/contrib/auth/




# PROXY

sudo apt install shadowsocks-libev
sudo nano /etc/shadowsocks-libev/config.json
{
    "server":["0.0.0.0"],   <--------
    "mode":"tcp_and_udp",
    "server_port":8388,
    "local_port":1080,
    "password":"7vmbPOHhFxHW",
    "timeout":86400,
    "method":"chacha20-ietf-poly1305"
}

sudo ufw allow 8388