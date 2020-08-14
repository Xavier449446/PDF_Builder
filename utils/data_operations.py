import pandas as pd


def get_data(filename):
    head = ["Student No", "Name of Candidate", "Registration", "Grade", "Gender", "Name of school", "Date of Birth",
            "City of Residence", "Date and time of test", "Country of Residence", "Extra time assistance",
            "Question No.",
            "Time Spent on question (sec)", "Score if correct", "Score if incorrect", "Attempt status",
            "What you marked",
            "Correct Answer", "Outcome (Correct/Incorrect/Not Attempted)", "Your score"]
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        data = pd.read_excel(filename, name=head)
    elif filename.endswith('.csv'):
        data = pd.read_csv(filename, name=head)
    data = data.dropna(axis=1, how="all")
    data = data.dropna(axis=0, thresh=6)
    data = data.fillna(value=" ")
    if not data.columns.any() == head:
        data.columns = head
    if (data[0:1] == head).values.any():
        data = data.iloc[1:]
    students_list = pd.unique(data["Student No"])
    data_sets = data.groupby('Student No')
    return students_list, data_sets
