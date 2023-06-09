## C64_robot_state_machine

Membres d'équipe : 
- Antonin Lenoir
- Jane Caron
- Mathieux Mailloux
- Alexandre Caron

## Librairie FiniteStateMachine

- Estimé de la proximité de ce que vous avez réalisé et la
conception donnée : 95%
- Surchage des blinkers réalisée mais non-utilisée; nous avons fait une fonction blink pour chacune des signatures que nous avons utilisées pour le reste du projet.  Cela dit, nous avons écrit la fonction blink avec surcharge (blinker_sideblinker.py ligne 187), mais par manque de temps pour le refactor, elle n'est pas utilisée là où elle pourrait être appelée.

## Infrastructure Robot

- Validation intégrité : On instancie les dispositifs du robot dans un try/catch, et on vérifie s'il ont bien tous été instanciés ou si l'un d'eux est None ce qui signifie que l'intégrité du robot est compromise et que le programme est dirigé vers son état terminal. 
- Télécommande : Nous avons créé une RemoteControlCondition qui hérite de Condition et qui prend en paramètre une valeur attendue et la télécomande du robot. Elle compare la valeur d'entrée de la télécommande et la valeur attendue. Une bascule simple est intégrée à la méthode compare().
- Télémètre et Servo moteur : Aucune abstraction réalisée.
- Moteurs : Aucune abstraction réalisée.
- Couleur pour les yeux : getter et setter dans le eye_blinker implémentés par les property de python.

## Structure générale du logiciel

- Le logiciel repose sur une librairie générique qui implémente les classes Finite State Machine, State, Transition et Condition. 
- Notre application C64 représente une machine d’états qui hérite d’une classe Finite State Machine. A partir de cette classe, différents états applicatifs sont définis, qui représentent les différents états de notre machine. Chaque états héritent d’une classe StateWithRobot qui hérite d’une classe Monitored State. La particularité de StateWithRobot est qu’il fait une agrégation d’une classe générique Robot. Dans notre projet, chaque états possèdent une Conditional Transition qui hérite d’une Transition. Chaque transition possède une condition adaptée, selon le comportement désiré. De plus nous avons créé une condition particulière permettant de prendre en considération les touches appuyées de la télécommande du robot. Le choix de la touche peut être configurable et permet une transition ou une action. 
- Avec l’architecture mise en place, il est aisé de rajouter une nouvelle tâche. Il nous suffit de créer une classe héritant de MonitoredState ou StateWithRobot et d’insérer l’action désirée dans sa méthode do_entering_action. 


## Autres éléments d’abstraction

- Nous avons créé 2 fonctions créant les transitions vers des états dans la classe Blinker du fichier blinker_sideblinker.py. La première "connect_monitoredstate_to_state" ajoute une transition vers un état à un monitored_state qui survient si une condition StateValueCondition est vrai. La deuxième "connect_timed_state_to_transit" ajoute une transition vers un état à un état qui survient si une condition StateEntryDurationCondition est vrai, et retourne la condition pour pouvoir y changer sa variable duration.
- Nous avons créé une méthode shut_down() dans la classe Robot du fichier robot.py qui permet d'éteindre les éléments du robot qui avaient été initialisés, avant sa fermeture et ce au plus bas niveau possible
- Ajout d'une condition StateValueInferiorCondition afin de mieux profiter du "range finder"
- Création d'une méthode blink() permettant une surcharge par le support de plusieurs signatures différentes.