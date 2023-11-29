## 🔐 Password Manager 🛡️

[![Python: 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


### Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Options](#command-line-options)
- [Contribution](#contributing) 
- [Security](#security) 
- [License](#license) 
- [Versioning](#versioning)
- [Contact](#contact)


### Overview

**PassMe** is an open-source Password Manager Tool written in Python 3. It securely generates and stores complex passwords, supporting custom and randomly generated passwords. It also includes features for key management, account creation, and password rotation.

### Features
- **Strong Encryption**: Utilizes industry-standard Fernet encryption for secure password storage.
- **User-Friendly Interface**: Interactive command-line interface for ease of use.
- **Account Management**: Supports account creation, username association, and password updates.
- **Key Rotation**: Implements key rotation for enhanced security.

### Getting Started

1. Clone the repository.

    ```bash
    git clone https://github.com/aniketchavan2211/Password-Manager.git
    cd Password-Manager
    ```

2. Install dependencies.

    ```bash
    pip install -r requirements.txt
    ```
   (Till yet no requirements.txt is uploaded.)

3. Run the Password Manager.

    ```bash
    python3 main.py
    ```

4. Follow the on-screen instructions to manage your passwords.


### Installation 
1. Clone the git repo 

```bash
git clone https://github.com/aniketchavan2211/Password-Manager.git
```

2. Navigate to downloaded directory 

```bash
cd Password-Manager
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

or 

```bash
python3 -m pip install -r requirements.txt 
```

### Usage

1. Run the Password Manager: 

```bash
python3 main.py
```

#### Run directly
```bash
# Give executable permission
chmod +x main.py

# Run
./main.py
```

2. Follow the on-screen instructions to manage your passwords.

### Command-Line Options

- **-h**, **--help**: Display help menu.
- **-g**, **--generate**: Generate a random password.
- **-u**, **--username**: Specify the username for actions.
- **-cs**, **--create-account**: Create a new user account.
- **-c**, **--create**: Create a new password entry.
- **-s**, **--show**: Show a stored password.
- **-k**, **--gen-key**, -generate-key: Generate a new Fernet key.
- **-i**, **--import-key filename**: Import a Fernet key from a file.
- **-e**, **--export-key filename**: Export the Fernet key to a file.
- **-r**, **--rotate-key**: Rotate the encryption key.

### Contributing

We welcome contributions to enhance and improve the Password Manager. If you'd like to contribute, please review our [Contribution Guidelines](CONTRIBUTING.md).

### Security

For information on security updates, reporting vulnerabilities, and our security policy, refer to [Security Guide](SECURITY.md).

### License

The Password Manager project is licensed under the [MIT License](LICENSE).

### Versioning

We use Semantic Versioning for this project. For a complete list of changes, see [Release Notes](CHANGELOG.md).


### Contact

If you have any questions or suggestions, feel free to reach out to Aniket Chavan via [Email](mailto:aniketchavan2211@gmail.com) or on [Twitter](https://twitter.com/Aniket86002211).
[Instagram](https://instagram.com/aniket_chavan_2211)
