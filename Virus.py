import pygame, random

WIDTH= 800
HEIGHT= 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VIRUS INEVITABLE")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect= text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT=100
    BAR_HEIGHT= 10
    fill = (percentage / 100) * BAR_LENGHT
    border= pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill=pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super(). __init__()
        self.image= pygame.image.load('Tarea9/descarga.jpg').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx= WIDTH // 2
        self.rect.bottom= HEIGHT - 10
        self.speed_x= 0
        self.shield = 100

    def update (self):
        self.speed_x= 0
        keystate= pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x= 5
        self.rect.x +=self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def disparar (self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        #sonido_laser.play()


class Covid (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(imagenes_covid)
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange (-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT -40 or self.rect.right> WIDTH + 40 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10) 

class Bullet(pygame.sprite.Sprite):
    def __init__ (self, x, y ):
        super().__init__()
        self.image = pygame.image.load("Tarea9/proyectil.jpg").convert()
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.y = y
        self.rect.centerx= x
        self.speedy= -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explocion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = Explocion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center= center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate= 50

    def update(self):
        now =pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(Explocion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = Explocion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center=center

def show_go_screen():
    screen.blit(Fondo, [0,0])
    draw_text(screen, "VIRUS INEVITABLE", 65, WIDTH //2, HEIGHT // 4)
    draw_text(screen,  "Francis Beltre", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen,  "Seras capaz dominar el virus", 27, WIDTH // 2, HEIGHT // 3)
    draw_text(screen, "Presiona una tecla ", 20, WIDTH // 2, HEIGHT * 3/ 7)
    pygame.display.flip()
    waiting = True

    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False




imagenes_covid =[]
covid_list2 = ['Tarea9/covid.jpg', 'Tarea9/covid 2.jpg', 'Tarea9/covid3.jpg', 'Tarea9/covid4.jpg']
for img in covid_list2:
    imagenes_covid.append(pygame.image.load(img).convert())

Explocion_anim= []
for i in range(4) :
    file = "Tarea9/explosion0{}.png".format(i)
    image = pygame.image.load(file).convert()
    image.set_colorkey(BLACK)
    image_scale = pygame.transform.scale(image, (70, 70))
    Explocion_anim.append(image_scale)


Fondo= pygame.image.load('Tarea9/Fondo.jpg').convert()


sonido_laser = pygame.mixer.Sound('Tarea9/lacer.ogg')
sonido_explosion = pygame.mixer.Sound('Tarea9/Explocion.ogg')
pygame.mixer.music.load('Tarea9/music.ogg')
pygame.mixer.music.set_volume(0.1)

all_sprites = pygame.sprite.Group()
covid_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

jugador = Jugador()
all_sprites.add(jugador)

for x in range(8):
    covid = Covid()
    all_sprites.add(covid)
    covid_list.add(covid)
score=0
pygame.mixer.music.play(loops=-1)


game_over =True
corriendo = True
while corriendo:
    if game_over:
        show_go_screen()

        game_over= False
        all_sprites = pygame.sprite.Group()
        covid_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        jugador = Jugador()
        all_sprites.add(jugador)

        for x in range(8):
            covid = Covid()
            all_sprites.add(covid)
            covid_list.add(covid)
        score=0        



    clock.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jugador.disparar()
    

    all_sprites.update()

    hits= pygame.sprite.groupcollide(covid_list, bullets, True, True)
    for hit in hits:
        score += 5 
        #sonido_explosion.play()
        explocion = Explocion(hit.rect.center)
        all_sprites.add(explocion)
        covid = Covid()
        all_sprites.add(covid)
        covid_list.add(covid)


    hits= pygame.sprite.spritecollide(jugador,covid_list, True)
    for hit in hits :
        jugador.shield -= 25
        covid = Covid()
        all_sprites.add(covid)
        covid_list.add(covid)

        if jugador.shield <= 0:
            game_over= True


    
    screen.blit(Fondo,[0, 0])
    all_sprites.draw(screen)

    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    draw_shield_bar(screen, 5, 5, jugador.shield)

    pygame.display.flip()
 
pygame.quit()