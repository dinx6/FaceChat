import cv2
import io
import numpy
from PIL import Image
import socket
import threading
cap=cv2.VideoCapture(0)

#       Creating server and listening on port provided
def inet_connect(serverport):

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.bind(('',serverport))

    s.listen(5)

    print("Wait...")

    while True:
        (client,(ip,port))=s.accept()

        print("Connection Established with :",ip,":",port)

        threading.Thread(target = sendAndReceive,args = (client,ip)).start()

#       Regularly sends and receives data
def sendAndReceive(client,ip):

    while True:

        vreceive(client,ip)

        send(client,ip)

#       First receiving size of the frame or data to receive and the data
def vreceive(sock,ip):

    totrec=0

    msgArray = bytearray()

    c= sock.recv(8)

    c=c.decode()

    length=int(c)

    while totrec < length:
        chunk = sock.recv(length - totrec)

        msgArray.extend(chunk)

        totrec+=len(chunk)

    show(msgArray,ip)

#       First sending the size of the frame and then the frame
def vsend(framestring,sock):

    totalsent = 0

    metasent = 0

    length =len(framestring)

    lengthstr=str(length).zfill(8)

    sent = sock.send((lengthstr).encode())

    sock.sendall(framestring)

#       Showing send frames(images)mySelfShowmySelfShowmySelfShow
def mySelfShow(im_b):

    p=io.BytesIO(im_b)

    pi=Image.open(p)

    img = cv2.cvtColor(numpy.array(pi), cv2.COLOR_RGB2BGR)

    cv2.imshow('Me',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        cap.release()

        cv2.destroyAllWindows()

#       showing received frames(images)
def show(im_b,ip):

    p=io.BytesIO(im_b)

    pi=Image.open(p)

    img = cv2.cvtColor(numpy.array(pi), cv2.COLOR_RGB2BGR)

    cv2.imshow(ip,img)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        cap.release()

        cv2.destroyAllWindows()


#       Capturing and sending frames(images)
def send(client,ip):

    ret,img=cap.read()

    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    pimg=Image.fromarray(img)

    b=io.BytesIO()

    pimg.save(b,'jpeg')

    im_b=b.getvalue()

    mySelfShow(im_b)

    vsend(im_b,client)


#       Taking port to create server
serverport=int(input("Enter port :"))

inet_connect(serverport)
