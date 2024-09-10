#!/bin/bash

# Get the output of ip route and extract the interfaces
routes=$(ip route show table main | grep -Eo 'dev (eth[0-9]+)' | awk '{print $2}' | sort | uniq)

# Counter for routing tables
table_id=100

# Create routing rules and tables for each interface
for iface in $routes; do
    # Get the IP associated with the interface
    ip_address=$(ip addr show $iface | grep -Eo 'inet [0-9.]+/[0-9]+' | awk '{print $2}' | cut -d'/' -f1)
    if [ -n "$ip_address" ]; then
    
         # Get the network range for the interface
        network_range=$(ip route show dev $iface | grep -Eo '[0-9.]+/[0-9]+' | awk '{print $1}' | cut -d'/' -f1)

        # Compute the gateway (assuming gateway is the network range with last octet as .1)
        IFS='.' read -r -a octets <<< "$network_range"
        gateway="${octets[0]}.${octets[1]}.${octets[2]}.1"

        # Add routing rules
        echo "Configuring $iface with IP $ip_address and table $table_id"
        sudo ip rule add from $ip_address table $table_id
        sudo ip route add default via $gateway dev $iface table $table_id
        table_id=$((table_id + 1))
    fi
done

# Confirm routing rules
echo "List of routing rules:"
ip rule list

echo "Routing setup completed."
