# функция для классификакий роста
def classify_height(h):
    if h < 160:
        return "Ниже среднего"
    if 160 <= h <= 190:
        return "Средний рост"
    if h > 190:
        return "Высокий рост"

# читаем файл и переводим данные в тип данных int
with open("heights", "r") as f:
    array = [int(i.strip()) for i in f.readlines()]

for h in array:
    print(f"{h} - {classify_height(h)}")