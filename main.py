import random

World_min = -100
World_max = 100
Max_steps = 30

world_elements = {
    (2, 3): "bonus",
    (-4, 1): "storm",
    (0, -2): "station"
}


def get_int(promp, default):
    try:
        return int(input(promp))

    except ValueError:
        print(f"Błędna wartość! Użyto wartości domyślnej: {default}")
        return default


def setup_game():

    print("Plan wyprawy")

    name = input("Imię łazika: ")

    start_x = get_int(" X: ", 0)
    start_y = get_int(" Y: ", 0)

    energy = get_int(" energia: ", 20)

    goal_x = get_int(" cel X: ", 5)
    goal_y = get_int(" cel Y: ", 5)

    game = {
        "name": name,
        "x": start_x,
        "y": start_y,
        "energy": energy,
        "goal_x": goal_x,
        "goal_y": goal_y,
        "steps": 0,
        "events": []
    }

    print("\n=== START WYPRAWY ===")
    print(f"Łazik: {name}")
    print(f"Położenie: ({start_x}, {start_y})")
    print(f"siła: {energy}")
    print(f" cel: ({goal_x} {goal_y})")
    print(f"Granice:  {World_min}  {World_max}")
    print(f"Limit kroków: {Max_steps}")

    return game


def move(game, direction):

    old_x = game["x"]
    old_y = game["y"]

    print(f"\nPozycja zanim ruszysz: ({old_x}, {old_y})")
    print(f"Energia zanim się poruszysz: {game['energy']}")

    if direction == "w":
        game["y"] += 1

    elif direction == "s":
        game["y"] -= 1

    elif direction == "a":
        game["x"] -= 1

    elif direction == "d":
        game["x"] += 1

    else:
        print("Zły kierunek!")
        return

    if (
        game["x"] < World_min, 
        game["x"] > World_max ,
        game["y"] < World_min ,
        game["y"] > World_max
    ):

        print("Próba wyjścia poza mapę! Ruch anulowany.")

        game["x"] = old_x
        game["y"] = old_y

    else:
        print(f"Nastepnie: ({game['x']}, {game['y']})")

    game["energy"] -= 1
    game["steps"] += 1

    print(f"Energia po ruchu: {game['energy']}")


def check_tile(game):

    position = (game["x"], game["y"])

    if position in world_elements:

        tile_type = world_elements[position]

        if tile_type == "bonus":

            game["energy"] += 5

            print("Znaleziono panel słoneczny! +5 energii")

            game["events"].append("Panel słoneczny")

        elif tile_type == "storm":

            game["energy"] -= 3

            print("Burza piaskowa! -3 energii")

            game["events"].append("Burza piaskowa")

        elif tile_type == "station":

            game["energy"] += 10

            print("Stacja ładowania! +10 energii")

            game["events"].append("Stacja ładowania")


def random_event(game):

    r = random.randint(1, 10)

    if r == 3:

        game["energy"] -= 2

        print("Losowe zdarzenie: Awaria silnika! -2 energii")

        game["events"].append("Awaria silnika")

    elif r == 7:

        game["energy"] += 2

        print("Losowe zdarzenie: Idealna pogoda do ładowania! +2 energii")

        game["events"].append("Dodatkowe ładowanie")


def check_end(game):

    if game["y"] == game["goal_y"] and game["x"] == game["goal_x"]:
        return True, "Dotarto do celu"

    if game["energy"] <= 0:
        return True, "Brak energii"

    if game["steps"] >= Max_steps:
        return True, "Przekroczono limit kroków"

    return False, ""


def final_report(game, reason):

    print("\n============================")
    print("      RAPORT KOŃCOWY")
    print("============================")

    print(f"łazik: {game['name']}")
    print(f"finished: ({game['x']}, {game['y']})")
    print(f" kroki: {game['steps']}")
    print(f" energia: {game['energy']}")
    print(f"Why zakończenia: {reason}")

    print("\nWażne zdarzenia:")

    if len(game["events"]) == 0:
        print("Brak specjalnych zdarzeń")

    else:
        for event in game["events"]:
            print(f"- {event}")

    score = game["energy"] * 10 - game["steps"]

    print(f"\nWynik: {score}")

    if reason == "Dotarto do celu":
        print("Status wyprawy: SUKCES")

    else:
        print("Status wyprawy: PORAŻKA")


def run_game():

    game = setup_game()

    running = True

    while running:

        print("\n-------------------------")
        print(f" krok: {game['steps'] + 1}")
        print(f"pozycja: ({game['x']}, {game['y']})")
        print(f" energia teraz: {game['energy']}")

        direction = input("Wybierz klawisz (w/a/s/d): ").lower()

        move(game, direction)

        check_tile(game)

        random_event(game)

        finished, reason = check_end(game)

        if finished:
            running = False

    final_report(game, reason)


if "__main__" == __name__:

    while True:

        run_game()

        again = input("\nCzy chcesz zagrać jeszcze raz? (t/n): ").lower()

        if again == "n":
            print("Dziękuję za grę!")
            break


