#!/bin/bash
#install script for wifination routers
#@author ibaguio

#function that creates the wireless networks & interfaces
function createWireless {

}

function flashRouter{

}

#function that creates the coova chilli defaults configuration file
function setCoovaConfig { 
  nas_id=$1
  wanif=$2
  lanif=$3
  echo nas_id
  echo wanif
  echo lanif

  default=$"HS_LOC_NAME=\"wifination\"\n\
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
  HS_UAMFORMAT=\"http://107.22.209.59/wifination/authenticate\"\n\
  HS_PROVIDER=\"WifiNation\"\n\
  HS_PROVIDER_LINK=\"http://wifination.ph/\"\n\n\
  HS_MODE=hotspot\n\
  HS_TYPE=chillispot\n\
  hs_lan_access=\"deny\"\n\n\
  #RADIUS CONFIG\n\
  HS_AAA=\"radius\"\n\
  HS_RADIUS=107.22.209.59\n\
  HS_RADIUS2=107.22.209.59\n\
  HS_RADSECRET=\"wifination123\"\n\n\
  HS_UAMSERVER=\"wifination.ph\"\n\
  HS_UAMSECRET=\"wifination123\"\n\
  HS_UAMALLOW=\"107.22.209.59 192.168.0.0/16 192.168.182.0/24\"\n\
  HS_UAMDOMAINS=\".facebook.com .facebook.net .fbcdn.net .apple.com captive.apple.com appleiphonecell.com\"\n\n\
  HS_DEFSESSIONTIMEOUT=1800"
  echo "Creating /etc/chilli/defaults file"
  echo -e $default >> /etc/chilli/defaults
}

#function that creates the init.d file and symbolic link
function setInitd {
  initd=$'#!/bin/sh /etc/rc.common\n\
  START=60\n\
  STOP=90\n\

  NAME=chilli\n\
  RUN_D=/var/run\n\
  CMDSOCK=$RUN_D/$NAME.sock\n\
  PIDFILE=$RUN_D/$NAME.pid\n\

  option_cb() { [ -n "$2" ] && echo "HS_$(echo $1|tr \'a-z\' \'A-Z\')=\"$2\"" | sed \'s/\$/\\\$/g\'; }\n\
  config_load hotspot > /etc/chilli/config\n\

  . /etc/chilli/functions\n\

  start() {\n\
   HS_DNS_DOMAIN=${HS_DNS_DOMAIN:-cap.coova.org}\n\
   HS_USELOCALUSERS=${HS_USELOCALUSERS:-off}\n\
   HS_PROXY_TYPE=${HS_PROXY_TYPE:-none}\n\
   HS_DEFSESSIONTIMEOUT=${HS_DEFSESSIONTIMEOUT:-1800}\n\
   HS_DEFIDLETIMEOUT=${HS_DEFIDLETIMEOUT:-0}\n\
   HS_DEFINTERIMINTERVAL=${HS_DEFINTERIMINTERVAL:-300}\n\
   HS_LAN_ACCESS=${HS_LAN_ACCESS:-deny}\n\
   HS_PROVIDER=${HS_PROVIDER:-Coova}\n\
   HS_PROVIDER_LINK=${HS_PROVIDER_LINK:-http://coova.org/}\n\
   HS_LOC_NAME=${HS_LOC_NAME:-My HotSpot}\n\
   HS_LOC_NETWORK=${HS_LOC_NETWORK:-wifination}\n\
   HS_OPENIDAUTH=${HS_OPENIDAUTH:-off}\n\
   HS_ANYIP=${HS_ANYIP:-off}\n\

   [ -z "$HS_LANIF" ] && {\n\
       [ -e /tmp/device.hotspot ] && {\n\
           stop\n\
       }\n\
       HS_LANIF=$(wlanconfig ath create wlandev wifi0 wlanmode ap)\n\
       for i in 0 1 2 3 4; do ifconfig ath$i mtu 1500; done 2>/dev/null\n\
       echo $HS_LANIF > /tmp/device.hotspot\n\
       iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\n\
       iwconfig $HS_LANIF essid ${HS_SSID:-Coova} 2>/dev/null\n\
   }\n\

   writeconfig\n\
   radiusconfig\n\
                                                                                      
   [ -d $RUN_D ] || mkdir -p $RUN_D\n\

   /sbin/insmod tun >&- 2>&-\n\
   /usr/sbin/chilli\n\
  }\n\

  stop() {\n\
   [ -f $PIDFILE ] && kill $(cat $PIDFILE)\n\
   rm -f $PIDFILE $LKFILE $CMDSOCK 2>/dev/null\n\
   iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE\n\
   wlanconfig $(cat /tmp/device.hotspot) destroy\n\
   rm /tmp/device.hotspot\n\
  }'
  echo "Creating init.d file: /etc/init.d/chilli"
  echo -e $initd >> /etc/init.d/chilli
  echo "Adding executable permission to /etc/init.d/chilli"
  chmod a+x chilli
  echo "Creating symbolic link to /etc/rc.d/"
  ln -s /etc/init.d/chilli /etc/rc.d/S60chilli
}

function showBanner {
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

function installCoova{
  echo "Updating opkg"
  opkg update
  echo "Installing coova-chilli"
  opkg install coova-chilli
  echo "Coova-chilli installed"
}

function updateConfigMobile{
  opkg install usb-modeswitch
  opkg install usb-modeswitch-data
}

function updateConfig{
  
}

function main {
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
  setCoovaConfig $nas_id $wanif $lanif
  setInitd

}

main