import pygame

pygame.init()

display_width = 1200
display_height = 752

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Стреляй или умри!')

'''Параметры первого(оранжевого корабля) игрока.'''
player1_width = 90
player1_height = 120
player1_x = 1050
player1_y = 120
health1 = 100
cool_down1 = 0

'''Параметры второго(белого корабля) игрока.'''
player2_width = 90
player2_height = 90
player2_x = 70
player2_y = 500
health2 = 100
cool_down2 = 0

clock = pygame.time.Clock()

background = pygame.image.load('bg.jpg')
player1 = pygame.image.load('player1.png')
player2 = pygame.image.load('player2.png')

bullets1 = []
bullets2 = []

class shell1:
    """Класс снарядов первого игрока."""

    def __init__(self, x1, y1, radius, color, facing):
        """
        Конструктор принимает следующие параметры:

        x1, y1 - координаты снаряда первого игрока
        radius - радиус снаряда
        color - цвет снаряда
        facing - направление снаряда
        vel1 - скорость снаряда
        """

        self.x1 = x1
        self.y1 = y1
        self.radius = radius
        self.color = color
        self.facing1 = facing
        self.vel1 = 12 * facing

    def draw(self, display1):
        """Функция отрисовывает снаряды перрого игрка на экране."""
        pygame.draw.circle(display1, self.color, (self.x1, self.y1), self.radius)


class shell2:
    """Класс снарядов второго игрока."""

    def __init__(self, x2, y2, radius, color, facing):
        """Конструктор принимает следующие параметры:

        x2, y2 - координаты снаряда второго игрока
        radius - радиус снаряда
        color - цвет снаряда
        facing - направление снаряда
        vel2 - скорость снаряда
        """

        self.x2 = x2
        self.y2 = y2
        self.radius = radius
        self.color = color
        self.facing2 = facing
        self.vel2 = 10 * facing

    def draw(self, display2):
        """Функция отрисовывает снаряды второго игрка на экране."""
        pygame.draw.circle(display2, self.color, (self.x2, self.y2), self.radius)

        
 def draw_display():
    """Функция отрисовывает основные объекты игры, то есть задний фон, игроки, снаряды и разделительная полоса."""
    display.blit(background, (0, 0))
    display.blit(player1, (player1_x, player1_y))
    display.blit(player2, (player2_x, player2_y))

    pygame.draw.line(display, (255, 255, 255), (600, 0), (600, 752), 1)

    for BULLET1 in bullets1:
        BULLET1.draw(display)

    for BULLET2 in bullets2:
        BULLET2.draw(display)

    pygame.display.update()



def print_text(message, x, y, font_color=(255, 255, 255), font_type='fonts/font.ttf', font_size=40):
    """
    Функция, которая печатает текст на экране.

    message - текст, который будет выведен на экрна
    x, y - координаты, в которых будет напечатано сообщение
    font_color - цвет текста
    font_type - шрифт текста
    font_size - размер текста
    """
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause_game():
    """Функция, которая ставит игру на паузу при нажатии кнопки ESC."""
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('ПАУЗА', 530, 300)
        print_text('Нажмите ENTER, чтобы продолжить игру', 320, 376)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)


