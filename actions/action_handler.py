def PerformAction(data):
    intent = data.get("INTENT")

    if intent in ["ask_damage", "ask_temperature"]:
        part = data.get("PART")
        direction = data.get("DIRECTION")
        side = data.get("SIDE")
        position = ""

        if direction == "front":
            if side == "left":
                position = "a"
            elif side == "right":
                position = "b"
        elif direction == "rear":
            if side == "left":
                position = "c"
            elif side == "right":
                position = "d"
        
        match intent:
            case "ask_damage":
                HandleDamageQuery(part, position)
            case "ask_temperature":
                HandleTemperatureQuery(part, position)
    else:
        print(intent)

def HandleDamageQuery(part, position):
    # Replace with getting appropriate data 
    print(f"{part} {position} is at 85%")

def HandleTemperatureQuery(part, position):
    # Replace with getting appropriate data 
    print(f"{part} {position} is at 90 degrees")