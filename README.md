## Пошаговое объяснение кода

Ниже приводится детальный разбор каждой части программы.

---

### 1. Импорт модулей и глобальные настройки

```javascript
python
```

Копировать

```javascript
import pygame
import random
import sys
```

1. **pygame** — основной модуль, обеспечивающий всё, что касается графики, обработки событий, звука и т. д.
2. **random** — модуль для получения случайных значений (нужно, чтобы случайно «рассыпать» яблоки).
3. **sys** — используется, чтобы корректно завершать работу программы при выходе (вызывает 

   ```javascript
   sys.exit()
   ```

   ).

Далее идут глобальные переменные:

```javascript
python
```

Копировать

```javascript
SCREEN_WIDTH = 640   # ширина игрового окна
SCREEN_HEIGHT = 480  # высота игрового окна
CELL_SIZE = 20       # размер одной ячейки (квадрата) в пикселях
FPS = 20             # целевая частота кадров для игры

BLACK = (0, 0, 0)    # некоторые цвета в формате RGB
RED = (255, 0, 0)
GREEN = (0, 255, 0)
```

- **SCREEN_WIDTH** и 

  ```javascript
  SCREEN_HEIGHT
  ```

   задают размеры окна: 640×480 пикселей.
- **CELL_SIZE** — размер одной клетки сетки (20×20).
- **FPS** — сколько раз в секунду будет обновляться экран. Нужно, чтобы змейка не перемещалась слишком быстро.
- **BLACK**, 

  ```javascript
  RED
  ```

  , 

  ```javascript
  GREEN
  ```

   — основные цвета, которые будем использовать для закрашивания объектов.

---

### 2. Базовый класс GameObject

```javascript
python
```

Копировать

```javascript
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
        self.body_color = BLACK

    def draw(self, surface):
        """
        Отрисовка объекта на поверхности Pygame.
        По умолчанию – пустая реализация, её переопределяют дочерние классы.
        """
        pass
```

- **GameObject** — базовый (родительский) класс для всех игровых объектов (змейка, яблоко).
- **position** — координаты на поле. По умолчанию ставим объект в центр экрана.
- **body_color** — цвет объекта, по умолчанию чёрный (будет переопределён в наследниках).
- **draw(...)** — метод для отрисовки объекта. Базовый класс не знает, как отрисовывать «абстрактный» объект, поэтому метод оставлен пустым (переопределим в классах-наследниках).

---

### 3. Класс Apple

```javascript
python
```

Копировать

```javascript
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

        # Перевод индексов ячейки в пиксельные координаты
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
```

- Apple наследуется от 

  ```javascript
  GameObject
  ```

  .
- При инициализации (

  ```javascript
  __init__
  ```

  ) задаём:
  - self.body_color = RED — цвет яблока (красный).
  - self.randomize_position() — метод, который сразу ставит яблоко в случайную ячейку.
- **randomize_position**:
  - Считаем количество ячеек по горизонтали (

    ```javascript
    cols
    ```

    ) и вертикали (

    ```javascript
    rows
    ```

    ).
  - Выбираем случайную ячейку с помощью 

    ```javascript
    random.randint(0, cols - 1)
    ```

     и 

    ```javascript
    random.randint(0, rows - 1)
    ```

    .
  - Превращаем эти индексы ячейки в координаты в пикселях (умножаем на 

    ```javascript
    CELL_SIZE
    ```

    ).
- **draw(...)** — метод для отрисовки яблока:
  - Создаём прямоугольник 

    ```javascript
    rect
    ```

     с размерами 

    ```javascript
    CELL_SIZE × CELL_SIZE
    ```

    .
  - Заливаем его цветом 

    ```javascript
    RED
    ```

     на игровом поле (поверхность 

    ```javascript
    surface
    ```

    ).

---

### 4. Класс Snake

```javascript
python
```

Копировать

```javascript
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
        self.direction = (CELL_SIZE, 0)   # смещение по оси X вправо
        self.next_direction = None

    def update_direction(self):
        """
        Обновляет текущее направление, основываясь на том, что было установлено
        в self.next_direction (при нажатии клавиш).
        """
        if self.next_direction is not None:
            current_dx, current_dy = self.direction
            next_dx, next_dy = self.next_direction

            # Проверяем, не являются ли направления противоположными
            # Если они противоположные, игнорируем смену
            if (current_dx + next_dx == 0) and (current_dy + next_dy == 0):
                pass  # противоположное направление, например вправо -> влево
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

        # Удаляем последний сегмент, если длина не увеличилась
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
```

Основные моменты:

- **positions** хранит список всех сегментов тела змейки (каждый сегмент — координаты).
- **length** — текущая длина змейки. Если она увеличится (змейка съела яблоко), при перемещении мы не удалим последний сегмент.
- **direction** хранит «смещение» по X и Y для головы змейки. По умолчанию змейка двигается вправо: 

  ```javascript
  (CELL_SIZE, 0)
  ```

  .
