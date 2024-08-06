def load_facts(filepath):
    with open(filepath, 'r') as file:
        facts = file.readlines()
    return [fact.strip() for fact in facts]

def load_rules(filepath):
    with open(filepath, 'r') as file:
        rules = file.readlines()
    return [rule.strip() for rule in rules]
