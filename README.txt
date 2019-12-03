[requirements]
pyQT5 
python-nmap


[Generate UI]
pyuic5 -x addsubnet.ui -o addsubnet_ui.py

[Build UI]
python setup.py build_ui

[Install]

pip3 install --user -e .



