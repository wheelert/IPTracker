#!/bin/bash

APPDIR=/usr/share/IPTracker

echo -e "\e[33m [ Checking for previous versions]\e[0m"
if [ -d "$APPDIR" ]; then
    rm -rf $APPDIR
fi



echo -e "\e[32m [ Installing IPTracker ]\e[0m"
mkdir $APPDIR
cp *.py $APPDIR
cp *.pyw $APPDIR
cp data.sqlite $APPDIR
cp -R gui $APPDIR
cp iptracker.png $APPDIR
cp IPTracker.desktop /usr/share/applications/
