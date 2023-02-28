import socket
import sys
import time
import os

# The animation of printing
def text_out(text: str) -> None:
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
        
        
class file:
    def separate(data):
        texts=data.split("<_SEPARATOR_>")
        datas=texts[0]
        ext=texts[1]    
        return datas,ext
        
    def compress(contents,filename):
       message=contents+"<_SEPARATOR_>"+filename
       return message
       
    def findExtension(file):
        if "/" in file:
            splitted=file.split("/")
            filename=splitted[-1:]
            return filename[0]
        else:
            filename=file
            return filename
            
    def openFile(file_dir,ext):
       extAll=ext.split(".")
       extension=extAll[1]
       all="jpg jpeg gif JPEG tiff mp4 mp3 dox ppx avi pdf wav ogg zip bin csv exe ico svg bat dat sql tar gz "
       if extension in all:
           return ''
       else:
           f=open(file_dir,"rt")
           contents=f.read()
       return contents


host=input("Enter Your server Name:: ")
if host=="":
    host="localhost"
    text_out("Default:: localhost")
    print("")
else:
    pass

port=5050
bufferSize=1048576


server=socket.socket()
server.bind((host,port))

text_out("Waiting  connections from clients...")

server.listen(2)
conn, addrs=server.accept()
os.system("clear")
text_out(f"A server connected to {addrs}")
print("")

print("\n\n")
text_out("         WAITING A MESSAGE FROM THE CLIENT !!!")
print("")

while True:
  try:
    # RECEIVING 
    data=conn.recv(bufferSize).decode()
    text_out("MESSAGE FROM CLIENT: ")
    received=str(data)
    if(received=="STOPPED"):
       text_out("\n        It seems client has some problem\n         connecting....")
       print("")
       break
    elif type(received) is bytes:
       print("bit file received")
       
    if type(received) is str:
     print("normal file received")
     compare=int(received.find("<_SEPARATOR_>"))
     if(compare>=0):
      contents,filename=file.separate(received)
      text_out(f"\n        THE FILE HAS BEEN RECEIVED - {filename} ")
      print("")
      file_path=input("     Where should the file be saved? \n     Default is Present Directory:: ")
      if(file_path==""):
         try:
             print(f"Trying openfile...{filename}")
             f=open(filename,"w")
             print("File opened (new) but contents not written")
             f.write(f'''{contents}''')
             print("File is written but problem is that it didn't close")
             f.close()
         except:
             conn.send("STOPPED".encode())
             text_out("   Error receiving file from client :: Present Directory!!")
             print("")
             break
         text_out("    File received at the current directory!!")
         print("")
      else:
         full=filepath+filename
         try:
             f=open(full,"w")
             f.write(f'''{contents}''')
             f.close()
         except:
             conn.send("STOPPED".encode())
             text_out(f"   Error receiving file from client :: at {full}!!")
             print("")
             break
         text_out(f"     {filename} saved! ")
         print("")
     else:
      text_out(received)
      print("")
    else:
      prin  
      
      
    # SENDING 
    message=input("MESSAGE to CLIENT:: ")
    message=f'''{message}'''
    if(message=="quit" or message=="q"):
        conn.send("STOPPED".encode())
        text_out("     [ 200 ] :: server shutteddown conditionally!!")
        print("")
        break
    elif(message=="file"):
       # when wanting to send files
       try:
          file_dir=input("         [File-Name]:: ")
          extension=file.findExtension(file_dir)
          contents=file.openFile(file_dir,extension)
          if(contents==''):
              print('')
              text_out("     [ 403 ] :: The type of the file you want to send is forbidden!!")
              print('')
              conn.send("STOPPED".encode())
              break
          message=file.compress(contents,extension)
       except:
          #using this in debug mode
          conn.send("STOPPED".encode())
          text_out("No such File or Directory!!")
          print("")                                        
          break
    
    conn.send(message.encode())
  except KeyboardInterrupt:
    conn.send("STOPPED".encode())
    text_out("  [ 200 ] :: Turning off server...")
    print("")
    break  
    
    
conn.close()
text_out("   [ 200 ] :: The server turned off successfully!!")
print("")
server.close()
