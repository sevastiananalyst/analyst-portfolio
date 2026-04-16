# Кейс 2: Оптимизация документооборота в строительстве (метро "Юго-Западная")

## Контекст
Компания-подрядчик **Розенберг** участвовала в строительстве станции метро "Юго-Западная" в Санкт-Петербурге.  
Участники процесса:  
- **Прораб (Розенберг)** — исполнитель работ  
- **ПТО (Розенберг)** — проверка смет и актов  
- **Подрядчик** (субподрядчик) — отдельные виды работ  
- **Генподрядчик** (например, Метрострой)  
- **Росстройконтроль** — государственный надзор

Проблемы до автоматизации:
- Бумажные акты КС-2, КС-3, пересылка курьером и email
- Цикл согласования 2-4 недели
- Потеря версий, отсутствие прозрачности для Росстройконтроля

## Моя роль
Системный аналитик:  
- Провёл интервью со всеми участниками  
- Описал AS-IS процесс (BPMN)  
- Спроектировал целевой процесс в Битрикс24 с маршрутизацией по ролям, SLA (1 день на ПТО, 3 дня на генподрядчика), интеграцией с API генподрядчика и Росстройконтроля  
- Настроил бизнес-процессы в Битрикс24, права доступа, формы  
- Разработал регламенты и чек-листы для каждого участника  
- Обучил 50+ пользователей

## Результаты
- Цикл согласования сокращён с 15 до **8 дней** (↓47%)  
- Количество ошибок в документации снижено на **40%**  
- Росстройконтроль получает акты в тот же день (через API) → снижение штрафов

## Диаграммы (BPMN, Sequence)

### AS-IS (как было — бумага, курьер, email)
![AS-IS](https://raw.githubusercontent.com/sevastiananalyst/analyst-portfolio/main/_assets/BPMN_As-Is.png)

### TO-BE (как стало — Битрикс24, SLA, API)
![TO-BE](https://raw.githubusercontent.com/sevastiananalyst/analyst-portfolio/main/_assets/BPMN_To-Be.png)

### Sequence интеграции с Росстройконтролем
![Sequence](https://raw.githubusercontent.com/sevastiananalyst/analyst-portfolio/main/_assets/Sequence.png)

## 📂 Ссылки на артефакты (исходные файлы)

- **BPMN исходники (PlantUML)**: [`diagrams/`](https://github.com/sevastiananalyst/analyst-portfolio/tree/main/02_bpmn_requirements_case/diagrams)
- **Чек-лист для КС-2**: [`templates/checklist_ks2.md`](https://github.com/sevastiananalyst/analyst-portfolio/blob/main/02_bpmn_requirements_case/templates/checklist_ks2.md)
- **Функциональные требования**: [`requirements/functional_req.md`](https://github.com/sevastiananalyst/analyst-portfolio/blob/main/02_bpmn_requirements_case/requirements/functional_req.md)
- **Нефункциональные требования**: [`requirements/nonfunctional_req.md`](https://github.com/sevastiananalyst/analyst-portfolio/blob/main/02_bpmn_requirements_case/requirements/nonfunctional_req.md)
- **User stories**: [`requirements/user_stories.md`](https://github.com/sevastiananalyst/analyst-portfolio/blob/main/02_bpmn_requirements_case/requirements/user_stories.md)
