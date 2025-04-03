import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
BALL_RADIUS = 15
PLAYER_WIDTH, PLAYER_HEIGHT = 120, 65
GRAVITY = 0.5
JUMP_STRENGTH = -10
BALL_BOUNCE = -15  # Increased bounce height further
NET_X = WIDTH // 2 - 5
NET_HEIGHT = HEIGHT // 3  # Reduced net height
POINTS_TO_WIN = 15
SETS_TO_WIN = 3
MAX_HITS = 3  # Maximum touches per player

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load images
red_player_img = pygame.image.load("images/red_player.png")
blue_player_img = pygame.image.load("images/blue_player.png")
volleyball_img = pygame.image.load("images/volleyball.png")

# Resize images
red_player_img = pygame.transform.scale(red_player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
blue_player_img = pygame.transform.scale(blue_player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
volleyball_img = pygame.transform.scale(volleyball_img, (BALL_RADIUS * 2, BALL_RADIUS * 2))

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Volleyball Game")
clock = pygame.time.Clock()

# Game variables
red_score, blue_score = 0, 0
red_sets, blue_sets = 0, 0
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = random.choice([-4, 4]), -5
red_x, red_y = 100, HEIGHT - PLAYER_HEIGHT
blue_x, blue_y = WIDTH - 120, HEIGHT - PLAYER_HEIGHT
red_jump, blue_jump = False, False
ball_last_hit = None  # Keeps track of the last player who touched the ball
red_hits, blue_hits = 0, 0  # Touch counters
background_color = WHITE

# Main game loop
running = True
while running:
    screen.fill(background_color)
    pygame.draw.rect(screen, BLACK, (NET_X, HEIGHT - NET_HEIGHT, 10, NET_HEIGHT))  # Net
    screen.blit(red_player_img, (red_x, red_y))  # Red Player
    screen.blit(blue_player_img, (blue_x, blue_y))  # Blue Player
    screen.blit(volleyball_img, (ball_x - BALL_RADIUS, ball_y - BALL_RADIUS))  # Ball
    
    # Display scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Red: {red_score} | Blue: {blue_score}", True, BLACK)
    set_text = font.render(f"Sets - Red: {red_sets} | Blue: {blue_sets}", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(set_text, (20, 50))
    
    pygame.display.flip()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and not red_jump:
        red_jump = True
        red_y += JUMP_STRENGTH
    if keys[pygame.K_UP] and not blue_jump:
        blue_jump = True
        blue_y += JUMP_STRENGTH
    if keys[pygame.K_a] and red_x > 0:
        red_x -= 5
    if keys[pygame.K_d] and red_x + PLAYER_WIDTH < NET_X:
        red_x += 5
    if keys[pygame.K_LEFT] and blue_x > NET_X + 10:
        blue_x -= 5
    if keys[pygame.K_RIGHT] and blue_x + PLAYER_WIDTH < WIDTH:
        blue_x += 5
    
    # Apply gravity
    if red_jump:
        red_y += GRAVITY
    if blue_jump:
        blue_y += GRAVITY
    
    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy
    ball_dy += GRAVITY  # Gravity effect on the ball
    
    # Keep ball within screen bounds
    if ball_x - BALL_RADIUS < 0 or ball_x + BALL_RADIUS > WIDTH:
        ball_dx = -ball_dx  # Reverse direction on wall hit
    if ball_y - BALL_RADIUS < 0:
        ball_dy = -ball_dy  # Prevent ball from going above screen
    
    # Ball collision with players
    if red_x < ball_x < red_x + PLAYER_WIDTH and red_y < ball_y < red_y + PLAYER_HEIGHT:
        if ball_last_hit == "red":
            red_hits += 1
        else:
            red_hits = 1
        ball_last_hit = "red"
        ball_dy = BALL_BOUNCE
    
    if blue_x < ball_x < blue_x + PLAYER_WIDTH and blue_y < ball_y < blue_y + PLAYER_HEIGHT:
        if ball_last_hit == "blue":
            blue_hits += 1
        else:
            blue_hits = 1
        ball_last_hit = "blue"
        ball_dy = BALL_BOUNCE
    
    # Ball collision with net
    if NET_X < ball_x < NET_X + 10 and ball_y + BALL_RADIUS > HEIGHT - NET_HEIGHT:
        ball_dx = -ball_dx  # Reverse ball direction
    
    # Check if player exceeded max touches
    if red_hits > MAX_HITS:
        blue_score += 1
        red_hits = 0
        blue_hits = 0
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    if blue_hits > MAX_HITS:
        red_score += 1
        red_hits = 0
        blue_hits = 0
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    
    # Collision with ground
    if ball_y + BALL_RADIUS > HEIGHT:
        if ball_x < NET_X:
            blue_score += 1
        else:
            red_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Reset ball
        ball_dx, ball_dy = random.choice([-4, 4]), -5
        red_hits = 0
        blue_hits = 0
    
    # Check for set win
    if red_score >= POINTS_TO_WIN:
        red_sets += 1
        red_score, blue_score = 0, 0
        background_color = RED
    elif blue_score >= POINTS_TO_WIN:
        blue_sets += 1
        red_score, blue_score = 0, 0
        background_color = BLUE
    
    # Check game over
    if red_sets >= SETS_TO_WIN or blue_sets >= SETS_TO_WIN:
        background_color = RED if red_sets >= SETS_TO_WIN else BLUE
        font = pygame.font.Font(None, 72)
        winner_text = font.render("RED WINS" if red_sets >= SETS_TO_WIN else "BLUE WINS", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

pygame.quit()
