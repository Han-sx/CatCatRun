import os
import pygame
import random
import cv2

pygame.init()
# 初始化混音器
pygame.mixer.init()

# 获取屏幕的实际分辨率
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h

# 创建全屏窗口
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CatCatRun!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

try:

    icon = pygame.image.load(os.path.join('image', 'icon.png'))
    pygame.display.set_icon(icon)
    # 加载并缩放玩家图片
    player_frames = [
        pygame.transform.scale(pygame.image.load(os.path.join('image', f'player_0{i}.png')),
                               (int(25 * (WIDTH / 1000)), int(40 * (HEIGHT / 600))))
        for i in range(1, 4)
    ]

    # 加载并缩放敌人图片
    enemy_images = [
        pygame.transform.scale(pygame.image.load(os.path.join('image', f'{enemy_type}.png')),
                               (int(45 * (WIDTH / 1000)), int(45 * (HEIGHT / 600))))
        for enemy_type in ['cat', 'dog', 'leopard', 'tiger']
    ]

    # 加载并缩放子弹图片
    bullet_img = pygame.transform.scale(pygame.image.load(os.path.join('image', 'bullet.png')),
                                        (int(5 * (WIDTH / 1000)), int(10 * (HEIGHT / 600))))

    # 加载并缩放暂停图片
    pause_img = pygame.transform.scale(pygame.image.load(os.path.join('image', 'pause2.png')),
                                       (int(400 * (WIDTH / 1000)), int(400 * (HEIGHT / 600))))

    # 加载并缩放开始背景图片
    start_bg_img = pygame.transform.scale(pygame.image.load(os.path.join('image', 'start_bg.png')),
                                          (WIDTH, HEIGHT))

    # 加载并缩放开始按钮图片
    start_btn_img = pygame.transform.scale(pygame.image.load(os.path.join('image','start_btn.png')),
                                           (int(200 * (WIDTH / 1000)), int(200 * (HEIGHT / 600))))
    start_btn_rect = start_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # 加载并缩放背景图片
    bg_img = pygame.transform.scale(pygame.image.load(os.path.join('image','mountain_forest.png')),
                                    (WIDTH, HEIGHT))

    # 加载音效
    shoot_sound = pygame.mixer.Sound(os.path.join('sound','shoot.wav'))
    shoot_sound.set_volume(0.4)
    hit_enemy_sound = pygame.mixer.Sound(os.path.join('sound', 'hit_enemy.wav'))
    enemy_hit_player_sound = pygame.mixer.Sound(os.path.join('sound', 'enemy_hit_player.wav'))
    enemy_hit_player_sound.set_volume(0.5)

    # 加载背景音乐
    pygame.mixer.music.load(os.path.join('sound', 'background_music.wav'))
    pygame.mixer.music.set_volume(0.5)  # 设置背景音乐音量

    # 加载结束视频
    cap = cv2.VideoCapture(os.path.join('video', 'end_video.mp4'))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)

except pygame.error as e:
    print(f"图片加载出错: {e}")
    pygame.quit()
    raise SystemExit
except FileNotFoundError as e:
    print(f"音效或音乐文件加载出错: {e}")
    pygame.quit()
    raise SystemExit
