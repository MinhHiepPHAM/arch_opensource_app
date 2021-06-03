import socket as sk

def communicate(host, port, request):
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.connect((host, port))
    s.send(request)
    response = s.recv(1024)
    s.close()
    return response
