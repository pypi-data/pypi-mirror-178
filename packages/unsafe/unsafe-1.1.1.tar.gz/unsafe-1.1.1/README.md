# unsafe

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Ahur4, MesutFD (™) 2022

## Examples of How To Use (Buggy Alpha Version)

* Hashing a Text with Different Methods

```python

>>> from unsafe import Encryptor
>>> enc = Encryptor()

>>> #all arguments except words are optional
>>> #hash a text
>>> my_md5 = enc.text_encrypt(words='YOUR WORD TO HASH', encode='UTF-8', hash_method='MD5')
>>> my_md5
'28488a21527473bec901c7cc2bfbd76b'
>>> my_shake128 = enc.text_encrypt(words='YOUR WORD TO HASH', encode='UTF-8', hash_method='SHAKE128', count = 22)
>>> my_shake128
'5f75455db6b0b3652f20cd6d67972a67746631f3a562'
>>> my_base64 = enc.text_encrypt(words='YOUR WORD TO HASH', encode='UTF-8', hash_method='BASE64')
>>> my_base64
b'WU9VUiBXT1JEIFRPIEhBU0g='

#hash a file
>>> my_md5_file = enc.file_encrypt(filename='unsafe.txt', encode='UTF-8', hash_method='MD5')
```

* Hash Cracking and Decode a Encrypted Text

```python

>>> from unsafe import Decrypter
>>> dec = Decrypter()

>>> #all arguments except words are optional
>>> #hash a text
>>> my_decrypted_md5 = dec.text_decrypt(hash='28488a21527473bec901c7cc2bfbd76b', words='YOUR WORD TO HASH', hash_method='MD5')
>>> my_decrypted_md5
'YOUR WORD TO HASH'
>>> my_decrypted_shake128 = dec.text_decrypt(hash='5f75455db6b0b3652f20cd6d67972a67746631f3a562', words='Wrong Words', hash_method='SHAKE128')
>>> #return a empty string when encrypted words dont match to hash
>>> my_decrypted_shake128
''
>>> my_decrypted_base64 = dec.text_decrypt(hash=b'WU9VUiBXT1JEIFRPIEhBU0g=', hash_method='BASE64')
>>> my_decrypted_base64
'YOUR WORD TO HASH'
```

* Collecting Proxies and Check Their Health.

```python

>>> from unsafe import Proxy
>>> proxy = Proxy()
>>> my_proxy_dict = proxy.wrapper(protocol='http', max_ping=200)
>>> my_proxy_dict
{'ip':'port', 'ip':'port', ...}
>>> check_proxy = proxy.checker(proxy_host='127.0.0.1', proxy_port='80', protocol='http', timeout=10)
>>> check_proxy
True
```

* Find Admin Panel.

```python

>>> from unsafe import BruteForcer
>>> brute = BruteForcer()
>>> a = brute.admin(domain='mohammadii.com', timeout=10, ext='php')
>>> a
{'http://example.com': ['http://example.com/wp-login.php']}

```
 
