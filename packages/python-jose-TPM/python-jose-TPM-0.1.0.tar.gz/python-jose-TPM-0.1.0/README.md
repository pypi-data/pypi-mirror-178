# python-jose-TPM

A JOSE implementation in Phython that uses a TPM for crpytographic operations.

## General information

This package depends on the [tpm2-pytss](https://github.com/tpm2-software/tpm2-pytss) library. Go to https://tpm2-pytss.readthedocs.io/en/latest/install.html and look how to set it up.

## Installation 

```
$ pip install python-jose-TPM
```

## Usage

```python
from python_jose_TPM import jwe, jwt
```
## Supported Algorithms

For JWS the following signature algorithms (`alg` parameter values) are supported:
- RS256

For JWE the following content encryption key algorithms (`alg` parameter values) are supported: 
- DIR
- RSA1_5

For JWE the following content encryption algorithms (`enc` parameter values) are supported:
- A128CBC-HS256

More algorithms will be implemented in the future. 

## Thanks

This library is based on the work of [python-jose](https://github.com/mpdavis/python-jose) from Michael Davis.