import csv
import json

import driver

from google import genai

def generate_text(prompt):
    client = genai.Client(api_key=str(open("api_key.txt").read()))

    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
    )
    return response.text

def create_prompt(question: str, rubric: str, responses: list, example_response: str):
    """
    Generates prompt
    question: string - the question you would like to be verified
    rubric: str - the rubric for the question
    ex: 
        +5 points - "Gives one of the following drawbacks:
        - cost, e.g. 'costs more to have two buses'

        - additional complexity

        - heat

        - power consumption"
        +5 points - Gives a 2nd drawback from the above list
        +0 points - Incorrect/Blank
    responses: list - a list of responses that need to be graded. Limit to 10
    """

    response_list = str()
    for response in responses:
        response_list += '"' + response + '"' + "\n"
    return (
        f"Here is a question:{question}\n"
        "Here is how the question's response should be graded:\n"
        f"{rubric}\n"
        "Given the above rubric, assign a graded score for the following responses with the one number for each response. You can be lenient with your grading. Simply provide an ordered list of the scores. Do not provide an explanation: \n"
        f"{response_list} \n\n"
        f"An example response would be: {example_response}\n"
        "There should only be numbers and commas and it should all be in one row"
    )

def read_csv_columns(file_path, score, response):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if score not in reader.fieldnames or response not in reader.fieldnames:
            print(f"Error: One or both columns not found in the CSV file. Available columns: {reader.fieldnames}")
            return
        responses: list = list()
        retscore: list = list()
        length: int = 0
        for row in reader:
            responses.append(row[response])
            length += 1
            retscore.append(row[score])

        return responses, score, length


