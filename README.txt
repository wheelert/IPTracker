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