class Button:
    """
    Класс кнопок, которые создаются на дисплее.
    Класс включает в себя функции, которые отвечают за отрисовку кнопки
    """

    def __init__(self, width, height):
        """
        Конструктор принимает параметры кнопки.

        width - ширина кнопки
        height - высота кнопки
        default_color - цвет заполнения кнопки
        effects - параметр, отвечающий за эффект заполнения кнопки цветом
        rect_width - ширина кнопки
        rect_height - высота кнопки, пока пользователь не наведет на нее
        clear - параметр, отвечающий за очищение эффекта заполнения кнопки цветом
        """
        self.width = width
        self.height = height
        self.default_color = (32, 68, 71)
        self.effects = False
        self.rect_height = 0
        self.rect_width = width
        self.clear = False

    def draw_normal_rect(self, mouse_x, mouse_y, x, y):
        """
        Функция, которая добавляет эффект отрисовки кнпоки, при наведении на нее курсором мышки.

        mouse_x - координата X курсора мыши
        mouse_y - координата Y курсора мыши
        x, y - координаты X и Y кнопки
        """
        if x <= mouse_x <= x + self.width and y <= mouse_y <= y + self.height:
            self.effects = True

        if self.effects:
            if mouse_x < x or mouse_x > x + self.width or mouse_y < y or y > y + self.height:
                self.clear = True
                self.effects = False

            if self.rect_height < self.height:
                self.rect_height += (self.height - 10) / 40

        if self.clear and not self.effects:
            if self.rect_height > 0:
                self.rect_height -= (self.height - 10) / 40
            else:
                self.clear = False

        draw_y = y + self.height - self.rect_height
        pygame.draw.rect(display, self.default_color, (x, draw_y, self.rect_width, self.rect_height))

    def draw_button(self, x, y, message, action=None, font_size=30):
        """
        Функция, которая отрисовывает кнопку на экране.

        x, y - координаты X и Y, где будет нарисована кнопка
        message - сообщение, которое будет печаться на кнопке
        action - дейстиве, которое будет выполняться по этой кнопке
        font_size - размер шрифта
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1 and action is not None:
                if action == quit:
                    pygame.quit()
                    quit()
                else:
                    action()

        self.draw_normal_rect(mouse[0], mouse[1], x, y)
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def menu():
    """Функция отвечает за отрисовку начального окна, где пользователь может либо начать игру, либо выйти из нее."""
    menu_bg = pygame.image.load('menu.jpg')
    play_button = Button(210, 90)
    exit_button = Button(190, 90)
    show = True
    while show:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_bg, (0, 0))

        play_button.draw_button(500, 240, 'Играть', start_game, 70)
        exit_button.draw_button(510, 380, 'Выход', quit, 70)

        pygame.display.update()
        clock.tick(60)


def start_game():
    """Функция, которая запускает игровой цикл."""
    run_game()


def stop_game():
    """Функция, которая останавливает игру после победы игрока."""
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(15)
        
        
 def Bullet1():
    """Функция регистрирует попадание снаряда в игрока, убирает снаряд с дисплея и убавляет здоровье."""
    global health2
    for bullet1 in bullets1:
        if 1200 > bullet1.x1 > 0:
            bullet1.x1 += bullet1.vel1
        else:
            bullets1.pop(bullets1.index(bullet1))

        if player2_x <= bullet1.x1 <= player2_x + player2_width and \
                player2_y <= bullet1.y1 <= player2_y + player2_height:
            bullets1.pop(bullets1.index(bullet1))
            health2 -= 10


 def Bullet2():
    global health1
    for bullet2 in bullets2:
        if 1200 > bullet2.x2 > 0:
            bullet2.x2 += bullet2.vel2
        else:
            bullets2.pop(bullets2.index(bullet2))

        if player1_x <= bullet2.x2 <= player1_x + player1_width and \
                player1_y <= bullet2.y2 <= player1_y + player1_height:
            bullets2.pop(bullets2.index(bullet2))
            health1 -= 10
            
 def run_game():
    """Игровой цикл, который продолжается, пока пользователь не закончит игру или не выйдет из нее."""
    global player1_x, player1_y, player2_x, player2_y, cool_down1, cool_down2, health1, health2
    game = True

    while game:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        Bullet1()
        Bullet2()

        draw_display()

        print_text('HP: ' + str(health1), 1050, 20)
        print_text('HP: ' + str(health2), 50, 20)

        if health2 == 0 and health1 == 0:
            print_text('Ничья!', 550, 376)
            stop_game()
        elif health2 == 0 and health1 != 0:
            print_text('Победил капитан оранжевого корабля!', 350, 376)
            stop_game()
        elif health2 != 0 and health1 == 0:
            print_text('Победил капиан белого корабля!', 350, 376)
            stop_game()

        """Переменная, запоминающая клавишы, которые нажал пользователь."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pause_game()

        if keys[pygame.K_p]:
            facing1 = -1
            if not cool_down1:
                if len(bullets1) < 5:
                    bullets1.append(shell1(round(player1_x), round(player1_y + player1_height // 2),
                                           5, (255, 0, 0), facing1))
                    cool_down1 = 3
            else:
                cool_down1 -= 1

        if keys[pygame.K_RIGHT] and player1_x < 1200 - player1_width - 5:
            player1_x += 5
        if keys[pygame.K_LEFT] and player1_x > 600:
            player1_x -= 5
        if keys[pygame.K_UP] and player1_y > 5:
            player1_y -= 5
        if keys[pygame.K_DOWN] and player1_y < 752 - player1_height - 5:
            player1_y += 5

        if keys[pygame.K_f]:
            facing2 = 1
            if not cool_down2:
                if len(bullets2) < 5:
                    bullets2.append(shell2(round(player2_x + player2_width), round(player2_y + player2_height // 2),
                                           5, (0, 255, 0), facing2))
                    cool_down2 = 3
            else:
                cool_down2 -= 1
        if keys[pygame.K_a] and player2_x > 5:
            player2_x -= 10
        if keys[pygame.K_d] and player2_x < 600 - player2_width - 5:
            player2_x += 10
        if keys[pygame.K_w] and player2_y > 5:
            player2_y -= 10
        if keys[pygame.K_s] and player2_y < 752 - player2_height - 5:
            player2_y += 10

        pygame.display.update()
        clock.tick(30)





if __name__ == "__main__":
    menu()
    pygame.quit()
    quit()
