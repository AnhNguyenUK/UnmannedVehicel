#! /bin/bash

# Number of maximum retry
max_retry=3
# Turning on modem
counter=0
echo "Turning on modem"
until sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='online'
do
    sleep 1
    [[ counter -eq $max_retry ]]  && echo "Failed!" && exit 1
    echo "Trying again. Try #$counter"
    ((counter++))
done
# Check status of modem
echo "Get modem status"
sudo qmicli -d /dev/cdc-wdm0 --dms-get-operating-mode
# Check Signal strength
echo "Get signal strength"
sudo qmicli -d /dev/cdc-wdm0 --nas-get-signal-strength
# Configure raw-ip protocol
sudo ip link set wwan0 down
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up
# Connecting to a mobile network 
counter=0
echo "Connecting to mobile network"
until sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='internet',ip-type=4" --client-no-release-cid
do
    sleep 1
    [[ counter -eq $max_retry ]]  && echo "Failed!" && exit 1
    echo "Trying again. Try #$counter"
    ((counter++))
done
# Assign IP for wwan0
echo Assign IP
counter=0
max_retry=3
until sudo udhcpc -i wwan0
do 
    sleep 1
    [[ counter -eq $max_retry]] && echo 'Failed!!' && exit 1
    echo "Try again. #$counter"
    ((counter++))
done