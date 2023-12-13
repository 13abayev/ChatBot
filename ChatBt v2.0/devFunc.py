import json

def showlist():
    file_path = 'intents.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    i = 1
    for intent in data['intents']:
        print(i, intent['tag'])
        i += 1

#Developer options

def add():
    file_path = 'intents.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    showlist()
    tg = input("New tags name : ")
    patt = []
    item = ''
    while True:
        if item == "quit":
            break
        item = input("pattern : ")
        patt.append(item)
    new_intent = {
        "tag": tg,
        "patterns": patt,
        "responses": ""
    }
    data['intents'].append(new_intent)
    with open(file_path, 'w') as fl:
        json.dump(data, fl, indent=2)

def add_pattern():
    file_path = 'intents.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    lst = ['']
    for intent in data['intents']:
        lst.append(intent['tag'])
    showlist()
    op = int(input())
    var = data['intets'][lst[op]]
    patt = ''
    while True:
        if patt == quit:
            break
        var.append(patt)
    with open(file_path, 'w') as fl:
        json.dump(data, fl, indent=2)

def yukle(bag: list, tag : str):
    file_path2 = "/ChatBt v2.0/tags.json"

    with open(file_path2, "r", encoding='utf-8') as file1:
        data = json.load(file1)

    if tag in data:
        if bag not in data[tag]:
            data[tag].append(bag)
    else:
        data[tag] = [bag]

    with open(file_path2, "w") as tf:
        json.dump(data, tf, indent=1)

