# clean up, efficient collisions, sizing and screen work, objects (wall, object, wall), Library with env class

import pygame
import math

class Player:
    def __init__(self, x, y, speed):
        # Player class with a rectangular hitbox and movement speed
        self.x = x
        self.y = y
        self.width = 10
        self.theta = math.pi/2
        self.hitbox = pygame.Rect(x, y, self.width, self.width)
        self.fov = []
        self.speed = speed


    
    def collision_detection(self, obstacles, x, y):
        # Takes in an amount moved in the x and y directions and a list of pygame.Rect objects
        # If after moving the player hasn't collided with something, finalize the move
        new_x = self.x + x
        new_y = self.y + y
        move_x = True
        move_y = True
        for obstacle in obstacles:
            obstacle = obstacle[0]
            if move_x == False and move_y == False:
                return 0
            if new_y + self.width >= obstacle.y and new_y <= obstacle.y + obstacle.width and self.x + self.width >= obstacle.x and self.x <= obstacle.x + obstacle.width and move_y:
                move_y = False
            if self.y + self.width >= obstacle.y and self.y <= obstacle.y + obstacle.width and new_x + self.width >= obstacle.x and new_x <= obstacle.x + obstacle.width and move_x:
                move_x = False
        if move_x:
            self.x += x
        if move_y:
            self.y += y


    def move(self, keys, obstacles):
        # Defines an amount to move based on what keys are being pressed
        # Checks for collisions and moves the player
        x_amount = 0
        y_amount = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # y_amount -= self.speed
            x_amount += math.cos(self.theta)*self.speed
            y_amount -= math.sin(self.theta)*self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            x_amount -= math.cos(self.theta)*self.speed
            y_amount += math.sin(self.theta)*self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x_amount -= math.cos(self.theta-math.pi/2)*self.speed
            y_amount += math.sin(self.theta-math.pi/2)*self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x_amount -= math.cos(self.theta+math.pi/2)*self.speed
            y_amount += math.sin(self.theta+math.pi/2)*self.speed
        
        self.collision_detection(obstacles, x_amount, y_amount)

    def draw(self, display, origin):
        # Draw a rectangle based at some origin
        self.hitbox = pygame.Rect(self.x + origin[0], self.y + origin[1], 10, 10)
        pygame.draw.rect(display, (0, 0, 255), self.hitbox)
        
    def line_collision(self, line, obstacles):
        # Takes in a line and a list of [pygame.Rect, color] to see if there is a collision anywhere
        # Returns the point of collision and color of collided block in a tuple

        point_of_collision = ()
        closest_distance = 10000
        final_color = (255, 255, 255)
        for obstacle in obstacles:
            color = obstacle[1]
            obstacle = obstacle[0]
            if line_of_collision := obstacle.clipline(line[0], line[1]):
                intersecting_point1, intersecting_point2 = line_of_collision
                x_distance_to1 = abs(intersecting_point1[0] - self.x)
                y_distance_to1 = abs(intersecting_point1[1] - self.y)

                x_distance_to2 = abs(intersecting_point2[0] - self.x)
                y_distance_to2 = abs(intersecting_point2[1] - self.y)

                dist_to_1 = math.sqrt(x_distance_to1**2 + y_distance_to1**2)
                dist_to_2 = math.sqrt(x_distance_to2**2 + y_distance_to2**2)

                if dist_to_1 < dist_to_2:
                    if dist_to_1 < closest_distance:
                        closest_distance = dist_to_1
                        point_of_collision = intersecting_point1
                        final_color = color

                else:
                    if dist_to_2 < closest_distance:
                        closest_distance = dist_to_2
                        point_of_collision = intersecting_point2
                        final_color = color
                
        return (point_of_collision, final_color)

    def raycasting_collision(self, display, theta, obstacles, three_d_view, width):
        # Sends out points for a ray of angle theta until the points collide with an obstacle (or the end of the screen)
        # Draws the lines for raycasting and saves a vertical (3D) block in the players FOV
        new_ray = [(self.x, self.y), (self.x + 1000*math.cos(theta), self.y - 1000*math.sin(theta))]
        if collided_obstacle := self.line_collision(new_ray, obstacles):
            point_of_collision = collided_obstacle[0]
            y_distance = abs(collided_obstacle[0][1] - self.y)
            x_distance = abs(collided_obstacle[0][0] - self.x)
            
            distance = math.sqrt(x_distance**2 + y_distance**2)
            distance *= math.cos(self.theta - theta)
            scale = distance/60
            if scale == 0:
                scale = 1
            height = 250/scale
            

            height_dif = 400 - height
            height_dif /= 2 

            y = 200
            color = collided_obstacle[1]
            red, green, blue = color
            red /= scale
            green /= scale
            blue /= scale
            if red > 255:
                red = 255
            if green > 255:
                green = 255
            if blue > 255:
                blue = 255

            pygame.draw.line(display, (255, 255, 255), (self.x + 600, self.y), (point_of_collision[0] + 600, point_of_collision[1]), 1)
            self.fov.append([pygame.Rect(three_d_view, y + height_dif, width, height), (red, green, blue)])

    def raycasting(self, display, obstacles):
        # Send out rays to find what is in the players FOV
        self.fov = []
        three_d_view = 10
        theta = self.theta + math.pi/6
        steps = math.pi/3 / .01
        increment = int(PLAY_AREA_WIDTH / steps)
        while theta > self.theta - math.pi/6:
            self.raycasting_collision(display, theta, obstacles, three_d_view, increment)
            three_d_view += increment
            theta -= .01

