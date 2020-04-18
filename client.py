import cv2
import io
import numpy
from PIL import Image
import socket

#import pyaudio
cap=cv2.VideoCapture(0)

#first receiving size of the frame or data to receive and the data
def vreceive(sock):

    totrec=0

    metarec=0

    msgArray = bytearray()

    metaArray = []

    c = sock.recv(8)

    c=c.decode()

    length=int(c)

    while totrec<length :

        chunk = sock.recv(length-totrec)

        msgArray.extend(chunk)

        totrec += len(chunk)

    show(msgArray)

#   first sending the size of the frame and then the frame
def vsend(framestring,sock):

    totalsent = 0

    metasent = 0

    length =len(framestring)

    lengthstr=str(length).zfill(8)#             To make sure that exactly 8 bit of data is being sent and received

    sent = sock.send((lengthstr).encode())#     first length of the data is sent to the server

    sock.sendall(framestring)

#showing send frames(images)
def mshow(im_b):

    p=io.BytesIO(im_b)

    pi=Image.open(p)

    img = cv2.cvtColor(numpy.array(pi), cv2.COLOR_RGB2BGR)

    cv2.imshow('Me',img)

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        cap.release()

        cv2.destroyAllWindows()

#showing received frames(images)
def show(im_b):

    p=io.BytesIO(im_b)

    pi=Image.open(p)

    img = cv2.cvtColor(numpy.array(pi),cv2.COLOR_RGB2BGR)

    cv2.imshow('Friend',img)

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        cap.release()

        cv2.destroyAllWindows()

#capturing and sending frames(images)
def send1(client):

    ret,img=cap.read()

    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    pimg=Image.fromarray(img)

    b=io.BytesIO()

    pimg.save(b,'jpeg')

    im_b=b.getvalue()

    mshow(im_b)

    vsend(im_b,client)

 #creating server and listening on port provided
def inet_connect(ip,serverport):

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect((ip,serverport))

    print("Connection Established with :",ip,":",serverport)

    print("Wait...")

    return s

serverport=int(input("Enter Port:"))

ip = '192.168.43.85'

s=inet_connect(ip,serverport)

#regularly sends and receives data
while True:

    send1(s)

    vreceive(s)
