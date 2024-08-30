import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
screen_width = 864
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pygame App")

# Load images
bg = pygame.image.load('bg.png')
tt = pygame.image.load('tt.png')

# Resize the tt image to a more appropriate size
tt_width = 100
tt_height = int(tt.get_height() * (tt_width / tt.get_width()))
tt = pygame.transform.scale(tt, (tt_width, tt_height))

# Set initial position of the tt image
tt_x = (screen_width - tt.get_width()) // 2
tt_y = screen_height - tt.get_height() - 50  # Position it near the bottom

# Set speed
speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the keys pressed
    keys = pygame.key.get_pressed()
    
    # Move tt image left or right
    if keys[pygame.K_LEFT]:
        tt_x -= speed
    if keys[pygame.K_RIGHT]:
        tt_x += speed

    # Boundary check to keep tt image within the screen
    if tt_x < 0:
        tt_x = 0
    if tt_x > screen_width - tt.get_width():
        tt_x = screen_width - tt.get_width()

    # Draw background and tt image
    screen.blit(bg, (0, 0))
    screen.blit(tt, (tt_x, tt_y))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Cap the frame rate at 60 FPS
