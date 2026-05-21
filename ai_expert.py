from openai import OpenAI
from openai import (
    APIConnectionError,
    RateLimitError,
    APIStatusError,
    AuthenticationError,
    APITimeoutError
)
import json
import api_key
import user_interface as ui

class AIQuestionGenerationError(Exception):
    """Raised when AI question generation fails."""
    pass

def generate_questions(wiki_content, child_age):
    client = OpenAI(
        api_key=api_key.api_key    )


    schema = {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "minItems": 4,
                "maxItems": 4,
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "choices": {
                            "type": "array",
                            "minItems": 4,
                            "maxItems": 4,
                            "items": {"type": "string"}
                        },
                        "correct_answer_index": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 3
                        },
                        "explanation": {"type": "string"},
                        "difficulty": {
                            "type": "string",
                            "enum": ["easy", "medium", "hard"]
                        }
                    },
                    "required": [
                        "question",
                        "choices",
                        "correct_answer_index",
                        "explanation",
                        "difficulty"
                    ],
                    "additionalProperties": False
                }
            }
        },
        "required": ["questions"],
        "additionalProperties": False
    }
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"""
    
    Create 4 multiple-choice questions for a child aged {child_age}. 
    MAKE THE QUESTIONS VERY EASY AND FUN!

    Use only the Wikipedia content below.

    Rules:
    - Questions must be suitable for the child's age. 
    - Write the question in an easy language and avoid
      difficult words like "conventionally" or treaties.
      Keep the language VERY simple
    - Do not make the questions too hard!
    - Make the questions fun!
    - Create exactly 4 questions.
    - Each question must have exactly 4 choices.
    - Do not add letters before the choices, for example A) or B) or C) or D).
    - Only one choice must be correct.
    - Do not use facts outside the provided content.
    - Keep the language simple.
    - Be sure that index of the correct choice should be distributed randomly.
    - Check that the questions follow these rules.  

    Wikipedia content:
    {wiki_content}
    """,
        text={
            "format": {
                "type": "json_schema",
                "name": "children_wikipedia_quiz",
                "schema": schema,
                "strict": True
            }
        }
    )

    except (APITimeoutError, AuthenticationError, RateLimitError,
            APIConnectionError, APIStatusError) as e:
        print("Error from open AI. Questions can not be derived due to ...", e)
        raise AIQuestionGenerationError("Questions can not be obtained. Need to abort") from e

    quiz = json.loads(response.output_text)

    # print(json.dumps(quiz, indent=2, ensure_ascii=False))
    return quiz


def run_quiz(quiz):


    # List to store the result of each question
    results = []

    # Counter for correct answers
    score = 0

    # enumerate() gives both:
    # - the index
    # - the actual question object
    #
    # question_index -> 0, 1, 2 ...
    # question_data  -> dictionary containing question data
    #
    for question_index, question_data in enumerate(quiz["questions"]):
        choices = question_data["choices"]

        ui.show_question(question_index, question_data, choices)
        # Get the index of the correct answer
        #
        # Example:
        # If correct_index = 2
        # then choices[2] is the correct answer
        #
        correct_index = question_data["correct_answer_index"]

        # Maximum number of attempts allowed
        max_attempts = 2

        # Start from attempt 1
        attempt = 1

        # Initially assume the answer is wrong
        is_correct = False

        # Keep asking while attempts remain
        while attempt <= max_attempts:

            # Ask the user for an answer
            #
            # input() returns a string,
            # so int() converts it to integer
            #
            user_answer = ui.user_answers_question(attempt)

            # Check if the answer is correct
            if user_answer == correct_index:


                ui.one_answer_feedback(True, False, choices[correct_index])

                # Increase score
                score += 1

                # Mark question as correctly answered
                is_correct = True

                # Exit the attempt loop
                # because the user answered correctly
                break

            else:

                # User answered incorrectly
                if attempt < max_attempts:
                    ui.one_answer_feedback(False, attempt >= max_attempts, "")

                else:
                    ui.one_answer_feedback(False, attempt >= max_attempts, choices[correct_index])


            # Move to the next attempt
            attempt += 1

        # Save question result into results list
        #
        # Each result is stored as a dictionary
        #
        results.append({

            # Store question text
            "question": question_data["question"],

            # Store user's final answer index
            "user_answer_index": user_answer,

            # Store correct answer index
            "correct_answer_index": correct_index,

            # True or False
            "is_correct": is_correct,

            # Number of attempts used
            "attempts_used": attempt
        })

    # Total number of questions
    total_questions = len(quiz["questions"])
    ui.score_board(score, total_questions)

    # Return all question results
    return results, score, total_questions