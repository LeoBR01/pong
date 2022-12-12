import socket
import pygame
import sys
import pickle

# Initialize Pygame
pygame.init()

# Set the window size and title
window_size = (800, 600)
window_title = 'Pong'
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_title)

# Set the background color
background_color = (0, 0, 0)

# Set the paddle dimensions
paddle_width = 20
paddle_height = 100

# Set the ball dimensions
ball_size = 20

# Set the paddle and ball speeds
paddle_speed = 10
ball_speed = 5

# Create a new socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
sock.connect(('localhost', 5555))

data = sock.recv(1024)

#receiving positions from server
positions = pickle.loads(data)

# Main game loop
while True:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sock.close()
            pygame.quit()
            sys.exit()

    # Set the colors of the paddles and ball
    paddle_color = (48,101,172)
    ball_color = (255, 255, 255)

    # Draw the paddles
    left_paddle = pygame.Rect(left_paddle_pos[0], left_paddle_pos[1], paddle_width, paddle_height)
    right_paddle = pygame.Rect(right_paddle_pos[0], right_paddle_pos[1], paddle_width, paddle_height)
    pygame.draw.rect(screen, paddle_color, left_paddle)
    pygame.draw.rect(screen, paddle_color, right_paddle)

    # Draw the ball ( Circle )
    ball = pygame.Rect(ball_pos[0], ball_pos[1], ball_size, ball_size)
    pygame.draw.rect(screen, ball_color, ball)

    pygame.display.update()

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle_pos = (left_paddle_pos[0], left_paddle_pos[1] - paddle_speed)
    if keys[pygame.K_DOWN]:
        paddle_pos = (left_paddle_pos[0], left_paddle_pos[1] + paddle_speed)

    # Send the current position of the paddle to the server
    positions = {
        'paddle_pos': paddle_pos,
    }
    # Serialize the initial positions using pickle
    serialized_data = pickle.dumps(positions)

    # Send the serialized data to the server or other client
    sock.sendall(serialized_data)

    # Receive the updated positions of the paddles and ball from the server
    data = sock.recv(1024)

    # Deserialize the data using pickle
    positions = pickle.loads(data)

    #updated positions for client

    left_paddle_pos = positions['left_paddle']
    right_paddle_pos = positions['right_paddle']
    ball_pos = positions['ball']