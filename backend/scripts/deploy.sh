rm -Rf ~/backend/__pycache__
rm -Rf ~/backend/*/__pycache__

service sup stop

cp -r /var/www/sup-server/* /var/www/backup/
rm -r /var/www/sup-server/*/
mv ~/backend/* /var/www/sup-server/
cp -r /var/www/backup/sup_env /var/www/sup-server/
mv /var/www/backup/.flask_secret /var/www/sup-server/
mkdir /var/www/sup-server/logs
rm /var/www/sup-server/configs/local.config.json
mv /var/www/backup/configs/local.config.json /var/www/sup-server/configs/
rm -R /var/www/sup-server/__pycache__
rm -R /var/www/sup-server/*/__pycache__

chown virt /var/www/sup-server -R
chgrp virt /var/www/sup-server -R

service sup start
service sup status

