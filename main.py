import argparse
import subprocess
import os

def generate(dirname):
    path = "dir"

    createDirectory(dirname)

    nbFile = subprocess.check_output("ls -1 dir | wc -l", shell=True)

    directoryNumber = str(int(nbFile))

    while len(directoryNumber) < 4:
        directoryNumber = "0" + directoryNumber
    path += "/" + directoryNumber 
    createDirectory(path)

    for i in range(100):
        fileNumber = str(i)
        while len(fileNumber) < 2:
            fileNumber = "0" + fileNumber
        for j in range(3):
            if j == 0:
                fichier = open(path + "/" +  fileNumber + "p", "a")
                fichier.write(random(48))
                fichier.close()
            elif j == 1:
                fichier = open(path + "/" +  fileNumber + "c", "a")
                fichier.write(random(2000))
                fichier.close()

            else:
                fichier = open(path + "/" +  fileNumber + "s", "a")
                fichier.write(random(48))
                fichier.close()

def random(size):
    listOfRandomNumber = ""
    with open("/dev/urandom", 'rb') as f:       
        for i in range(size):
            listOfRandomNumber += convertIntToBinary(int.from_bytes(f.read(1), 'big'))
    return listOfRandomNumber

def convertIntToBinary(number):
    '''
    Convert an integer in base 2

            Parameters:
                    number (int): a integer to convert

            Returns:
                    binaryNumber (string): the convertion of integer in base 2 with 8 bits.
    '''

    binaryNumber = '{0:08b}'.format(number)
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
        binaryLetter = convertIntToBinary(ord(letter))
        binaryText += binaryLetter
    return binaryText


def createDirectory(dirname):
    os.makedirs(dirname, exist_ok=True)

def sendText(text):
    path = "dir"
    nbFile = subprocess.check_output("ls -1 dir | wc -l", shell=True)

    for i in range(int(nbFile)):
        directoryNumber = str(i)
        while len(directoryNumber) < 4:
            directoryNumber = "0" + directoryNumber
        path += "/" + directoryNumber 
        for j in range(100):
            fileNumber = str(i)
            while len(fileNumber) < 2:
                fileNumber = "0" + fileNumber
            if os.path.exists(path + "/" + fileNumber + "c") :
                # path += "/" + fileNumber
                print(fileNumber)
                break
        break

    f = open(path + "/" + fileNumber + "c", "r")
    padC = f.read()
    f.close()

    textEncoded = ""
    print(len(text))
    for i in range(int(len(text)/8)):
        number = int(text[i*8:i*8+8], 2) + int(padC[i*8:i*8+8], 2)
        textEncoded += '{0:09b}'.format(number)
    
    f = open(path + "/" + fileNumber + "p", "r")
    padP = f.read()
    f.close()

    f = open(path + "/" + fileNumber + "s", "r")
    padS = f.read()
    f.close()


    print(textEncoded)
    textInFileT = padP + textEncoded + padS
    print(len(textInFileT))
    fichier = open("dir-"+directoryNumber+"-"+fileNumber+"t", "w")

    fichier.write(textInFileT)
    fichier.close()
    


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description = "Write or read text in a PNG file")
    parser.add_argument("-g", type = str, help = "text to write in the PNG")
    parser.add_argument("-s", type = str, help = "file to write in the PNG")
    parser.add_argument("-r", type = str, help = "file to write in the PNG")
    parser.add_argument("-t", type = str, help = "text to write in the PNG")
    parser.add_argument("-f", type = str, help = "file to write in the PNG")
    args = parser.parse_args()


    if args.s:
        print("Send")
        if args.t:
            text = args.t
        elif args.f:
            textInFile = open(args.f, "r")
            text = textInFile.read()
            textInFile.close()
        else:
            text = input("Enter your text : ")

        text = convertToAsciiBinary(text) + "00000011"
        if len(text) > 2000:
            raise Exception('the length of the text is too big and not exceed 2000 bytes. The length was: {}'.format(len(text)))
        print("halloS")
        sendText(text)
    elif args.r:
        print("Receive")
    elif args.g:
        dirname = args.g
        print ("Generate")
        generate(dirname)