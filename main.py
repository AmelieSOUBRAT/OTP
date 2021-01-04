import argparse
import subprocess
import os

def addZeros(pathName, size):
    '''
    Add zeros to a filename or dirname

            Parameters:
                    pathName (string): name of the directory of file
                    size (int) : number of zeros that be to added to the name

            Returns:
                    pathName (string): the name of the file or directory in the good format
    '''

    while len(pathName) < size:
        pathName = "0" + pathName
    return pathName

def createFile(path, content):
    '''
    Create file

            Parameters:
                    path (string): path of the files
                    content (string) : content for the file
    '''

    newFile = open(path, "w")
    newFile.write(content)
    newFile.close()

def readFile(path):
    '''
    read file

            Parameters:
                    path (string): path of the file to read
            Returns:
                    contentOfFile (string): content of the file
    '''

    file = open(path, "r")
    contentOfFile = file.read()
    file.close()
    return contentOfFile

def generate(dirname):
    '''
    Generate 100 pads in a subfolder of the directory specified in the position argument, the directory must contains less than 9999 directories 

            Parameters:
                    dirname (string): name of the position argument, the directory
    '''

    createDirectory(dirname)
    nbOfFiles = subprocess.check_output("ls -1 "+dirname+" | wc -l", shell = True)
    directoryNumber = addZeros(str(int(nbOfFiles)), 4)
    createDirectory(dirname + "/" + directoryNumber)
    if int(nbOfFiles) < 9999:
        for i in range(100):
            fileNumber = addZeros(str(i), 2)
            path = dirname + "/" + directoryNumber + "/" + fileNumber
            for j in range(3):
                if j == 0:
                    createFile(path + "p", random(48))
                elif j == 1:
                    createFile(path + "c", random(2000))
                else:
                    createFile(path + "s", random(48))

        
        createDirectory(dirname+"-receiver")
        subprocess.call("cp -r "+ dirname + "/" + directoryNumber+ "/ " + dirname +"-receiver/", shell=True)
    else:
        print("Number of file in the directory " + dirname + " is too big: >= 9999")

def random(size):
    '''
    Generate n random binary number 

            Parameters:
                    size (int): size of the list of binary number in bytes
            Returns:
                    listOfRandomNumber (string): list of random binary number
    '''

    listOfRandomNumber = ""
    with open("/dev/urandom", 'rb') as f:       
        for i in range(size):
            listOfRandomNumber += convertIntToBinary8(int.from_bytes(f.read(1), 'big'))
    return listOfRandomNumber

def convertIntToBinary8(number):
    '''
    Convert an integer in base 2

            Parameters:
                    number (int): a integer to convert

            Returns:
                    binaryNumber (string): the convertion of integer in base 2 with 8 bits.
    '''

    binaryNumber = '{0:08b}'.format(number)
    return binaryNumber

def convertIntToBinary9(number):
    '''
    Convert an integer in base 2

            Parameters:
                    number (int): a integer to convert

            Returns:
                    binaryNumber (string): the convertion of integer in base 2 with 9 bits.
    '''

    binaryNumber = '{0:09b}'.format(number)
    return binaryNumber

def convertToAsciiBinary(text):
    '''
    Convert an acsii in base 2

            Parameters:
                    text (string): the text to convert

            Returns:
                    binaryText (string): the convertion of the text in base 2 with 8 bits.
    '''

    binaryText = ""
    for letter in text:
        binaryLetter = convertIntToBinary8(ord(letter))
        binaryText += binaryLetter
    return binaryText


def createDirectory(dirname):
    '''
    Create directory

            Parameters:
                    dirname (string): name of the directory that will be created
    '''
    
    os.makedirs(dirname, exist_ok = True)

def sendText(dirname, text):
    '''
    Encode th text and write it in the file "directory"-"directory2"-"file"t

            Parameters:
                    dirname (string): name of the directory that will be read
                    text (string): the text that will be translated
    '''

    nbFile = subprocess.check_output("ls -1 " + dirname + " | wc -l", shell = True)
    exist = False
    for i in range(int(nbFile)):
        directoryNumber = addZeros(str(i), 4)
        for j in range(100):
            fileNumber = addZeros(str(j), 2)
            path = dirname + "/" + directoryNumber + "/" + fileNumber
            if os.path.exists(path + "c") :
                exist = True
                break
        if exist == True:
            break
    if exist == True :
        padC = readFile(path + "c")

        textEncoded = ""
        for i in range(0, int(len(text)), 8):
            number = int(text[i:i+8], 2) + int(padC[i:i+8], 2)
            textEncoded += convertIntToBinary9(number)
        
        padP = readFile(path + "p")
        padS = readFile(path + "s")
        textInFileT = padP + textEncoded + padS
    
        createFile(dirname+"-"+directoryNumber+"-"+fileNumber+"t", textInFileT)
        subprocess.call("rm " + path + "c", shell = True)
    else:
        print("Please, choose an other directory, there is no more pad C")

    
def receiveText(dirname, text):
    '''
    Decode th text and write it in the file "directory"-"directory2"-"file"m

            Parameters:
                    dirname (string): name of the directory that will be read
                    text (string): the text that will be translated
    '''

    decoded = False
    prefix = text[:384]
    message = text[384:-384]
    nbFile = subprocess.check_output("ls -1 "+dirname+" | wc -l", shell = True)
    for i in range(int(nbFile)):
        directoryNumber = addZeros(str(i), 4)
        for j in range(100):
            fileNumber = addZeros(str(j), 2)
            path = dirname + "/" + directoryNumber + "/" + fileNumber
            if os.path.exists(path + "p") :
                padP = readFile(path + "p")
                if padP == prefix:
                    padC = readFile(path + "c")
                    textEncoded = ""
                    for m in range(int(len(message)/9)):
                        number = int(message[m*9:m*9+9], 2) - int(padC[m*8:m*8+8], 2)
                        textEncoded += chr(number)
                    createFile(dirname+"-"+directoryNumber+"-"+fileNumber+"m", textEncoded[:-1])
                    subprocess.call("rm " + path + "c", shell = True)
                    subprocess.call("rm " + path + "p", shell = True)
                    decoded = True
                    break
        if decoded == True:         
            break
    if decoded == False:
        print("There is no pad corresponding")

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description = "Write or read text in a PNG file")
    parser.add_argument("directory", type = str, help = "name of directory")
    parser.add_argument("-g", help = "generate directory, must the name of this directory", action = "store_true")
    parser.add_argument("-s", help = "send mode, specify input folder to encode the text", action = "store_true")
    parser.add_argument("-r", type = str, help = "read the encoded text, arguments : text to decode")
    parser.add_argument("-t", type = str, help = "text to encoded")
    parser.add_argument("-f", type = str, help = "file to encoded")
    args = parser.parse_args()

    response = os.system("ping -c 1 google.com")
    if response == 0:
        print ("Internet connected")
    else:
        print ("Internet not connected")

    dirname = args.directory
    if args.s:
        print("Send")
        if args.t:
            text = args.t
        elif args.f:
            text = readFile(args.f)
        else:
            text = input("Enter your text : ")
        #Add EOT
        text = convertToAsciiBinary(text) + "00000011"

        if len(text) <= 2000:
            sendText(dirname, text)
        else:
            print("the length of the text is too big and it must not exceed 2000 bytes. The length was:"+len(text))

    elif args.r:
        print("Receive")
        text = readFile(args.r)
        receiveText(dirname, text)

    else:
        print ("Generate")
        generate(dirname)