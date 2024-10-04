"""
Auteur: Baptiste LE ROUX
Date: 18/03/2023
Projet: Simulateur Jeu d'Instructions
Fichier : VM
Contacts: bapt.leroux29@gmail.com
"""
import random
import time
from MemCache import *

opcode = {"add": 1, "sub": 2, "mul": 3, "div": 4, "and": 5, "or": 6, "xor": 7, "shl": 8, "shr": 9, "slt": 10,
          "sle": 11, "seq": 12, "load": 13, "store": 14, "jmp": 15, "braz": 16, "branz": 17, "scall": 18, "stop": 19}
reg = {"r0": 0, "r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6, "r7": 7, "r8": 8, "r9": 9, "r10": 10,
       "r11": 11, "r12": 12, "r13": 13, "r14": 14, "r15": 16, r"17": 17, "r18": 18,
       "r19": 19, "r20": 20, "r21": 21, "r22": 22, "r23": 23, r"24": 24, "r25": 25,
       "r26": 26, "r27": 27, "r28": 28, "r29": 29, "r30": 30, r"31": 31}

label = {20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1}
register = [0 for i in range(32)]
nb_instr_executed = 0

op = {
    0: lambda x, y: x + y,
    1: lambda x, y: x + y,
    2: lambda x, y: x - y,
    3: lambda x, y: x * y,
    4: lambda x, y: x / y if y > 0 else 0,
    5: lambda x, y: x & y,
    6: lambda x, y: x | y,
    7: lambda x, y: x ^ y,
    8: lambda x, y: x << y,
    9: lambda x, y: x >> y,
    10: lambda x, y: 1 if x < y else 0,
    11: lambda x, y: 1 if x <= y else 0,
    12: lambda x, y: 1 if x == y else 0,
}
dec_op = [27, 22, 21, 5, 0]
dec_jump = [27, 26, 5, 0]
dec_braz = [27, 22, 0]
dec_scall = [27, 0]

pos_op = [0xF8000000, 0x7C00000, 0x200000, 0x1FFFE0, 0x1F]
pos_jump = [0xF8000000, 0x4000000, 0x3FFFFE0, 0x1F]
pos_braz = [0xF8000000, 0x7C00000, 0x3FFFFF]
pos_scall = [0xF8000000, 0x7C00000]


def file_layout(file):
    """
    This function decodes the instructions in the input list and returns a list of decoded instructions.

    Args:
            file: File with hexa instructions.

    Returns:
            list_instr: List of instructions to be decoded.
    """
    list_instr = []
    for lines in file:
        instr = lines.split()
        instr[1] = instr[1].replace("\n", "")
        hex_list = [int(x, 16) for x in instr]
        list_instr.append(hex_list)
    return list_instr


def instr_decode(list_instr):
    """
    This function decodes the instructions in the input list and returns a list of decoded instructions.

    Args:
            list_instr: List of instructions to be decoded.

    Returns:
            list_instr_decode: List of instructions decoded.
    """
    list_id = []
    list_instr_decode = []
    for instr in list_instr:
        list_op = []
        opc = (instr[1] & 0xF8000000) >> 27
        if opc >= 15:
            if opc == 15:
                for i in range(len(dec_jump)):
                    list_op.append((instr[1] & pos_jump[i]) >> dec_jump[i])
            elif opc == 16 or opc == 17:
                for i in range(len(dec_braz)):
                    list_op.append((instr[1] & pos_braz[i]) >> dec_braz[i])
            elif opc == 18:
                for i in range(len(dec_scall)):
                    list_op.append((instr[1] & pos_braz[i]) >> dec_braz[i])
            elif opc >= 19:
                list_op.append(opc)
                if opc > 19:
                    label[opc] = list_instr.index(instr)
        else:
            for i in range(len(dec_op)):
                list_op.append((instr[1] & pos_op[i]) >> dec_op[i])
        list_id.append(instr[0])
        list_instr_decode.append(list_op)
    return list_instr_decode


