import pygame
import sys

pygame.init()
pygame.mixer.init()
sound_on = True
sound_paddle = pygame.mixer.Sound("sounds/paddle.wav")
sound_brick = pygame.mixer.Sound("sounds/brick.wav")
sound_win = pygame.mixer.Sound("sounds/win.wav")
sound_lose = pygame.mixer.Sound("sounds/lose.wav")
sound_pause = pygame.mixer.Sound("sounds/pause.wav")
sound_spielfertig = pygame.mixer.Sound("sounds/spielfertig.wav")
def play_sound(sound):
    if sound_on:
        sound.play()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("BAP!!!")
clock = pygame.time.Clock()

paddle = None
ball = None
bricks = []
lives = 3
current_level = 1
ball_speed = [3, -3]

# Paddle, Ball und Steine
def reset_level():
    global paddle, ball, bricks, lives, ball_speed
    paddle_width = max(40, 100 - (current_level // 5) * 10)
    paddle = pygame.Rect(400 - paddle_width // 2, 550, paddle_width, 10)
    ball = pygame.Rect(390, 300, 10, 10)
    bricks = [pygame.Rect(x*80+10, y*30+10, 70, 20) for y in range(3) for x in range(10)]
    lives = 3
    speed_base = 3 + (current_level - 1) * 0.2
    ball_speed = [speed_base, -speed_base]

pause = False
font = pygame.font.SysFont(None, 30)
font_big = pygame.font.SysFont(None, 70)
font_small = pygame.font.SysFont(None, 22)
font_middle = pygame.font.SysFont(None, 50)

# Startbildschirm
def show_start_screen():
    while True:
        screen.fill((0, 0, 0))
        title = font_big.render("Willkommen bei BAP!!!", True, (255, 255, 255))
        start = font_middle.render("Drücke LEERTASTE zum Starten", True, (0, 255, 0))
        einstellungen = font.render("Drücke (E) für Einstellungen",True, (0, 255, 255))
        schließen = font.render("ESC zum schließen",True, (255, 0, 0))
        regeln = font.render("Drücke (R) für Regeln",True, (255, 0, 255))
        screen.blit(title, (130, 200))
        screen.blit(start, (130, 300))
        screen.blit(einstellungen, (500, 10))
        screen.blit(schließen, (10, 10))
        screen.blit(regeln, (10, 580))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    return
                elif e.key == pygame.K_e:
                    show_settings_menu()
                elif e.key == pygame.K_r:
                    show_regel_menu()
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()   

# Einstellungsmenü
def show_settings_menu():
    while True: 
        screen.fill((0, 0, 0))
        title = font_big.render("Einstellungen", True, (255, 255, 255))
        schließen = font.render("ESC zum Zurückgehen", True, (200, 200, 200))
        sound = font_middle.render("Drücke S für Sound AN/AUS", True, (0, 255, 0))
        screen.blit(title, (250, 150))
        screen.blit(schließen, (10, 10))
        screen.blit(sound, (200, 300))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                global sound_on
                sound_on = not sound_on
                print("Sound ist jetzt", "AN" if sound_on else "AUS")

#Regelmenü
def show_regel_menu():
    while True:
        screen.fill((0, 0, 0,))
        title = font_big.render("REGELN", True, (0, 255,0))
        schließen = font.render("ESC zum Zurückgehen",True, (200, 200, 200))
        regel1 = font.render("1. Ziel",True, (0, 255, 255))
        regel11 = font_small.render("1.1 Zerstöre alle Blöcke mit dem Ball.",True, (255, 255, 255))
        regel2 = font.render("2. Steuerung:",True, (0, 255, 255))
        regel21 = font_small.render("2.1 Pfeiltasten zum Bewegen des Paddles.",True, (255, 255, 255))
        regel22 = font_small.render("2.2 Mit P Kannst du das Spiel Pausieren.",True, (255, 255, 255))
        regel23 = font_small.render("2.3 Mit S Sound an/aus im Pause- oder Einstellungsmenü",True, (255, 255, 255))
        regel3 = font.render("3. Ballverhalten:",True, (0, 255, 255))
        regel31 = font_small.render("3.1 Der Ball aprallt an Wänden, dem Paddle und Blöcken ab",True, (255, 255, 255))
        regel32 = font_small.render("3.2 Wenn der Ball den unteren Bildschirmrand berührt, verlierst du ein Leben",True, (255, 255, 255))
        regel4 = font.render("4. Leben:",True, (0, 255, 255))
        regel41 = font_small.render("4.1 Du startest jedes Level mit 3 Leben",True, (255, 255, 255))
        regel42 = font_small.render("4.2 Verlierst du alle Leben, ist das Spiel vorbei Game Over",True, (255, 255, 255))
        regel5 = font.render("5. Levelsystem:",True, (0, 255, 255))
        regel51 = font_small.render("5.1 Mit jedem Level wird der Ball schneller und das Paddle kleiner.",True, (255, 255, 255))
        regel52 = font_small.render("5.2 Nach jedem Level bekommst du einen kurzen Level geschafft Bilschirm",True, (255, 255, 255))
        regel53 = font_small.render("5.3 Nach Level 30 gewinnst du das gesamte Spiel",True, (255, 255, 255))
        regel6 = font.render("6. Blöcke",True, (0, 255, 255))
        regel61 = font_small.render("6.1 Blöcke: Jeder getroffene Block verschwindet sofort",True, (255, 255, 255))
        regel62 = font_small.render("6.2 Es gibt keine Spezialblöcke oder Power-Ups",True, (255, 255, 255))
        regel7 = font.render("7. Start & Menüs:",True, (0, 255, 255))
        regel71 = font_small.render("7.1 Drücke Leertaste auf dem Startbildschirm, um das Spiel zu starten",True, (255, 255, 255))
        regel72 = font_small.render("7.2 Mit E kommst du ins Eiinstellungsmenü",True, (255, 255, 255))
        regel73 = font_small.render("7.3 Mit R siehst du diese Regeln",True, (255, 255, 255))
        regel74 = font_small.render("7.4 Mit ESC verlässt du Menüs oder das Spiel",True, (255, 255, 255))
        screen.blit(title, (300, 10))
        screen.blit(schließen, (10, 10))
        screen.blit(regel1, (50, 50))
        screen.blit(regel11, (90, 72))
        screen.blit(regel2, (50, 94))
        screen.blit(regel21, (90 ,116))
        screen.blit(regel22, (90, 138))
        screen.blit(regel23, (90, 160))
        screen.blit(regel3, (50, 182))
        screen.blit(regel31, (90, 204))
        screen.blit(regel32, (90, 226))
        screen.blit(regel4, (50, 248))
        screen.blit(regel41, (90, 270))
        screen.blit(regel42, (90, 292))
        screen.blit(regel5, (50, 314))
        screen.blit(regel51, (90, 336))
        screen.blit(regel52, (90, 358))
        screen.blit(regel53, (90, 380))
        screen.blit(regel6, (50, 402))
        screen.blit(regel61, (90, 424))
        screen.blit(regel62, (90, 446))
        screen.blit(regel7, (50, 468))
        screen.blit(regel71, (90, 490))
        screen.blit(regel72, (90, 512))
        screen.blit(regel73, (90, 534))
        screen.blit(regel74, (90, 556))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

# Pausemenü
def show_pause_menu():
    play_sound(sound_pause)
    global pause, sound_on
    if sound_on:
        sound_pause.play(loops=-1)
    while True:
        screen.fill((0, 0, 0))
        pause_text = font_big.render("Pause", True, (255, 255, 255))
        weiter_text = font_middle.render("Drücke P zum Fortsetzen", True, (255, 255, 255))
        hauptmenu_text = font_middle.render("Drücke M für Hauptmenü", True, (0, 255, 0))
        sound_text = font_middle.render("Drücke S für Sound AN/AUS", True, (255, 255, 0))
        screen.blit(pause_text, (320, 200))
        screen.blit(weiter_text, (180, 300))
        screen.blit(hauptmenu_text, (180, 350))
        screen.blit(sound_text, (180, 400))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    sound_pause.stop()
                    pause = False
                    return
                elif e.key == pygame.K_m:
                    sound_pause.stop()
                    reset_level()
                    show_start_screen()
                    return
                elif e.key == pygame.K_s:
                    sound_on = not sound_on
                    print("Sound ist jetzt", "AN" if sound_on else "AUS")

#win und lose animation
def show_win_animation():
    play_sound(sound_spielfertig)
    for i in range(60):
        screen.fill((0, 0, i * 0))
        text = font_big.render("GEWONNEN!", True, (255, 0, 0))
        screen.blit(text, (250, 250))
        pygame.display.flip()
        clock.tick(30)
    pygame.time.wait(20000)
    reset_level()
    show_start_screen()

def show_lose_animation():
    play_sound(sound_lose)
    for i in range(60):
        screen.fill((i * 4, 0, 0))
        text = font_big.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (250, 250))
        pygame.display.flip()
        clock.tick(30)
    pygame.time.wait(2000)
    reset_level()
    show_start_screen()

def show_level_complete_screen():
    global current_level
    play_sound(sound_win)
    start_time = pygame.time.get_ticks()
    wait_time = 5000  # 5000 = 5sek

    while pygame.time.get_ticks() - start_time < wait_time:
        screen.fill((0, 0, 0))
        text1 = font_big.render("LEVEL GESCHAFFT!", True, (0, 255, 0))
        text2 = font.render(f"Weiter in {(5 - (pygame.time.get_ticks() - start_time) // 1000)}...", True, (255, 255, 255))
        screen.blit(text1, (200, 250))
        screen.blit(text2, (300, 350))
        pygame.display.flip()
        clock.tick(30)

    if current_level < 30:
        start_next_level()
    else:
        show_win_animation()

def start_next_level():
    global ball_speed, current_level
    current_level += 1
    speed_base = 3 + (current_level - 1) * 0.1
    direction_x = 1 if ball_speed[0] >= 0 else -1
    ball_speed = [direction_x * speed_base, -speed_base]
    reset_level()

# Starte mit Startbildschirm
show_start_screen()
reset_level()

# Hauptschleife
while True:
    screen.fill((0, 0, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                pause = not pause
    
    if pause:
        show_pause_menu()
        clock.tick(15)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        paddle.x -= 6
    if keys[pygame.K_RIGHT]: 
        paddle.x += 6
    paddle.x = max(0, min(800 - paddle.width, paddle.x))

    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball-Kollisionen
    if ball.left <= 0 or ball.right >= 800: ball_speed[0] *= -1
    if ball.top <= 0: ball_speed[1] *= -1
    if ball.colliderect(paddle):
        ball_speed[1] *= -1
        play_sound(sound_paddle)
    if ball.bottom >= 600:
        lives -= 1
        ball.x, ball.y = 390, 300
        ball_speed = [abs(ball_speed[0]), -abs(ball_speed[1])]
        if lives == 0:
            show_lose_animation()
            reset_level()
            
    # Steine treffen
    hit = ball.collidelist(bricks)
    if hit != -1:
        del bricks[hit]
        ball_speed[1] *= -1
        play_sound(sound_brick)

    # Sieg
    if not bricks:
        if current_level < 30: 
            show_level_complete_screen()
        else:
            show_win_animation()

    level_text = font.render(f"Level: {current_level}", True, (255, 0, 0))
    pause_hint = font.render("P = Pause", True, (255, 0, 0))
    screen.blit(level_text, (10, 570))
    screen.blit(pause_hint, (670, 570))

    pygame.draw.rect(screen, (255, 255, 255), paddle)
    pygame.draw.ellipse(screen, (255, 0, 0), ball)
    for b in bricks:
        pygame.draw.rect(screen, (0, 0, 255), b)

    text = font.render(f"Leben: {lives}", True, (255, 0, 0))
    screen.blit(text, (350, 10))

    pygame.display.flip()
    clock.tick(60)
