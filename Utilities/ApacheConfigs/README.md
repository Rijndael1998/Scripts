# Apache Tools
Hi! These tools are pretty simple:


### Bash scripts
| Command                  | Parameter 1 | Parameter 2 | Parameter 3 |
|--------------------------|-------------|-------------|-------------|
| CreateSecureRedirect.sh  | Domain      |             |             |
| CreateSSLReverseProxy.sh | Domain      | Redirect    | KeyLocation |

#### Examples:
Making a secure redirect
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
