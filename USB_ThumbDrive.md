# Use a USB thumb drive for photo / video storage

Get to an auto mount USB disk


```
sudo apt-get install autofs
```


## format USB drive

```
sudo fdisk -l
# pick the USB thumb drive
sudo fdisk /dev/sdb
```

Delete partition table and create a new one, with primary partition at table entry `1`

```
p

d

o

n
p
1
[Enter]
[Enter]
w
```

Create the filesystem


```shell
sudo mkfs.ext3 -L motion-data /dev/sdb1
```


## get UUID of USB Flash drive

```shell
sudo blkid | grep /sdb
```

```
/dev/sdb1: LABEL="motion-data" UUID="eab7992d-85a2-4d6f-ace7-47b6baf5dc81" SEC_TYPE="ext2" TYPE="ext3" PARTUUID="922e3ef6-01"
```

## `/etc/auto.misc`


```shell
sudo vi /etc/auto.misc
```

```
motion-data       -fstype=ext4,rw         :/dev/disk/by-uuid/eab7992d-85a2-4d6f-ace7-47b6baf5dc81
```

```shell
grep eab7992d-85a2-4d6f-ace7-47b6baf5dc81 /etc/auto.misc
```

##  `/etc/auto.master`

```bash
sudo vi /etc/auto.master
```

```
/misc	/etc/auto.misc
```


```bash
## pick up changes
sudo service autofs restart
sudo service autofs status
journalctl -u autofs
df -h /misc/motion-data
dmesg | tail
```

## create data directory

`~/.motion/motion.conf` should have something like:

```
target_dir /misc/motion-data/data
```

```
sudo mkdir -p /misc/motion-data/data
sudo chown dpc:dpc /misc/motion-data/data
sudo usermod -aG video dpc

sudo service motion@dpc.service status
sudo service motion@dpc.service restart
```


## inspect

```shell
tail -f /home/dpc/.motion/motion.log
ls -latr /misc/motion-data/data
```



## maintenance
