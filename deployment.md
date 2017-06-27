
# deploying yapy

## starting/stopping thanks to Runit

Using [Runit](http://smarden.org/runit/) (usually as an add-on, not as a sysvinit replacement).

```
/etc/sv/
|-- yapy/
|   |-- log/
|   |   |-- run
|   |   `-- supervise/   # runit generated
|   |-- run
|   `-- supervise/       # runit generated
```

The runit `run` script for yapy:
```sh
#!/bin/sh

# /etc/sv/yapy/run

export YAPY_PORT=5001
cd /home/yapy && \
  exec 2>&1 chpst -u yapy python server.py
```

The runit `run` script for the yapy logger:
```sh
#!/bin/sh

# /etc/sv/yapy/log/run

exec chpst -u yapy svlogd -v /var/log/yapy/
```


## reverse proxy thanks to Nginx

```
# /etc/nginx/sites-available/yapy

server {
  list 443 ssl;
  listen [::]:443 ssl;
  server_name yapy.lambda.io;

  include snippets/ssl-yapy.lambda.io.conf;  #
  include snippets/ssl-params.conf;          # SSL config

  access_log /var/log/yapy/https.access.log;
  error_log /var/log/yapy/https.error.log;

  location / {
    send_timeout 5m;
    proxy_pass http://127.0.0.1:5001;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $host;
  }
```

