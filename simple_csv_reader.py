import csv


def classify_score(score):
    if score < 50:
        return 'Неудовлетворительно'
    elif 50 <= score <= 85:
        return 'Хорошо'
    elif score > 85:
        return 'Отлично'

mycsv = r"C:\Users\sultan.zhubaniyazov\OneDrive - Freedom Holding Corporation\Рабочий стол\students.csv"

with open(mycsv, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name, score = row
        score = int(score)
        print(f"{name} - {score} - {classify_score(score)}")