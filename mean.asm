#Test de la moyenne

scall 0 #a=4
add r0, r1, r2 #r0+r1=r2 (dans l'exemple pour a=4 on a r2=4)
scall 0 #a=4
add r1, r2, r3 #r1+r2=r3 (dans l'exemple pour a=4 on a r3=8)
div r3, r2, r4 #r3/r2=r4 (dans l'exemple pour a=4 on a r4=2)
add r0, r4, r1 #r0+r4=r1 (dans l'ex, r1 = 2)
scall 1