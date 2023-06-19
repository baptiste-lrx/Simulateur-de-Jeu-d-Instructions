        add r0, 4, r1       #init r1 à 4
        add r0, 8, r2       #init r2 à 8
        add r1, r2, r3      #Addition r1+r2 = r3
        sub r2, r1, r4      #Soustraction r2-r1=r4
        add r0, 20, r30     #On initialise r30 pour tester la soustraction par l'addition
        add r0, 6, r31      #On initialise r31 utilisé par braz
label1:
        add r30, -2, r30    #On teste la soustraction par l'addition
        sub r31, 2, r31     #soustraction du registre 31
        mul r1, r2, r5      #Multiplixation r1*r2=r5
        div r2, r1, r6      #etc etc se référer au cours
        and r1, r4, r7
        or r1, r4, r8
        xor r1, r4, r9
        shl r1, r2, r10
        shr r2, r1, r11
        branz r31, label1   #Tant que r31 ne vaut pas 0, on remonte au label 1
        slt r2, r1, r12
        sle r1, r2, r13
        seq r6, r9, r14
        load r0, 10, r15
        store r0, 21, r16
        stop                #Break
