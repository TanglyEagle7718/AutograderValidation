import csv
import json
import os
import re
import time
import prompt_generation

MAX_REQUESTS_PER_MINUTE = 15
RATE_LIMIT_RESET_TIME = 60

HOMEWORK = "homework3"
QUESTION = "question2.4"

def extract_numbers(input_string):
    numbers = re.findall(r'\d+', input_string)
    return [int(num) for num in numbers]



# Load questions json
with open('questions.json', 'r') as file:
    data = json.load(file)

file_path = data[HOMEWORK]["csv_file"]
responses, score, rows_len = prompt_generation.read_csv_columns(file_path, 
                                    data[HOMEWORK][QUESTION]["ta_score"],
                                    data[HOMEWORK][QUESTION]["student_response"]
                                    )
#print(responses)


start_time = time.time()
api_requests = 0

llm_grading = list()
for i in range(0, rows_len, 20):

    end = i + 20
    if end > rows_len:
        end = rows_len
        break


    prompt = prompt_generation.create_prompt(data[HOMEWORK][QUESTION]["question"], 
                                            data[HOMEWORK][QUESTION]["rubric"], 
                                            responses[i:end],
                                            data[HOMEWORK][QUESTION]["example_llm_response"])

    resp = prompt_generation.generate_text(prompt)

    extracted_nums = extract_numbers(resp)
    for num in extracted_nums:
        llm_grading.append(num)

    api_requests += 1
    if api_requests == MAX_REQUESTS_PER_MINUTE - 1:
        tmp_time = time.time()
        time.sleep(RATE_LIMIT_RESET_TIME - (tmp_time - start_time) + 2)
        start_time = time.time()
        api_requests = 0

# write output of model to csv. Naming convention: '{assignment name}-{question num/name}'

# pre formatting:
ids: list = prompt_generation.get_ids(file_path)
ids = ['Student Id'] + ids

llm_grading = ["llm score"] + llm_grading

score = ["ta score"] + score

folder_name = HOMEWORK
filename = f"{QUESTION}.csv"

# Check if the folder exists, and create it if it doesn't
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
file_path = os.path.join(folder_name, filename)

final_data = [ids, score, llm_grading]
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write each row from the list
    writer.writerows(zip(*final_data))
