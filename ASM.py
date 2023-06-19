"""
Auteur: Baptiste LE ROUX
Date: 18/03/2023
Projet: Simulateur Jeu d'Instructions
Fichier : ASM
Contacts: bapt.leroux29@gmail.com
"""

import os
import sys

# Variables
opcode = {"add": 1, "sub": 2, "mul": 3, "div": 4, "and": 5, "or": 6, "xor": 7, "shl": 8, "shr": 9, "slt": 10,
          "sle": 11, "seq": 12, "load": 13, "store": 14, "jmp": 15, "braz": 16, "branz": 17, "scall": 18, "stop": 19}
register = {"r0": 0, "r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6, "r7": 7, "r8": 8, "r9": 9, "r10": 10,
            "r11": 11, "r12": 12, "r13": 13, "r14": 14, "r15": 15, "r16": 16, "r17": 17, "r18": 18,
            "r19": 19, "r20": 20, "r21": 21, "r22": 22, "r23": 23, "r24": 24, "r25": 25,
            "r26": 26, "r27": 27, "r28": 28, "r29": 29, "r30": 30, "r31": 31}
label = {}

dec = [[27, 22, 21, 5, 0], [27, 26, 5, 0], [27, 22, 0], [27, 22], [27]]

length = [5, 4, 3, 2, 1, 0]


# Fonction pour parser le fichier d'instructions :
def file_layout(file):
    list_instr = []
    for line in file:
        if ":" or "," in line:
            line = line.replace(":", "").replace(",", " ").split()
        list_instr.append(line)
    for line in list_instr:
        for i in range(len(line)):
            if "#" in line[i]:
                del (line[i:])
                break
        if len(line) == 0:
            list_instr.remove(line)
    if [] in list_instr:
        list_instr.remove([])
    return list_instr


# Décodage des instructions:
def decode_instr_bin(list_instr):
    list_instr_bin = []
    for instr in list_instr:
        instr_bin = []
        if "stop" not in instr[0] and "label" not in instr[0] and "scall" not in instr[0]:
            if instr[0] in opcode:
                instr_bin.append(opcode[instr[0]])
                if "jmp" in instr[0]:
                    instr_bin.append(0)
                for i in range(1, len(instr) - 1):
                    if instr[i].isdigit() or instr[i][0] == '-' and instr[i][1:].isdigit():
                        instr_bin.append(1)
                        if instr[i][0] == '-':
                            instr[i] = int(instr[i]) + 2 ** 16
                            instr_bin.append(int(instr[i]))
                        else:
                            instr_bin.append(int(instr[i]))
                    else:
                        if i == 2:
                            instr_bin.append(0)
                            instr_bin.append(register[instr[i]])
                        elif "label" in instr[i]:
                            if instr[i + 1] in label:
                                instr_bin.append(label[instr[i + 1]])
                            else:
                                label[instr[i]] = 20 + int(instr[i].replace("label", ""))
                            instr_bin.append(label[instr[i]])
                        else:
                            instr_bin.append(register[instr[i]])
                if i + 1 < len(instr):
                    if "label" in instr[i + 1]:
                        if instr[i+1] in label:
                            instr_bin.append(label[instr[i+1]])
                        else:
                            label[instr[i+1]] = 20 + int(instr[i+1].replace("label", ""))
                        instr_bin.append(label[instr[i + 1]])
                    else:
                        instr_bin.append(register[instr[i + 1]])
            else:
                print(" La chaine " + str(instr[0]) + " n'est pas reconnue, le script ne peut pas lire votre code")
                list_instr_bin = []
                return list_instr_bin
        else:
            if instr[0] == 'stop':
                instr_bin.append(opcode[instr[0]])
            if instr[0] == 'scall':
                instr_bin.append(opcode[instr[0]])
                instr_bin.append(int(instr[1]))
            if 'label' in instr[0]:
                if instr[0] in label:
                    instr_bin.append(label[instr[0]])
                else:
                    label[instr[0]] = 20 + int(instr[0].replace("label", ""))
                instr_bin.append(label[instr[0]])
        list_instr_bin.append(instr_bin)
    return list_instr_bin


# Décalage des informations sur 32 bits:
def instr_decalage(list_instr_bin):
    list_instr_hex = []
    n = 0
    for lines in list_instr_bin:
        instr = 0
        while len(lines) != length[n]:
            n += 1
        for i in range(len(lines)):
            instr += lines[i] << dec[n][i]
        n = 0
        list_instr_hex.append(hex(instr))
    return list_instr_hex


def main():
    # Code principal
    if len(sys.argv) < 2:
        print("Usage: python convert_to_hex.py <filename>")
        sys.exit()
    filename = sys.argv[1]
    with open('testdata/filename', 'r') as f:
        lines = f.readlines()
    list_instr = file_layout(lines)
    list_instr_bin = decode_instr_bin(list_instr)
    list_instr_hex = instr_decalage(list_instr_bin)

    if os.path.exists("file_bin.txt"):
        os.remove("file_bin.txt")
    file_bin = open("file_bin.txt", "a")

    for i in range(len(list_instr_hex)):
        file_bin.write(hex(i))
        file_bin.write(" ")
        file_bin.write(list_instr_hex[i])
        file_bin.write("\n")
    file_bin.close()


if __name__ == '__main__':
    # Appel de la fonction principale
    main()
    os.system("echo " + "fichier binaire créé : file_bin.txt")
