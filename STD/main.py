import random
import json
import csv
import os

locations = {
    "beach": "You are on a beautiful beach by the sea. The sand is soft, the water is crystal clear.",
    "city": "City center with noise and hustle. There are many shops and cafes here.",
    "forest": "Dense forest with thick foliage. Trees are rustling around you.",
}

items_on_beach = {"mattress", "swimsuit", "sunscreen"}
items_in_city = {"coffee", "book", "bag"}
items_in_forest = {"compass", "knife", "flashlight"}

def enter_name():
    while True:
        name = input("Enter your name: ")
        if name:
            return name
        else:
            print("Please enter a name.")

def choose_location():
    print("Choose a location:")
    for location in locations:
        print(location)
    while True:
        try:
            choice = input("Your choice: ")
            if choice in locations:
                return choice
            else:
                print("Please choose one of the available locations.")
        except KeyboardInterrupt:
            print("\nExiting the game.")
            exit()

def choose_item(location):
    if location == "beach":
        items = items_on_beach
    elif location == "city":
        items = items_in_city
    elif location == "forest":
        items = items_in_forest

    if items:
        return random.choice(list(items))
    else:
        return None

def solve_riddles():
    riddles = [
        "Riddle 1: What can you see with your eyes closed?",
        "Riddle 2: What always runs but never walks?",
        "Riddle 3: What has a key but can't open anything?",
    ]
    answers = ["dreams", "time", "keyboard"]

    for i in range(len(riddles)):
        print(riddles[i])
        while True:
            user_answer = input("Your answer: ").strip().lower()
            if user_answer == answers[i]:
                print("Correct! Move on to the next riddle.")
                break
            else:
                print("Incorrect. Try again.")

    print('You did it! You found the artifact. Now you can do anything.')

def search_for_artifact(character_name):
    print(f"{character_name}: I set out to find the artifact in the forest, as told by a stranger.")
    probability_of_finding = random.random()

    if probability_of_finding < 0.3:
        print("You spent a lot of time searching, but could not find the artifact. On your way back, you encountered a powerful wizard, and unable to defeat him, you were killed.")
    else:
        print("While you were searching, your efforts were not in vain. You found a magical artifact!")

        print("You have to solve 3 riddles to unlock the magical power of the artifact.")
        solve_riddles()

def dialogue(character_name, interlocutor):
    print(f"{interlocutor['name']}: Hello, {character_name}. What brings you to this forest?")
    response = input(f"{character_name}: ")
    print(f"{character_name}: {response}")

    if interlocutor['name'] == "Wizard":
        print(f"{interlocutor['name']}: Welcome to my forest. I heard you are looking for a magical artifact. I will tell you a story: this artifact is hidden deep in the forest and is guarded by magical traps. If you can pass through them, the artifact will be yours.")
    else:
        print(f"{interlocutor['name']}: Let me tell you a story. Long ago, a wizard lived in this forest. He hid a magical artifact somewhere here, but no one could find it. You can try your luck and find this artifact. What do you say?")

    while True:
        try:
            if interlocutor['name'] == "Wizard":
                choice = input(f"{character_name} (1 - Continue, 2 - Refuse): ")
            else:
                choice = input(f"{character_name} (1 - Agree, 2 - Refuse): ")
            if choice == '1':
                if interlocutor['name'] == "Wizard":
                    search_for_artifact(character_name)
                else:
                    print(f"{character_name}: Agree, I will try to find the artifact.")
                break
            elif choice == '2':
                print(f"{character_name}: Refusing, I'm not interested in this.")
                break
            else:
                print("Please enter 1 to agree or 2 to refuse.")
        except KeyboardInterrupt:
            print("\nExiting the game.")
            exit()

def save_game(name, happiness):
    data = {"name": name, "happiness": happiness}
    with open("save.json", "w") as file:
        json.dump(data, file)

def load_game():
    try:
        with open("save.json", "r") as file:
            data = json.load(file)
            return data["name"], data["happiness"]
    except FileNotFoundError:
        return None, 0

def main():
    name, happiness = load_game()
    if name:
        print(f"Welcome back, {name}!")

    if happiness >= 2:
        print("Your happiness: happy ending! You found sunscreen and returned home with a great tan.")
    else:
        print("Your happiness: The end of the story!")

    if input("Do you want to start a new game? (y/n): ").strip().lower() != 'y':
        delete_save()
        return

    name = enter_name()
    print(f"Welcome, {name}!")

    happiness = 0

    for _ in range(3):
        current_location = choose_location()
        location_description = locations[current_location]
        selected_item = choose_item(current_location)

        print(location_description)
        if selected_item:
            print(f"You found an item: {selected_item}")
            if "sunscreen" in selected_item:
                happiness += 1

    dialogue(name, {"name": "Stranger"})
    dialogue(name, {"name": "Girl"})
    dialogue(name, {"name": "Wizard"})

    save_game(name, happiness)
    print("The game is over. Your data has been saved.")

    with open("data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, happiness])

def delete_save():
    try:
        os.remove("save.json")
        print("Save deleted.")
    except FileNotFoundError:
        print("Save not found.")

main()
