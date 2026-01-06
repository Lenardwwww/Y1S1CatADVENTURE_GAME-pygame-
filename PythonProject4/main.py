# main.py
import pygame
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 导入模块
from constants import *
from src.entities.cat import Cat
from src.entities.platform import Platform
from src.ui.dialogue_box import DialogueBox
from src.ui.font_manager import font_manager
from src.ui.hint_system import HintSystem
from src.games.tic_tac_toe import TtkTicTacToe

# 检查并导入新增模块
try:
    from src.world.background import StrictBackground
    from src.world.camera import Camera
except ImportError as e:
    print(f"✗ 导入背景或相机失败: {e}")
    sys.exit(1)

# 尝试导入前景层和全屏对话框
try:
    from src.world.foreground_layer import ForegroundLayer

    print("✓ 成功导入前景层")
except ImportError as e:
    print(f"✗ 导入前景层失败: {e}")


    # 创建一个空类以便程序继续运行
    class ForegroundLayer:
        def __init__(self, *args, **kwargs):
            self.foreground_objects = []

        def add_foreground(self, *args, **kwargs): pass

        def draw(self, *args, **kwargs): pass

        def toggle_debug(self, *args, **kwargs): pass

try:
    from src.ui.fullscreen_dialogue import FullscreenDialogue

    print("✓ 成功导入全屏对话框")
except ImportError as e:
    print(f"✗ 导入全屏对话框失败: {e}")


    # 创建一个空类以便程序继续运行
    class FullscreenDialogue:
        def __init__(self, *args, **kwargs):
            self.trigger_areas = []
            self.active = False

        def check_triggers(self, *args, **kwargs): return None

        def show(self, *args, **kwargs): return False

        def hide(self, *args, **kwargs): pass

        def update(self, *args, **kwargs): pass

        def draw(self, *args, **kwargs): pass


def initialize_pygame():
    """初始化Pygame"""
    pygame.init()
    pygame.font.init()  # 初始化字体模块
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)  # 初始化音频模块

    # 创建字体（加载主字体）
    try:
        # 加载各种大小的字体
        FONT_SMALL_OBJ = font_manager.get_font(FONT_SMALL)
        FONT_MEDIUM_OBJ = font_manager.get_font(FONT_MEDIUM)
        FONT_LARGE_OBJ = font_manager.get_font(FONT_LARGE)
        FONT_XLARGE_OBJ = font_manager.get_font(FONT_XLARGE)
        FONT_XXLARGE_OBJ = font_manager.get_font(FONT_XXLARGE)
        print("✓ 字体加载完成")
    except Exception as e:
        print(f"✗ 字体加载失败: {e}")
        print("将使用系统默认字体")
        FONT_SMALL_OBJ = pygame.font.SysFont("Arial", FONT_SMALL)
        FONT_MEDIUM_OBJ = pygame.font.SysFont("Arial", FONT_MEDIUM)
        FONT_LARGE_OBJ = pygame.font.SysFont("Arial", FONT_LARGE)
        FONT_XLARGE_OBJ = pygame.font.SysFont("Arial", FONT_XLARGE)
        FONT_XXLARGE_OBJ = pygame.font.SysFont("Arial", FONT_XXLARGE)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("上烟囱")

    # 将字体对象存储在全局变量中
    global FONTS
    FONTS = {
        'small': FONT_SMALL_OBJ,
        'medium': FONT_MEDIUM_OBJ,
        'large': FONT_LARGE_OBJ,
        'xlarge': FONT_XLARGE_OBJ,
        'xxlarge': FONT_XXLARGE_OBJ
    }
    return screen


