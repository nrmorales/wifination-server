#!/bin/ash
#install script for wifination routers
#@author ibaguio

#function that creates the wireless networks & interfaces
#createWireless(){}

createMobileNetwork(){
  network="config interface 'loopback'\n\
    option ifname 'lo'\n\
    option proto 'static'\n\
    option ipaddr '127.0.0.1'\n\
    option netmask '255.0.0.0'\n\n\

  config interface 'lan'\n\
    option ifname 'eth0'\n\
    option _orig_ifname 'eth0'\n\
    option _orig_bridge 'false'\n\
    option proto 'dhcp'\n\n\

  config interface 'wifi'\n\
    option proto 'static'\n\
    option ipaddr '192.168.0.1'\n\
    option netmask '255.255.255.0'\n\n\

  config interface 'wan'\n\
    option _orig_ifname 'eth0'\n\
    option _orig_bridge 'false'\n\
    option ifname 'ppp0'\n\
    option proto '3g'\n\
    option device '/dev/ttyUSB0'\n\
    option service 'umts'\n\
    option apn 'internet.globe.com.ph'\n"

  cd ~/
  wget http://pastebin.com/raw.php?i=X02kvTgF
  mv raw.php?i=X02kvTgF /etc/config/network2

  #echo "Creating network file"
  #echo -e $network >> /etc/config/network2
}

createMobileWireless(){
  wireless="config wifi-iface\n\
    option device 'radio0'\n\
    option mode 'ap'\n\
    option encryption 'none'\n\
    option ssid 'WiFi Nation portable'\n\
    option network 'wifi'\n"

  echo "Creating Mobile Wireless settings"
  echo -e $wireless >> /etc/config/wireless2

}

createMobileFirewall(){
  firewall="\
    config defaults\n\
      option syn_flood '1'\n\
      option input 'ACCEPT'\n\
      option output 'ACCEPT'\n\
      option forward 'REJECT'\n\n\

    config zone\n\
      option name 'lan'\n\
      option network 'lan'\n\
      option input 'ACCEPT'\n\
      option output 'ACCEPT'\n\
      option forward 'REJECT'\n\
      option masq '1'\n\
      option mtu_fix '1'\n\n\

    config include\n\
      option path '/etc/firewall.user'\n\n\

    config zone\n\
      option input 'ACCEPT'\n\
      option forward 'REJECT'\n\
      option output 'ACCEPT'\n\
      option name 'wifi'\n\
      option network 'wifi'\n\n\

    config zone\n\
      option input 'ACCEPT'\n\
      option forward 'REJECT'\n\
      option output 'ACCEPT'\n\
      option name '3gwan'\n\
      option network 'wan'\n\
      option masq '1'\n\
      option mtu_fix '1'\n\n\

    config forwarding\n\
      option dest '3gwan'\n\
      option src 'wifi'\n\n\

    config forwarding\n\
      option dest 'lan'\n\
      option src 'wifi'"

  cd ~/
  wget http://pastebin.com/raw.php?i=ExV4hfJH
  mv raw.php?i=ExV4hfJH /etc/config/firewall2
  
  #echo "Creating Mobile Firewall Settings"
  #echo -e $firewall >> /etc/config/firewall2
}

createMobileDHCP(){
  dhcp="config dnsmasq\n\
      option domainneeded '1'\n\
      option boguspriv '1'\n\
      option filterwin2k '0'\n\
      option localise_queries '1'\n\
      option rebind_protection '1'\n\
      option rebind_localhost '1'\n\
      option local '/lan/'\n\
      option domain 'lan'\n\
      option expandhosts '1'\n\
      option nonegcache '0'\n\
      option authoritative '1'\n\
      option readethers '1'\n\
      option leasefile '/tmp/dhcp.leases'\n\
      option resolvfile '/tmp/resolv.conf.auto'\n\n\

    config dhcp 'lan'\n\
      option interface 'lan'\n\
      option start '100'\n\
      option limit '150'\n\
      option leasetime '12h'\n\n\

    config dhcp 'wan'\n\
      option interface 'wan'\n\
      option ignore '1'\n\n\

    config dhcp\n\
      option start '100'\n\
      option leasetime '12h'\n\
      option limit '150'\n\
      option interface 'wifi'"\n\

  cd ~/
  wget http://pastebin.com/raw.php?i=2PuXburN
  mv raw.php?i=2PuXburN /etc/config/dhcp2

  #echo "Creating Mobile DHCP Settings"
  #echo -e $dhcp >> /etc/config/dhcp2
}

#flashRouter(){}

