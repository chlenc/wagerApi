import base64
from Crypto.Cipher import AES

msg_text = b'test some plain text here'.rjust(32)
secret_key = b'1234567890123456'

cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously
encoded = base64.b64encode(cipher.encrypt(msg_text))
print(encoded)
decoded = cipher.decrypt(base64.b64decode(encoded))
print(decoded)