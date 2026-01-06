"""
游戏常量定义
"""
# constants.py
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 资源路径
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'audio')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
# 前景目录
FOREGROUND_DIR = os.path.join(IMAGES_DIR, 'foregrounds')
# 对话框目录
DIALOGUES_DIR = os.path.join(IMAGES_DIR, 'dialogues')

# 字体文件名常量（新增）
FONT_FILE = "myfont.ttf"  # 您的字体文件名
FONT_PATH = os.path.join(FONTS_DIR, FONT_FILE)

# 字体大小常量（新增）
FONT_SMALL = 16
FONT_MEDIUM = 20
FONT_LARGE = 24
FONT_XLARGE = 32
FONT_XXLARGE = 36
# 窗口设置
SCREEN_WIDTH = 1225
SCREEN_HEIGHT = 700
FPS = 60
WINDOW_TITLE = "小猫探险 - 烟囱之谜"
FULLSCREEN = False

# 世界设置
WORLD_WIDTH = 7000
WORLD_HEIGHT = 700
GRAVITY = 0.6
#MAX_FALL_SPEED = 15

# 小猫属性
CAT_WIDTH = 140  # 小猫宽度（像素）
CAT_HEIGHT = 112  # 小猫高度（像素）
CAT_SPEED = 8  # 移动速度（没有加速，直接速度）
CAT_JUMP_POWER = -15  # 跳跃力量
CAT_GRAVITY = 0.7  # 重力
MAX_FALL_SPEED = 20  # 最大下落速度

# 平台属性
PLATFORM_HEIGHT = 10
PLATFORM_COLORS = {
    'ground': (112, 171, 133),
    'stone': (100, 100, 100),
    'wood': (160, 120, 80),
    'grass': (69, 54, 64)
}

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (100, 149, 237)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 182, 193)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# UI设置
DIALOGUE_BOX_HEIGHT = 150
DIALOGUE_TEXT_SPEED = 3  # 字符/帧
BUTTON_HOVER_COLOR = (200, 200, 255)
BUTTON_NORMAL_COLOR = (150, 150, 200)

# 相机设置
CAMERA_SMOOTHNESS = 0.2
CAMERA_DEADZONE = 25
CAMERA_VERTICAL_FOLLOW = False

# 游戏状态
STATE_MAIN_MENU = 0
STATE_GAME_OVER = 3
STATE_VICTORY = 4

# 游戏状态常量
STATE_PLAYING = "playing"
STATE_DIALOGUE = "dialogue"
STATE_FULLSCREEN_DIALOGUE = "fullscreen_dialogue"
STATE_PAUSED = "paused"
# 在原有文件末尾添加以下内容（不要修改原有代码）

# ==============================================
# 新增常量（仅添加，不修改原有内容）
# ==============================================

# 音频路径
BGM_PATH = "assets/audio/bgm/main_theme.mp3"

# 游戏状态常量
GAME_STATE_MAIN_MENU = "main_menu"
GAME_STATE_START_CG1 = "start_cg1"
GAME_STATE_START_CG2 = "start_cg2"
GAME_STATE_PLAYING = "playing"
GAME_STATE_FULLSCREEN_DIALOGUE = "fullscreen_dialogue"
GAME_STATE_TTT_GAME = "ttk_tic_tac_toe"

# CG持续时间（秒）
CG_DURATION = 3.0

# 对话框按键映射
DIALOGUE_KEYS = {
    'start_ttk': 'F',  # 开始井字棋
    'exit': 'ESC',     # 退出对话
    'next': 'D',       # 继续/下一步
    'close': 'ESC',    # 关闭对话框
}

# 初始界面配置
TITLE_TEXT = " "
START_BUTTON_TEXT = "开始游戏"
HINT_TEXT = "点击'开始游戏'进入冒险"

# 界面颜色（你可以根据喜好调整）
TITLE_COLOR = (255, 223, 186)      # 暖黄色
#BUTTON_NORMAL_COLOR = (69, 54, 64)   # 深褐色
#BUTTON_HOVER_COLOR = (112, 171, 133) # 绿色
BUTTON_BORDER_COLOR = (255, 223, 186) # 暖黄色边框
BUTTON_TEXT_COLOR = (255, 255, 255)   # 白色

# CG跳过提示
SKIP_HINT_TEXT = "点击跳过或等待3秒..."
SKIP_HINT_COLOR = (255, 255, 255)