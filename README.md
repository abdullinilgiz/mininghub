# mininghub
ITMO, AI Talent Hub, Data-Centric AI
## ДЗ 3
Python код с активным обучением `active/acrive_learning.py`
Опискание пайплайна: `active/ACTIVE.md`
## ДЗ 2
ТЗ для разметчика: `annotations/ANNOT.md`
Выводы: `annotations/RESULT.md`
## ДЗ 1
### Что было сделано?
Мы взяли датасет с вакансиями и изучили его. Оказалось, что в нем есть некоторое количество признаков, от которых можно избавиться (например, множество признаков с образованием просто повторяют друг друга). После отсеивания данных признаков, провели EDA оригинального датасета (файл `eda_original.ipynb`).

Это позволило нам определить признаки, которые нас интересуют. Это важно, так как необходимо понимать, какого рода информацию нужно добывать. Так как  работа ведется с датасетом вакансий, мы решили попробовать обратиться к API сервисов поиска работы. Таким сервисом оказался trudvsem.ru (файл `trudvsem.ipynb`).

Был написан запрос, после которого стала ясна структура получаемого ответа (к сожалению, у данного сервиса нет документации, поэтому ответы приходилось интерпретировать по мере их получения). Далее из добытой информации выделили информацию, которую хотим получать (на основе EDA из оригинального датасета). После изучали несоответствия между категориальными признаками оригинального датасета и добытого с помощью API trudvsem.ru. Проведя аналогии между двумя датасетами, мы поняли, как трансформировать признаки добытой информации в признаки оригинальной. Разумеется, провели трансформацию. Приведя оба датасета к общему виду, объединили и провели EDA общего датасета (файл `eda_mined.ipynb`).

### Возможное применение этих данных в контексте машинного обучения.
Эти данные можно исползовать для базового предсказания заработной платы по определенной вакансии. Такое решение помогло бы работодателям выставлять более справедливые по рынку зарплатные предложения.