import socket
import datetime
import base64
from base58 import b58decode
import webcolors
import re
import string
from collections import Counter
import nltk
from nltk.corpus import words
from dotenv import load_dotenv
import os
from math import gcd


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
    port = os.getenv("PORT_SERVER") # Penser a le changer dans le .env
    if not port or not port.isdigit():
        raise ValueError(f"La variable PORT_SERVER n'est pas valide : {port}")
    port = int(port)
    print(f"Connexion au serveur {host}:{port}")
    
    try: 
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect.connect((host, port))
        print(f"Connexion établie")
        print(f"~~~~~~~~~~~~~~~~\n")
        answer = connect.recv(1024).decode()
        print(answer)
        return connect
    
    except ConnectionError as e:
        print(f"Erreur de connexion : {e}")
        exit()
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        exit()
        
def wait_answer(cnct):
    """
    Fonction permettant de récuperer la réponse du serveur
    :param cnct: socket
    :return: string
    """
    try:
        answer = cnct.recv(1024).decode()
        print(answer)
        if answer == "Réponse incorrecte, connexion fermée":
            exit()
        return answer
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
    Le message peut etre base64, base32, base85, base58
    :param message: string
    :return answer: string
    """
    try:
        decoders = {
        'base64': base64.b64decode,
        'base32': base64.b32decode,
        'base85': base64.b85decode,
        'base58': b58decode
        }
        
        for encoding, decoder in decoders.items():
            try:
                answer = decoder(message)
                return answer.decode('utf-8')
            except Exception:
                pass 
        
    except Exception as e:
        print(f"Erreur lors du décodage du message: {e}")
        exit()
    
def morse_to_text(morse):
    """
    Convertit du morse en texte.
    :param morse: string
    :return text: string
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
    :return decoded_word: string
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
    :return color_name: string
    """
    value = rgb.strip("RGB()").split(",")
    r, g, b = map(int, value)
    try:
        return webcolors.rgb_to_name((r, g, b))
    except ValueError:
        print("Erreur lors de la conversion RGB en nom de couleur.")

def decrypt_cesar(text, key):
    """
    Décrypte un message chiffré en César
    :param text: string
    :param key: int
    :return decryptedText: string
    """
    lowercaseAlphabet = string.ascii_lowercase
    uppercaseAlphabet = string.ascii_uppercase
    decryptedText = []

    for el in text:
        if el in lowercaseAlphabet:  
            newChar = (lowercaseAlphabet.index(el) - key) % 26
            decryptedText.append(lowercaseAlphabet[newChar])
        elif el in uppercaseAlphabet:  
            newChar = (uppercaseAlphabet.index(el) - key) % 26
            decryptedText.append(uppercaseAlphabet[newChar])
        else: 
            decryptedText.append(el)
    
    return ''.join(decryptedText)

def bruteforce_cesar(text):
    """ 
    Fonction permettant de décrypter un message chiffré en César sans avoir la clé.
    On teste toutes les possibilitées, et on vérifie la présence de chacune dans le dictionnaire
    :param text: string
    :return bestWord: string
    """ 
    bestWord = None
    for i in range(26):
        decrypted = decrypt_cesar(text, i)
        if decrypted in words.words():
            bestWord = decrypted
            break
    if bestWord is None:
        Exception("Aucun mot trouvé.")
    return bestWord



#################################################################
###########                                    ##################
###########  Fonctions de réponses aux flags   ##################
###########                                    ##################
#################################################################

def flag1(cnct):
    """
    Fonction permettant de répondre à la question 1
    L'objectif est simplement d'envoyer son nom prénom classe
    format : prenom/nom/classe
    :param cnct: socket
    :return: string
    """
    try: 
        answer = "celian/pinquier/3si2"
        cnct.sendall(answer.encode())
        print(f"Réponse envoyée : {answer}")
        wait_answer(cnct)
        return answer
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")

def flag2(cnct):
    """
    Fonction permettant de répondre à la question 2
    Il faut ici renvoyer la date du jour
    :param cnct: socket
    :return wait_answer(cnct): string
    :return date: string
    """
    try: 
        date = datetime.datetime.now().strftime("%d/%m")
        cnct.sendall(date.encode())
        print(f"Réponse envoyée : {date}")
        return wait_answer(cnct), date
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        
def flag3(cnct, statement):
    """
    Fonction permettant de répondre à la question 3
    Le but est de récupérer l'opération (deux opérands et un symbole) puis renvoyer le résultat
    :param cnct: socket
    :param statement: string
    :return wait_answer(cnct): string
    :return answer: int
    """
    try: 
        cleananswer = statement.split("résultat de ")[1]
        cleananswer = cleananswer.split(" ?")[0]
        oper1, signe, oper2 = cleananswer.split(" ")
        print(f"Calcul : {oper1} {signe} {oper2}")
        if signe == "+":
            answer = int(oper1) + int(oper2)
        elif signe == "-":
            answer = int(oper1) - int(oper2)
        elif signe == "*":
            answer = int(oper1) * int(oper2)
        cnct.sendall(str(answer).encode())
        print(f"Réponse envoyée : {answer}")
        return wait_answer(cnct), answer
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")

def flag4(cnct, statement):
    """
    Fonction permettant de répondre à la question 4
    Il faut décoder un message (je ne comprend pas excepé b64 et b32 pour le moment)
    :param cnct: socket
    :param statement: string
    :return wait_answer(cnct): string
    :return decodedanswer: string
    """
    cleanAwser = statement.split(" ")[-1]
    decodedanswer = decode_message(cleanAwser)
    if decodedanswer:
        cnct.sendall(str(decodedanswer).encode())
        print(f"Réponse envoyée : {decodedanswer}")
        return wait_answer(cnct), decodedanswer

def flag5(cnct, statement):
    """
    Fonction permettant de répondre à la question 5
    Le code donné est en fait un code morse, à traduire en texte
    :param cnct: socket
    :param statement: string
    :return wait_answer(cnct): string
    :return finalAnswer: string
    """

    try:
        cleanAwser = statement.split(" ")[-1] 
        # Convertis de hexa à texte
        decodedanswer = bytes.fromhex(cleanAwser).decode('utf-8')
        # Convertis de morse à texte
        finalAnswer = morse_to_text(decodedanswer)
        cnct.sendall(finalAnswer.encode())
        print(f"Réponse décodée : {finalAnswer}")
        return wait_answer(cnct), finalAnswer
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")

def flag6(cnct, statement):
    """
    Fonction permettant de répondre à la question 6
    Le code est ici un code braille, à traduire en texte
    :param cnct: socket
    :param statement: string
    :return wait_answer(cnct): string
    :return finalAnswer: string
    """

    try:
        cleanAwser = statement.split(" ")[-1]
        # Convertis de hexa à texte
        decodedanswer = bytes.fromhex(cleanAwser).decode('utf-8')
        print("Hexa décodé : ", decodedanswer)
        # Convertis de braille à texte
        finalAnswer = decode_braille(decodedanswer)
        cnct.sendall(finalAnswer.encode())
        print(f"Réponse décodée : {finalAnswer}")
        return wait_answer(cnct), finalAnswer
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
    
def flag7(cnct, statement):
    """
    Fonction permettant de répondre à la question 7
    On reçoit un code RGB RGB(xxx,yyy,zzz) qu'il faut convertir en nom de couleur
    :param cnct: socket
    :param statement: string
    :return wait_answer(cnct): string
    :return finalAnswer: string
    """
    try:
        print(statement)
        if "RGB" in statement:
            start = statement.find("RGB")
            cleananswer = statement[start:].strip()
            cleananswer = cleananswer.split(" ?")[0]
            cleananswer = cleananswer.replace(" ", "")
            print(f"Valeurs extraites : {cleananswer}")
            finalAnswer = rgb_to_name(cleananswer)
            if finalAnswer:
                cnct.sendall(finalAnswer.encode())
                print(f"Réponse envoyée : {finalAnswer}")
                return wait_answer(cnct), finalAnswer
        else:
            print("Format inattendu pour la question 7.")
            exit()
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
    
def flag8(cnct, statement, allanswers):
    """
    Fonction permettant de répondre à la question 8
    On doit redonner la réponse à la question demandée
    :param cnct: socket
    :param statement: string
    :param allanswers: dict
    :return wait_answer(cnct): string
    :return allanswers[answerNumber]: string
    """
    try:
        answerNumber = int(statement.split(" ")[-1])
        cnct.sendall(str(allanswers[answerNumber]).encode())
        print(f"Réponse envoyée : {allanswers[answerNumber]}")
        return wait_answer(cnct), allanswers[answerNumber]
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
        
def flag9(cnct, statement):
    """ 
    Fonction permettant de répondre à la question 9
    L'idée ici est de récupérer la derniere lettre d'un mot aléatoire d'une liste
    :param cnct: socket
    :param statement: string
    :return wait_answer(cnct): string
    :return answer: string
    """
    try:
        index = int(re.findall(r'\d+', statement)[2]) - 1
        answer = statement.split(":")[-1].strip().split()[index][-1]
        print("Réponse envoyée : ", answer)
        cnct.sendall(answer.encode())
        return wait_answer(cnct), answer
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
        
def flag10(cnct, statement, allanswers):
    """
    Fonction permettant de répondre à la question 10
    On doit redonner toutes les réponses précédentes séparées par un underscore
    :param cnct: socket
    :param statement: string
    :param allanswers: dict
    :return wait_answer(cnct): string
    """
    try:
        answer = "_".join(str(value) for value in allanswers.values())
        print("Réponse envoyée : ", answer)
        cnct.sendall(answer.encode())
        return wait_answer(cnct)
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
    :return wait_answer(cnct): string
    """
    try: 
        cleananswer = statement.split(" ")[-1]
        bestWord = bruteforce_cesar(cleananswer)
        if bestWord is None:
            raise Exception("Aucun mot trouvé.")
        print(f"Meilleur mot : {bestWord}")
        cnct.sendall(bestWord.encode())
        return wait_answer(cnct)
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()

