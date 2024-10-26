import pygame
import serial
import time
import random

# Set up the serial connection (update the COM port as needed)
arduino = serial.Serial('COM12', 9600)  # Replace 'COM4' with your Arduino port
time.sleep(2)  # Wait for the serial connection to establish

# Initialize Pygame
pygame.init()

# Set up the drawing window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Joystick Snake Game")

# Define colors
LIGHT_LAVENDER = (230, 230, 250)  # Light lavender background color
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up fonts
font_title = pygame.font.SysFont("Arial", 40)
font_score = pygame.font.SysFont("Arial", 30)
font_game_over = pygame.font.SysFont("Arial", 50)

# Snake parameters
snake_size = 20  # Decreased size for smaller pixels
snake_speed = 10  # Control speed by adjusting this value

# Define the initial snake
snake = [(width // 2, height // 2)]
snake_direction = (snake_size, 0)  # Start moving right

# Food parameters
food_position = (random.randint(0, (width - snake_size) // snake_size) * snake_size,
                 random.randint(0, (height - snake_size) // snake_size) * snake_size)

# Game loop flag
running = True
clock = pygame.time.Clock()

# Dead zone for joystick input
dead_zone = 100  # Adjust this value for sensitivity

# Movement control
move_time = 0  # Track time for snake movement
move_interval = 200  # Interval in milliseconds to move the snake

# Score variable
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read the joystick position from Arduino
    if arduino.in_waiting > 0:
        data = arduino.readline().decode('utf-8').strip()
        try:
            x_value, y_value, button_state = map(int, data.split(','))

            # Calculate joystick movement
            delta_x = x_value - 512  # Centering joystick
            delta_y = y_value - 512  # Centering joystick

            # Determine the snake's new direction with a dead zone
            if abs(delta_x) > dead_zone:
                snake_direction = (snake_size * (1 if delta_x > 0 else -1), 0)  # Move left or right
            if abs(delta_y) > dead_zone:
                snake_direction = (0, snake_size * (1 if delta_y > 0 else -1))  # Move up or down

        except ValueError:
            continue

    # Check if it's time to move the snake
    if pygame.time.get_ticks() - move_time > move_interval:
        # Update the snake's position
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # Check for collision with food
        if new_head == food_position:
            # Spawn new food
            food_position = (random.randint(0, (width - snake_size) // snake_size) * snake_size,
                             random.randint(0, (height - snake_size) // snake_size) * snake_size)
            score += 1  # Increase the score when food is eaten
        else:
            # Remove the last segment of the snake if not eating
            snake.pop()

        # Check for collisions with boundaries
        if (new_head[0] < 0 or new_head[0] >= width or
                new_head[1] < 0 or new_head[1] >= height or
                new_head in snake[1:]):  # Check for self-collision
            print("Game Over!")
            running = False

        # Update move time
        move_time = pygame.time.get_ticks()

    # Clear the screen with light lavender background
    screen.fill(LIGHT_LAVENDER)

    # Draw the snake as circles
    for segment in snake:
        pygame.draw.circle(screen, GREEN, (segment[0] + snake_size // 2, segment[1] + snake_size // 2), snake_size // 2)

    # Draw the food as a square (can change to circle if desired)
    pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], snake_size, snake_size))

    # Render and display the game title
    title_surface = font_title.render("Joystick Snake Game", True, BLACK)
    screen.blit(title_surface, (width // 2 - title_surface.get_width() // 2, 10))

    # Render and display the score
    score_surface = font_score.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surface, (width - 150, 10))

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Game Over message
screen.fill(LIGHT_LAVENDER)  # Fill the background with light lavender for the Game Over screen
game_over_surface = font_game_over.render("Game Over!", True, RED)
screen.blit(game_over_surface, (width // 2 - game_over_surface.get_width() // 2, height // 2 - 50))
final_score_surface = font_score.render(f"Final Score: {score}", True, BLACK)
screen.blit(final_score_surface, (width // 2 - final_score_surface.get_width() // 2, height // 2 + 10))
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()
arduino.close()
