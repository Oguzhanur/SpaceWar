import pygame as p
import sys, time, random

p.init()

# Ekran boyutları
screen_size_x = 800
screen_size_y = 500
screen_size = (screen_size_x, screen_size_y+100)
screen = p.display.set_mode(screen_size)

screen_size_min = 0

draw_engine = True # Using
sound_engine = True
input_engine = True # Using

developer_mode = False

font = p.font.Font("assets/other/main.ttf", 36)

mouse_x, mouse_y = 0, 0

wait = 0
# Player
player_pos_x = 334
player_pos_y = 450
player_size_x = 50
player_size_y = 50

player_speed = 0.4

score = 0
# Bullet
bullet_max_shoot = 30
bullet_shoot = 0
bullet_size = 30
bullet_color = (0, 0, 0)
bullet_speed = 0.7
bullets = []

can_fire = True
fire_cooldown = 0.4
last_fire_time = 0

# Main Colors
Black = (0, 0, 0)
White = (255, 255, 255)
Background = (128, 128, 128)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Orange = (255, 128, 0)

# Alt Colors
Dark_green = (0, 102, 0)  # Koyu yeşil
A_blue = (14, 16, 215)



# Monsters

monster_size_x = 50
monster_size_y = 50
monster_speed = 0.1

monsters = []
spawn_interval = 2  # spawn time

last_spawn_time = 0
    




p.display.set_caption("FlappyWariar")

full_screen = False

started = False
running = True
while running:
    current_time = time.time()

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
            p.quit

    screen.fill(Background)
    
    mouse_x, mouse_y = p.mouse.get_pos()
    
    
    if started:
        pass
    
    # Bird

    if input_engine:
        keys = p.key.get_pressed()

        if keys[p.K_LEFT] or keys[p.K_a]:
            if player_pos_x > 0:
                player_pos_x -= player_speed
        elif keys[p.K_RIGHT] or keys[p.K_d]:
            if player_pos_x < screen_size_x - player_size_x:
                player_pos_x += player_speed
                
        if keys[p.K_UP] or keys[p.K_w]:
            if player_pos_y > 0:
                player_pos_y -= player_speed
        elif keys[p.K_DOWN] or keys[p.K_s]:
            if player_pos_y < screen_size_y - player_size_y:
                player_pos_y += player_speed

        if keys[p.K_x] and can_fire and current_time - last_fire_time >= fire_cooldown and bullet_shoot < bullet_max_shoot :
            bullet_shoot += 1
            new_bullet = [player_pos_x + player_size_x // 2 - bullet_size // 2, player_pos_y]
            bullets.append(new_bullet)
            last_fire_time = current_time
            
        if keys[p.K_ESCAPE]:
            p.quit()
            
        if keys[p.K_F1]:
            developer_mode = True
        elif keys[p.K_F2]:
            developer_mode = False
            
        
        # Fullscreen
        if keys[p.K_F4]:
            if full_screen:
                p.display.set_mode(screen_size)
                full_screen = False
            else:
                p.display.set_mode(screen_size, p.FULLSCREEN)
                full_screen = True

    # Bullet Config
    bullets_to_remove = []
    monsters_to_remove = []

    for bullet in bullets:
        bullet[1] -= bullet_speed

        if bullet[1] < -30:
            bullets_to_remove.append(bullet)
        else:
            for monster in monsters:
                if (bullet[0] + bullet_size > monster[0] and bullet[0] < monster[0] + monster_size_x and
                        bullet[1] + bullet_size > monster[1] and bullet[1] < monster[1] + monster_size_y):
                    bullets_to_remove.append(bullet)
                    monsters_to_remove.append(monster)

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    for monster in monsters_to_remove:
        monsters.remove(monster)
        score += 1
        
    if current_time - last_spawn_time >= spawn_interval:
        monsters.append([random.randint(0, screen_size_x - monster_size_x), -60])
        last_spawn_time = current_time

    for monster in monsters:
        monster[1] += monster_speed

        # Canavarın alt kenarı ekrandan çıkarsa listeden kaldır
        if monster[1] > screen_size_y + 60:
            monsters.remove(monster)

    if draw_engine:
        # Resim yükleme
        player_image_path = "assets//image//player.png" 
        player_image = p.image.load(player_image_path)
        
        bullet_image_path = "assets//image//bullet.png" 
        bullet_image = p.image.load(bullet_image_path)
        
        fatman_image_path = "assets//image//fat_man.png" 
        fatman_image = p.image.load(fatman_image_path)
        
        # Resim boyutlandırma
        player_image_y = player_size_y
        player_image_x = player_size_x
        player_image = p.transform.scale(player_image, (player_image_x, player_image_y))
        
        bullet_image_y = bullet_size
        bullet_image_x = bullet_size
        bullet_image = p.transform.scale(bullet_image, (bullet_image_x, bullet_image_y))
        
        fatman_image_y = monster_size_y
        fatman_image_x = monster_size_x
        fatman_image = p.transform.scale(fatman_image, (fatman_image_x, fatman_image_y))
        
        # Çizim
        screen.blit(player_image, (player_pos_x,player_pos_y))
        
        
        for bullet in bullets:
            screen.blit(bullet_image, (bullet[0], bullet[1]))


        for monster in monsters:
            screen.blit(fatman_image, (monster[0], monster[1]))
        #
        
        p.draw.rect(screen, A_blue, (0, screen_size_y, screen_size_x, 100)) # Arayüz
        
        p.draw.rect(screen, White, (30, 525, 100, 60))
        
        p.draw.rect(screen, White, (160, 525, 100, 60))
        
        # Text
    
        if developer_mode:
            if full_screen:
                text0 = font.render("Fullscreen", True, Black)
            else:
                text0 = font.render("Windowed", True, Black)
            text1 = font.render(f"x: {mouse_x} y: {mouse_y}", True, Black)
            text2 = font.render(f"fire: {bullet_shoot}", True, Black)
            text3 = font.render(f"score: {score}", True, Black)
        else:
            text0 = font.render("", True, Black)
            text1 = font.render("", True, Black)
            text2 = font.render("", True, Black)
            text3 = font.render("", True, Black)

        screen.blit(text0, (0, 0))
        screen.blit(text1, (0, 30))
        screen.blit(text2, (0, 60))
        screen.blit(text3, (0, 90))
        
        a_text1 = font.render(f"{bullet_shoot}/{bullet_max_shoot}", True, Black)
        a_text2 = font.render(f"{score}", True, Black)
        
        
        screen.blit(a_text1, (48, 535))
        screen.blit(a_text2, (160 + 35, 535))
    

    p.display.flip()

p.quit()
sys.exit()
