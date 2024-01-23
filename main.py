import pygame
import sys
import math
import random
import os
from moviepy.editor import ImageSequenceClip

# Initialize Pygame
if not os.path.exists("game_frames"):
    os.makedirs("game_frames")

for x in os.listdir("game_frames"):
    os.remove("game_frames/" + str(x))

if not os.path.isfile("collisions.txt"):
    f = open('collisions.txt', 'w')
    f.close()

with open("collisions.txt", "w") as file:
    file.write("")
    
    
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BALL_COLOR = (255, 0, 0)
CIRCLE_COLOR = (128, 128, 128)  # Gray color
BACKGROUND_COLOR = (128, 128, 128)  # Grey
BALL_SIZE = 10
VELOCITY_INCREASE = 1.0
SIZE_INCREASE = 1.2
CIRCLE_RADIUS = min(WIDTH, HEIGHT) // 2 - BALL_SIZE
COLLISION_COOLDOWN = 200
GRAVITY = 9.81  # Acceleration due to gravity (m/s^2)
FRAME_RATE = 60  # Assuming 60 frames per second

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Circle")

# Ball settings
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [2, 2]

# Load sound
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

# Frame capture setup
frame_folder = "game_frames"
os.makedirs(frame_folder, exist_ok=True)
frame_count = 0

# Collision timestamps
collision_timestamps = []

# Main loop
running = True
last_collision_time = 0  # Stores the time of the last collision

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gravity effect
    # Update the ball's vertical velocity to include gravity
    ball_vel[1] += GRAVITY / FRAME_RATE

    # Move the ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check for collision with the circle
    if (current_time - last_collision_time > COLLISION_COOLDOWN) and is_colliding_with_circle(ball_pos[0], ball_pos[1]):
        last_collision_time = current_time
        bing_sound.play()
        collision_timestamps.append(current_time / 1000.0)  # Record collision time in seconds

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

    # Check if the ball's size is >= 0.9 times the circle's radius
    if BALL_SIZE >= 0.999 * CIRCLE_RADIUS:
        running = False
        
        BALL_SIZE = .98 * CIRCLE_RADIUS
        
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_SIZE)  # Draw ball
        # This will stop the game loop

    # Drawing
    screen.fill(BACKGROUND_COLOR)  # Fill screen with grey
    pygame.draw.circle(screen, (0, 0, 0), (WIDTH // 2, HEIGHT // 2), CIRCLE_RADIUS)  # Draw large black circle
    pygame.draw.circle(screen, CIRCLE_COLOR, (WIDTH // 2, HEIGHT // 2), CIRCLE_RADIUS, 3)  # Draw enclosing circle with outline
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_SIZE)  # Draw ball

    # Save the current frame as an image
    frame_path = os.path.join(frame_folder, f"frame{frame_count}.jpeg")
    pygame.image.save(screen, frame_path)
    frame_count += 1

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FRAME_RATE)

# Save collision timestamps to a file

# Move ball to center


with open("collisions.txt", "w") as file:
    for timestamp in collision_timestamps:
        file.write(f"{timestamp}\n")

# After game loop ends, create the video (this part can be slow)
frames = [os.path.join(frame_folder, f"frame{i}.jpeg") for i in range(frame_count)]
clip = ImageSequenceClip(frames, fps=60)
clip.write_videofile("game.mp4", fps=60)

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

# Load the video file
video = VideoFileClip("game.mp4")

# Load the sound
sound = AudioFileClip("bing.wav")

# Read collision timestamps from file
collision_timestamps = []
with open("collisions.txt", "r") as file:
    collision_timestamps = [float(line.strip()) for line in file]


decrease_increment = 0.75
for i in range(9):
    collision_timestamps[i] -= decrease_increment
    decrease_increment -= 0.05


# Calculate the frame rate of the video
frame_rate = video.fps

# Create a list of audio clips to be added with adjusted timestamps
audio_clips = [sound.set_start(t - i / frame_rate) for i, t in enumerate(collision_timestamps)]

# Combine the audio clips
composite_audio = CompositeAudioClip(audio_clips)

# Set the composite audio to the video
video = video.set_audio(composite_audio)

# Write the result to a file
#output_filename = "game_with_sound_adjusted.mp4"
#video.write_videofile(output_filename, codec='libx264', audio_codec='aac')

# Close the clips
video.close()
sound.close()
#for clip in audio_clips:
#    clip.close()

#print(f"Video saved as {output_filename}")

pygame.quit()
sys.exit()
