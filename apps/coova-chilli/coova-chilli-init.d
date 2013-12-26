#!/bin/sh /etc/rc.common
START=60
STOP=90

NAME=chilli
RUN_D=/var/run
CMDSOCK=$RUN_D/$NAME.sock
PIDFILE=$RUN_D/$NAME.pid

option_cb() { [ -n "$2" ] && echo "HS_$(echo $1|tr 'a-z' 'A-Z')=\"$2\"" | sed 's/\$/\\\$/g'; }
config_load hotspot > /etc/chilli/config

. /etc/chilli/functions

start() {
 HS_DNS_DOMAIN=${HS_DNS_DOMAIN:-cap.coova.org}
 HS_USELOCALUSERS=${HS_USELOCALUSERS:-off}
 HS_PROXY_TYPE=${HS_PROXY_TYPE:-none}
 HS_DEFSESSIONTIMEOUT=${HS_DEFSESSIONTIMEOUT:-0}
 HS_DEFIDLETIMEOUT=${HS_DEFIDLETIMEOUT:-0}
 HS_DEFINTERIMINTERVAL=${HS_DEFINTERIMINTERVAL:-300}
 HS_LAN_ACCESS=${HS_LAN_ACCESS:-deny}
 HS_LOC_NAME=${HS_LOC_NAME:-WiFiNation}
 HS_LOC_NETWORK=${HS_LOC_NETWORK:-WiFiNation}
 HS_OPENIDAUTH=${HS_OPENIDAUTH:-off}
 HS_ANYIP=${HS_ANYIP:-off}

 [ -z "$HS_LANIF" ] && {
     [ -e /tmp/device.hotspot ] && {
         stop
     }
     HS_LANIF=$(wlanconfig ath create wlandev wifi0 wlanmode ap)
     for i in 0 1 2 3 4; do ifconfig ath$i mtu 1500; done 2>/dev/null
     echo $HS_LANIF > /tmp/device.hotspot
     iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
     iwconfig $HS_LANIF essid ${HS_SSID:-Coova} 2>/dev/null
 }

 writeconfig
 radiusconfig
                                                                                    
 [ -d $RUN_D ] || mkdir -p $RUN_D

 /sbin/insmod tun >&- 2>&-
 /usr/sbin/chilli
}

stop() {
 [ -f $PIDFILE ] && kill $(cat $PIDFILE)
 rm -f $PIDFILE $LKFILE $CMDSOCK 2>/dev/null
 iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
 wlanconfig $(cat /tmp/device.hotspot) destroy
 rm /tmp/device.hotspot
}