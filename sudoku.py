import random
import sys
import os


class SudokuGame:
    def __init__(self, theme='light'):
        self.size = 9
        self.cursor = [0, 0]
        self.theme = theme
        self.command_history = []
        self.max_history = 5
        self.generate_sudoku()

    def clear_screen(self):
        """Очищает экран"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_theme_colors(self):
        """Возвращает цвета для текущей темы"""
        if self.theme == 'dark':
            return {
                'text': '\033[37m',  # белый
                'border': '\033[36m',  # голубой
                'cursor': '\033[41m',  # красный фон
                'fixed': '\033[33m',  # желтый
                'input': '\033[32m',  # зеленый
                'error': '\033[31m',  # красный
                'success': '\033[32m',  # зеленый
                'reset': '\033[0m',
                'title': '\033[1;36m',  # жирный голубой
                'highlight': '\033[1;35m'  # жирный фиолетовый
            }
        else:  # light theme
            return {
                'text': '\033[30m',  # черный
                'border': '\033[34m',  # синий
                'cursor': '\033[44m',  # синий фон
                'fixed': '\033[33m',  # желтый
                'input': '\033[32m',  # зеленый
                'error': '\033[31m',  # красный
                'success': '\033[32m',  # зеленый
                'reset': '\033[0m',
                'title': '\033[1;34m',  # жирный синий
                'highlight': '\033[1;35m'  # жирный фиолетовый
            }

    def generate_sudoku(self):
        """Генерирует новое судоку"""
        # Базовое решение
        base = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

        # Перемешиваем строки и столбцы
        for _ in range(10):
            # Меняем местами строки в пределах блока 3x3
            block = random.randint(0, 2) * 3
            r1 = block + random.randint(0, 2)
            r2 = block + random.randint(0, 2)
            base[r1], base[r2] = base[r2], base[r1]

            # Меняем местами столбцы в пределах блока 3x3
            block = random.randint(0, 2) * 3
            c1 = block + random.randint(0, 2)
            c2 = block + random.randint(0, 2)
            for row in base:
                row[c1], row[c2] = row[c2], row[c1]

        # Создаем копии для игры
        self.solution = [row[:] for row in base]
        self.initial_board = [row[:] for row in base]
        self.board = [row[:] for row in base]

        # Удаляем числа для создания головоломки
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        to_remove = random.randint(40, 50)
        for i in range(to_remove):
            r, c = cells[i]
            self.initial_board[r][c] = 0
            self.board[r][c] = 0

    def display_game_window(self):
        """Отображает игровое окно с исправленным отображением"""
        colors = self.get_theme_colors()

        # Очищаем экран
        self.clear_screen()

        # Верхняя часть окна - заголовок
        print(f"{colors['title']}{'=' * 60}{colors['reset']}")
        print(f"{colors['title']}               ИГРА СУДОКУ                     {colors['reset']}")
        print(f"{colors['title']}{'=' * 60}{colors['reset']}")
        print(f"Тема: {colors['highlight']}{'Тёмная' if self.theme == 'dark' else 'Светлая'}{colors['reset']} | "
              f"Курсор: строка {colors['highlight']}{self.cursor[0] + 1}{colors['reset']}, "
              f"столбец {colors['highlight']}{self.cursor[1] + 1}{colors['reset']}")
        print(f"{colors['border']}{'-' * 60}{colors['reset']}")

        # Сетка судоку (упрощенная версия)
        print()
        print(f"{colors['text']}   1 2 3   4 5 6   7 8 9{colors['reset']}")
        print(f"{colors['border']}  {'-' * 25}{colors['reset']}")

        for i in range(9):
            # Номер строки
            row_num = i + 1
            row_display = f"{colors['text']}{row_num} {colors['reset']}{colors['border']}|{colors['reset']}"

            for j in range(9):
                # Отображаем клетку
                if self.cursor == [i, j]:
                    # Клетка с курсором
                    if self.board[i][j] == 0:
                        cell = f"{colors['cursor']}  {colors['reset']}"
                    else:
                        cell = f"{colors['cursor']}{self.board[i][j]:^2}{colors['reset']}"
                else:
                    # Обычная клетка
                    if self.board[i][j] == 0:
                        cell = f"{colors['text']} .{colors['reset']}"
                    else:
                        if self.initial_board[i][j] != 0:
                            # Изначальные числа
                            cell = f"{colors['fixed']}{self.board[i][j]:^2}{colors['reset']}"
                        else:
                            # Числа, введенные игроком
                            cell = f"{colors['input']}{self.board[i][j]:^2}{colors['reset']}"

                row_display += f" {cell}"

                # Добавляем разделители блоков
                if j == 2 or j == 5:
                    row_display += f" {colors['border']}|{colors['reset']}"
                elif j == 8:
                    row_display += f" {colors['border']}|{colors['reset']}"

            print(row_display)

            # Горизонтальные разделители блоков
            if i == 2 or i == 5:
                print(f"{colors['border']}  {'-' * 25}{colors['reset']}")

        print(f"{colors['border']}  {'-' * 25}{colors['reset']}")

        # Разделитель между доской и командной строкой
        print(f"\n{colors['border']}{'=' * 60}{colors['reset']}")

        # Командная строка
        print(f"\n{colors['title']}КОМАНДНАЯ СТРОКА:{colors['reset']}")
        print(f"{colors['border']}{'-' * 60}{colors['reset']}")

        # История команд
        if self.command_history:
            print(f"{colors['text']}Последние команды:{colors['reset']}")
            for cmd in self.command_history[-self.max_history:]:
                print(f"  {colors['input']}>{colors['reset']} {cmd}")
            print()

        # Доступные команды в две колонки
        print(f"{colors['text']}Доступные команды:{colors['reset']}")
        commands_left = [
            f"{colors['input']}left(n){colors['reset']} - влево на n клеток",
            f"{colors['input']}right(n){colors['reset']} - вправо на n клеток",
            f"{colors['input']}up(n){colors['reset']} - вверх на n клеток",
            f"{colors['input']}down(n){colors['reset']} - вниз на n клеток",
            f"{colors['input']}1-9{colors['reset']} - поставить число"
        ]

        commands_right = [
            f"{colors['input']}0{colors['reset']} - очистить клетку",
            f"{colors['input']}space{colors['reset']} - очистить клетку",
            f"{colors['input']}restart{colors['reset']} - новая игра",
            f"{colors['input']}theme{colors['reset']} - сменить тему",
            f"{colors['input']}help{colors['reset']} - справка",
            f"{colors['input']}quit{colors['reset']} - выход"
        ]

        # Выводим команды в две колонки
        for i in range(max(len(commands_left), len(commands_right))):
            left = commands_left[i] if i < len(commands_left) else ""
            right = commands_right[i] if i < len(commands_right) else ""
            print(f"  {left:<30}  {right}")

        print(f"{colors['border']}{'-' * 60}{colors['reset']}")

    def add_to_history(self, message):
        """Добавляет сообщение в историю"""
        self.command_history.append(message)
        if len(self.command_history) > self.max_history:
            self.command_history.pop(0)

    def move_cursor(self, direction, steps=1):
        """Перемещает курсор"""
        steps = max(1, min(steps, 8))

        old_pos = self.cursor.copy()

        if direction == "left":
            self.cursor[1] = max(0, self.cursor[1] - steps)
        elif direction == "right":
            self.cursor[1] = min(8, self.cursor[1] + steps)
        elif direction == "up":
            self.cursor[0] = max(0, self.cursor[0] - steps)
        elif direction == "down":
            self.cursor[0] = min(8, self.cursor[0] + steps)

        # Добавляем в историю только если позиция изменилась
        if old_pos != self.cursor:
            self.add_to_history(f"{direction}({steps})")

    def insert_number(self, num):
        """Вставляет число в текущую позицию"""
        row, col = self.cursor

        # Проверяем, можно ли изменять эту клетку
        if self.initial_board[row][col] != 0:
            self.add_to_history(f"Ошибка: клетка [{row + 1},{col + 1}] заблокирована")
            return False

        if num == 0:
            self.board[row][col] = 0
            self.add_to_history(f"Клетка [{row + 1},{col + 1}] очищена")
        else:
            # Проверяем, можно ли поставить это число
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                self.add_to_history(f"В [{row + 1},{col + 1}] поставлено {num}")

                if self.check_win():
                    return True
            else:
                self.add_to_history(f"Ошибка: число {num} нельзя поставить в [{row + 1},{col + 1}]")

        return False

    def is_valid_move(self, row, col, num):
        """Проверяет, можно ли поставить число в клетку"""
        # Проверяем строку
        for j in range(9):
            if self.board[row][j] == num and j != col:
                return False

        # Проверяем столбец
        for i in range(9):
            if self.board[i][col] == num and i != row:
                return False

        # Проверяем квадрат 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num and (i != row or j != col):
                    return False

        return True

    def check_win(self):
        """Проверяет, решено ли судоку"""
        # Проверяем на пустые клетки
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False

        # Проверяем строки
        for i in range(9):
            row = self.board[i]
            if sorted(row) != list(range(1, 10)):
                return False

        # Проверяем столбцы
        for j in range(9):
            col = [self.board[i][j] for i in range(9)]
            if sorted(col) != list(range(1, 10)):
                return False

        # Проверяем квадраты 3x3
        for box_i in range(0, 9, 3):
            for box_j in range(0, 9, 3):
                square = []
                for i in range(3):
                    for j in range(3):
                        square.append(self.board[box_i + i][box_j + j])
                if sorted(square) != list(range(1, 10)):
                    return False

        return True

    def show_help(self):
        """Показывает справку"""
        colors = self.get_theme_colors()

        self.clear_screen()
        print(f"{colors['title']}{'=' * 60}{colors['reset']}")
        print(f"{colors['title']}                      СПРАВКА                     {colors['reset']}")
        print(f"{colors['title']}{'=' * 60}{colors['reset']}")
        print()
        print(f"{colors['text']}Цель игры:{colors['reset']}")
        print("  Заполнить все клетки цифрами от 1 до 9 так,")
        print("  чтобы в каждой строке, столбце и квадрате 3x3")
        print("  каждая цифра встречалась только один раз.")
        print()
        print(f"{colors['text']}Управление:{colors['reset']}")
        print(f"  {colors['input']}left(n){colors['reset']}  - переместить курсор влево на n клеток")
        print(f"  {colors['input']}right(n){colors['reset']} - переместить курсор вправо на n клеток")
        print(f"  {colors['input']}up(n){colors['reset']}    - переместить курсор вверх на n клеток")
        print(f"  {colors['input']}down(n){colors['reset']}  - переместить курсор вниз на n клеток")
        print(f"  {colors['input']}1-9{colors['reset']}     - поставить соответствующее число")
        print(f"  {colors['input']}0{colors['reset']}       - очистить текущую клетку")
        print(f"  {colors['input']}space{colors['reset']}   - также очистить текущую клетку")
        print()
        print(f"{colors['text']}Другие команды:{colors['reset']}")
        print(f"  {colors['input']}restart{colors['reset']} - начать новую игру")
        print(f"  {colors['input']}theme{colors['reset']}   - переключить тему (светлая/тёмная)")
        print(f"  {colors['input']}help{colors['reset']}    - показать эту справку")
        print(f"  {colors['input']}quit{colors['reset']}    - выйти из игры")
        print()
        print(f"{colors['text']}Обозначения:{colors['reset']}")
        print(f"  {colors['fixed']} 5 {colors['reset']} - изначальное число (нельзя изменить)")
        print(f"  {colors['input']} 3 {colors['reset']} - число, введенное игроком")
        print(f"  {colors['cursor']}[7]{colors['reset']} - текущая позиция курсора")
        print(f"  {colors['text']} .{colors['reset']}  - пустая клетка")
        print()
        print(f"{colors['border']}{'-' * 60}{colors['reset']}")
        input(f"\n{colors['input']}Нажмите Enter для возврата в игру...{colors['reset']}")

    def switch_theme(self):
        """Переключает тему"""
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.add_to_history(f"Тема изменена на {'тёмную' if self.theme == 'dark' else 'светлую'}")

    def restart_game(self):
        """Перезапускает игру"""
        self.cursor = [0, 0]
        self.generate_sudoku()
        self.command_history = []
        self.add_to_history("Новая игра начата")

    def parse_command(self, command):
        """Разбирает и выполняет команду"""
        cmd = command.strip().lower()

        if cmd in ["quit", "exit", "close"]:
            print("Спасибо за игру!")
            sys.exit(0)

        elif cmd == "restart":
            self.restart_game()
            return False

        elif cmd == "theme":
            self.switch_theme()
            return False

        elif cmd == "help":
            self.show_help()
            return False

        elif cmd == "":
            return False

        # Команды перемещения
        elif cmd.startswith("left"):
            steps = 1
            if "(" in cmd and ")" in cmd:
                try:
                    steps_str = cmd.split("(")[1].split(")")[0]
                    if steps_str:
                        steps = int(steps_str)
                except:
                    steps = 1
            self.move_cursor("left", steps)
            return False

        elif cmd.startswith("right"):
            steps = 1
            if "(" in cmd and ")" in cmd:
                try:
                    steps_str = cmd.split("(")[1].split(")")[0]
                    if steps_str:
                        steps = int(steps_str)
                except:
                    steps = 1
            self.move_cursor("right", steps)
            return False

        elif cmd.startswith("up"):
            steps = 1
            if "(" in cmd and ")" in cmd:
                try:
                    steps_str = cmd.split("(")[1].split(")")[0]
                    if steps_str:
                        steps = int(steps_str)
                except:
                    steps = 1
            self.move_cursor("up", steps)
            return False

        elif cmd.startswith("down"):
            steps = 1
            if "(" in cmd and ")" in cmd:
                try:
                    steps_str = cmd.split("(")[1].split(")")[0]
                    if steps_str:
                        steps = int(steps_str)
                except:
                    steps = 1
            self.move_cursor("down", steps)
            return False

        # Ввод чисел
        elif cmd == " " or cmd == "space":
            return self.insert_number(0)

        elif cmd.isdigit() and 0 <= int(cmd) <= 9:
            return self.insert_number(int(cmd))

        else:
            self.add_to_history(f"Неизвестная команда: {cmd}")
            return False

    def run(self):
        """Запускает игровой цикл"""
        while True:
            try:
                # Показываем игровое окно
                self.display_game_window()

                # Получаем команду
                colors = self.get_theme_colors()
                command = input(f"\n{colors['input']}Введите команду > {colors['reset']}")

                # Обрабатываем команду
                win = self.parse_command(command)

                # Если игра выиграна
                if win:
                    self.display_game_window()
                    colors = self.get_theme_colors()
                    print(f"\n{colors['success']}{'★' * 30}{colors['reset']}")
                    print(f"{colors['success']}        ПОЗДРАВЛЯЮ! СУДОКУ РЕШЕНО!       {colors['reset']}")
                    print(f"{colors['success']}{'★' * 30}{colors['reset']}")

                    choice = input(f"\n{colors['input']}Новая игра? (да/нет): {colors['reset']}").lower()
                    if choice in ["да", "yes", "y", "д"]:
                        self.restart_game()
                    else:
                        print("Спасибо за игру!")
                        sys.exit(0)

            except KeyboardInterrupt:
                print("\n\nИгра прервана.")
                sys.exit(0)
            except Exception as e:
                print(f"\nОшибка: {e}")
                input("Нажмите Enter для продолжения...")


def main():
    """Точка входа"""
    # Очищаем экран при запуске
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=" * 60)
    print("              ИГРА СУДОКУ С КОМАНДАМИ")
    print("=" * 60)
    print()
    print("Выберите тему:")
    print("  1. Светлая (по умолчанию)")
    print("  2. Тёмная")
    print()

    while True:
        choice = input("Ваш выбор (1/2): ").strip()
        if choice in ["1", "2", ""]:
            theme = 'dark' if choice == '2' else 'light'
            break
        else:
            print("Пожалуйста, введите 1 или 2")

    # Запускаем игру
    game = SudokuGame(theme)
    game.run()


if __name__ == "__main__":
    main()