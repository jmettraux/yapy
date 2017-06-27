
# deploying yapy

Using [runit](http://smarden.org/runit/) (usually as an add-on, not as a sysvinit replacement).

```
/etc/sv/
|-- yapy/
|   |-- log/
|   |   |-- run
|   |   `-- supervise/
|   |-- run
|   `-- supervise/
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