# a list of colors, use this to define the play area. a 0 is an empty space.
color_map = [ (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
        (255, 255, 255), 0, (255, 255, 0), (255, 0, 0), 0, 0, (255, 0, 0), (255, 255, 255),
        (255, 255, 255), 0, 0, (0, 255, 0), 0, 0, 0, (255, 255, 255),
        (255, 255, 255), 0, (255, 0, 0), (255, 0, 0), 0, (255, 0, 0), 0, (255, 255, 255),
        (255, 255, 255), 0, 0, 0, 0, (255, 0, 0), 0, (255, 255, 255),
        (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]

# A map of True or Falses based on spaces in the color map
map = [True if i else False for i in color_map]


def get_hitboxes():
    # Returns the actual hitboxes for each block in the map
    hitboxes = []
    x = 0
    y = 0
    for i in range(len(map)):
        if map[i]:
            hitboxes.append((pygame.Rect(x, y, 80, 80), color_map[i]))
        if x < BLOCK_WIDTH * math.sqrt(len(map)):
            x += BLOCK_WIDTH
        else:
            x = 0
            y += BLOCK_WIDTH

    return hitboxes

def draw_map():
    # Draws each block in the map and a corresponding mini map
    x = 600
    y = 0
    for i in range(len(map)):
        if map[i]:
            pygame.draw.rect(display, color_map[i], pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_WIDTH))
        
        if x < 600 + BLOCK_WIDTH * math.sqrt(len(map)):
            x += BLOCK_WIDTH
        else:
            x = 600
            y += BLOCK_WIDTH

    pygame.draw.rect(display, (0, 0, 255), pygame.Rect(10, 200, 525, 200))
    pygame.draw.rect(display, (0, 0, 125), pygame.Rect(10, 400, 525, 200))
    for i in player.fov:
        pygame.draw.rect(display, i[1], i[0])

def draw_screen(): 
    # Draws everything
    display.fill((0, 0, 0))
    draw_map()
    player.draw(display, origin = (600, 0))
    player.raycasting(display, map_hitboxes)
    pygame.display.update()

# Constants
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600
BLOCK_WIDTH = 80
PLAY_AREA_WIDTH = 600

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting")
clock = pygame.time.Clock()
map_hitboxes = get_hitboxes()

player = Player(100, 300, 1)
lock_mouse = False

run = True
while run: # Main loop
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    # Handle locking the mouse and using it for rotating the player
    if not pygame.mouse.get_visible():
        mouse_pos = pygame.mouse.get_pos()
        movement = pygame.mouse.get_rel()
        if movement[0] < 0:
            player.theta += .07
        elif movement[0] > 0:
            player.theta -= .07

    if keys[pygame.K_z] and lock_mouse == False:
        lock_mouse = True
        pygame.mouse.set_visible(pygame.mouse.get_visible()^1)
        pygame.event.set_grab(pygame.mouse.get_visible()^1)
    elif not keys[pygame.K_z]:
        lock_mouse = False

    player.move(keys, map_hitboxes)

    draw_screen()

pygame.quit()