#function that creates the coova chilli defaults configuration file
setCoovaConfig(){
  nas_id=$1
  wanif=$2
  lanif=$3
  echo "NAS_ID:" "$nas_id"
  echo "WANIF:" "$wanif"
  echo "LANIF:" "$lanif"

  default="HS_LOC_NAME=\"wifination\"\n\
  HS_NASID=\"${nas_id:-'nas01'}\"\n\n\
  HS_WANIF=${wanif:-'eth0'}\n\
  HS_LANIF=${lanif:-'wlan0'}\n\
  HS_UAMPORT=3990\n\
  HS_UAMUIPORT=4990\n\n\
  HS_NETWORK=192.168.182.0\n\
  HS_NETMASK=255.255.255.0\n\
  HS_UAMLISTEN=192.168.182.1\n\
  HS_DYNIP=192.168.182.0\n\
  HS_DYNIP_MASK=255.255.255.0\n\n\
  HS_UAMHOMEPAGE=\"\"\n\
  HS_UAMFORMAT=\"http://wifination.ph/wifination/demo\"\n\
  HS_PROVIDER=\"WifiNation\"\n\
  HS_PROVIDER_LINK=\"http://wifination.ph/\"\n\n\
  HS_MODE=hotspot\n\
  HS_TYPE=chillispot\n\
  hs_lan_access=\"deny\"\n\n\
  #RADIUS CONFIG\n\
  HS_AAA=\"radius\"\n\
  HS_RADIUS=radius1.wifination.ph\n\
  HS_RADIUS2=radius2.wifination.ph\n\
  HS_RADSECRET=\"wifination123\"\n\n\
  HS_UAMSERVER=\"wifination.ph\"\n\
  HS_UAMSECRET=\"wifination123\"\n\
  HS_UAMALLOW=\"192.168.0.0/16 192.168.182.0/24\"\n\
  HS_UAMDOMAINS=\".facebook.com .facebook.net .fbcdn.net .apple.com captive.apple.com appleiphonecell.com wifination.ph\"\n\n\
  HS_DEFSESSIONTIMEOUT=1800"
  rm /etc/chilli/defaults
  echo "Creating /etc/chilli/defaults file"
  echo -e $default >> /etc/chilli/defaults
}

#function that creates the init.d file and symbolic link
setInitd (){
  wget http://pastebin.com/raw.php?i=dzpNYHcX
  echo "Downloading and Creating init.d file: /etc/init.d/chilli"
  mv raw.php?i=dzpNYHcX /etc/init.d/chilli
  echo "Adding executable permission to /etc/init.d/chilli"
  chmod a+x /etc/init.d/chilli
  echo "Creating symbolic link to /etc/rc.d/"
  ln -s /etc/init.d/chilli /etc/rc.d/S60chilli
}

showBanner (){
  echo "============================================================"
  echo "        .__  _____.__                 __  .__               "
  echo "__  _  _|__|/ ____\__|   ____ _____ _/  |_|__| ____   ____  "
  echo "\ \/ \/ /  \   __\|  |  /    \\\__  \\\   __\  |/  _ \ /    \ "
  echo " \     /|  ||  |  |  | |   |  \/ __ \|  | |  (  <_> )   |  \\"
  echo "  \/\_/ |__||__|  |__| |___|  (____  /__| |__|\____/|___|  /"
  echo "                            \/     \/                    \/ "
  echo "Install script for WiFi Nation powered routers"
  echo "@author ibaguio"
  echo "============================================================"
  echo
}

installCoova(){
  echo "Updating opkg"
  opkg update
  echo "Installing coova-chilli"
  opkg install coova-chilli
  echo "Coova-chilli installed"
}

installMobile(){
  opkg install comgt kmod-usb2 kmod-usb-ohci kmod-usb-uhci 
  opkg install kmod-usb-serial kmod-usb-serial-option kmod-usb-serial-wwan
  opkg install usb-modeswitch usb-modeswitch-data sdparm
  opkg install luci-proto-3g
}
#updateConfig(){}

main(){
  local ismobile
  showBanner

  #ask for router name
  while true; do
    read -p "Input Router Name: " nas_id
    if [ "$nas_id" == "" ]; then
      echo "Invalid Router Name"
    else
      break
    fi
  done

  #ask if this is a mobile router
  while true; do
    read -p "Is this a mobile router?(y/n): " yn
    case $yn in
        [Yy]* ) ismobile=true; break;;
        [Nn]* ) ismobile=false; break;;
        * ) echo "Please answer yes or no.";
    esac
  done

  if $ismobile; then
    wanif='3g-wan'
    lanif='wlan0'
  else
    wanif='eth0'
    lanif='wlan0'
  fi

  installCoova
  if $ismobile; then
    installMobile
  fi

  setCoovaConfig "$nas_id" "$wanif" "$lanif"
  setInitd
}

main