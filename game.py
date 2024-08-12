import json
import random

def generate_virtual_board():
    # Listes des éléments de jeu
    pieces = ["cuisine", "salon", "bureau", "bibliothèque", "toilette", "garage"]
    personnages = ["Moutarde", "Rose", "Violet", "Olive", "Leblanc", "Pervenche"]
    armes = ["couteau", "chandelier", "revolver", "corde", "poison", "stylet"]

    # Mélanger les listes pour obtenir des éléments aléatoires
    random.shuffle(pieces)
    random.shuffle(personnages)
    random.shuffle(armes)

    # Sélectionner le coupable, la victime, l'arme et la salle du meurtre
    coupable = personnages.pop(random.randint(0, len(personnages) - 1))
    victime = personnages.pop(random.randint(0, len(personnages) - 1))
    arme_crime = random.choice(armes)
    salle_meurtre = random.choice(pieces)

    # Assigner les autres personnages et armes aux autres pièces
    board = {
        "salle_depart": pieces[0],
        "coupable": coupable,
        "victime": victime,
        "arme_crime": arme_crime,
        "salle_meurtre": salle_meurtre,
        "pieces": {}
    }

    for i, piece in enumerate(pieces):
        board["pieces"][piece] = {
            "personnage": personnages[i] if i < len(personnages) else None,
            "arme": armes[i] if i < len(armes) else None,
            "nord": None,
            "sud": None,
            "est": None,
            "ouest": None
        }

    # Définir les connexions entre les pièces (exemple simple de connexion)
    if len(pieces) >= 2:
        board["pieces"][pieces[0]]["sud"] = pieces[1]
        board["pieces"][pieces[1]]["nord"] = pieces[0]
    if len(pieces) >= 3:
        board["pieces"][pieces[1]]["est"] = pieces[2]
        board["pieces"][pieces[2]]["ouest"] = pieces[1]
    if len(pieces) >= 4:
        board["pieces"][pieces[2]]["sud"] = pieces[3]
        board["pieces"][pieces[3]]["nord"] = pieces[2]
    if len(pieces) >= 5:
        board["pieces"][pieces[3]]["est"] = pieces[4]
        board["pieces"][pieces[4]]["ouest"] = pieces[3]
    if len(pieces) >= 6:
        board["pieces"][pieces[4]]["sud"] = pieces[5]
        board["pieces"][pieces[5]]["nord"] = pieces[4]

    # Sauvegarder le tableau virtuel dans un fichier JSON
    with open('data/state_board.json', 'w') as outfile:
        json.dump(board, outfile, indent=4, ensure_ascii=False)

    print("Tableau virtuel généré avec succès : virtual_board.json")
