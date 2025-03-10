import json
import time
import prompt_generation

MAX_REQUESTS_PER_MINUTE = 15
RATE_LIMIT_RESET_TIME = 60

# Load questions json
with open('questions.json', 'r') as file:
    data = json.load(file)

file_path = data["homework3"]["csv_file"]
responses, score, rows_len = prompt_generation.read_csv_columns(file_path, 
                                    data["homework3"]["question2.4"]["ta_score"],
                                    data["homework3"]["question2.4"]["student_response"]
                                    )
#print(responses)


start_time = time.time()
api_requests = 0
for i in range(0, rows_len, 20):

    end = i + 20
    if end > rows_len:
        end = rows_len


    prompt = prompt_generation.create_prompt(data["homework3"]["question2.4"]["question"], 
                                            data["homework3"]["question2.4"]["rubric"], 
                                            responses[i:end],
                                            data["homework3"]["question2.4"]["example_llm_response"])

    print(prompt_generation.generate_text(prompt))
    api_requests += 1
    if api_requests == MAX_REQUESTS_PER_MINUTE - 1:
        tmp_time = time.time()
        time.sleep(RATE_LIMIT_RESET_TIME - (tmp_time - start_time) + 2)
        start_time = time.time()
        api_requests = 0
