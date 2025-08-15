#Create and empty set
s = set()

#Add elements to set
s.add(1)
s.add(2)
s.add(3)
s.add(4)
s.add(5)
s.add(1)

s.remove(3)

print(s)
print(f"The set has {len(s)} elements")
