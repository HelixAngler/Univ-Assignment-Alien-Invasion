import sys
import pygame
from time import *
from pygame.sprite import *
import pygame.font
class Button():
    def __init__(self, setting, screen, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        #set the properties of the button
        self.width, self.height = 200,50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        #The button message needs to be prepped only once
        self.prep_msg(msg)
    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw the blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Scoreboard():

    def __init__(self, setting, screen, stats,ship):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.setting = setting
        self.stats = stats

        # Font settings for scoreing information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        rounded_score = int(round(self.stats.score,-1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.setting.color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.setting.color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
class GameStats():
    def __init__(self, setting):
        self.setting = setting
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.ship_left = self.setting.ship_limit
        self.score = 0
class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.color = (230, 230, 230)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 300
        self.ship_limit=2
        self.drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1
        self.fleet_direction = 1
        self.alien_points = 50
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
class Bullet(Sprite):
    def __init__(self,setup,ship,screen):
        super(Bullet,self).__init__()
        self.screen=screen
        self.rect = pygame.Rect(0, 0, setup.bullet_width, setup.bullet_height)
        self.rect.centerx = ship.indicator.centerx
        self.rect.bottom = ship.indicator.top
        self.y = float(self.rect.y)
        self.color = setup.bullet_color
        self.speed = setup.bullet_speed
    def update(self):
        #moving the bullet forward
        self.y -= self.speed
        #changing the bullet's position
        self.rect.y = self.y
        # print(self.rect.y)
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
class Alien (Sprite):
    def __init__(self, setting, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.setting = setting

        self.image = pygame.image.load("alien.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.setting.alien_speed *
                   self.setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        self.rect.clamp_ip(screen_rect)
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

class ship():
    def __init__(self,screen,stats,setup):
        self.screen=screen
        self.image=pygame.image.load('Starship.png')
        self.indicator=self.image.get_rect()
        self.dim=self.screen.get_rect()
        self.middle=self.dim.centerx
        self.indicator.centerx=self.middle
        self.indicator.bottom=self.dim.bottom
        self.drol = stats.ship_left+1
        self.sett = setup
        self.pict = pygame.image.load('bg.png').convert()
        self.ind=self.pict.get_rect()
    def center_ship(self):
        self.centerx = self.indicator.centerx
    def running(self,setup,bullets,aliens,stats,sb):
        self.aln=aliens
        self.sett=setup
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.middle-=self.sett.ship_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.middle+=self.sett.ship_speed

        self.indicator.centerx = self.middle
        self.indicator.clamp_ip(self.dim)
    def goroub(self,setup,bullets,aliens,stats,sb):
        bullets.update()
        for alien in aliens.sprites():
            if alien.check_edges():
                for alien in aliens.sprites():
                    alien.rect.y += self.sett.drop_speed
                self.sett.fleet_direction *= -1
                break
        aliens.update()
        self.rect=self.indicator
        for alien in aliens.sprites():
            if alien.rect.bottom > self.dim.bottom:
                self.toncat(setup, bullets, aliens, stats)
                break
        if pygame.sprite.spritecollideany(self, aliens):
            self.toncat(setup, bullets, aliens, stats)
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        collision = pygame.sprite.groupcollide(bullets, aliens, True, True)

        if collision:
            for aliens in collision.values():
                stats.score += self.sett.alien_points * len(aliens)
                sb.prep_score()
            check_high_score(stats, sb)
        if len(aliens) == 0:
            bullets.empty()
            self.sett.increase_speed()
            create_fleet(self.sett, self.screen, aliens, self)
    def toncat(self,setup,bullets,aliens,stats):
        if stats.ship_left > 0:
            stats.ship_left -= 1
            self.drol-=1
            aliens.empty()
            bullets.empty()
            create_fleet(setup, self.screen, aliens, self)
            self.center_ship()
            sleep(0.5)
        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)
            self.drol=self.sett.ship_limit+1
    def sign(self):
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        shiple_str = "Lives: %s" % self.drol
        self.shiple_image = self.font.render(shiple_str, True, self.text_color, self.sett.color)
        self.shiple_rect = self.shiple_image.get_rect()
        self.shiple_rect.left = 20
        self.shiple_rect.top = 20
        self.screen.blit(self.shiple_image, self.shiple_rect)
    def showup(self,scr,bullets,aliens,stats,play_button,sb):
        self.aln = aliens
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.pict,self.ind)
        self.sign()
        sb.show_score()
        self.screen.blit(self.image, self.indicator)
        self.aln.draw(scr)
        for bullet in bullets:
            bullet.draw_bullet()
        if not stats.game_active:
            play_button.draw_button()
        pygame.display.flip()
def get_number_aliens_x(setting,alien_width):
    available_space = setting.screen_width - (2 * alien_width)
    num_alien_x = int(available_space / (2 * alien_width))
    return num_alien_x
def get_number_rows(setting, ship_height, alien_height):
    available_space_y = setting.screen_height - (3*alien_height) - ship_height
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows
def create_alien(setting, screen, aliens, alien_number, row_number):
    alien = Alien(setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)
def create_fleet(setting, screen, aliens, ship):
    alien = Alien(setting, screen)
    number_aliens_x = get_number_aliens_x(setting, alien.rect.width)
    for row_number in range(get_number_rows(setting, ship.indicator.height, alien.rect.height)):
        for alien_number in range(number_aliens_x):
            create_alien(setting, screen, aliens, alien_number, row_number)
def check_high_score(stats, sb):
    if stats.score>stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
def check_play_button(setting, screen, stats, play_button, sb, ship, aliens, bullets):
    mouse_x=0
    mouse_y=0
    for evente in pygame.event.get():
        if evente.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
        elif evente.type == pygame.QUIT:
            sys.exit()
        elif evente.type == pygame.KEYDOWN:
            if evente.key == pygame.K_q:
                sys.exit()
            elif evente.key == pygame.K_SPACE:
                sound = pygame.mixer.Sound("chewy1.wav")
                sound.play(loops=0)
                new_bullet = Bullet(setting,ship,screen)
                bullets.add(new_bullet)
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        setting.initialize_dynamic_settings()

        pygame.mouse.set_visible(False)

        stats.reset_stats()
        sb.prep_score()
        sb.show_score()

        stats.game_active = True

        aliens.empty()
        bullets.empty()

        create_fleet(setting, screen, aliens, ship)
        ship.center_ship()

def run():
    pygame.init()
    pygame.mixer.music.load("star-wars-theme-song.mp3")
    pygame.mixer.music.play(-1)
    sett=Settings()
    screen = pygame.display.set_mode((sett.screen_width, sett.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(sett, screen, "Play")
    stats = GameStats(sett)
    shi = ship(screen,stats,sett)
    sb = Scoreboard(sett, screen, stats,shi)

    bullets = Group()
    aliens=Group()
    create_fleet(sett,screen,aliens,shi)
    while True:
        check_play_button(sett, screen, stats, play_button, sb, shi, aliens, bullets)
        if stats.game_active:
            shi.running(sett, bullets, aliens, stats, sb)
            shi.goroub(sett, bullets, aliens, stats, sb)
        shi.showup(screen,bullets,aliens,stats,play_button,sb)
run()