import pygame
from random import *

from sqlalchemy import column
# 레벨에 맞게 설정


def setup(level):
    # 얼만동안 숫자를 보여줄지
    global display_time
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1)
    # 얼마나 많은 숫자를 보여줄 것인가?
    number_count = (level // 3) + 5
    number_count = min(number_count, 20)

    # 실제 화면에 grid 형태로 숫자를 랜덤으로 배치
    shuffle_grid(number_count)


def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130  # 각 그리드의 셀 별 가로, 세로 크기
    button_size = 110  # 그리드 셀 내에 실제로 그려질 버튼 크기
    screen_left_margin = 55  # 전체 스크린 왼쪽 여백
    screen_top_margin = 20

    grid = [[0 for col in range(columns)] for row in range(rows)]

    number = 1  # 시작숫자를 1로 설정
    while number <= number_count:
        row_idx = randrange(0, rows)
        col_idx = randrange(0, columns)

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number
            number += 1

            # 현재 grid cell 위치 기준으로 x, y 위치를 구함
            center_x = screen_left_margin + \
                (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + \
                (row_idx * cell_size) + (cell_size / 2)

            # 숫자 버튼 만들기
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)


def display_start_screen():  # 시작화면 보여주기
    # 어디에 그릴것인지, # 무슨 색으로 그릴것인지, # 스타트위치, # 반지름 길이, # 선의 두께
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)


def display_game_screen():
    global hidden
    if not hidden:
        elpased_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elpased_time > display_time:
            hidden = True
    for idx, rect in enumerate(number_buttons, start=1):
        if hidden:
            # 버튼 사각형 그리기
            pygame.draw.rect(screen, WHITE, rect)
        else:
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)


def check_buttons(pos):  # pos에 해당하는 버튼 확인
    global start, start_ticks

    if start:
        check_number_bottons(pos)
    # collidepoint는 위치를 확인하는 함수
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks()  # 타이머를 시작


def check_number_bottons(pos):
    global hidden, start, cur_level
    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]:
                print("Correct")
                del number_buttons[0]
                if not hidden:
                    hidden = True
            else:
                print("Wrong")
            break
    if len(number_buttons) == 0:
        start = False
        hidden = False
        cur_level += 1
        setup(cur_level)


def game_over():
    global running
    running = False
    msg = game_font.render(f"Your level is {cur_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)

    # 초기화
pygame.init()
screen_width = 1280  # 가로 길이
screen_height = 720  # 세로 길이
screen = pygame.display.set_mode((screen_width, screen_height))  # pygame 화면 세팅
# https://www.pygame.org/docs/ref/display.html#pygame.display.set_caption
pygame.display.set_caption("Memory Game")  # 프로그램이 실행되면 창 맨위에 써지는 멘트
game_font = pygame.font.Font(None, 120)  # 폰트 정의


# 시작 버튼
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

# 색깔
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

number_buttons = []  # 플레이어가 눌러야 하는
cur_level = 1
display_time = None  # 숫자를 보여주는 시간
start_ticks = None


# 게임 시작 여부
start = False
# 숫자 숨김 여부(사용자가 1을 클릭했거나, 보여주는 시간 초과했을 때)
hidden = False
# 게임 시작 전에 게임 설정 함수 수행
setup(cur_level)

# 게임 루프
# 사용자가 마우스랑 키보드를 사용하다가 게임 종료 조건이 되면 종료될 수 있도록 하는 코드
running = True  # 지금 게임이 실행중인가?
while running:
    click_pos = None

    # 이벤트 루프(사용자 행동을 지켜보는 곳)
    for event in pygame.event.get():  # 어떤 이벤트ㅏ 발생하였는가?
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트인가?
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()  # 클릭 좌표를 알 수 있는 함수
            print(click_pos)
    # 화면 전체를 까맣게 칠함
    screen.fill(BLACK)

    if start:
        display_game_screen()  # 게임 화면
    else:
        display_start_screen()  # 시작 화면

    # 사용자가 클릭한 좌표값이 있는 경우 : 즉, 어딘가 클릭한 경우
    if click_pos:
        check_buttons(click_pos)
    # 화면 업데이트
    pygame.display.update()

pygame.time.delay(5)

# 게임 종료
pygame.quit()
