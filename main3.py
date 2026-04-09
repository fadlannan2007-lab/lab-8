import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

squares = []

# --- Create squares ---
for _ in range(20):
    size = random.randint(10, 40)

    # smaller = faster
    speed = 200 / size

    angle = random.uniform(0, 2 * math.pi)

    square = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "vx": math.cos(angle) * speed,
        "vy": math.sin(angle) * speed,
        "size": size,
        "color": (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        ),
    }
    squares.append(square)

running = True

while running:
    dt = clock.tick(60) / 1000  # convert ms → seconds

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    for square in squares:

        # FLEE behavior
        for other in squares:
            if other is square:
                continue

            if other["size"] > square["size"]:
                dx = square["x"] - other["x"]
                dy = square["y"] - other["y"]
                dist = math.hypot(dx, dy)

                if dist < 80 and dist > 0:
                    # normalize direction
                    dx /= dist
                    dy /= dist

                    # push away
                    square["vx"] += dx * 50
                    square["vy"] += dy * 50

        # Move (time-based)
        square["x"] += square["vx"] * dt
        square["y"] += square["vy"] * dt

        # Bounce walls
        if square["x"] <= 0 or square["x"] >= WIDTH:
            square["vx"] *= -1
        if square["y"] <= 0 or square["y"] >= HEIGHT:
            square["vy"] *= -1

    # --- Draw ---
    screen.fill((0, 0, 0))

    for square in squares:
        pygame.draw.rect(
            screen,
            square["color"],
            (square["x"], square["y"], square["size"], square["size"]),
        )

    # --- FPS HUD ---
    fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()

pygame.quit()