import json
def wipe():
    filepath = "DoneRes.json"

    # Clearing json file storing ids
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)

    print("Jason is wiped hell yeah")
if __name__=="__main__":
    wipe()
