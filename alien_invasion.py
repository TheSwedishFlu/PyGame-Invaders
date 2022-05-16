from operator import ifloordiv
import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import Game_Stats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class for game"""

    def __init__(self):
        """Init the game and create resources"""
        pygame.init()
        self.settings = Settings()

        """setting screen size"""
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        """Making fullscreen, remove screen size setting above"""
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Dick invader")

        self.stats = Game_Stats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        """start mainloop for game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()

                #get rid of all bullets that have disapear from screen
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            #print(len(self.bullets))
            self._check_bullet_alien_collisions()
            self._update_screen()

    def _check_bullet_alien_collisions(self):
        '''respond to alien collisions'''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            #destroy existing bullets
            self.bullets.empty()
            self._create_fleet()
    

            

    def _check_events(self):
        """respond to keypress and mouse"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                    
                    
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """respond to keypress"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """respont to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create a new bullet and add it to bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """create the fllet of aliens"""
        #make an alien and find the number of aliens in a row
        #spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        #self.aliens.add(alien)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        #determine the number of rows of aliens that fit screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        #create the first row of aliens / full fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            #create an alien and place it in the row
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien_width = alien.rect.width
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien_height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)


    def _check_fleet_edges(self):
        """responds if any aliens reach the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop entire fleet of aliens and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """check if the fllet is at an edge, then update the position of all aliens"""
        self._check_fleet_edges()
        self.aliens.update()
        #llok for ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print('Dick in trouble!!')
        self._check_aliens_bottom()


    def _update_screen(self):
        """updates images on screen and flip to new screen"""
        #redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        """make recent screen visible"""
        pygame.display.flip()

    def _ship_hit(self):
        '''respond to ship when hit an alien'''
        if self.stats.ships_left > 0:

            #decrement ship left
            self.stats.ships_left -= 1

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create new fleet
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)

        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break



if __name__ == '__main__':
     """Make a game instance, run the game"""
     ai = AlienInvasion()
     ai.run_game()

