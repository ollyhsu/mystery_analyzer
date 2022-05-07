## Info

Mystery Solidity analyzer is an automated security vulnerability audit tool for smart contracts based on [Mythril](https://github.com/ConsenSys/mythril) and [Slither](https://github.com/crytic/slither)

## Requirements

- Install Ethereum Compiler solc:

For Ubuntu:

```
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc
```

- Install Xdot:

```
apt-get install python3 python3-pip 
apt install gir1.2-gtk-3.0 python3-gi python3-gi-cairo python3-numpy graphviz
apt install xdot
```

- Install pip requirements:

```
pip3 install -r requirements.txt
```

## Usage

```
python manage.py runserver 8000
```