def load_menu_resources():
    """加载菜单和CG资源"""
    resources = {}

    # 尝试加载初始界面背景
    bg_path = "assets/images/ui/title_bg.png"
    if os.path.exists(bg_path):
        try:
            resources['title_bg'] = pygame.image.load(bg_path).convert()
            resources['title_bg'] = pygame.transform.scale(resources['title_bg'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            print("✓ 加载初始界面背景")
        except Exception as e:
            print(f"✗ 加载初始界面背景失败: {e}")
            resources['title_bg'] = create_default_background()
    else:
        print("⚠ 初始界面背景图片不存在: assets/images/ui/title_bg.png")
        resources['title_bg'] = create_default_background()

    # 尝试加载开始CG
    cg_paths = [
        ("start_cg1", "assets/images/ui/start_cg1.png"),
        ("start_cg2", "assets/images/ui/start_cg2.png")
    ]

    for name, path in cg_paths:
        if os.path.exists(path):
            try:
                resources[name] = pygame.image.load(path).convert()
                resources[name] = pygame.transform.scale(resources[name], (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"✓ 加载CG: {name}")
            except Exception as e:
                print(f"✗ 加载CG失败 {name}: {e}")
                resources[name] = create_default_cg(name)
        else:
            print(f"⚠ CG图片不存在: {path}")
            resources[name] = create_default_cg(name)

    return resources


def create_default_background():
    """创建默认背景"""
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill((69, 54, 64))  # 使用游戏主题色
    return surface


def create_default_cg(name):
    """创建默认CG"""
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    if name == "start_cg1":
        surface.fill((80, 60, 70))
    else:  # start_cg2
        surface.fill((70, 60, 80))

    # 添加文字说明
    font = font_manager.get_font(32, bold=True)
    text = font.render(f"这是 {name} 的占位图", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(text, text_rect)

    return surface


def initialize_bgm():
    """初始化并播放背景音乐"""
    if os.path.exists(BGM_PATH):
        try:
            pygame.mixer.music.load(BGM_PATH)
            # 设置初始音量30%
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # -1表示循环播放
            print("✓ 背景音乐开始播放，音量: 30%")
            return True
        except Exception as e:
            print(f"✗ 播放背景音乐失败: {e}")
            return False
    else:
        print(f"⚠ 背景音乐文件不存在: {BGM_PATH}")
        return False


def adjust_bgm_volume(delta):
    """调整BGM音量"""
    current_volume = pygame.mixer.music.get_volume()
    new_volume = current_volume + delta
    # 限制音量在0.0到1.0之间
    new_volume = max(0.0, min(1.0, new_volume))
    pygame.mixer.music.set_volume(new_volume)
    # 不显示文字提示，只打印调试信息
    print(f"BGM音量调整为: {int(new_volume * 100)}%")


def create_game_objects():
    """创建游戏对象"""
    print("\n" + "=" * 60)

    # 创建相机
    camera = Camera(WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

    # 创建小猫（如果图片不存在会退出）
    cat = Cat(200, 560)

    # 创建背景（如果图片不存在会退出）
    bg_image_path = "assets/images/backgrounds/backgrounds.png"
    background = StrictBackground(bg_image_path, WORLD_WIDTH, WORLD_HEIGHT)

    # 创建前景层
    foreground_layer = ForegroundLayer(WORLD_WIDTH, WORLD_HEIGHT)

    # 创建平台
    platforms = create_platforms()

    # 创建前景对象（特别注意myforeground.png缩放7倍）
    create_foregrounds(foreground_layer)

    # 创建UI
    print("创建UI元素...")
    dialogue_box = DialogueBox()
    hint_system = HintSystem()

    # 创建全屏对话框系统（新增）
    print("创建全屏对话框系统...")
    fullscreen_dialogue = FullscreenDialogue(SCREEN_WIDTH, SCREEN_HEIGHT)

    # 创建井字棋游戏
    print("创建井字棋游戏...")
    ttk_game = TtkTicTacToe(SCREEN_WIDTH, SCREEN_HEIGHT, font_manager)

    print("✓ 所有游戏对象创建完成")
    print("=" * 60)

    return {
        'camera': camera,
        'cat': cat,
        'background': background,
        'foreground_layer': foreground_layer,
        'platforms': platforms,
        'dialogue_box': dialogue_box,
        'hint_system': hint_system,
        'fullscreen_dialogue': fullscreen_dialogue,
        'ttk_game': ttk_game  # 井字棋游戏
    }


def create_platforms():
    """创建平台"""
    platforms = [
        # 地面平台
        Platform(0, 560, WORLD_WIDTH, 7, PLATFORM_COLORS['ground']),
        # 障碍物
        Platform(1176, 448, 49, 112, PLATFORM_COLORS['stone']),
        # 跳跃平台
        Platform(1827, 406, 238, 7, PLATFORM_COLORS['grass']),
        Platform(2070, 259, 294, 14, PLATFORM_COLORS['grass']),
        Platform(2338, 133, 182, 56, PLATFORM_COLORS['grass']),
        Platform(2373, 350, 126, 42, PLATFORM_COLORS['grass']),
        Platform(3339, 413, 224, 21, PLATFORM_COLORS['grass']),
        Platform(3500, 301, 315, 35, PLATFORM_COLORS['grass']),
        Platform(3710, 413, 231, 21, PLATFORM_COLORS['grass']),
        Platform(4585, 448, 133, 112, PLATFORM_COLORS['grass']),
        Platform(4767, 329, 315, 231, PLATFORM_COLORS['grass']),
        Platform(5103, 413, 63, 147, PLATFORM_COLORS['grass']),
        Platform(5509, 490, 35, 70, PLATFORM_COLORS['grass']),
        Platform(5551, 357, 49, 196, PLATFORM_COLORS['grass']),
        Platform(5600, 154, 84, 399, PLATFORM_COLORS['grass']),
    ]
    return platforms


def create_foregrounds(foreground_layer):
    """创建前景对象"""
    # 检查前景图片目录是否存在
    if not os.path.exists(FOREGROUND_DIR):
        print(f"✗ 前景图片目录不存在: {FOREGROUND_DIR}")
        return

    # 特别注意：myforeground.png需要缩放7倍
    myforeground_path = os.path.join(FOREGROUND_DIR, "myforeground.png")
    if os.path.exists(myforeground_path):
        foreground_layer.add_foreground(
            image_path=myforeground_path,
            x=0,  # 世界坐标X
            y=0,  # 世界坐标Y
            scale=7.0,  # 缩放7倍
            alpha=255
        )
    else:
        print(f"⚠ 未找到myforeground.png: {myforeground_path}")

    print(f"✓ 已创建 {len(foreground_layer.foreground_objects)} 个前景对象")


def draw_main_menu(screen, resources):
    """绘制初始界面"""
    # 绘制背景
    screen.blit(resources['title_bg'], (0, 0))

    # 绘制"上烟囱"标题
    title_font = font_manager.get_font(72, bold=True)
    title = title_font.render(TITLE_TEXT, True, TITLE_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title, title_rect)

    # 绘制"开始"按钮
    button_font = font_manager.get_font(36)
    button_text = button_font.render(START_BUTTON_TEXT, True, BUTTON_TEXT_COLOR)
    button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    # 按钮背景（根据鼠标悬停状态改变颜色）
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        button_color = BUTTON_HOVER_COLOR
        # 改变鼠标光标
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        button_color = BUTTON_NORMAL_COLOR
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # 绘制按钮背景
    pygame.draw.rect(screen, button_color, button_rect.inflate(30, 20), border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect.inflate(30, 20), 3, border_radius=10)

    # 绘制按钮文字
    screen.blit(button_text, button_rect)

    # 绘制提示
    hint_font = font_manager.get_font(18)
    hint_text = hint_font.render(HINT_TEXT, True, (200, 200, 200))
    screen.blit(hint_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

    return button_rect


def draw_start_cg(screen, resources, cg_num):
    """绘制开始CG"""
    cg_key = f"start_cg{cg_num}"
    screen.blit(resources[cg_key], (0, 0))

    # 显示跳过提示
    hint_font = font_manager.get_font(20)
    hint_text = hint_font.render(SKIP_HINT_TEXT, True, SKIP_HINT_COLOR)
    hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))

    # 半透明背景
    bg_surface = pygame.Surface((hint_rect.width + 20, hint_rect.height + 10), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 128))
    screen.blit(bg_surface, (hint_rect.left - 10, hint_rect.top - 5))
    screen.blit(hint_text, hint_rect)


def main():
    """游戏主循环"""
    screen = initialize_pygame()
    clock = pygame.time.Clock()

    # 初始化并播放背景音乐
    bgm_loaded = initialize_bgm()

    # 加载菜单资源
    print("加载菜单资源...")
    menu_resources = load_menu_resources()

    # 创建游戏对象
    game_objects = create_game_objects()
    camera = game_objects['camera']
    cat = game_objects['cat']
    background = game_objects['background']
    foreground_layer = game_objects['foreground_layer']
    platforms = game_objects['platforms']
    dialogue_box = game_objects['dialogue_box']
    hint_system = game_objects['hint_system']
    fullscreen_dialogue = game_objects['fullscreen_dialogue']
    ttk_game = game_objects['ttk_game']  # 井字棋游戏

    # 游戏状态
    game_state = GAME_STATE_MAIN_MENU  # 初始状态为菜单
    running = True

    # CG播放相关
    cg_timer = 0
    current_cg = 1

    # 调试模式控制
    show_trigger_areas = True  # 显示对话框触发区域

    print("\n游戏开始！")
    print("当前状态: 初始菜单")
    print("控制: A/D 移动, 空格跳跃, E 交互, ESC 退出")
    print("提示: 靠近指定坐标按E键触发对话，按F键开始井字棋")
    print("音量控制: +/- 键调节BGM音量")

    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 音量控制事件（适用于所有游戏状态）
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    # 增大音量（+键）
                    adjust_bgm_volume(0.1)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    # 减小音量（-键）
                    adjust_bgm_volume(-0.1)

            # 根据游戏状态处理事件
            if game_state == GAME_STATE_MAIN_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 检查是否点击了开始按钮
                    start_button_rect = draw_main_menu(screen, menu_resources)
                    if start_button_rect.collidepoint(event.pos):
                        game_state = GAME_STATE_START_CG1
                        cg_timer = 0
                        print("进入开始CG1")

            elif game_state == GAME_STATE_START_CG1:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    # 跳过第一张CG，进入第二张
                    game_state = GAME_STATE_START_CG2
                    cg_timer = 0
                    print("进入开始CG2")

            elif game_state == GAME_STATE_START_CG2:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    # 跳过第二张CG，进入游戏
                    game_state = GAME_STATE_PLAYING
                    print("进入游戏")

            elif game_state == GAME_STATE_FULLSCREEN_DIALOGUE:
                # 全屏对话框状态下的按键处理
                result = fullscreen_dialogue.handle_key_event(event)
                if result == "exit":
                    game_state = GAME_STATE_PLAYING
                    print("退出对话框，恢复游戏")
                elif result == "start_tic_tac_toe":
                    game_state = GAME_STATE_TTT_GAME
                    print("进入井字棋游戏")
                elif result == "exit_dialogue":
                    game_state = GAME_STATE_PLAYING
                    print("退出对话，恢复游戏")

            elif game_state == GAME_STATE_TTT_GAME:

                # 井字棋状态下的按键处理
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # 退出井字棋
                        game_state = GAME_STATE_PLAYING
                        print("退出井字棋游戏")

                        # 根据游戏结果决定下一步
                        if ttk_game.ttk_winner == "doll":
                            # 玩家输了，显示mydialogue2，猫头像切换为head3
                            fullscreen_dialogue.show("mydialogue2")
                            # 设置猫猫状态为cat_head3
                            cat.set_head_state("cat_head3")
                            # 更新对话系统的猫猫状态
                            fullscreen_dialogue.set_cat_head_state("cat_head3")
                            game_state = GAME_STATE_FULLSCREEN_DIALOGUE
                            print("玩家输了，显示mydialogue2，猫头像切换为head3")
                        elif ttk_game.ttk_winner == "player":
                            # 玩家赢了，显示mydialogue3
                            fullscreen_dialogue.show("mydialogue3")
                            game_state = GAME_STATE_FULLSCREEN_DIALOGUE
                            print("玩家赢了，显示mydialogue3")
                        elif ttk_game.ttk_winner == "draw":
                            # 平局，回到游戏
                            print("井字棋平局")

                        # 重置井字棋游戏
                        ttk_game.ttk_reset_game()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 鼠标左键点击
                    if ttk_game.ttk_handle_click(event.pos):
                        print("玩家落子")

            elif game_state == GAME_STATE_PLAYING:
                # 正常游戏状态
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_F2:
                        show_trigger_areas = not show_trigger_areas
                        print(f"触发区域显示: {'开启' if show_trigger_areas else '关闭'}")
                    elif event.key == pygame.K_e:
                        # 检查是否触发全屏对话框
                        triggered_dialogue = fullscreen_dialogue.check_triggers(
                            cat.x, cat.y, 40, 40
                        )
                        if triggered_dialogue:
                            print(f"触发对话框: {triggered_dialogue}")

                            # 如果是特殊CG序列，显示序列
                            if triggered_dialogue == "special_cg":
                                if fullscreen_dialogue.show("special_cg"):
                                    game_state = GAME_STATE_FULLSCREEN_DIALOGUE
                                    print(f"进入特殊CG序列播放")
                            else:
                                # 普通单个对话
                                if fullscreen_dialogue.show(triggered_dialogue):
                                    game_state = GAME_STATE_FULLSCREEN_DIALOGUE
                                    print(f"进入全屏对话框模式: {triggered_dialogue}")
                        else:
                            print(f"未触发对话框，小猫位置: ({cat.x}, {cat.y})")

        # 更新游戏状态
        if game_state == GAME_STATE_START_CG1 or game_state == GAME_STATE_START_CG2:
            # CG播放计时
            cg_timer += dt
            if cg_timer >= CG_DURATION:
                # 自动切换到下一张CG或游戏
                if game_state == GAME_STATE_START_CG1:
                    game_state = GAME_STATE_START_CG2
                    cg_timer = 0

                    print("自动切换到CG2")
                elif game_state == GAME_STATE_START_CG2:
                    game_state = GAME_STATE_PLAYING
                    print("自动进入游戏")

        elif game_state == GAME_STATE_PLAYING:
            # 正常游戏更新
            keys = pygame.key.get_pressed()
            cat.update(keys, platforms, dt)
            camera.update(cat.x, cat.y)
            hint_system.update(dt)

        elif game_state == GAME_STATE_FULLSCREEN_DIALOGUE:
            # 在全屏对话框模式下，小猫不能移动
            # 但可以更新对话框的动画等
            fullscreen_dialogue.update()
            # 注意：不更新小猫位置和相机

        elif game_state == GAME_STATE_TTT_GAME:
            # 井字棋游戏更新
            ttk_game.ttk_update()

        # 绘制游戏
        if game_state == GAME_STATE_MAIN_MENU:
            # 绘制初始界面
            draw_main_menu(screen, menu_resources)

        elif game_state == GAME_STATE_START_CG1:
            # 绘制第一张CG
            draw_start_cg(screen, menu_resources, 1)

        elif game_state == GAME_STATE_START_CG2:
            # 绘制第二张CG
            draw_start_cg(screen, menu_resources, 2)

        elif game_state == GAME_STATE_PLAYING:
            # 1. 绘制背景（最底层）
            background.draw(screen, camera.x)

            # 2. 绘制平台
            for platform in platforms:
                platform.draw(screen, camera)

            # 3. 绘制猫猫
            cat.draw(screen, camera)

            # 4. 绘制前景（覆盖在猫猫和平台之上）
            if hasattr(foreground_layer, 'foreground_objects') and len(foreground_layer.foreground_objects) > 0:
                foreground_layer.draw(screen, camera.x)

            # 5. 绘制对话框触发区域（调试用）

            # 6. 绘制UI（文字对话框和提示系统）
            dialogue_box.draw(screen)
            hint_system.draw(screen)

            # 7. 绘制游戏信息（帧率、位置等）
            # 显示帧率
            fps_text = FONTS['small'].render(f"FPS: {int(clock.get_fps())}", True, WHITE)
            screen.blit(fps_text, (10, 10))

            # 显示位置信息
            pos_text = FONTS['small'].render(f"位置: ({int(cat.x)}, {int(cat.y)})", True, WHITE)
            screen.blit(pos_text, (10, 40))

            # 显示相机位置
            cam_text = FONTS['small'].render(f"相机: {int(camera.x)}", True, WHITE)
            screen.blit(cam_text, (10, 70))

            # 显示游戏状态
            state_colors = {
                GAME_STATE_PLAYING: WHITE,
                GAME_STATE_FULLSCREEN_DIALOGUE: (255, 255, 100),
                GAME_STATE_TTT_GAME: (100, 255, 100)
            }
            state_text = FONTS['small'].render(f"状态: {game_state}", True,
                                               state_colors.get(game_state, WHITE))
            screen.blit(state_text, (10, 100))

            # 显示游戏标题
            title_text = FONTS['xlarge'].render("小猫探险：上烟囱", True, (69, 54, 64))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - 150, 10))

            # 显示控制提示（根据游戏状态显示不同的提示）
            controls_text = FONTS['small'].render("控制: A/D移动 空格跳跃 E交互 ESC退出 ", True,
                                                  (69, 54, 64))
            screen.blit(controls_text, (SCREEN_WIDTH // 2 - 168, 50))

            # 如果猫猫在触发区域附近，显示提示
            triggered = fullscreen_dialogue.check_triggers(cat.x, cat.y)
            if triggered:
                hint_text = FONTS['medium'].render(f"按 E 键交互！！！", True, (112, 171, 133))
                screen.blit(hint_text, (SCREEN_WIDTH // 2 - 100, 80))

            # 如果猫猫在小院区域，显示提示
            if 2284 < cat.x < 3000:
                yard_text = FONTS['large'].render("神秘小院", True, (112,171,133))
                screen.blit(yard_text, (SCREEN_WIDTH // 2 - 50, 80))

        elif game_state == GAME_STATE_FULLSCREEN_DIALOGUE:
            # 绘制全屏对话框
            fullscreen_dialogue.draw(screen)

        elif game_state == GAME_STATE_TTT_GAME:
            # 绘制井字棋游戏
            background.draw(screen, camera.x)

            # 2. 绘制平台
            for platform in platforms:
                platform.draw(screen, camera)

            # 3. 绘制猫猫
            cat.draw(screen, camera)

            # 4. 绘制前景（覆盖在猫猫和平台之上）
            if hasattr(foreground_layer, 'foreground_objects') and len(foreground_layer.foreground_objects) > 0:
                foreground_layer.draw(screen, camera.x)
            ttk_game.ttk_draw(screen)

        # 更新显示
        pygame.display.flip()

    # 游戏退出时停止音乐
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()