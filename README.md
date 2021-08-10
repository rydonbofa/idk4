# Hide.me-LinuxClient


As of today, there is no official GUI App for people who are using Hide.me on Linux.

This project is supposed to simplify the VPN usage by giving Hide.me users a GUI, which can be used instad of the terminal.

The GUI is still very basic and is still in developement.

## Installation



### Tkinter
This project relies on the tkinter GUI Framework.
Tkinter can be installed on Debian/Ubuntu based Systems by using the following command:
```
apt-get install python-tk
```

For other ditros use the official documentation, which can be found here:
https://tkdocs.com/tutorial/install.html

### Script
Installation of the script can be done by using the following commands:

```
wget https://github.com/BastianLo/Hide.me-LinuxClient/archive/refs/heads/master.zip

unzip master.zip

pip install -r Hide.me-LinuxClient-master/requirements.txt

rm master.zip

python3 Hide.me-LinuxClient-master/hideme/app.py
```

## Images
![alt text](https://i.imgur.com/5kM1ata.png)
