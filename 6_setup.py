import pygame # 파이게임 라이브러리 사용 설정
from random import *

def setup(level):
    # 얼마동안 숫자를 보여줄지
    global display_time
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1) # 1초 미만이면 1초로 처리

    # 얼마나 많은 숫자를 보여줄 것인가?
    number_count = (level // 3) + 5 # //은 몫이다.
    number_count = min(number_count, 20) # 만약 20을 초과하면 20으로 처리

    # 실제 화면에 grid 형태로 숫자를 랜덤으로 배치
    shuffle_grid(number_count)

# 숫자 섞기( 이 프로젝트에서 가장 중요)
def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130 # 각 Grid cell 별 가로, 세로 크기
    button_size = 110 # Grid cell 내에 실제로 그려질 버튼 크기
    screen_left_margin = 55 # 전체 스크린 왼쪽 여백
    screen_top_margin = 20 # 전체 스크린 위쪽 여백

    #[0,0,0,0,0,0,0,0,0]
    grid = [[0 for col in range(columns)] for row in range(rows)] # 5 x 9

    number = 1 # 시작 숫자를 1부터 number_count 까지, 만약 5라면 5까지 숫자를 배치
    while number <= number_count:
        row_idx = randrange(0, rows) # 0, 1, 2, 3, 4 중에서 랜덤으로 뽑기
        col_idx = randrange(0, columns) # 0 ~ 8 중에서 랜덤으로 뽑기

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number # 숫자 지정
            number += 1

            # 현재 Grid cell 위치 기준으로 x, y 위치를 구한다.
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # 숫자 버튼 만들기
            button = pygame.Rect(0,0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)
    
    #배치된 랜덤 숫자 확인
    print(grid)

def display_start_screen(): # 시작 버튼 표시, 그리기
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5) # 흰색 동그라미를 그리고 중심좌표는 start_button 의 중심좌표를 따라가고, 반지름은 60, 두께는 5

    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(start_button.center))

    screen.blit(msg, msg_rect)

def display_game_screen(): # 게임 화면 표시
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_time > display_time:
            hidden = True

    for idx, rect in enumerate(number_buttons, start=1):
        if hidden:
            # 사각형 버튼 그리기
            pygame.draw.rect(screen, WHITE, rect)
        else:
            #숫자 텍스트
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center = rect.center)
            screen.blit(cell_text, text_rect)

# 마우스를 클릭해서 얻은 좌표값을 position에 저장 
def check_buttons(position): # 들어온 좌표 값 확인
    global start, start_ticks

    if start: # 게임이 시작했으면?
        check_number_buttons(position)
    elif start_button.collidepoint(position): # 마우스로 start_button의 범위에 해당하는 영역을 누른게 확인 될 때, collidepoint 충돌영역
        start = True #시작
        start_ticks = pygame.time.get_ticks() # 타이머 시작(현재시각 적용)

def check_number_buttons(position):
    global hidden, start ,curr_level

    for button in number_buttons:
        if button.collidepoint(position):
            if button == number_buttons[0]: # 올바른 숫자 클릭
                print("Correct")
                del number_buttons[0] # 앞에 있는 숫자를 지움
                if not hidden:
                    hidden = True # 숫자 숨김 처리
            else: # 잘못된 숫자 클릭
                game_over()
            break
    
    # 모든 숫자를 다 맞혔다면? 레벨을 높여서 다시 시작 화면으로 감
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level + 1)

# 게임 종료 처리, 메세지도 보여줌
def game_over():
    global running
    running = False

    msg = game_font.render(f"Your level is {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)

#초기화
pygame.init()
screen_width = 1280 #가로크기
screen_height = 720 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height)) # 게임 창 띄우기
pygame.display.set_caption("Brain Game") #게임 이름

#시작 버튼
center_x = 120 # 센터 x축
center_y = screen_height-120 # 센터 y축
start_button = pygame.Rect(0, 0, 120, 120) #버튼 생성
start_button.center = (center_x, center_y) # 버튼의 중심위치 설정
game_font = pygame.font.Font(None, 120) # 폰트 정의
start_font = pygame.font.Font(None,30) # 파이썬 기본폰트, 글자 크기는 30으로 설정

#화면색깔
BLACK = (0, 0, 0) #RGB
WHITE = (255, 255, 255) #RGB
GRAY = (50, 50, 50)

number_buttons = [] # 플레이어가 누르는 버튼 관리
curr_level = 1 # 현재 레벨
display_time = None # 시간을 보여주는 변수
start_ticks = None # 시간 계산 (현재 시간 정보를 저장)

# 게임 시작 여부
start = False # 초기에 게임을 시작하지 않았다고 설정
# 숫자 숨김 여부 (사용자가 1을 클릭했거나, 보여주는 시간을 초과했을 때)
hidden = False

# 게임 시작 전에 게임 설정 함수 수행
setup(1)

#게임 루프
running = True # 게임이 실행중인가?
while running:
    click_pos = None # null값 설정, 파이썬은 None으로 표현

    #이벤트루프
    for event in pygame.event.get(): #어떤 이벤트가 발생했는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트인가?
            running = False #게임이 더 이상 실행중이 아니다.
        elif event.type == pygame.MOUSEBUTTONUP: # 사용자가 마우스를 클릭했을때
            click_pos = pygame.mouse.get_pos() #마우스 좌표값 변수 설정
            print(click_pos) # 마우스 좌표값 출력

    #화면 전체를 까맣게 색칠
    screen.fill(BLACK) #fill은 채우다라는 뜻이다. 해석하면 검은색으로 스크린을 채워라는 뜻

    if start: # start 버튼을 눌렀으면, True 상태면
        display_game_screen() #게임 화면 표시

    else: # start 버튼을 누르지 않았으면
        display_start_screen()         # 시작 화면 표시

    if click_pos: #사용자가 클릭한 좌표값이 있다면
        check_buttons(click_pos) # 클릭한 좌표의 값을 확인해봄
    
    # 화면 업데이트
    pygame.display.update()

#5초 정도 보여줌
pygame.time.delay(5000)

#게임 종료
pygame.quit()
