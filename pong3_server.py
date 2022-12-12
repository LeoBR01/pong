import socket
import pickle
import threading

HOST = 'localhost'  # The server's hostname or IP address
PORT = 5555  # The port used by the server
window_size = (800, 600)
paddle_width = 20
paddle_height = 100
paddle_speed = 10
ball_speed = 5
ball_size = 20
connection = []

# Create a new socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
sock.bind((HOST, PORT))

# Listen for incoming connections
sock.listen(2)

# Set the initial positions of the paddles and ball
left_paddle_pos = (50, (window_size[1] - paddle_height) / 2)
right_paddle_pos = (window_size[0] - 50 - paddle_width, (window_size[1] - paddle_height) / 2)
ball_pos = ((window_size[0] - ball_size) / 2, (window_size[1] - ball_size) / 2)

# Send the initial positions of the paddles and ball to the client
positions = {
    'left_paddle_pos': left_paddle_pos,
    'right_paddle_pos': right_paddle_pos,
    'ball': ball_pos,
}

# Serialize the initial positions using pickle
serialized_data = pickle.dumps(positions)

# Set the initial direction of the ball
ball_dir = (-1, 1)

def sendpositions(conn):
    while True:
        # Serialize the initial positions using pickle
        serialized_data = pickle.dumps(positions)
        # Receive the initial positions of the paddles and ball from the clients
        conn.sendall(serialized_data)


def handleclient(conn):
    right_score = 0
    left_score = 0

    while True:
        # Receive the current position of the paddle from the clients
        data = conn.recv(1024)

        # Deserialize the data using pickle
        positions = pickle.loads(data)

        # Update the positions of the paddles
        left_paddle_pos = positions['paddle_pos']
        right_paddle_pos = positions['right_paddle']

        # Move the ball
        ball_pos = (ball_pos[0] + ball_speed * ball_dir[0], ball_pos[1] + ball_speed * ball_dir[1])

        # Check for collisions with the paddles
        if ball_pos[0] <= left_paddle_pos[0] + paddle_width and ball_pos[1] >= left_paddle_pos[1] and ball_pos[1] <= left_paddle_pos[1] + paddle_height:
            ball_dir = (1, ball_dir[1])

        if ball_pos[0] >= right_paddle_pos[0] and ball_pos[1] >= right_paddle_pos[1] and ball_pos[1] <= right_paddle_pos[1] + paddle_height:
            ball_dir = (-1, ball_dir[1])

        # Check for collisions with the walls
        if ball_pos[1] <= 0 or ball_pos[1] >= window_size[1] - ball_size:
            ball_dir = (ball_dir[0], -ball_dir[1])

        # Check for a score
        if ball_pos[0] <= 0:
            right_score += 1
            ball_pos = ((window_size[0] - ball_size) / 2, (window_size[1] - ball_size) / 2)
        if ball_pos[0] >= window_size[0] - ball_size:
            left_score += 1
            ball_pos = ((window_size[0] - ball_size) / 2, (window_size[1] - ball_size) / 2)


# Main game loop

while True:
    conn, addr = sock.accept()
    connection.append(conn)
    print("Connected to:", addr)

    if len(connection) == 2:

        t1 = threading.Thread(target=handleclient, args=(connection[0],))
        t2 = threading.Thread(target=handleclient, args=(connection[1],))
        t3 = threading.Thread(target=sendpositions, args=(connection[0],))
        t4 = threading.Thread(target=sendpositions, args=(connection[1],))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
    else:
        print('Esperando outro cliente')