except cv2.error as e:
    print(f"视频加载出错: {e}")
    pygame.quit()
    raise SystemExit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = player_frames
        self.right_frames = [pygame.transform.flip(frame, True, False) for frame in player_frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - int(10 * (HEIGHT / 600))
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.animation_time = 0
        self.animation_delay = 50
        self.paused = False
        self.pause_start_time = 0
        self.facing_right = False

    def update(self):
        if not self.paused:
            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_a]:
                self.speedx = -int(5 * (WIDTH / 1000))
                self.facing_right = False
            if keystate[pygame.K_d]:
                self.speedx = int(5 * (WIDTH / 1000))
                self.facing_right = True
            if keystate[pygame.K_w]:
                self.speedy = -int(5 * (HEIGHT / 600))
            if keystate[pygame.K_s]:
                self.speedy = int(5 * (HEIGHT / 600))
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

        self.animation_time += clock.get_time()
        if self.animation_time > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            if self.facing_right:
                self.image = self.right_frames[self.current_frame]
            else:
                self.image = self.frames[self.current_frame]
            self.animation_time = 0

    def shoot(self):
        if not self.paused:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            # 播放射击音效
            shoot_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        range_width = WIDTH - self.rect.width
        if range_width > 0:
            self.rect.x = random.randrange(range_width)
        else:
            self.rect.x = 0
        self.rect.y = random.randrange(-int(100 * (HEIGHT / 600)), -int(40 * (HEIGHT / 600)))
        self.speedy = random.randrange(1, 4)
        self.health = health
        self.speedx = 0

    def update(self):
        if not player.paused:
            # 一定概率随机改变水平速度
            if random.random() < 0.02:
                self.speedx = random.randint(-int(2 * (WIDTH / 1000)), int(2 * (WIDTH / 1000)))

            # 更新敌人位置
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            # 限制敌人不超出窗口边界
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.speedx = 0
            if self.rect.left < 0:
                self.rect.left = 0
                self.speedx = 0
            if self.rect.top > HEIGHT + int(10 * (HEIGHT / 600)):
                range_width = WIDTH - self.rect.width
                if range_width > 0:
                    self.rect.x = random.randrange(range_width)
                else:
                    self.rect.x = 0
                self.rect.y = random.randrange(-int(100 * (HEIGHT / 600)), -int(40 * (HEIGHT / 600)))
                self.speedy = random.randrange(1, 4)
                self.speedx = 0

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -int(10 * (HEIGHT / 600))

    def update(self):
        if not player.paused:
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    enemy_type_index = random.randint(0, 3)
    enemy_image = enemy_images[enemy_type_index]
    if enemy_type_index == 0:
        health = 1
    elif enemy_type_index == 1:
        health = 2
    elif enemy_type_index == 2:
        health = 5
    else:
        health = 10
    enemy = Enemy(enemy_image, health)
    all_sprites.add(enemy)
    enemies.add(enemy)

score = 0
# 指定支持中文的字体，这里以 Windows 上的黑体为例
font_name = pygame.font.match_font('SimHei')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, int(size * (WIDTH / 1000)))
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


clock = pygame.time.Clock()
running = True
in_start_menu = True
in_end_menu = False

# 开始播放背景音乐
pygame.mixer.music.play(-1)

# 背景滚动相关变量
bg_y1 = 0
bg_y2 = -HEIGHT
bg_speed = 1

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif in_start_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_btn_rect.collidepoint(mouse_pos):
                    in_start_menu = False
        elif in_end_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    player.shoot()
                # 按 ESC 键退出全屏
                if event.key == pygame.K_ESCAPE:
                    running = False

    if in_start_menu:
        win.blit(start_bg_img, (0, 0))
        win.blit(start_btn_img, start_btn_rect)
    elif in_end_menu:
        ret, frame = cap.read()
        if not ret:
            # 视频播放结束，将视频指针重置到开头
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # 顺时针旋转90度
            frame = pygame.surfarray.make_surface(frame)
            win.blit(frame, (0, 0))
    else:
        # 滚动背景
        bg_y1 += bg_speed
        bg_y2 += bg_speed

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        # 绘制背景
        win.blit(bg_img, (0, bg_y1))
        win.blit(bg_img, (0, bg_y2))

        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            player.lives -= 1
            # 播放敌人撞到角色的音效
            enemy_hit_player_sound.play()
            if player.lives <= 0:
                in_end_menu = True
            else:
                player.paused = True
                player.pause_start_time = pygame.time.get_ticks()

        if player.paused:
            current_time = pygame.time.get_ticks()
            if current_time - player.pause_start_time >= 1000:
                player.paused = False

        all_sprites.update()

        # 移除超出屏幕的子弹
        for bullet in bullets.copy():
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
                all_sprites.remove(bullet)

        if not player.paused:
            hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in hits.items():
                for bullet in bullet_list:
                    if enemy.hit():
                        score += 10
                        # 播放打中敌人的音效
                        hit_enemy_sound.play()
                        enemy_type_index = random.randint(0, 3)
                        enemy_image = enemy_images[enemy_type_index]
                        if enemy_type_index == 0:
                            health = 1
                        elif enemy_type_index == 1:
                            health = 2
                        elif enemy_type_index == 2:
                            health = 5
                        else:
                            health = 10
                        new_enemy = Enemy(enemy_image, health)
                        all_sprites.add(new_enemy)
                        enemies.add(new_enemy)

        all_sprites.draw(win)
        draw_text(win, str(score), 18, WIDTH // 2, int(10 * (HEIGHT / 600)))
        # 调整 Lives 的显示位置
        draw_text(win, "剩余血量" + f": {player.lives}", 18, int(50 * (WIDTH / 1000)), int(10 * (HEIGHT / 600)))

        if player.paused:
            win.blit(pause_img, ((WIDTH - pause_img.get_width()) // 2, HEIGHT - pause_img.get_height()))

    pygame.display.flip()

# 停止背景音乐
pygame.mixer.music.stop()
# 释放视频捕获对象
cap.release()
pygame.quit()