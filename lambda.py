people = [
        {"name": "Harry", "house": "Gryffindor"},
        {"name": "Cho", "house": "Ravenclaw"},
        {"name": "Draco", "house": "Slytherine"},
        ]

people.sort(key= lambda person: person["house"])

print(people)
