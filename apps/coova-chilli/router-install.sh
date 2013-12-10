#!/bin/bash
#install script for wifination routers
#@author ibaguio

function setConfig {
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
  HS_UAMDOMAINS=\"www.facebook.com .facebook.net .fbcdn.net .pixel.facebook.com .ak.facebook.com error.facebook.com apps.facebook.com beta.facebook.com\"\n\n\
  HS_DEFSESSIONTIMEOUT=1800"
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
  opkg update
  opkg install coova-chilli
}

function updateConfigMobile{

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

  echo -e $default >> out.txt  
}

main