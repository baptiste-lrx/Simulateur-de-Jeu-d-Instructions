label1 : #init
		add r0, 0, r6
		add r0, 10, r7
		scall 5	#Le programme genere un nb aléatoire entre la valeur stockée dans r6 et celle stockée dans r7 et le met dans r2
             
label2: #ask player a number
		scall 0 
          	add r1, 0, r3  #Valeur du joueur dans r3

label3: #comparaison
		add r0, 1, r4
		slt r3, r2, r4
            braz r4, label5
            slt r2, r3, r4
            braz r4, label4
            jmp label6, r5

label4 : #Affiche que c'est plus
		scall 7			
       	add r20, 1, r20
       	jmp label2, r5

label5 : #Affiche que c'est moins
		scall 6			 
      	add r20, 1, r20
      	jmp label2, r5

label6 : #Victory
		add r20,1,r20
         scall 8