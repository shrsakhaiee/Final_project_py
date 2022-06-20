import os
import pygame


pygame.font.init()  # اضافه کردن فونت‌های کتابخونه پای گیم
pygame.mixer.init()  # اضافه کردن صداهای پای گیم
WIDTH, HEIGHT = 900, 600  # رزولوشن پنجره بازی
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("SISI's 2 Player Space Shooter") 

WHITE = (255, 255, 255)  #کد سفید
BLACK = (0, 0, 0)  # کد سیاه
GREEN = (110, 194, 54)  # کد گلوله یار سبز
BLUE = (53, 180, 235)  # کد گلوله بازیکن آبی

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)  

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'sfx_hit.ogg'))  
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'sfx_fire.ogg')) 
GAME_END_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'sfx_game_over.ogg'))  

HEALTH_FONT = pygame.font.SysFont('kenvector_future.ttf', 40) 
WINNER_FONT = pygame.font.SysFont('kenvector_future.ttf', 100) 

FPS = 60  #این ها پیش فرض های پیشنهاد شده پای گیم هستند
VELOCITY = 5  
BULLET_VELOCITY = 7  
MAX_NUM_OF_BULLETS = 5  
SHIP_WIDTH, SHIP_HEIGHT = 55, 40  
BULLET_WIDTH, BULLET_HEIGHT = 10, 5  

GREEN_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

GREEN_SHIP_IMG = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'shipGreen.png')),
                                         270)  # وارد کردن عکس فضاپیمای سبز
BLUE_SHIP_IMG = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'shipBlue.png')),
                                        90)  # فضاپیمای آبی

GREEN_SHIP = pygame.transform.scale(GREEN_SHIP_IMG, (SHIP_WIDTH, SHIP_HEIGHT)) 
BLUE_SHIP = pygame.transform.scale(BLUE_SHIP_IMG, (SHIP_WIDTH, SHIP_HEIGHT))  

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')),
                                    (WIDTH, HEIGHT))  #تصویر زمینه بازی



def draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health):
    WINDOW.blit(BACKGROUND, (0, 0))  
    pygame.draw.rect(WINDOW, BLACK, BORDER)  # بوردرها

    green_health_text = HEALTH_FONT.render("♥: " + str(green_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("♥: " + str(blue_health), 1, WHITE)
    WINDOW.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))  
    WINDOW.blit(blue_health_text, (10, 10))  #

    WINDOW.blit(GREEN_SHIP, (green.x, green.y)) 
    WINDOW.blit(BLUE_SHIP, (blue.x, blue.y)) 

    for bullet in green_bullets:
        pygame.draw.rect(WINDOW, GREEN, bullet)  
    for bullet in blue_bullets:
        pygame.draw.rect(WINDOW, BLUE, bullet)  

    pygame.display.update()  #تابع آپدیت صفحه در کتابخونه پای گیم


#کنترل بازیکن سبز
def green_movement_handler(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - VELOCITY > -5:  # چپ
        green.x -= VELOCITY
    if keys_pressed[pygame.K_d] and green.x - VELOCITY + green.width < BORDER.x - 5:  # راست
        green.x += VELOCITY
    if keys_pressed[pygame.K_w] and green.y - VELOCITY > 0:  # بالا
        green.y -= VELOCITY
    if keys_pressed[pygame.K_s] and green.y - VELOCITY + green.height < HEIGHT - 5:  # پایین
        green.y += VELOCITY


# کنترل بازیکن آبی
def blue_movement_handler(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VELOCITY > BORDER.x + BORDER.width - 5:  # چپ
        blue.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and blue.x - VELOCITY + blue.width < WIDTH - 5:  # راست
        blue.x += VELOCITY
    if keys_pressed[pygame.K_UP] and blue.y - VELOCITY > 0:  # بالا
        blue.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and blue.y - VELOCITY + blue.height < HEIGHT - 5:  # پایین
        blue.y += VELOCITY


# اگر گلوله شلیک بشه چی میشه؟
def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += BULLET_VELOCITY
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            green_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VELOCITY
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


# نمایش متن برنده بازی
def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(winner_text, (WIDTH // 2 - winner_text.get_width() / 2, HEIGHT // 2 - winner_text.get_height() / 2))
    pygame.display.update()
    GAME_END_SOUND.play()
    pygame.time.delay(5000)


# تابع اصلی که فراخونی میکنیم
def main():
    green = pygame.Rect(100, 100, SHIP_WIDTH, SHIP_HEIGHT)
    blue = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)

    green_bullets = []
    blue_bullets = []

    green_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        # اطمینان از فریم در ثانیه ۶۰ تایی
        clock.tick(FPS)
        for event in pygame.event.get():

            #اگر بازی خارج شد تابع خروح احرا بشه
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < MAX_NUM_OF_BULLETS:
                    bullet = pygame.Rect(green.x + green.width, green.y + green.height // 2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_NUM_OF_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + blue.height // 2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == GREEN_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if green_health < 0:
            winner_text = "Green Wins"

        if blue_health < 0:
            winner_text = "Blue Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        green_movement_handler(keys_pressed, green)
        blue_movement_handler(keys_pressed, blue)

        handle_bullets(green_bullets, blue_bullets, green, blue)

        draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health)

    main()


if __name__ == "__main__":
    main()
