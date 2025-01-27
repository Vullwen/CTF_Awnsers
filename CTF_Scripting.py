import socket
import datetime
import base64
import webcolors
import re
import string
from collections import Counter
import nltk
from nltk.corpus import words
from dotenv import load_dotenv
import os


##################################################################
###########                                      #################
########### Fonctions de connexion et de lecture #################
###########                                      #################
##################################################################

def connexion():
    """
    Fonction permettant de se connecter au serveur
    :return: socket
    """
    load_dotenv()
    
    host = os.getenv("IP_SERVER")
    port = os.getenv("PORT_SERVER")
    if not port or not port.isdigit():
        raise ValueError(f"La variable PORT_SERVER n'est pas valide : {port}")
    port = int(port)
    print(f"Connexion au serveur {host}:{port}")
    
    try: 
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect.connect((host, port))
        print(f"Connexion établie")
        print(f"~~~~~~~~~~~~~~~~\n")
        awnser = connect.recv(1024).decode()
        print(awnser)
        return connect
    
    except ConnectionError as e:
        print(f"Erreur de connexion : {e}")
        exit()
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        exit()
        
def wait_awnser(cnct):
    """
    Fonction permettant de récuperer la réponse du serveur
    :param cnct: socket
    :return: string
    """
    try:
        awnser = cnct.recv(1024).decode()
        print(awnser)
        if awnser == "Réponse incorrecte, connexion fermée":
            print("Réponse incorrecte, connexion fermée")
            exit()
        return awnser
    except Exception as e:
        print(f"Erreur lors de la récuperation de la réponse: {e}")
        exit()
    
    
    
#################################################################
###########                                    ##################
########### Fonctions utiles pour les flags    ##################
###########                                    ##################
#################################################################

def decode_message(message):
    """
    Fonction permettant de décoder un message
    :param message: string
    :return: string
    """
    try:
        if message.endswith("==="):  # Test Base32
            decoded = base64.b32decode(message)
            print(f"Base32 décodé (bytes): {decoded}")
            return decoded.decode("utf-8", errors="ignore")  
        elif message.endswith("="):  # Test Base64
            decoded = base64.b64decode(message)
            print(f"Base64 décodé (bytes): {decoded}")
            return decoded.decode("utf-8", errors="ignore") 
        else:
            print("Encodage inconnu.")
            exit()
    except Exception as e:
        print(f"Erreur lors du décodage du message: {e}")
        exit()
    
def morse_to_text(morse):
    """
    Convertit du morse en texte.
    :param morse: string
    :return: string
    """
    morseDict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z'
    }
    try:
        letters = morse.split() 
        decoded_word = ''.join(morseDict.get(letter, '?') for letter in letters)
        return ''.join(decoded_word)
    except Exception as e:
        print(f"Erreur lors de la conversion Morse à texte : {e}")
        exit()
    
def decode_braille(braille):
    """ 
    Convertit du braille en texte.
    :param braille: string
    :return: string
    """
    brailleDict = {
        '\u2801': 'a', '\u2803': 'b', '\u2809': 'c', '\u2819': 'd', '\u2811': 'e',
        '\u280b': 'f', '\u281b': 'g', '\u2813': 'h', '\u280a': 'i', '\u281a': 'j',
        '\u2805': 'k', '\u2807': 'l', '\u280d': 'm', '\u281d': 'n', '\u2815': 'o',
        '\u280f': 'p', '\u281f': 'q', '\u2817': 'r', '\u280e': 's', '\u281e': 't',
        '\u2825': 'u', '\u2827': 'v', '\u283a': 'w', '\u282d': 'x', '\u283d': 'y',
        '\u2835': 'z', '\u2821': ' '
    }
    try: 
        letters = braille.split()
        decoded_word = ''.join(brailleDict.get(letter, '?') for letter in letters)
        return ''.join(decoded_word)
    except Exception as e:
        print(f"Erreur lors de la conversion Braille à texte : {e}")
        exit()
    
def rgb_to_name(rgb):
    """
    Convertit une couleur RGB en nom de couleur.
    :param rgb_str: string
    :return: string
    """
    value = rgb.strip("RGB()").split(",")
    r, g, b = map(int, value)
    try:
        # Conversion en nom de couleur
        return webcolors.rgb_to_name((r, g, b))
    except ValueError:
        print("Erreur lors de la conversion RGB en nom de couleur.")

