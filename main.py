import pygame
import sys
import math
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
BALL_COLOR = (255, 0, 0)
CIRCLE_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (128, 128, 128)  #Grey
BALL_SIZE = 10
VELOCITY_INCREASE = 1.1
SIZE_INCREASE = 2.0
CIRCLE_RADIUS = min(WIDTH, HEIGHT) // 2 - BALL_SIZE
COLLISION_COOLDOWN = 800 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Circle")


ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [2, 2]

bing_sound = pygame.mixer.Sound("bing.wav")  # Replace 'bing.wav' with the path to your sound file

# Function to check collision with circle
def is_colliding_with_circle(x, y):
    distance_from_center = math.sqrt((x - WIDTH // 2) ** 2 + (y - HEIGHT // 2) ** 2)
    return distance_from_center + BALL_SIZE > CIRCLE_RADIUS

# Function to adjust ball position after collision
def adjust_ball_position():
    angle_to_center = math.atan2(ball_pos[1] - HEIGHT // 2, ball_pos[0] - WIDTH // 2)
    ball_pos[0] = WIDTH // 2 + math.cos(angle_to_center) * (CIRCLE_RADIUS - BALL_SIZE)
    ball_pos[1] = HEIGHT // 2 + math.sin(angle_to_center) * (CIRCLE_RADIUS - BALL_SIZE)

# Clock for controlling FPS
clock = pygame.time.Clock()

# Main loop
running = True
last_collision_time = 0  # Stores the time of the last collision

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check for collision with the circle
    if (current_time - last_collision_time > COLLISION_COOLDOWN) and is_colliding_with_circle(ball_pos[0], ball_pos[1]):
        last_collision_time = current_time
        bing_sound.play()

        # Increase the size of the ball by the constant and the magnitude of the velocity
        velocity_magnitude = math.sqrt(ball_vel[0]**2 + ball_vel[1]**2)
        BALL_SIZE += SIZE_INCREASE + velocity_magnitude
        COLLISION_COOLDOWN = COLLISION_COOLDOWN * .825

        # Calculate the angle of reflection
        angle_of_incidence = math.atan2(ball_pos[1] - HEIGHT // 2, ball_pos[0] - WIDTH // 2) + math.pi
        random_angle = random.uniform(-math.pi / 4, math.pi / 4)  # Random angle within +/- 45 degrees
        reflection_angle = angle_of_incidence + random_angle

        # Update velocity based on reflection angle
        ball_vel[0] = math.cos(reflection_angle) * velocity_magnitude * VELOCITY_INCREASE
        ball_vel[1] = math.sin(reflection_angle) * velocity_magnitude * VELOCITY_INCREASE

        # Adjust ball position smoothly
        adjust_ball_position()

    # Drawing
    screen.fill(BACKGROUND_COLOR)  # Fill screen with grey
    pygame.draw.circle(screen, (0, 0, 0), (WIDTH // 2, HEIGHT // 2), CIRCLE_RADIUS)  # Draw large black circle
    pygame.draw.circle(screen, CIRCLE_COLOR, (WIDTH // 2, HEIGHT // 2), CIRCLE_RADIUS, 3)  # Draw enclosing circle with outline
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_SIZE)  # Draw ball

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)  # Set FPS to 60

# Freeze the program
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
