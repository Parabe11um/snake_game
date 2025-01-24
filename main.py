import pygame
import random
import sys

# --- Глобальные настройки ---
SCREEN_WIDTH = 640  # ширина окна
SCREEN_HEIGHT = 480  # высота окна
CELL_SIZE = 20       # размер одной ячейки
FPS = 20             # количество кадров в секунду (частота обновления)

# Цвета в формате (R, G, B)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class GameObject:
    """
    Базовый класс для игровых объектов.
    Хранит общие атрибуты и методы для наследников.
    """

    def __init__(self):
        """
        Инициализирует объект с базовыми значениями.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = BLACK  # Цвет по умолчанию зададим чёрный (переопределится в наследниках)

    def draw(self, surface):
        """
        Отрисовка объекта на поверхности Pygame.
        По умолчанию – пустая реализация, её переопределяют дочерние классы.
        """
        pass


class Apple(GameObject):
    """
    Класс, описывающий объект «Яблоко» на игровом поле.
    """

    def __init__(self):
        """
        Инициализация яблока: задаём цвет и случайную позицию.
        """
        super().__init__()
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """
        Задаёт случайное положение яблока на игровом поле,
        при этом координаты соответствуют сетке размером CELL_SIZE.
        """
        cols = SCREEN_WIDTH // CELL_SIZE
        rows = SCREEN_HEIGHT // CELL_SIZE

        # Случайный выбор ячейки
        random_col = random.randint(0, cols - 1)
        random_row = random.randint(0, rows - 1)

        # Перевод индексов ячейки в реальные координаты
        x = random_col * CELL_SIZE
        y = random_row * CELL_SIZE

        self.position = (x, y)

    def draw(self, surface):
        """
        Отрисовывает яблоко на поверхности Pygame.
        """
        x, y = self.position
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """
    Класс, описывающий змейку: хранит список координат её сегментов,
    логику движения и отрисовки, а также методы сброса состояния.
    """

    def __init__(self):
        """
        Инициализирует змейку:
        - начальная длина 1,
        - начальное направление — движение вправо,
        - позиции всех сегментов (в начале один сегмент в центре экрана).
        """
        super().__init__()
        self.body_color = GREEN
        self.length = 1
        self.positions = [self.position]  # список координат сегментов змейки
        self.direction = (CELL_SIZE, 0)   # смещение по оси X в одну ячейку вправо
        self.next_direction = None

    def update_direction(self):
        """
        Обновляет текущее направление, основываясь на том, что было установлено
        в self.next_direction (при нажатии клавиш).
        """
        if self.next_direction is not None:
            # Проверяем, чтобы новая направление не было «противоположным» текущему
            # Например, если змейка двигается вправо, то она не может сразу пойти влево.
            current_dx, current_dy = self.direction
            next_dx, next_dy = self.next_direction

            # Если вектор меняется на противоположный, игнорируем
            if (current_dx + next_dx == 0) and (current_dy + next_dy == 0):
                # напр. (20, 0) + (-20, 0) == (0, 0) → противоположные направления
                pass
            else:
                self.direction = self.next_direction

    def move(self):
        """
        Двигает змейку на одну ячейку в направлении self.direction.
        Добавляет новую голову и удаляет хвост, если длина змейки не изменилась.
        """
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина змейки не увеличилась, удаляем последний сегмент
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """
        Отрисовывает змейку на игровом поле.
        Каждый сегмент — квадрат размером CELL_SIZE x CELL_SIZE.
        """
        for segment in self.positions:
            x, y = segment
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки (первый элемент в self.positions).
        """
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние:
        - длина 1,
        - позиция в центре экрана,
        - направление движения вправо.
        """
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None


def handle_keys(event, snake):
    """
    Обрабатывает события с клавиатуры и устанавливает
    новое направление движения змейки.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            snake.next_direction = (0, -CELL_SIZE)
        elif event.key == pygame.K_DOWN:
            snake.next_direction = (0, CELL_SIZE)
        elif event.key == pygame.K_LEFT:
            snake.next_direction = (-CELL_SIZE, 0)
        elif event.key == pygame.K_RIGHT:
            snake.next_direction = (CELL_SIZE, 0)


def main():
    """
    Главная функция, в которой инициализируются объекты, запускается основной цикл игры,
    обрабатываются события и выполняется отрисовка.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    # Создаём объекты змейки и яблока
    snake = Snake()
    apple = Apple()

    while True:
        # 1. Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_keys(event, snake)

        # 2. Обновляем направление и двигаем змейку
        snake.update_direction()
        snake.move()

        # 3. Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # 4. Проверяем, столкнулась ли змейка сама с собой
        head = snake.get_head_position()
        # Если голова совпадает с любым другим сегментом — перезапускаем змейку
        if head in snake.positions[1:]:
            snake.reset()

        # 5. Отрисовка
        # Заливаем экран чёрным цветом
        screen.fill(BLACK)

        # Отрисовываем яблоко и змейку
        apple.draw(screen)
        snake.draw(screen)

        # Обновляем экран
        pygame.display.update()

        # 6. Регулируем частоту кадров, чтобы игра не летела слишком быстро
        clock.tick(FPS)


if __name__ == "__main__":
    main()
