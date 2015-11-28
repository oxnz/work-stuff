# system

## grub2

	set root=(hd1,msdos5)
	set isofile=/path/to/net-inst.iso
	loopback loop $isofile
	linux (loop)/boot/x86_64/loader/linux install=hd:$isofile
	initrd (loop)/boot/x86_64/loader/initrd
	boot


# linuxrc

## network auth

	wpa_supplicant -B -i wlan0 -c /path/to/wpa.conf
	dhcpcd wlan0


# refs

1. [how to use wpa supplicant](https://wiki.netbsd.org/tutorials/how_to_use_wpa_supplicant/#index2h1)
2. [Linux WPA/WPA2/IEEE 802.1X Supplicant](http://w1.fi/wpa_supplicant/)
3. [Wireless network configuration](https://wiki.archlinux.org/index.php/Wireless_network_configuration#Manual_setup)
4. [Linuxrc](https://en.opensuse.org/SDB:Linuxrc)
5. [init](http://linux.chinaunix.net/techdoc/net/2008/12/18/1053772.shtml)
