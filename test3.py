f = open("klasser.json", "r")
x = f.read()
y = json.loads(x)

snart = y['overwriteOtherData']['data']['classes']
klasser = []

for klass in snart:
    namn = klass['groupName']
    klasser.append(namn)

print(klasser)