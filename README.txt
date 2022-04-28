IPTracker is a simple IP Scanner that allows you to scan a connected network of ips and 
identify ips in use and keep notes on the ips. You can manage multiple networks. 

Install video https://youtu.be/n-P9D8ekjcQ

[requirements]
Docutils
pyQT5 
python-nmap

[Running]
Once the dependancies are installed you can run IPTracker by double clicking IPTracker.pyw




[Development bulding notes]
[Generate UI]
pyuic5 -x addsubnet.ui -o addsubnet_ui.py

[Build UI]
python setup.py build_ui

[Install]

pip3 install --user -e .



