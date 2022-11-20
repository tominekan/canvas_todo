import json
from jsondiff import diff

var1 = json.dumps({"a": [1, 2, 3, 4]})
var2 = json.dumps({"a": [1, 2, 3, 4, 5]})
diffs = diff(var1, var2, load=True)

print(diffs)
print(diffs["a"])
print(diffs["a"].values())
print(list(diffs["a"].values())[0])

if (len(diffs) == 0):
    print("tonkaaa")