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
