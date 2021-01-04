
# OTP

The purpose of this application is:

* Generate directory in the form "0000", "0001" ..., each containing 99 files * 3. Each file is a pad. There are three types of pad: prefix, central, suffix. 
These pad are filled with random numbers. I used urandom rather than random, because due to the large number of files generated, urandom generated them faster. A directory named [directory]-receiver represents the recipient's file. It's a copy of the directory [directory].

To run the build command use :
```python3 main.py [directory]```

* send a message. For that you have three possibilities, write a text with the argument -t in prefix, read a file with the argument -f in prefix, or do not put any argument. In this case you will be asked to enter a message. Don't forget to specify the folder with which you want to encode your message. Once the pad C is used, it is removed in the directory of the sender. It cannot be used anymore.   
The encoded message will be stored in a file with the name [directory]-[0000-9999]-[00-99]t at the root of the main.py

To run the build command use :
```python3 main.py [directory] -s [-t or -f or nothing]```

  
* receive a message. For that you must specify the directory to use, in this case it will take the form [directory]-receiver /.
The decoded message will be stored in a file with the name [directory]-receiver-[0000-9999]-[00-99]m at the root of the main.py. Once the message is decoded the pad P and C are removed in the directory of the receiver.

To run the build command use :
```python3 main.py [directory] -r [file]```
