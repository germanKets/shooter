#Создай собственный Шутер!

#подключение музыки и модулей
from pygame import *
from random import randint
font.init()
font1 = font.SysFont('Times New Roman', 30)
font2 = font.SysFont('Times New Roman', 30)
mixer.init()
# mixer.music.load('crazy.ogg')
# mixer.music.play()


#окно
window = display.set_mode((700, 500))
display.set_caption('minicrysis')

def init_game():
    global main_player, villain1, villain2, villain3, villain, villain5, monsters, bullets, btn, game, finish, menu, clock, FPS, current_level_index, menu_channel, game_channel
    main_player = Player('mainperson.png', 65, 65, 15, 50, 400)
    villain1 = Enemy('villain.png', 65, 65, randint(1, 3), randint(0, 635), 0)
    villain2 = Enemy('villain.png', 65, 65, randint(1, 3), randint(0, 635), 0)
    villain3 = Enemy('villain.png', 65, 65, randint(1, 3), randint(0, 635), 0)
    villain4 = Enemy('villain.png', 65, 65, randint(1, 3), randint(0, 635), 0)
    villain5 = Enemy('villain.png', 65, 65, randint(1, 3), randint(0, 635), 0)
    monsters = sprite.Group()
    monsters.add(villain1, villain2, villain3, villain4, villain5)
    bullets = sprite.Group()
    btn = GameSprite('images.png', 150, 80, 15, 50, 400)
    game = True
    finish = False
    menu = True
    clock = time.Clock()
    FPS = 60
    current_level_index = 0
    # menu_channel = mixer.Channel(0)
    # game_channel = mixer.Channel(1)
    load_level(current_level_index)

def update_game():
    pass

def draw_game():
    screen.fill((0, 0, 0))
    pygame.display.update()

# def show_menu():
#     game_channel.stop()
#     menu_channel.play(mixer.Sound('menu_sound.ogg'), loops =-1)

def main():
    # menu_channel.stop()
    game_channel.play(mixer.Sound('crazy.ogg'), loops =-1)



#классы
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (w, h)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -=10
        elif keys_pressed[K_s] and self.rect.y < 440:
            self.rect.y +=10
        elif keys_pressed[K_a] and self.rect.x > -1:
            self.rect.x -=10
        elif keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x +=10
    
    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, 17, self.rect.centerx, self.rect.top)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >=500:
            self.rect.y = -100
            self.rect.x = randint(0, 700 - self.rect.width)
            self.speed = randint(3, 7)
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <=0:
            self.kill()

#персонажи

#смена уровней
levels = [
    {"enemy_count": 5},
    {"enemy_count": 10},
    {"enemy_count": 15}
]


def load_level(level_index):
    global monsters, lost, dead
    monsters.empty()
    lost = 0
    dead = 0
    level_data = levels[level_index]
    for i in range(level_data["enemy_count"]):
        monsters.add(Enemy(
            "villain.png", 65, 65, randint(1, 3), randint(0, 635), 0)
            )

def check_level_complete():
    return len(monsters) == 0





#фон
background = transform.scale(
    image.load('crysis.png'),
    (700, 500)
)
background1 = transform.scale(
    image.load('theme.png'),
    (700, 500)
)




win = font2.render(
    'YOU WON!', True, (0, 255, 0)
)
lose = font2.render(
    'YOU LOSE!', True, (255, 0, 0)
)


init_game()

#игровой цикл
while game:
    if menu:
        # show_menu()
        window.blit(background1, (0, 0))
        btn.reset()
        for e in event.get():
                if e.type == QUIT:
                    game = False
                if e.type == MOUSEBUTTONDOWN:
                    x, y = e.pos
                    if btn.rect.collidepoint(x, y):
                        menu = False


    if finish == False and menu == False:
        main()
        window.blit(background, (0, 0))
        main_player.reset()
        main_player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render(
            'Пропущено:' + str(lost), 1, (255, 0, 0)
        )
        text_kill = font1.render(
            'Убито:' + str(dead), 1, (255, 0, 0)
        )
        window.blit(text_lose, (50, 50))
        window.blit(text_kill, (100, 100))

        sprites_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        sprites_list1 = sprite.spritecollide(
            main_player, monsters, False
        )
        
        for monster in sprites_list:
            dead +=1
            
        if lost >= 20 or len(sprites_list1) >=1:
            finish = True
            window.blit(lose, (250, 200))

        for e in event.get():
                if e.type == QUIT:
                    game = False
                if e.type == MOUSEBUTTONDOWN:
                    main_player.fire()
                if e.type == KEYDOWN:
                    if e.key == K_r:
                        init_game() 


    #проверка завершения уровня
        if check_level_complete():
            current_level_index +=1

            if current_level_index < len(levels):
                load_level(current_level_index)
            else:
                finish = True
                window.blit(win, (250, 200))


    if finish == True and menu == False:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                    if e.key == K_r:
                        init_game() 

    display.update()
    clock.tick(FPS)
