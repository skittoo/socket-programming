# Pythonic Linux Server Service For Fast Data Retrieval
## IP:PORT ==> 65.109.10.37:5557

## Creating Daemon Service 
1) sudo ln -s /root/python_socket/server_service.service  /usr/lib/systemd/system/server_service.service
2) sudo systemctl daemon-reload
3) sudo systemctl start server_service.service
