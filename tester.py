t = [("pessoa", "F"), ("criança", "F"), ("adultos", "M")]

print([item for item in t if item[1] == "F"])
print([item for item in t if item[0] == "adultos"][0][1])

d = {"ele": "elu"}
print("elu" in d)

l = [("ele", "ela", "elu"), ("eles", "elas", "elus")]
print([i[0] for i in l])