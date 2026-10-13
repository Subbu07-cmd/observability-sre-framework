# Runbook: HostDiskWillFillIn4h

1. `df -h` and `du -xh / --max-depth=2 2>/dev/null | sort -h | tail -20`
2. Common causes:
   - `/var/log` growth: check `logrotate -d /etc/logrotate.conf` and run `journalctl --vacuum-size=500M`
   - Container images: `docker system prune -af` or `crictl rmi --prune`
   - Core dumps in `/var/lib/systemd/coredump`
3. If the growth is legitimate, expand the EBS volume (`aws ec2 modify-volume`), then run `growpart` and `xfs_growfs`.
4. Follow up with a ticket for capacity planning, log retention or right-sizing.
