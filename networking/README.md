
sudo iptables -t nat -I OUTPUT -p tcp -m owner \! --uid-owner mitmproxy --dport 80 -j DNAT --to 127.0.0.1:8080; \
sudo iptables -t nat -I OUTPUT -p tcp -m owner \! --uid-owner mitmproxy --dport 443 -j DNAT --to 127.0.0.1:8080

sudo iptables -I OUTPUT -m owner \! --uid-owner mitmproxy --dport 443 -j REDIRECT --to-port 10052
sudo iptables -t nat -I OUTPUT -p tcp -m owner \! --uid-owner mitmproxy -j REDIRECT --to 127.0.0.1:10052

sudo iptables -t nat -I OUTPUT -p tcp -m owner \! --uid-owner mitmproxy --dport 80 -j DNAT --to 127.0.0.1:10052

iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner proxy --dport 80 -j REDIRECT --to-port 3128

sudo -u mitmproxy mitmweb --transparent -wport=11152 --wiface=eth0 --wfile=mitm_res.out --wdebug --port 10052 && sudo iptables -t nat -F; \

    
sudo iptables -t nat -I PREROUTING 1 -p tcp --match multiport --dports 80,443 -j REDIRECT --to-port 8080
sudo iptables -t nat -I OUTPUT 1 -o eth0 -p tcp --match multiport --dports 80,443 -j REDIRECT --to-port 8080