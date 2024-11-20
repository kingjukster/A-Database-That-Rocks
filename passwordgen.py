import hashlib

passw = input()

salt = "RockyBestMovieEva"
passw = passw + salt

password = hashlib.md5(passw.encode())

print(password.hexdigest())

