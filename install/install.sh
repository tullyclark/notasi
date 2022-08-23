#!/bin/bash

#exit on error
set -e

#check root
if [ $(whoami) != "root" ]; then
        echo "Please be root"
        exit 1
fi

#get dependancies
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
apt-get install python3-pip libxmlsec1-dev pkg-config virtualenv uwsgi nginx postgresql postgresql-server-dev-all libmysqlclient-dev unixodbc-dev chromium-chromedriver
ACCEPT_EULA=Y apt-get install msodbcsql17

#get installation location
read -e -p "Install Location [/opt/notasi]: " InstallLocation
InstallLocation=$(readlink \-f "${InstallLocation:-/opt/notasi}")

#clone from git
git clone https://github.com/tullyclark/notasi $InstallLocation

#get Selenium Storage Location
read -e -p "Selenium Storage Location [${InstallLocation}/site/storage]: " StorageLocation
StorageLocation=$(readlink \-f "${StorageLocation:-${InstallLocation}/site/storage}")
mkdir -p ${StorageLocation}

#What user will run it?
read -e -p "Owner (User) [${SUDO_USER:-$(whoami)}]: " User
User="${User:-${SUDO_USER:-$(whoami)}}"

sudo chown -R $User $InstallLocation


# read -e -p "Use SSL (Y/N) [Y]: " SSL
# SSL=${SSL:="Y"}


# #do nginx stuff

# if [ $SSL == "Y" ]; then
# 	echo "If SSL files don't exist, starting the NGINX server will fail"

# 	read -e -p "SSL Certification Location []: " Certificate
# 	echo $Certificate

# 	read -e -p "SSL Private Key Location []: " PrivateKey
# 	echo $PrivateKey

# 	read -e -p "SSL Private Key Passphrase Location []: " PrivateKeyPassphrase
# 	echo $PrivateKeyPassphrase

# 	echo "Generating NGINX File"
# 	InstallLocation=$InstallLocation \
# 	Certificate=$Certificate \
# 	PrivateKey=$PrivateKey \
# 	PrivateKeyPassphrase=$PrivateKeyPassphrase \
# 	envsubst '$InstallLocation $Certificate $PrivateKey $PrivateKeyPassphrase'< $InstallLocation/install/https-nginx-template.txt > /etc/nginx/sites-available/notasi
# else
	echo "Generating NGINX File"
	InstallLocation=$InstallLocation \
	envsubst '$InstallLocation'< $InstallLocation/install/http-nginx-template.txt > /etc/nginx/sites-available/notasi
# fi



echo "Generating systemd File"
InstallLocation=$InstallLocation \
User=$User \
envsubst < $InstallLocation/install/systemd-template.txt > /etc/systemd/system/notasi.service


#initiate virtualenv

sudo -i -u $User bash << EOF
virtualenv $InstallLocation/env --python=python3
source $InstallLocation/env/bin/activate
pip3 install -r $InstallLocation/requirements.txt
deactivate
EOF


#configure NGINX

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/notasi /etc/nginx/sites-enabled

NotasiPassword=$(openssl rand -base64 32)
echo "DB Username: notasi"
echo "DB Password: ${NotasiPassword}"
read -p "Press enter to continue"

#configure database
sudo -u postgres -i << EOF

echo "SELECT 'DROP DATABASE notasi' WHERE EXISTS (SELECT FROM pg_database WHERE datname = 'notasi')\gexec" | psql postgres
echo "SELECT 'DROP role notasi' WHERE EXISTS (SELECT FROM pg_catalog.pg_roles WHERE  rolname = 'notasi')\gexec" | psql postgres
echo "CREATE USER notasi WITH PASSWORD '${NotasiPassword}' CREATEDB\gexec" | psql postgres
echo "CREATE DATABASE notasi OWNER notasi\gexec" | psql postgres
echo "CREATE SCHEMA notasi" | psql notasi
EOF


#Generate files

echo "Generating Config File"
FlaskSecretKey=$(openssl rand -base64 32) \
SQLAlchemySecretKey=$(openssl rand -base64 32) \
NotasiPassword=$NotasiPassword \
StorageLocation=$StorageLocation \
envsubst < $InstallLocation/install/config-template.py > $InstallLocation/site/config.py


#reload services

systemctl daemon-reload
systemctl restart nginx
systemctl restart notasi.service
systemctl status notasi.service
