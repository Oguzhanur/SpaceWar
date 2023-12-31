import pygame as p
import sys, time, random, json
import mods.levels.levels as mll

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
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Orange = (255, 128, 0)

# Alt Colors
Dark_green = (0, 102, 0)  # Koyu yeşil
A_blue = (7, 8, 125)
Background = (53, 53, 53)
Start_Background = (65, 65, 65)
ft_green = (125, 8, 7)

# Monsters

level = 1

monster_size_x = 50
monster_size_y = 50
monster_speed = 0.1

monsters = []
spawn_interval = 2  # spawn time

last_spawn_time = 0
    

p.display.set_caption("FlappyWar")

full_screen = False

started = False
screen_page = 0
level = 1
running = True
auto_start = False

mod_support = True

# json
difficulty = "none"

if auto_start:
    screen_page = 1


mod_support = True

button_rect = p.Rect((240, 250, 250, 70))

def level_system():
    pass

while screen_page == 0:
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                screen_page = 1
            if event.key == p.K_q:
                screen_page = 1
            if event.key == p.K_e:
                screen_page = 1
        elif event.type == p.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                screen_page = 1
                
    screen.fill(Start_Background)
    
    one_start = font.render("Play", True, White)
    
    p.draw.rect(screen, ft_green, button_rect)

    screen.blit(one_start, (345, 260))
    
    p.display.flip()

while screen_page == 1:
    current_time = time.time()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()

    screen.fill(Background)
    
    mouse_x, mouse_y = p.mouse.get_pos()
    
    
    if started:
        pass
    
    # Modding
    
    json_path = mll.get_json_path(level)

    if json_path:
        with open(json_path) as f:
            d = json.load(f)
    else:
        print("Json error ")
     
    # Bird++

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
        # Adding mod Assets
        
        
        try:
            player_image_path = "mods//assets//player.png" 
            player_image = p.image.load(player_image_path)
            set_player_img = True
        except FileNotFoundError:
            set_player_img = False
        
        try:
            bullet_image_path = "mods//assets//bullet.png" 
            bullet_image = p.image.load(bullet_image_path)
            set_bullet_img = True
        except FileNotFoundError:
            set_bullet_img = False
        
        try:
            fatman_image_path = "mods//assets//fat_man.png" 
            fatman_image = p.image.load(fatman_image_path)
            set_fatman_img = True
        except FileNotFoundError:
            set_fatman_img = False
            
        
        if not set_player_img:
            player_image_path = "assets//image//player.png" 
            player_image = p.image.load(player_image_path)
        if not set_bullet_img:
            bullet_image_path = "assets//image//bullet.png" 
            bullet_image = p.image.load(bullet_image_path)
        if not set_fatman_img:
            fatman_image_path = "assets//image//fat_man.png" 
            fatman_image = p.image.load(fatman_image_path)
        
        
        
        # Update images 
        player_image_y = player_size_y
        player_image_x = player_size_x
        player_image = p.transform.scale(player_image, (player_image_x, player_image_y))
        
        bullet_image_y = bullet_size
        bullet_image_x = bullet_size
        bullet_image = p.transform.scale(bullet_image, (bullet_image_x, bullet_image_y))
        
        fatman_image_y = monster_size_y
        fatman_image_x = monster_size_x
        fatman_image = p.transform.scale(fatman_image, (fatman_image_x, fatman_image_y))
        
        # Write
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
            if mod_support:
                text4 = font.render("json files: on", True, Green)
            else:
                text4 = font.render("json files: off", True, Red)
            
        else:
            text0 = font.render("", True, Black)
            text1 = font.render("", True, Black)
            text2 = font.render("", True, Black)
            text3 = font.render("", True, Black)
            text4 = font.render("", True, Black)

        screen.blit(text0, (0, 0))
        screen.blit(text1, (0, 30))
        screen.blit(text2, (0, 60))
        screen.blit(text3, (0, 90))
        screen.blit(text4, (0, 120))
        
        a_text1 = font.render(f"{bullet_shoot}/{bullet_max_shoot}", True, Black)
        a_text2 = font.render(f"{score}", True, Black)
        
        alt_text1 = font.render(f"{difficulty}", True, Black)
        
        
        screen.blit(a_text1, (48, 535))
        screen.blit(a_text2, (160 + 35, 535))
        
        screen.blit(alt_text1, (300, 535))
    

    p.display.flip()

p.quit()
sys.exit()