def instr_operation(list_instr_decode, start_address, end_address, nb_instr):
    """
        This function performs the operations specified in the instruction list.

        Args:
            list_instr_decode: List of instructions to be executed.
            start_address: Starting address of the instruction list.
            end_address: Ending address of the instruction list.
            nb_instr: Number of instructions executed.

        Returns:
            Tuple containing register and number of instructions executed.
        """
    for i in range(start_address, end_address+1):
        nb_instr += 1
        opc = list_instr_decode[i][0]
        if opc <= 12:
            rs1, imm, rs2, rd = list_instr_decode[i][1], list_instr_decode[i][2], list_instr_decode[i][3], \
                list_instr_decode[i][4]
            if imm == 0:
                register[rd] = op[opc](register[rs1], register[rs2])
            else:
                if list_instr_decode[i][3] < 2 ** (15):
                    register[rd] = op[opc](register[rs1], rs2)
                else:
                    mask = 2 ** 16 - 1
                    rs2 = -(mask - rs2 + 1)
                    register[rd] = op[opc](register[rs1], rs2)
        else:
            if opc == 13:
                ra, imm, offset, rd = list_instr_decode[i][1], list_instr_decode[i][2], list_instr_decode[i][3], \
                list_instr_decode[i][4]
                register[rd] = int(get_data(register[ra] + offset), 16)

            elif opc == 14:
                ra, imm, offset, rs = list_instr_decode[i][1], list_instr_decode[i][2], list_instr_decode[i][3], list_instr_decode[i][4]
                write_data(register[ra] + offset, rs)

            elif opc == 15:
                imm, ra, rd = list_instr_decode[i][1], list_instr_decode[i][2],list_instr_decode[i][3]
                if imm == 0:
                    start_address = label[ra]
                else:
                    start_address = ra
                register[rd] = i + 1
                _, nb_instr = instr_operation(list_instr_decode, start_address, end_address, nb_instr)

            elif opc == 16:
                rs, addr = list_instr_decode[i][1], list_instr_decode[i][2]
                if register[rs] == 0:
                    start_address = label[addr]
                    _, nb_instr = instr_operation(list_instr_decode, start_address, end_address, nb_instr)

            elif opc == 17:
                rs, addr = list_instr_decode[i][1], list_instr_decode[i][2]
                if register[rs] != 0:
                    start_address = label[addr]
                    _, nb_instr = instr_operation(list_instr_decode, start_address, end_address, nb_instr)

            elif opc == 18:
                n = list_instr_decode[i][1]
                if n == 0:
                    tries = 0
                    while 1:
                        a = input("Enter the value that you want to put into the register 1 :")
                        tries +=1
                        if tries == 3:
                            break
                        if a.isdigit():
                            a = int(a)
                            break
                        else:
                            os.system("echo Error!! please enter a int character")
                    register[1] = a
                elif n == 1:
                    print(register[1])
                elif n == 5:
                    register[2] = random.randint(register[6], register[7])
                    print("Welcome to the Guessing Game ! A random number has just been chosen, it's up to you to play!")
                elif n == 6:
                    print("It's more!")
                elif n == 7:
                    print("It's more!")
                elif n == 8:
                    print("Victory! Well played!")
            elif opc == 19:
                break
    return register, nb_instr


def main():
    create_memory()
    # Ouverture du fichier binaire
    file = open("examples/file_bin.txt", "r")
    list_instr = file_layout(file)
    list_instr_decode = instr_decode(list_instr)
    start_time = time.time()
    final_register = instr_operation(list_instr_decode, 0, len(list_instr_decode) - 1, nb_instr=0)
    end_time = time.time()
    exe_time = end_time - start_time
    return(exe_time, final_register)


if __name__ == '__main__':
    # Appel de la fonction principale
    exe_time, final_register = main()
    os.system('echo Etats des registres : ' + str(final_register[0]))
    os.system('echo Execution time : ' + str(exe_time) + ' seconds')
    if exe_time !=0:
        os.system('echo Instructions par seconde: ' + str(final_register[1] / exe_time))
        os.system('echo MIPS: ' + str(final_register[1] / exe_time/1000000))


