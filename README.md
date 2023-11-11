## 🔐 Password Manager 🔐

`PassMe` | `Password Manager Tool` |<br />
`Open Source Python Security Project`

**PassMe** is **Password Manager Tool** use to generate randomly hard complex password and saved them securely, you add custom password  and also features keys manually import, and export and rotate function for better security. 


<br />

```zsh
$ python3 ./main.py -h
usage: main.py [-h] [-g] [-u username] [-cs] [-c] [-s] [-k]
               [-i filename] [-e filename] [-r]               
Password Management Tool

options:                                                        -h, --help            show this help message and exit         -g, --generate        Generate a random password
  -u username, --username username                                                    Specify the username for actions        -cs, --create-account                                                               Create a new account
  -c, --create          Create a new password entry
  -s, --show            Show a stored password
  -k, --gen-key, -generate-key                                                        Generate a new Fernet key
  -i filename, --import-key filename
                        Import a Fernet key from a file
  -e filename, --export-key filename
                        Export the Fernet key to a file         -r, --rotate-key      Rotate the encryption key
```

**Clone git repo by**

```bash
git clone https://github.com/aniketchavan2211/Password-Manager.git
```

**Run script simply by**

```bash
python main.py
python3 main.py
python3 ./main.py
```

**Run directly**
```bash
# Give executable permission
chmod +x main.py

# Run
./main.py
```

### Passing arguments

- help menu

```bash
# short args
python3 main.py -h
```

```bash
#long args
python3 main.py --help
```
