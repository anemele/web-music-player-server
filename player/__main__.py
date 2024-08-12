from .app import app

DEBUG = False
PORT = 80

if DEBUG:
    host = 'localhost'
else:
    import socket
    import subprocess

    import qrcode

    host = socket.gethostbyname(socket.gethostname())
    tmp = 'qrcode.png'

    qrcode.make(host).save(tmp)
    print(tmp)
    subprocess.run(f'start {tmp}', shell=True)

app.run(host=host, port=PORT, debug=DEBUG)
