# Boot Camp 2024 Python


Структура документу
1. DevOps 
    - Розміщення бази даних 
    - Розміщення серверу
2. Endpoint
---
## 1. DevOps
### Розміщення бази даних
Даний проект розміщено у FreeSQLdatabase.
Після створення даного серверу, дані до підключення було передано Python та Java розробникам.

| Переваги                                   | Недоліки                                                                        |
|--------------------------------------------|---------------------------------------------------------------------------------|
| Безкоштовне розміщення однієї БД           | У разі розширення, необхідно створювати додаткові акаунти / шукати альтернативу |
| Невеликий час налаштування та запуску БД   | Обсяг даних: 5 мб (шукається альтернатива)                                      |
| Підтримка основних операцій з базами даних ||
|Підтримка віддаленого доступу до БД	||
---
### Розміщення серверу
Сервер розміщено на [render.com](https://render.com)<br>
Для запуску серверу використовувався Flasko. Додаткові залежності вказано у фалі requirements.txt

Налаштування серверу:
- Регіон (місце на якому фізично зберігаються дані серверу): Frankfurt(EU central)
- Гілка з якої відбувається deply: main
- Runtime: python 3
- Build command: ```$ pip install -r requirements.txt```
- Start command: ```$ gunicorn app:app```
- Auto deploy: yes

Безкоштовна версія render.com передбачає за собою "засинання серверу", якщо на нього ніхто не заходив більше ніж 15 хв. Для вирішення даної проблеми було створено get-запити, які надсилаються один раз на 10 хв через сервіс [cron-job.org](https://console.cron-job.org).

---
## 2. Endpoints
> https://itclusterpython2024.onrender.com/department - Кафедри
> https://itclusterpython2024.onrender.com/disciplines - Дисципліни і курси
> https://itclusterpython2024.onrender.com/discipline-blocks - Блоки дисциплін
> https://itclusterpython2024.onrender.com/discipline-groups - Групи дисциплін
> https://itclusterpython2024.onrender.com/education-levels - Освітні рівні
> https://itclusterpython2024.onrender.com/education-programs - Освітні програми
> https://itclusterpython2024.onrender.com/position - Посади викладачів
> https://itclusterpython2024.onrender.com/service_info - Сервісна інформація
> https://itclusterpython2024.onrender.com/specialties - Спеціальності
> https://itclusterpython2024.onrender.com/teachers - Викладачі
> https://itclusterpython2024.onrender.com/universities - Університети
