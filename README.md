# Autograding Manual Grading Questions

This project looks at understanding how LLM's can be used to streamline the manual grading process for CS 2200 (not necessarily limited to this class) exams and homeworks.

This project must be run on your local machine in order to prevent student information being leaked. 

## Setting up your environment

Before you being, make sure that you have pipx and Poetry installed:

Instructions to install pipx: https://pipx.pypa.io/stable/installation/

Instructions to install Poetry: https://python-poetry.org/docs/

Once you have Poetry installed, clone this repo to your machine w/ `git clone`

Activate your environment: `poetry shell`

Once you have activated your environment, install the necessary requirements:
`poetry install --no-root` 

Once you have done all these steps, you are done setting up your environment

## Setting up your files

For this project to work, you will need 3 types of files:

1. `api_key.txt` - This file contains the api key to a gemini model
2. `{assignment name}.csv` - This file contains the downloaded responses from gradescope
3. `questions.json` - This file contains information about the question and grading rubric.
The `questions.json` file is the main file for telling the llm what exactly needs to be done. Here is an example of the formatting:
```
{
    "homeworkX": {
        "csv_file": "homeworkX.csv",
        "questionY.Z": {
            "question": "{The question as stated in gradescope}",
            "rubric": "{The rubric for the question. If there are multiple lines, then make sure to at '\n' to the end of each line}",
            "ta_score": "Question Y.Z Score",
            "student_response": "Question Y.Z Response",
            "example_llm_response": "5, 10, 5, 10, 10, 5, 10, 5, 10, 10"
        }
    }
}
```

Params for `'homeworkX'`:

`csv_file`: This is a relative (to `questions.json`) path to the `homeworkX` csv file downloaded from gradescope

`questionY.Z`: The question you would like to analyze

`rubric`: The rubric for `questionY.Z`

`ta_score`: Name of the column that contains the score that the TA provided

`student_response`: Name of the column that contains the student responses

`example_llm_response`: An example of a list of ta scores. (ex: if a ta gives student A a score of 5, student B a score of 10, etc, then a example response would be `"5, 10"`)

## Running the model

Once you have setup your files, go to the `driver.py` file and set the `HOMEWORK` and `QUESTION` global variables to the `"homeworkX"` and `"questionY.Z"` fields in `questions.json`. Once you have done this, run it in the termianl with `python driver.py`
