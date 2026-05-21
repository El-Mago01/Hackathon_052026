import threading
import fetch_wiki_data as fwd
import user_interface as ui
import ai_expert as ask_ai
from threading import Thread
import requests




MAP_CATEGORY_TO_TITLE = {
    "Animals": [
        "Animal", "Dog", "Cat", "Pinniped" ],
    "Space" : [
        "Outer space", "Moon", "Milky Way", "Galaxy"],
    "Dinosaurs" : [
        "Dinosaur", "Tyrannosaurus", "Velociraptor", "Diplodocus"],
    "POWER-KID": [ "Dog", "Milky Way", "Tyrannosaurus"]
    }


def can_reach_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code < 500
    except requests.exceptions.RequestException:
        return False


def main():
    rounds_played = 0
    round_results = []          # Stores dictionaries of round number, score, total questions for each round played

    if not can_reach_url("https://google.com/"):
        print("Cannot reach internet. Please check your connection.")
        exit()
    name, age = ui.get_user_profile()
    # Infinite loop:
    # The quiz restarts as long as the user types "yes"

    while True:

        selected_category = ui.get_user_category(MAP_CATEGORY_TO_TITLE)
        wiki_data = ""
        for sub_category in MAP_CATEGORY_TO_TITLE[selected_category]:
            wiki_data += fwd.fetch_wiki_data(sub_category)
        child_wiki_data = (age, wiki_data)
        stop_event = threading.Event()
        loader_thread = threading.Thread(
            target = ui.print_image_ascii_art,
            args = (selected_category, stop_event, 0.4), daemon = True,)
        loader_thread.start()
        try:
            quiz=ask_ai.generate_questions(age, wiki_data)
        finally:
            stop_event.set()
            loader_thread.join()
        rounds_played += 1
        results, score, total_questions = ask_ai.run_quiz(quiz)

        round_dict = {
            'round': rounds_played,
            'score': score,
            'total_questions': total_questions
        }

        round_results.append(round_dict)

        # print(round_results)

        # Ask if the user wants to play again
        if ui.play_game_again() == False:
            # Exit the loop if answer is not "yes"
            break
    # print(round_results)
    ui.display_final_scoreboard(round_results)
    ui.thank_you(name)

if __name__ == "__main__":
    main()