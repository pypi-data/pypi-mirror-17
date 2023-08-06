#!/bin/bash

set -e

if [[ "$OSTYPE" == "darwin"* ]]; then
	cd libvncserver
	make clean
#	rm /usr/local/lib/libvnc* || # yay
#	rm /usr/local/include/rfb || # yay
	brew install openssl
	./libserver-configure.mac --with-ssl=/usr/local/opt/openssl
	make
	make install
fi