# 게임 화면 크기와 보드 관련 상수
WIDTH, HEIGHT = 800, 800  # 창 크기
BOARD_SIZE = 15  # 15x15 오목판
CELL_SIZE = (WIDTH - 140) // BOARD_SIZE  # 각 칸의 크기
BOARD_PADDING = 70  # 보드 주변 여백

# 게임에서 사용할 색상들을 RGB로 정의
BACKGROUND = (246, 240, 230)     # 크림색 배경
BOARD_COLOR = (235, 200, 160)    # 나무색 보드
GRID_COLOR = (160, 126, 95)      # 격자선 색상
BLACK = (45, 45, 45)             # 검은 돌
WHITE = (250, 250, 250)          # 흰 돌
BUTTON_COLOR = (205, 175, 145)   # 버튼 색상
BUTTON_HOVER = (215, 185, 155)   # 버튼 호버 효과
TEXT_COLOR = (90, 77, 65)        # 텍스트 색상
STATUS_BAR_COLOR = (235, 225, 215)  # 상태바 배경
