import argparse

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description = "Write or read text in a PNG file")
    parser.add_argument("-g", type = str, help = "text to write in the PNG")
    parser.add_argument("-s", type = str, help = "file to write in the PNG")
    parser.add_argument("-r", type = str, help = "file to write in the PNG")
    args = parser.parse_args()


    if args.s:
        print("Send")
    elif args.r:
        print("Receive")
    else:
        print ("Generate")