import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Конфигурация
JIRA_URL = "url в жиру с окном авторизаций"
JIRA_USERNAME = "мой логин от жиры"
JIRA_PASSWORD = "мой пароль от жиры"
JIRA_FILTER_URL = "url в жиру с отфильтрованными задачами"
TEAMS_WEBHOOK_URL = "url группы в тимс"

# Открытие браузера
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Для отправки сообщения
STATUS_MAP = {
    "In progress": "в работе",
    "Hold": "на холде",
    "Backlog": "бэклог"
}

task_data = []

try:
    # Вход
    driver.get(JIRA_URL)
    time.sleep(2)
    driver.find_element(By.ID, "login-form-username").send_keys(JIRA_USERNAME)
    driver.find_element(By.ID, "login-form-password").send_keys(JIRA_PASSWORD)
    driver.find_element(By.ID, "login-form-submit").click()
    time.sleep(4)

    # Переход к фильтру
    driver.get(JIRA_FILTER_URL)
    time.sleep(6)

    # Сбор ссылок на задачи
    task_links = driver.find_elements(By.CSS_SELECTOR, 'a.splitview-issue-link')
    task_hrefs = [link.get_attribute("href") for link in task_links]

    print(f"Найдено задач: {len(task_hrefs)}")

    for href in task_hrefs:
        driver.get(href)
        time.sleep(2)

        try:
            key = driver.find_element(By.ID, "key-val").text
            summary = driver.find_element(By.ID, "summary-val").text
            status = driver.find_element(
                By.XPATH, '//div[@id="opsbar-opsbar-transitions"]//span[@class="dropdown-text"]'
            ).text
            description = driver.find_element(By.ID, "description-val").text

            task_data.append({
                "key": key,
                "summary": summary,
                "status": status,
                "description": description
            })

            print(f"{key} ({status}): {summary}")

        except Exception as e:
            print(f"Ошибка при чтении задачи {href}: {e}")

finally:
    driver.quit()

# Формируем текст сообщения
lines = ["Доброе утро, по задачам:"]
for task in task_data:
    readable_status = STATUS_MAP.get(task["status"], task["status"].lower())
    lines.append(f"{task['key']} - {readable_status}, {task['summary'].lower()}.")

message_text = "\n".join(lines)
print("\n Текст для Microsoft Teams:\n")
print(message_text)

# Отправка в MC Teams
payload = {
    "text": message_text
}

response = requests.post(TEAMS_WEBHOOK_URL, json=payload)
if response.status_code == 200:
    print("SUCCESS")
else:
    print(f"ERROR: {response.status_code}, {response.text}")
