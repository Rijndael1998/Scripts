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
```xml
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
```xml
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

### GenerateProxyApacheConfig.py
`GenerateProxyApacheConfig.py` reads from the `proxy-websites.json` file (or `proxy-websites.json.sample` if `proxy-websites.json` doesn't exist). It runs `CreateSecureRedirect.sh` to create a configuration file to redirect HTTP into HTTPS traffic. It then runs `CreateSSLReverseProxy.sh` to create the secure reverse proxy. The outputs are saved into the folder specified by the parameter. 

| Command                       | Parameter     |
|-------------------------------|---------------|
| GenerateProxyApacheConfig.py  | Output Folder |

#### Structure of `proxy-websites.json` file
The file structure is a very simple JSON file. It is structured as so:
```json
[
    {
        "domain": "example.com",
        "reverse": "http://localhost:80/",
        "keys": "/etc/letsencrypt/live/*/"
    },
    {
        ...
    },
    
    ...
]
```

The domain should be the domain to forward without http://, https:// or / in any part of the string. It should also not include any characters following the top level domain. 

The reverse is a URL to the target server. It doesn't need to be `http://localhost/`, it can be any server that accepts your requests. 

The key is the folder location of `fullchain.pem` and `privkey.pem` files. These keys are used to encrypt the HTTPS traffic incoming into the server.

#### Examples:
##### Creating a simple configuration for an example domain for Apache.
We'll be using `example.com` as the domain for a service running on `http://localhost:3000/`. They keys are stored in `/etc/letsencrypt/live/example.com/`

To do this, we need to write the new configuration to `proxy-websites.json`:
```json
[
    {
        "domain": "example.com",
        "reverse": "http://localhost:3000/",
        "keys": "/etc/letsencrypt/live/example.com/"
    }
]
```

Execure the Python script:
```bash
python3 GenerateProxyApacheConfig.py /etc/apache2/sites-enabled/
```

This overwrites existing `example.com.conf` and `example.com-le-ssl.conf` files in `/etc/apache2/sites-enabled/`:

**example.com.conf:**
```xml
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

**example.com-le-ssl.conf:**
```xml
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
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/

    SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```

To apply the configuration, restart the server:
```bash
systemctl restart apache2
```

##### Creating a configuration for an example domain fowarding to another machine.
If you wanted to forward some Pterodactyl dashboard (pterodactyl.example.com) running on another machine (`http://192.168.0.2:80/`), you could the same approch as above. 

Create the `proxy-websites.json` file:
```json
[
    {
        "domain": "pterodactyl.example.com",
        "reverse": "http://192.168.0.2:80/",
        "keys": "/etc/letsencrypt/live/pterodactyl.example.com/"
    }
]
```
Execure the Python script:
```bash
python3 GenerateProxyApacheConfig.py /etc/apache2/sites-enabled/
```

This overwrites existing `example.com.conf` and `example.com-le-ssl.conf` files in `/etc/apache2/sites-enabled/`:

**pterodactyl.example.com.conf:**
```xml
<VirtualHost *:80>
    ServerName pterodactyl.example.com

    DocumentRoot /var/www/html

    ErrorLog /error.log
    CustomLog /access.log combined

    RewriteEngine on
    RewriteCond %{SERVER_NAME} =pterodactyl.example.com
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```

**pterodactyl.example.com-le-ssl.conf:**
```xml
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName pterodactyl.example.com
    DocumentRoot /var/www/html

    ErrorLog /error.log
    CustomLog /access.log combined
    ProxyPreserveHost On

    <Proxy *>
            Order deny,allow
            Allow from all
    </Proxy>

    RequestHeader set X-Forwarded-Proto https
    ProxyPass / http://192.168.0.2:80/
    ProxyPassReverse / http://192.168.0.2:80/

    SSLCertificateFile /etc/letsencrypt/live/pterodactyl.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/pterodactyl.example.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```

To apply the configuration, restart the server:
```bash
systemctl restart apache2
```


##### Creating configurations for multiple example domains
If we were to combine both of these services into one Apache server, the configuration file would look like this:
```json
[
    {
        "domain": "example.com",
        "reverse": "http://localhost:3000/",
        "keys": "/etc/letsencrypt/live/example.com/"
    },
    {
        "domain": "pterodactyl.example.com",
        "reverse": "http://192.168.0.2:80/",
        "keys": "/etc/letsencrypt/live/pterodactyl.example.com/"
    }
]
```

Execure the Python script:
```bash
python3 GenerateProxyApacheConfig.py /etc/apache2/sites-enabled/
```

This creates both files used in the examples.

To apply the configuration, restart the server:
```bash
systemctl restart apache2
```
