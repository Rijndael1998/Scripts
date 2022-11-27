#!/bin/bash
locaddr=$1
locport=$2
destaddr=$3
destport=$4
inter=$5
 
#echo local addresss: $locaddr
#echo local port: $locport
#echo destination address: $destaddr
#echo destination port: $destport
#echo interface: $inter
 
if [ $(($inter)) == "" ]; then
  echo interface empty!
  inter="enp8s0"
fi
 
 
echo iptables -t nat -A PREROUTING -i $inter -p tcp -m tcp --dport $locport -j DNAT --to-destination $destaddr:$destport
echo iptables -t nat -A POSTROUTING -o $inter -j SNAT --to-source $locaddr