def flag12(cnct, statement):
    """
    Fonction permettant de répondre à la question 12
    Concretement, on va décoder le message dans cet ordre: Base (64, 32, 85, 58) -> César -> Base (64, 32, 85, 58) -> vérification de la présence du mot dans le dico -> ggwp
    puis rappeler decode_message si nécessaire.
    :param cnct: socket
    :param statement: string
    :return wait_answer(cnct): string
    """

    cleanAwser = statement.split(" ")[-1]
    resultat = None
    try:
        firstDecode = decode_message(cleanAwser)
        for i in range(26):
            decrypted = decrypt_cesar(firstDecode, i)
            
            final = decode_message(decrypted)
            if final in words.words():
                print(f"Le résultat est : {final}")
                resultat = final
                break

        if resultat is None:
            raise Exception("Aucune clé César valide n'a produit un résultat correct.")

        cnct.sendall(resultat.encode())
        return wait_answer(cnct)
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
        statement4, responses[4] = flag4(cnct, statement3) 
        statement5, responses[5] = flag5(cnct, statement4)
        statement6, responses[6] = flag6(cnct, statement5)
        statement7, responses[7] = flag7(cnct, statement6)
        statement8, responses[8] = flag8(cnct, statement7, responses)
        statement9, responses[9] = flag9(cnct, statement8)
        statement10 = flag10(cnct, statement9, responses)
        statement11 = flag11(cnct, statement10)  
        statement12 = flag12(cnct, statement11)