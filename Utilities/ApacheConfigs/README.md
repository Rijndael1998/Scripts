# Apache Tools
Hi! These tools are pretty simple:


### Bash scripts
| Command                  | Parameter 1 | Parameter 2 | Parameter 3 |
|--------------------------|-------------|-------------|-------------|
| CreateSecureRedirect.sh  | Domain      |             |             |
| CreateSSLReverseProxy.sh | Domain      | Redirect    | KeyLocation |

#### Examples:
##### Making a secure redirect
```bash
./CreateSecureRedirect.sh example.com 
```


This generate a valid Apache2 config file that redirects from HTTP to HTTPS traffic:
```
<VirtualHost *:80>
    ServerName example.com

    DocumentRoot /var/www/html

    ErrorLog /error.log
    CustomLog /access.log combined

    RewriteEngine on
    RewriteCond %{SERVER_NAME} =example.com
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```

##### Making a secure reverse proxy
```bash
./CreateSSLReverseProxy.sh example.com http://localhost:80/ /etc/letsencrypt/live/example.com/
```


This generates a secure reverse proxy for `example.com`. It will take traffic from HTTPS and forward it onto a local HTTP server. It includes the `X-Forwarded-Proto` header to let the service know that it has securely connected. It includes the `/etc/letsencrypt/options-ssl-apache.conf` file as this is what I use. 
```
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/html

    ErrorLog /error.log
    CustomLog /access.log combined
    ProxyPreserveHost On

    <Proxy *>
            Order deny,allow
            Allow from all
    </Proxy>

    RequestHeader set X-Forwarded-Proto https
    ProxyPass / http://localhost:80/
    ProxyPassReverse / http://localhost:80/

    SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```
