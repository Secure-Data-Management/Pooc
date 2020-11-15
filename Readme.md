# PrOOf of Concept

## Installation

Pre requisite: Linux system (can be also wsl, wsl2, docker)

You first need to install pypbc for that you need to follow those instruction:
```shell script
sudo su <<ROOT
apt-get install -yqq --no-install-recommends libgmp-dev curl git wget build-essential flex bison python3 python3-pip
wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xvf pbc-0.5.14.tar.gz
cd pbc-0.5.14
./configure --prefix=/usr --enable-shared
make
make install
ldconfig
cd ..
git clone https://github.com/debatem1/pypbc
cd pypbc
(echo "#define PY_SSIZE_T_CLEAN" && cat pypbc.h) > pypbc.h.temp && mv pypbc.h.temp pypbc.h
pip3 install .
cd ..
rm -r pypbc pbc-0.5.14 pbc-0.5.14.tar.gz
ROOT
```

Once this is done the last line should be `Successfully installed pypbc-0.2`

If it is not make sure that you have indeed installed the required libraries without error, that you are using a recent linux version and 
that no file were conflicting with your installation process (you might want to do it line by line then)

Run `pip3 install -r requirements.txt`

## Running

You can simply run: `python3 test.py`

You should get:
```md
Client 0: decryption is: This is the message
Client 1: decryption is: This is the message
(0x1941044B179D046D7647F9F2F23ABC602E0F9AB66110D6DCC7823D2102258E034EDB743281CD5CEFBFA1CA939D319D73AA7593C5E0B7ACF972DFF02DF01849F1, 0x3A19D7B3A56A274E657810AF2BB3E8561AC93F70788881E628CBD3540D511592642B6989A79A8266076DC4B1ADB3B089FECC7071AC52651C5ACCEB8F3960623B)
(0x1941044B179D046D7647F9F2F23ABC602E0F9AB66110D6DCC7823D2102258E034EDB743281CD5CEFBFA1CA939D319D73AA7593C5E0B7ACF972DFF02DF01849F1, 0x3A19D7B3A56A274E657810AF2BB3E8561AC93F70788881E628CBD3540D511592642B6989A79A8266076DC4B1ADB3B089FECC7071AC52651C5ACCEB8F3960623B)
1
```

Which tells you that the message for client 0 and 1 was successfully decrypted and that the server test was too for the given keyword.