- **next_direction** — временное хранение того направления, которое выбрал пользователь (при нажатии клавиши). «Подключается» в методе 

  ```javascript
  update_direction()
  ```

  .
- **move()**:
  - Вычисляет новую позицию головы, добавляет её в начало списка.
  - Если длина змейки не изменилась, удаляем хвост (последний элемент списка), чтобы сместить змейку вперёд.
- **reset()** — сбрасывает змейку после столкновения (чтобы начать заново).

---

### 5. Функция handle_keys

```javascript
python
```

Копировать

```javascript
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
```

Здесь мы смотрим, нажата ли какая-то клавиша (**pygame.KEYDOWN**), и если это одна из стрелок, то подготавливаем новое направление (snake.next_direction). Фактически, это лишь «запрос» на смену направления; действительно сменится оно только в методе update_direction().

---

### 6. Главная функция main()

```javascript
python
```

Копировать

```javascript
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
        if head in snake.positions[1:]:
            snake.reset()

        # 5. Отрисовка
        screen.fill(BLACK)  # заливаем экран чёрным цветом
        apple.draw(screen)  # рисуем яблоко
        snake.draw(screen)  # рисуем змейку
        pygame.display.update()

        # 6. Устанавливаем скорость игры
        clock.tick(FPS)
```

1. **pygame.init()** — инициализация модулей Pygame.
2. **Создание окна**: 

   ```javascript
   pygame.display.set_mode(...)
   ```

    задаёт размеры окна (640×480).

   ```javascript
   pygame.display.set_caption("Змейка")
   ```

    — заголовок окна.
3. **Создаём часы**: 

   ```javascript
   clock = pygame.time.Clock()
   ```

   . С помощью 

   ```javascript
   clock.tick(FPS)
   ```

    ограничиваем скорость игры (20 кадров в секунду).
4. **Создаём объекты**: 

   ```javascript
   snake = Snake()
   ```

   , 

   ```javascript
   apple = Apple()
   ```

   .
5. **Главный цикл** 

   ```javascript
   while True
   ```

   **:**
   - События (все 

     ```javascript
     pygame.event.get()
     ```

     ):
     - Если пришёл сигнал закрытия окна — выходим.
     - Обработка нажатий клавиш 

       ```javascript
       handle_keys(event, snake)
       ```

       .
   - Обновляем направление (

     ```javascript
     snake.update_direction()
     ```

     ) и двигаем змейку (

     ```javascript
     snake.move()
     ```

     ).
   - Проверяем, не съела ли змейка яблоко (координаты головы совпали с 

     ```javascript
     apple.position
     ```

     ). Если да:
     - Увеличиваем длину змейки (

       ```javascript
       snake.length += 1
       ```

       ).
     - Ставим яблоко в новую случайную позицию (

       ```javascript
       apple.randomize_position()
       ```

       ).
   - Проверяем, не столкнулась ли змейка сама с собой:
     - Берём координаты головы 

       ```javascript
       head
       ```

       .
     - Если 

       ```javascript
       head
       ```

        уже есть в 

       ```javascript
       snake.positions[1:]
       ```

        (то есть в теле, не считая головы), значит, произошло столкновение. Сбрасываем змейку (

       ```javascript
       snake.reset()
       ```

       ).
   - **Отрисовка**:
     - screen.fill(BLACK) заливает весь экран чёрным фоном.
     - apple.draw(screen) рисует яблоко.
     - snake.draw(screen) рисует всю змейку.
     - pygame.display.update() обновляет окно.
   - clock.tick(FPS) задерживает выполнение цикла, чтобы он шёл не более 20 раз в секунду.

Наконец, при запуске файла как основной программы (if __name__ == "__main__":), вызывается функция main() и игра начинается.

---

## Как запустить игру

1. Убедитесь, что установлен Python 3 и библиотека **Pygame**. pip install pygame\\text{pip install pygame}pip install pygame
2. Сохраните код в файл, например, **snake_game.py**.
3. Запустите игру командой: \\text{python snake_game.py}
4. Откроется окно игры. Змейка начинает двигаться вправо. Управление с помощью стрелок (вверх, вниз, влево, вправо).

---

## Основные выводы

- Игра «Змейка» делится на **логическую часть** (управление положениями и столкновениями) и **визуальную часть** (отрисовка на экране).
- Используемый подход с классами 

  ```javascript
  Snake
  ```

   и 

  ```javascript
  Apple
  ```

   хорошо структурирует код.
- Отслеживание нажатий клавиш сделано через обработку событий Pygame.
- Для плавной анимации нужно обновлять экран в бесконечном цикле, но ограничивать этот процесс по времени (

  ```javascript
  clock.tick(FPS)
  ```

  ).

На этом базовая версия «Змейки» завершена. При желании можно добавлять новые возможности: счёт, меню, стены, разные уровни и т. д.
