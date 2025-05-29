import pygame
import random

themes = {
    '1': 'background1.png',
    '2': 'background2.jpeg',
    '3': 'background3.jpg',
    '4': 'background4.jpg',
    '5': 'background5.jpg'
}

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def show_mode_selection(screen, font):
    screen.fill(COLOR_BLACK)
    title = font.render("Select Mode:", True, COLOR_WHITE)
    option1 = font.render("1 - Player vs Player", True, COLOR_WHITE)
    option2 = font.render("2 - Player vs Computer", True, COLOR_WHITE)

    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
    screen.blit(option1, option1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    screen.blit(option2, option2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
    pygame.display.flip()

    selected_mode = None
    while selected_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_mode = "PVP"
                elif event.key == pygame.K_2:
                    selected_mode = "PVC"
    return selected_mode

def move_ai_paddle(paddle_rect, ball_rect, delta_time):
    if ball_rect.centery < paddle_rect.centery:
        paddle_rect.top -= 0.3 * delta_time
    elif ball_rect.centery > paddle_rect.centery:
        paddle_rect.top += 0.3 * delta_time
    paddle_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

def create_ball():
    ball = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)
    accel_x = random.randint(2, 4) * 0.15
    accel_y = random.randint(2, 4) * 0.15
    if random.choice([True, False]):
        accel_x *= -1
    if random.choice([True, False]):
        accel_y *= -1
    return ball, accel_x, accel_y

def handle_input_events(events, paddle_1_move, paddle_2_move):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle_1_move = -0.5
            elif event.key == pygame.K_s:
                paddle_1_move = 0.5
            elif event.key == pygame.K_UP:
                paddle_2_move = -0.5
            elif event.key == pygame.K_DOWN:
                paddle_2_move = 0.5
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle_1_move = 0.0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle_2_move = 0.0
    return paddle_1_move, paddle_2_move

def update_positions(paddle_1, paddle_2, ball, paddle_1_move, paddle_2_move, ball_accel_x, ball_accel_y, delta_time):
    paddle_1.top += paddle_1_move * delta_time
    paddle_2.top += paddle_2_move * delta_time
    paddle_1.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    paddle_2.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    ball.left += ball_accel_x * delta_time
    ball.top += ball_accel_y * delta_time
    return paddle_1, paddle_2, ball

def check_collisions(ball, paddle_1, paddle_2, ball_accel_x, ball_accel_y):
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_accel_y *= -1
        ball.top = max(0, ball.top)
        ball.bottom = min(SCREEN_HEIGHT, ball.bottom)

    if paddle_1.colliderect(ball) and ball_accel_x < 0:
        ball_accel_x *= -1
        ball.left = paddle_1.right
    elif paddle_2.colliderect(ball) and ball_accel_x > 0:
        ball_accel_x *= -1
        ball.right = paddle_2.left

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        return None, None
    return ball_accel_x, ball_accel_y

def draw_elements(screen, paddle_1, paddle_2, ball, font, score_p1, score_p2, bg_image):
    screen.blit(bg_image, (0, 0))
    pygame.draw.rect(screen, COLOR_WHITE, paddle_1)
    pygame.draw.rect(screen, COLOR_WHITE, paddle_2)
    pygame.draw.rect(screen, COLOR_WHITE, ball)
    score_text = font.render(f"{score_p1} - {score_p2}", True, COLOR_WHITE)
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 30)))
    exit_text = font.render("Exit", True, (255, 0, 0))
    exit_button = exit_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(exit_text, exit_button)
    pygame.display.flip()
    return exit_button

def show_start_screen(screen, font):
    screen.fill(COLOR_BLACK)
    text = font.render('Press SPACE to Start', True, COLOR_WHITE)
    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    pygame.display.flip()

def show_game_over_screen(screen, font):
    screen.fill(COLOR_BLACK)
    text = font.render('You Lost! Press SPACE to Restart', True, COLOR_WHITE)
    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def show_winner_screen(screen, font, winner_text):
    screen.fill(COLOR_BLACK)
    text = font.render(winner_text, True, COLOR_WHITE)
    prompt = font.render("Press SPACE to Restart", True, COLOR_WHITE)
    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
    screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def show_theme_selection(screen, font):
    screen.fill(COLOR_BLACK)
    title = font.render("Select Background Theme:", True, COLOR_WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    options = [
        "1 - Red vs Blue",
        "2 - Footballer",
        "3 - Tennis",
        "4 - Sung Jinwoo",
        "5 - Me"
    ]
    for i, text in enumerate(options, 1):
        option = font.render(text, True, COLOR_WHITE)
        screen.blit(option, (SCREEN_WIDTH // 2 - option.get_width() // 2, 150 + i * 40))
    pygame.display.flip()

    selected = None
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.unicode in themes:
                selected = themes[event.unicode]
    return selected

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    font = pygame.font.SysFont("Consolas", 30)

    theme_image_path = show_theme_selection(screen, font)
    bg_image = pygame.image.load(theme_image_path)
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    score_p1 = 0
    score_p2 = 0
    mode = show_mode_selection(screen, font)

    while True:
        paddle_1 = pygame.Rect(30, 0, 7, 100)
        paddle_2 = pygame.Rect(SCREEN_WIDTH - 50, 0, 7, 100)
        paddle_1_move = 0
        paddle_2_move = 0
        ball, ball_accel_x, ball_accel_y = create_ball()

        started = False
        while not started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = True
            show_start_screen(screen, font)
            clock.tick(60)

        while True:
            delta_time = clock.tick(60)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        return

            paddle_1_move, paddle_2_move = handle_input_events(events, paddle_1_move, paddle_2_move)
            exit_button = draw_elements(screen, paddle_1, paddle_2, ball, font, score_p1, score_p2, bg_image)

            if mode == "PVC":
                move_ai_paddle(paddle_2, ball, delta_time)
            else:
                paddle_2.top += paddle_2_move * delta_time
                paddle_2.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

            paddle_1.top += paddle_1_move * delta_time
            paddle_1.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

            ball.left += ball_accel_x * delta_time
            ball.top += ball_accel_y * delta_time

            if ball.left <= 0:
                score_p2 += 1
                winner = "Computer Won!" if mode == "PVC" else "Player 2 Won!"
                show_winner_screen(screen, font, winner)
                break
            if ball.right >= SCREEN_WIDTH:
                score_p1 += 1
                winner = "Player 1 Won!"
                show_winner_screen(screen, font, winner)
                break

            result = check_collisions(ball, paddle_1, paddle_2, ball_accel_x, ball_accel_y)
            if result == (None, None):
                show_game_over_screen(screen, font)
                break
            else:
                ball_accel_x, ball_accel_y = result

if __name__ == '__main__':
    main()
