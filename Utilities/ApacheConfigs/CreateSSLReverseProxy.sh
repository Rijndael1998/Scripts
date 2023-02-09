#!/bin/bash

echo "<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName $1
    DocumentRoot /var/www/html

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    ProxyPreserveHost On

    <Proxy *>
            Order deny,allow
            Allow from all
    </Proxy>

    RequestHeader set X-Forwarded-Proto "https"
    ProxyPass / $2
    ProxyPassReverse / $2

    SSLCertificateFile $3fullchain.pem
    SSLCertificateKeyFile $3privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
"
