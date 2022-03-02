from ArnauGrisoBot import ArnauGrisoBot
from sys import argv

if "__main__" :
    token = argv[1] if (len(argv) >= 2) else ""
    ArnauGrisoBot(token)
