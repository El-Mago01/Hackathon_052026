from PIL import Image
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyfiglet import Figlet
import time


IMAGES_DIR = "images"
SOUND_DIR = "sounds"

class BColors:
    """Utility class to represent colors on the terminal."""

    USER_QUESTIONS = "\033[96m"
    CATEGORIES = "\033[93m"
    ART = "\033[95m"
    ANSWERS = "\033[97m"
    CORRECT = "\033[92m"
    WRONG = "\033[91m"
    QUIZ_END = "\033[95m"
    SCORE = "\033[93m"
    PLAY_AGAIN = "\033[96m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def print_image_ascii_art(selected_category, stop_event, sleep_time:float=0.4,
                          width:int=80, height:int=40):
    image_to_convert = os.path.join(IMAGES_DIR, selected_category+".jpg")
    ASCII = "@%#*+=-:. "

    img = Image.open(image_to_convert)
    img = img.resize((width, height))
    img = img.convert("L")
    pixels = img.getdata()
    chars = "".join(ASCII[pixel // 26] for pixel in pixels)
    for i in range(0, len(chars), width):
        time.sleep(sleep_time)
        print(BColors.ART + chars[i:i+width] + BColors.ENDC)

def pretty_print_text(text):
    figlet = Figlet(font="slant")
    print(BColors.ART + figlet.renderText(text) + BColors.ENDC)

def print_welcome_message():
    pretty_print_text("Let's Play!")
    # print("Welcome to the Child's wiki game!")

def get_user_profile():
    print_welcome_message()
    name = input(BColors.USER_QUESTIONS + "What is your name? : " + BColors.ENDC)
    while True:
        try:
            age = int(input(BColors.USER_QUESTIONS + "What is your age?  : " + BColors.ENDC))
            break
        except ValueError:
            print("That wasn't a number. Please enter a number")
    return name, age

def get_input_category(number_categories):
    while True:
        try:
            category_index = int(input(BColors.USER_QUESTIONS + "What category do you want to select : " + BColors.ENDC))
            if category_index > number_categories or category_index == 0:
                raise IndexError(BColors.USER_QUESTIONS + "This number is out of range")
            return category_index
        except ValueError:
            print("Please provide a number, not text.")
        except IndexError as e:
            print(e)

def get_user_category(categories):
    category_keys = list(categories.keys())
    index = 1
    for category in category_keys:
        print(f"{BColors.ANSWERS}{index:5} {category}")
        index += 1
    category_index = get_input_category(len(categories))
    return category_keys[category_index-1]

def one_answer_feedback(answer_correct, max_attempt_reached: int=0, correct_answer:str=""):
    pygame.mixer.init()
    if answer_correct:
        print(f"{BColors.CORRECT}{BColors.BOLD}✅Correct")
        pygame.mixer.music.load(os.path.join(SOUND_DIR, "dog.mp3"))
        pygame.mixer.music.play()
    else:
        if max_attempt_reached:
            print(f"{BColors.WRONG}{BColors.BOLD}❌Not quite...{BColors.ENDC}")
            print(f"{BColors.CORRECT}The correct answer is: {correct_answer}{BColors.ENDC}")
            pygame.mixer.music.load(os.path.join(SOUND_DIR, "cat.mp3"))
            pygame.mixer.music.play()
        else:
            print(f"{BColors.WRONG}Not quite...Try again{BColors.ENDC}")


def thank_you(name):
    pretty_print_text(f"Bye {name}!")
    img_path ="Diplodocus"
    print_image_ascii_art(img_path,None, 0, 50, 20)

def show_question(question_index, question_data,choices):
    print(BColors.ANSWERS + "=====================================" + BColors.ENDC)

    # Display question number
    # +1 because indexes start at 0
    print(f"{BColors.USER_QUESTIONS}{BColors.BOLD}Question {question_index + 1}: + {BColors.ENDC}")

    # Print the question text
    print(BColors.USER_QUESTIONS + question_data["question"] + BColors.ENDC)

    # Store the answer choices in a variable
    # Print all answer choices
    #
    # choice_index -> 0,1,2,3
    # choice       -> answer text
    #
    for choice_index, choice in enumerate(choices):
        print(f"{BColors.ANSWERS}{choice_index + 1}. {choice}{BColors.ENDC}")

def user_answers_question(attempt):
    while True:
        try:
            user_answer = int(input(f"{BColors.USER_QUESTIONS}Attempt {attempt} - Your answer: {BColors.ENDC}"))
            if 1 <= user_answer <= 4:
                user_answer = user_answer - 1  # _fix_ Fixes the index by -1
                return user_answer
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("That wasn't a number. Please enter a number between 1 and 4")

def score_board(score, total_questions):
    print(f"{BColors.QUIZ_END}===================={BColors.ENDC}")
    print(f"{BColors.QUIZ_END}{BColors.BOLD}Quiz finished{BColors.ENDC}")

    # Display final score
    print(f"{BColors.SCORE}Score: {score}/{total_questions}{BColors.ENDC}")

def play_game_again() -> bool:
    while True:
        play_again = input(f"{BColors.PLAY_AGAIN}Play again? yes/no: {BColors.ENDC}").lower()
        if play_again not in ("yes", "no", "y", "n"):
            print("Please answer yes or no (y or n).")
        else:
            break

    if play_again in ("yes", "y"):
        return True
    else:
        return False


def display_final_scoreboard(round_results):
    """
    Displays the results of each round and the total results.

    """
    total_score = 0
    number_of_questions = 0

    print(f"{BColors.QUIZ_END}{BColors.BOLD}--- Round Scores ---\n")
    for i in range(len(round_results)):
        print(f"{BColors.SCORE}    Round {i + 1}")
        print(f"{BColors.SCORE}    {round_results[i]['score']}/{round_results[i]['total_questions']}")
        total_score += round_results[i]['score']
        number_of_questions += round_results[i]['total_questions']
    print(f"{BColors.QUIZ_END}{BColors.BOLD}\n=== Final Score ===")
    percentage = round((total_score / number_of_questions) * 100)
    print(f"{BColors.SCORE}   {total_score}/{number_of_questions} - {percentage}%")

    input(f"{BColors.PLAY_AGAIN}Press Enter to quit.")