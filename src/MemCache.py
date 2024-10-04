"""
Auteur: Baptiste LE ROUX
Date: 18/03/2023
Projet: Simulateur Jeu d'Instructions
Fichier : Cache Memory
Contacts: bapt.leroux29@gmail.com
"""

import os
# Paramètres du cache
S = 16  # nombre d'ensembles
E = 1  # nombre de lignes par ensemble
B = 2  # nombre d'octets par ligne
m = 4  # nombre de bits d'adresse

# Initialisation du cache
cache = [[[[None for i in range(B)]for k in range(B)] for j in range(E)] for i in range(S)]


def get_data(address):
    # Calcul de l'ensemble et de l'offset
    index_bits = address%S #Index du set
    offset_bits = address & (B-1) #Index du bloc
    # Rechercher la donnée dans le cache
    for i in range(E):
        if cache[index_bits][i][offset_bits][0] == address: #[]ensemble[]ligne[]bloc[]addresse id 0 du bloc
            # Hit
            return cache[index_bits][i][offset_bits][1]
        else:
            # Miss : accès à la mémoire plus lente
            # Récupération des données adjacentes
            for j in range(B):
                if cache[index_bits][i][j][0] is None:
                    # Si l'adresse est vide, on la lit depuis la mémoire plus lente
                    address_adjacent = (address & ~(B-1)) + j # On remplace l'index du bloc par l'index j de la ligne
                    data_adjacent = read_data_from_memory(address_adjacent)
                    # On stocke la donnée dans le cache
                    cache[index_bits][i][j] = [address_adjacent, data_adjacent]
            return cache[index_bits][i][offset_bits][1]


def write_data(addr, data):
    with open("../memory.txt", "r") as f:
        lines = f.readlines()
    # Modifier la ligne correspondant à l'adresse spécifiée
    lines[addr] = str(addr) + " " + str(data) + "\n"
    # Écrire les données modifiées dans le fichier
    with open("../memory.txt", "w") as f:
        f.writelines(lines)
    return 0


def read_data_from_memory(address):
    # Simulation d'un accès à la mémoire plus lente
    with open("../memory.txt", "r") as f:
        # Lecture de toutes les lignes dans une liste
        lines = f.readlines()
    if address < len(lines):
        data = lines[address].split()[1] # Récupération de la deuxième colonne de la ligne
    else:
        print("Error, address doesn't exist anywhere")
        return 1
    return data


def create_memory():
    if os.path.exists("../memory.txt"):
        os.remove("../memory.txt")
    file_bin = open("../memory.txt", "a")
    for i in range(32):
        file_bin.write(hex(i))
        file_bin.write(" ")
        file_bin.write(hex(0))
        file_bin.write("\n")
    file_bin.close()