def decrypt_cesar(text, key):
    """
    Décripte un message chiffré en minsucule en César
    :param ciphertext: string
    :param key: int
    :return: string
    """
    alphabet = string.ascii_lowercase
    decryptedText = []
    for el in text:
        newChar = (alphabet.index(el) - key) % 26
        decryptedText.append(alphabet[newChar])
    return ''.join(decryptedText)


#################################################################
###########                                    ##################
###########  Fonctions de réponses aux flags   ##################
###########                                    ##################
#################################################################

def flag1(cnct):
    """
    Fonction permettant de répondre à la question 1
    L'objectif est simplement d'envoyer son nom prénom classe
    :param cnct: socket
    """
    try: 
        awnser = "celian/pinquier/3si2"
        cnct.sendall(awnser.encode())
        print(f"Réponse envoyée : {awnser}")
        wait_awnser(cnct)
        return awnser
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")

def flag2(cnct):
    """
    Fonction permettant de répondre à la question 2
    Il faut ici renvoyer la date du jour
    :param cnct: socket
    """
    try: 
        date = datetime.datetime.now().strftime("%d/%m")
        cnct.sendall(date.encode())
        print(f"Réponse envoyée : {date}")
        return wait_awnser(cnct), date
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        
def flag3(cnct, statement):
    """
    Fonction permettant de répondre à la question 3
    Le but est de récupérer l'opération (deux opérands et un symbole) puis renvoyer le résultat
    :param cnct: socket
    :param statement: string
    """
    try: 
        cleanAwnser = statement.split("résultat de ")[1]
        cleanAwnser = cleanAwnser.split(" ?")[0]
        oper1, signe, oper2 = cleanAwnser.split(" ")
        print(f"Calcul : {oper1} {signe} {oper2}")
        if signe == "+":
            awnser = int(oper1) + int(oper2)
        elif signe == "-":
            awnser = int(oper1) - int(oper2)
        elif signe == "*":
            awnser = int(oper1) * int(oper2)
        cnct.sendall(str(awnser).encode())
        print(f"Réponse envoyée : {awnser}")
        return wait_awnser(cnct), awnser
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")

def flag4(cnct, statement):
    """
    Fonction permettant de répondre à la question 4
    Il faut décoder un message (je ne comprend pas excepé b64 et b32 pour le moment)
    :param cnct: socket
    :param statement: string
    """
    cleanAwser = statement.split(" ")[-1]
    decodedAwnser = decode_message(cleanAwser)
    if decodedAwnser:
        cnct.sendall(str(decodedAwnser).encode())
        print(f"Réponse envoyée : {decodedAwnser}")
        return wait_awnser(cnct), decodedAwnser

def flag5(cnct, statement):
    """
    Fonction permettant de répondre à la question 5
    Le code donné est en fait un code morse, à traduire en texte
    :param cnct: socket
    :param statement: string
    """

    try:
        cleanAwser = statement.split(" ")[-1] 
        # Convertis de hexa à texte
        decodedAwnser = bytes.fromhex(cleanAwser).decode('utf-8')
        # Convertis de morse à texte
        finalAnswer = morse_to_text(decodedAwnser)
        cnct.sendall(finalAnswer.encode())
        print(f"Réponse décodée : {finalAnswer}")
        return wait_awnser(cnct), finalAnswer
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")

def flag6(cnct, statement):
    """
    Fonction permettant de répondre à la question 6
    Le code est ici un code braille, à traduire en texte
    :param cnct: socket
    :param statement: string
    """

    try:
        cleanAwser = statement.split(" ")[-1]
        # Convertis de hexa à texte
        decodedAwnser = bytes.fromhex(cleanAwser).decode('utf-8')
        print("Hexa décodé : ", decodedAwnser)
        # Convertis de braille à texte
        finalAnswer = decode_braille(decodedAwnser)
        cnct.sendall(finalAnswer.encode())
        print(f"Réponse décodée : {finalAnswer}")
        return wait_awnser(cnct), finalAnswer
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
    
