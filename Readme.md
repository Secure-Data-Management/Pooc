# POOC
Mpeck


https://github.com/playerxq/ABKS-demo

https://github.com/blynn/pbc

https://jhuisi.github.io/charm/toolbox/pairinggroup.html

https://github.com/alanbaby/Cipherchain



On windows use WSL and install python 3.6 to 3.8 (no other version than those 3)
then install pybc

sudo apt-get install libgmp-dev curl git wget build-essential flex bison python3 python3-pip
wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xvf pbc-0.5.14.tar.gz
cd pbc-0.5.14
./configure --prefix=/usr --enable-shared
make
sudo make install
sudo ldconfig
cd ..
git clone https://github.com/debatem1/pypbc
cd pypbc
edit pypbc.h (add #define PY_SSIZE_T_CLEAN at the top)
sudo pip3 install .