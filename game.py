import json
import random

import random

def generate_virtual_board():
    # Listes des éléments de jeu
    pieces = ["cuisine", "salon", "bureau", "bibliotheque", "toilette", "garage"]
    personnages = ["Moutarde", "Rose", "Violet", "Olive", "Leblanc", "Pervenche"]
    armes = ["couteau", "chandelier", "revolver", "corde", "poison", "stylet"]

    # Mélanger les listes pour obtenir des éléments aléatoires
    random.shuffle(pieces)
    random.shuffle(personnages)
    random.shuffle(armes)

    # Sélectionner le coupable, la victime, l'arme et la salle du meurtre
    coupable = personnages.pop(random.randint(0, len(personnages) - 1))
    victime = personnages.pop(random.randint(0, len(personnages) - 1))
    arme_crime = armes[random.randint(0, len(armes) - 1)]
    salle_meurtre = random.choice(pieces)

    # Sélectionner une piece différente pour le coupable
    pieces_restantes = [piece for piece in pieces if piece != salle_meurtre]
    salle_coupable = random.choice(pieces_restantes)

    # Répartir les personnages et les armes dans les pieces
    board = {
        "salle_depart": pieces[0],
        "coupable": coupable,
        "victime": victime,
        "arme_crime": arme_crime,
        "salle_meurtre": salle_meurtre,
        "pieces": {}
    }

    for piece in pieces:
        if piece == salle_meurtre:
            # La salle du meurtre doit contenir la victime 
            personnage = victime
            arme = armes.pop() if armes else None
        elif piece == salle_coupable:
            # Placer le coupable dans une piece différente
            personnage = coupable
            arme = armes.pop() if armes else None
        else:
            # Assigner les personnages et armes restants
            personnage = personnages.pop() if personnages else None
            arme = armes.pop() if armes else None

        board["pieces"][piece] = {
            "personnage": personnage,
            "arme": arme
        }
                
    # Sauvegarder le tableau virtuel dans un fichier JSON
    with open('data/state_board.json', 'w') as outfile:
        json.dump(board, outfile, indent=4, ensure_ascii=False)
    
    return board

def generate_facts(board):
    facts = [
        f'EstMort({board["victime"]})',
        f'Personne_Piece({board["victime"].capitalize()},{board["salle_meurtre"].capitalize()})',
        f'Arme_Piece({board["arme_crime"].capitalize()},{board["salle_meurtre"].capitalize()})'
    ]

    # for piece, data in board["pieces"].items():
    #     if data["personnage"]:
    #         facts.append(f'Personne_Piece({data["personnage"]}, {piece})')
    #     if data["arme"]:
    #         facts.append(f'Arme_Piece({data["arme"]}, {piece})')

    return facts
