# Simulateur de Jeu d'Instructions

Bienvenue dans le projet de simulateur de jeu d'instruction en Python !

Ce projet comprend un assembleur (ASM) pour la conversion du code d'assemblage en code machine, une machine virtuelle (VM) pour l'exécution du code machine et une mémoire cache pour stocker les données les plus fréquemment utilisées. Le but de ce projet est de permettre aux utilisateurs d'écrire et d'exécuter leur propre code machine en utilisant un ensemble prédéfini d'instructions.

Le simulateur de jeu d'instruction peut être exécuté en utilisant le fichier principal "main.py". Il permet à l'utilisateur d'entrer du code d'assemblage et de le convertir en code machine en utilisant l'assembleur. Le code machine est ensuite chargé dans la VM pour être exécuté. La VM interagit avec la mémoire cache pour stocker et accéder aux données.

Le simulateur de jeu d'instruction prend en charge un ensemble prédéfini d'instructions pour les opérations arithmétiques, logiques et de saut. Les instructions sont définies dans le fichier "instruction_set.py". Les utilisateurs peuvent ajouter de nouvelles instructions en les définissant dans ce fichier.

Le fichier "memory.py" contient la mémoire cache. Les utilisateurs peuvent spécifier la taille de la mémoire cache et les adresses qu'ils souhaitent stocker en cache. Les adresses qui ne sont pas stockées en cache sont stockées dans la mémoire principale.

Le simulateur de jeu d'instruction peut être utilisé à des fins éducatives ou pour tester des programmes qui utilisent un ensemble prédéfini d'instructions. Les utilisateurs sont invités à explorer le code et à le modifier selon leurs besoins.

J'espère que ce projet sera utile pour vous et n'hésitez pas à me contacter si vous avez des questions ou des commentaires !