def flag7(cnct, statement):
    """
    Fonction permettant de répondre à la question 7
    On reçoit un code RGB RGB(xxx,yyy,zzz) qu'il faut convertir en nom de couleur
    """
    try:
        print(statement)
        if "RGB" in statement:
            start = statement.find("RGB")
            cleanAwnser = statement[start:].strip()
            cleanAwnser = cleanAwnser.split(" ?")[0]
            cleanAwnser = cleanAwnser.replace(" ", "")
            print(f"Valeurs extraites : {cleanAwnser}")
            finalAnswer = rgb_to_name(cleanAwnser)
            if finalAnswer:
                cnct.sendall(finalAnswer.encode())
                print(f"Réponse envoyée : {finalAnswer}")
                return wait_awnser(cnct), finalAnswer
        else:
            print("Format inattendu pour la question 7.")
            exit()
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
    
def flag8(cnct, statement, allAwnsers):
    """
    Fonction permettant de répondre à la question 8
    On doit redonner la réponse à la question demandée
    :param cnct: socket
    :param statement: string
    :param allAwnsers: dict
    """
    try:
        awnserNumber = int(statement.split(" ")[-1])
        cnct.sendall(str(allAwnsers[awnserNumber]).encode())
        print(f"Réponse envoyée : {allAwnsers[awnserNumber]}")
        return wait_awnser(cnct), allAwnsers[awnserNumber]
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
        
def flag9(cnct, statement):
    """ 
    Fonction permettant de répondre à la question 9
    L'idée ici est de récupérer la derniere lettre d'un mot aléatoire d'une liste
    :param cnct: socket
    :param statement: string
    """
    try:
        index = int(re.findall(r'\d+', statement)[2]) - 1
        awnser = statement.split(":")[-1].strip().split()[index][-1]
        print("Réponse envoyée : ", awnser)
        cnct.sendall(awnser.encode())
        return wait_awnser(cnct), awnser
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
        
def flag10(cnct, statement, allAwnsers):
    """
    Fonction permettant de répondre à la question 10
    On doit redonner toutes les réponses précédentes séparées par un underscore
    :param cnct: socket
    :param statement: string
    :param allAwnsers: dict
    """
    try:
        awnser = "_".join(str(value) for value in allAwnsers.values())
        print("Réponse envoyée : ", awnser)
        cnct.sendall(awnser.encode())
        return wait_awnser(cnct)
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()

def flag11(cnct, statement):
    """ 
    Fonction permettant de répondre à la question 11
    On doit décrypter un message chiffré en César sans avoir la clé, et renvoyer le plus probable
    Ce que je fais ici, c'est que je teste toutes les clés possibles et je renvoie le mot qui correspond le plus à un mot anglais (fréquence des lettres)
    C'est bancal et marche une fois sur 2
    :param cnct: socket
    :param statement: string
    """
    try: 
        cleanAwnser = statement.split(" ")[-1]
        bestWord = None
        
        for i in range(26):
            decrypted = decrypt_cesar(cleanAwnser, i)
            if decrypted in words.words():
                bestWord = decrypted
                break
        if bestWord is None:
            Exception("Aucun mot trouvé.")
        print(f"Meilleur mot : {bestWord}")
        cnct.sendall(bestWord.encode())
        return wait_awnser(cnct)
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()

#################################################################
###########                                    ##################
###########          Execution du code         ##################
###########                                    ##################
#################################################################
    
if __name__ == "__main__":
    responses = {}
    cnct = connexion()
    
    if cnct:
        responses[1] = flag1(cnct)
        statement2, responses[2] = flag2(cnct)
        statement3, responses[3] = flag3(cnct, statement2)
        statement4, responses[4] = flag4(cnct, statement3) # Pour le moment seulement base64 et base32 (je trouve pas le reste)
        statement5, responses[5] = flag5(cnct, statement4)
        statement6, responses[6] = flag6(cnct, statement5)
        statement7, responses[7] = flag7(cnct, statement6)
        statement8, responses[8] = flag8(cnct, statement7, responses)
        statement9, responses[9] = flag9(cnct, statement8)
        statement10 = flag10(cnct, statement9, responses)
        statement11 = flag11(cnct, statement10)  
        print("ggwp")
