[
    [
        "program",
        "Начальный слот",
        {
            "params": [
                [
                    "int",
                    "task_dim",
                    "10",
                    "Размерность задачи"
                ],
                [
                    "int",
                    "pop_size",
                    "100",
                    "Размер популяции"
                ],
                [
                    "int",
                    "generations",
                    "100",
                    "Число итераций"
                ]
            ],
            "title": "Начальный шаблон",
            "id": "default",
            "contains": [
                "better",
                "encoding",
                "algorithm"
            ],
            "include": [
                "\"stdafx.h\"",
                "<algorithm>"
            ]
        }
    ],
    [
        "better",
        "Какая задача решается",
        {
            "title": "Максимизация",
            "id": "max",
            "contains": [],
            "details": "// Поиск максимума целевой функции"
        },
        {
            "title": "Минимизация",
            "id": "min",
            "contains": [],
            "details": "// Поиск минимума целевой функции"
        }
    ],
    [
        "encoding",
        "Тип кодирования",
        {
            "vars": {
                "gtype": "int"
            },
            "id": "bool",
            "contains": [],
            "details": "// Кодирование решений двоичными последовательностями",
            "title": "Двоичное кодирование",
            "switches": [
                "ENCODING_BOOL"
            ]
        },
        {
            "params": [
                [
                    "int",
                    "min_value",
                    "0",
                    "минимум"
                ],
                [
                    "int",
                    "max_value",
                    "1",
                    "максимум"
                ]
            ],
            "id": "int",
            "contains": [],
            "details": "// Кодирование решений целочисленными последовательностями",
            "vars": {
                "gtype": "int"
            },
            "title": "Целочисленное кодирование",
            "switches": [
                "ENCODING_INT"
            ]
        },
        {
            "params": [
                [
                    "double",
                    "min_value",
                    "-10.0",
                    "минимум"
                ],
                [
                    "double",
                    "max_value",
                    "10.0",
                    "максимум"
                ]
            ],
            "id": "real",
            "contains": [],
            "details": "// Кодирование решений последовательностями действительных чисел",
            "vars": {
                "gtype": "double"
            },
            "title": "Действительнозначное кодирование",
            "switches": [
                "ENCODING_REAL"
            ]
        }
    ],
    [
        "algorithm",
        "Тип алгоритма",
        {
            "title": "Генетический алгоритм",
            "id": "ga",
            "contains": [
                "selectpopulation",
                "crossoverpopulation",
                "mutatepopulation",
                "printpopulation"
            ],
            "details": "// Стандартная версия генетического алгоритма"
        },
        {
            "params": [
                [
                    "double",
                    "eta",
                    "0.9",
                    "коэффициент сопротивления среды"
                ],
                [
                    "double",
                    "v0",
                    "1.0",
                    "максимальное начальное значение скорости частиц"
                ],
                [
                    "double",
                    "tau",
                    "1.0",
                    "шаг времени"
                ]
            ],
            "id": "psoa",
            "contains": [
                "getalphabeta",
                "printpopulation"
            ],
            "details": "// Стандартная версия метода роя частиц",
            "title": "Метод роя частиц",
            "depends": {
                "encoding": [
                    "real"
                ]
            },
            "types": [
                [
                    "double",
                    "p",
                    "array",
                    "лучшая точка трактории частицы"
                ],
                [
                    "double",
                    "v",
                    "array",
                    "вектор скорости частицы"
                ]
            ]
        }
    ],
    [
        "selectpopulation",
        "Схема отбора",
        {
            "params": [
                [
                    "double",
                    "rank_a",
                    "1.5",
                    "a"
                ]
            ],
            "id": "rank",
            "contains": [],
            "details": "// Отбор методом ранжирования",
            "include": [
                "<algorithm>"
            ],
            "title": "Отбор методом ранжирования",
            "depends": {
                "algorithm": [
                    "ga"
                ]
            }
        },
        {
            "include": [
                "<algorithm>"
            ],
            "id": "roulette",
            "contains": [],
            "details": "// Отбор методом рулетки",
            "title": "Отбор методом рулетки",
            "depends": {
                "algorithm": [
                    "ga"
                ]
            }
        },
        {
            "params": [
                [
                    "int",
                    "tournament_size",
                    "2",
                    "Рамер турнира"
                ]
            ],
            "id": "tournament",
            "contains": [],
            "details": "// Турнирная схема отбора",
            "title": "Турнирная схема отбора",
            "depends": {
                "algorithm": [
                    "ga"
                ]
            }
        }
    ],
    [
        "select",
        "Оператор отбора",
        {
            "title": "Турнирная схема отбора",
            "id": "tournement",
            "contains": [],
            "details": "// Турнирная схема отбора"
        }
    ],
    [
        "crossoverpopulation",
        "Схема скрещивания",
        {
            "params": [
                [
                    "double",
                    "p_cross",
                    "0.5",
                    "вероятность выполнения скрещивания в заданной паре"
                ]
            ],
            "id": "shuffling",
            "contains": [
                "crossover"
            ],
            "details": "// Схема скрещивания на основе перемешивания популяции",
            "title": "Схема скрещивания на основе перемешивания популяции",
            "depends": {
                "algorithm": [
                    "ga"
                ]
            }
        }
    ],
    [
        "crossover",
        "Оператор скрещивания",
        {
            "title": "Двухточечное скрещивание",
            "id": "doublepoint",
            "contains": [],
            "details": "// Двухточечное скрещивание"
        },
        {
            "title": "Одноточечное скрещивание",
            "id": "singlepoint",
            "contains": [],
            "details": "// Одноточечное скрещивание"
        },
        {
            "params": [
                [
                    "double",
                    "p_swap",
                    "0.1",
                    "вероятность обмена значениями выбранной пары генов"
                ]
            ],
            "title": "Равномерное скрещивание",
            "id": "uniform",
            "contains": [],
            "details": "// Равномерное скрещивание"
        }
    ],
    [
        "mutatepopulation",
        "Схема мутации",
        {
            "params": [
                [
                    "double",
                    "p_mut",
                    "0.1",
                    "вероятность мутации заданного решения"
                ]
            ],
            "title": "Стандартная схема мутации",
            "id": "default",
            "contains": [
                "mutate"
            ],
            "details": "// Стандартная схема мутации"
        }
    ],
    [
        "mutate",
        "Оператор мутации",
        {
            "params": [
                [
                    "double",
                    "p_mutation_rate",
                    "0.01",
                    "Вероятность мутации одного гена"
                ]
            ],
            "id": "bool",
            "contains": [],
            "details": "// Случайная инверсия каждого бита заданной последовательности \n// с вероятностью p_mutate_rate.",
            "title": "Двоичная мутация",
            "depends": {
                "encoding": [
                    "bool"
                ]
            }
        },
        {
            "params": [
                [
                    "double",
                    "p_mutation_rate",
                    "0.01",
                    "Вероятность мутации одного гена"
                ]
            ],
            "id": "intglobal",
            "contains": [],
            "details": "// Замена каждого числа заданной последовательности случайным числом из заданного диапазона. \n// Выполняется с вероятностью p_mutate_rate.",
            "title": "Целочисленная мутация",
            "depends": {
                "encoding": [
                    "int"
                ]
            }
        },
        {
            "params": [
                [
                    "double",
                    "p_mutation_rate",
                    "0.01",
                    "Вероятность мутации отдельного гена "
                ],
                [
                    "int",
                    "mutate_variance",
                    "1",
                    "Максимальное изменение одного гена"
                ]
            ],
            "id": "intlocal",
            "contains": [],
            "details": "// Замена каждого числа заданной последовательности случайным соседним числом. \n// Выполняется с вероятностью p_mutate_rate.",
            "title": "Целочисленная локальная мутация",
            "depends": {
                "encoding": [
                    "int"
                ]
            }
        },
        {
            "params": [
                [
                    "double",
                    "p_mutation_rate",
                    "0.01",
                    "Вероятность мутации одного гена"
                ]
            ],
            "id": "realglobal",
            "contains": [],
            "details": "// Замена каждого числа заданной последовательности случайным числом из заданного диапазона. \n// Выполняется с вероятностью p_mutate_rate.",
            "title": "Действительнозначная мутация",
            "depends": {
                "encoding": [
                    "real"
                ]
            }
        },
        {
            "params": [
                [
                    "double",
                    "p_mutation_rate",
                    "0.01",
                    "Вероятность мутации отдельного гена "
                ],
                [
                    "double",
                    "mutate_variance",
                    "0.1",
                    "Максимальное изменение одного гена"
                ]
            ],
            "id": "reallocal",
            "contains": [],
            "details": "// Замена каждого числа заданной последовательности случайным числом из локальной окрестности. \n// Выполняется с вероятностью p_mutate_rate.",
            "title": "Действительнозначная локальная мутация",
            "depends": {
                "encoding": [
                    "real"
                ]
            }
        }
    ],
    [
        "getalphabeta",
        "Выбор параметров обновление скорости",
        {
            "params": [
                [
                    "double",
                    "alpha",
                    "0.5",
                    "альфа "
                ],
                [
                    "double",
                    "beta",
                    "0.5",
                    "бета"
                ]
            ],
            "title": "Фиксированные параметры обновления скорости",
            "id": "fixed",
            "contains": [],
            "details": "// Фиксированные параметры обновления скорости"
        }
    ],
    [
        "printpopulation",
        "Печать популяции",
        {
            "params": [
                [
                    "bool",
                    "printpopulation",
                    "0",
                    "печать всей популяции"
                ],
                [
                    "bool",
                    "printbestsolution",
                    "1",
                    "печать лучшего решения"
                ],
                [
                    "bool",
                    "printstatistics",
                    "1",
                    "печать среднего и лучшего значений целевой функции"
                ]
            ],
            "id": "default",
            "contains": [],
            "details": "// Печать данных о текущей популяции: все решения, лучшее решение, статистика",
            "include": [
                "<iostream>"
            ],
            "title": "Печать данных о популяции"
        }
    ]
]