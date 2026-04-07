import pygame
import random
import math

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Create squares ---
squares = []

for _ in range(20):
    size = random.randint(10, 40)  # different sizes
    square = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "vx": random.uniform(-3, 3),
        "vy": random.uniform(-3, 3),
        "size": size,
        "color": (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        ),
    }
    squares.append(square)

# --- Main loop ---
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update logic ---
    for square in squares:
        # Move
        square["x"] += square["vx"]
        square["y"] += square["vy"]

        # Bounce on edges
        if square["x"] <= 0 or square["x"] >= WIDTH:
            square["vx"] *= -1
        if square["y"] <= 0 or square["y"] >= HEIGHT:
            square["vy"] *= -1

        # --- Avoid bigger squares ---
        for other in squares:
            if other is square:
                continue

            # If other is bigger
            if other["size"] > square["size"]:
                dx = other["x"] - square["x"]
                dy = other["y"] - square["y"]
                distance = math.hypot(dx, dy)

                # If too close → avoid
                if distance < 60:
                    # reverse direction
                    square["vx"] *= -1
                    square["vy"] *= -1

                    # add randomness (jitter)
                    square["vx"] += random.uniform(-1, 1)
                    square["vy"] += random.uniform(-1, 1)

    # --- Draw ---
    screen.fill((0, 0, 0))

    for square in squares:
        pygame.draw.rect(
            screen,
            square["color"],
            (square["x"], square["y"], square["size"], square["size"]),
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()