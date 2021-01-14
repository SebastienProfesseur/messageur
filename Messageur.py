# Votre nom
# installer python en mode administrateur : https://www.python.org/downloads/
# https://pypi.org/project/pyserial/
# pip install pyserial
# https://pypi.org/project/requests/
# pip install requests
# Déposer le script dans C:\Users\Etudiant
#    - Modifier le port pour celui utilisé dans Arduino (COM7, COM3, etc.)
#    - S'assurer que Arduino utilise le même baudrate
#    - Ajuster le chemin de l'URL ainsi que les paramètres reçus par ce script
# En cas de probleme verifier les logs dans C:\xampp\apache\logs

import serial
import time
import requests

entree = serial.Serial(
    port='COM7',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

print("Connecté à : " + entree.portstr)


listeLettres = []
ligne = 1
while True:
    for octet in entree.read():
        listeLettres.append(chr(octet))  
        valeur = ''.join(str(lettre) for lettre in listeLettres) # Transforme un type tableau en chaîne de caractères

        if chr(octet) == '\n':
            print("Ligne " + str(ligne) + ': ' + valeur)
            requests.post('http://localhost/service.meteo/ajouter-meteo.php', data={'luminosite':valeur})
            listeLettres = []
            ligne += 1
            break


entree.close()
