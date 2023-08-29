# Quickly install on system

```bash
apt -y install crontab
echo "@reboot root bash /root/Scripts/Mining/autorun.sh" >> /etc/crontab
reboot
```


