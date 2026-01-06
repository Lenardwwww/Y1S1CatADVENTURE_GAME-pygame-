# src/entities/cat.py
"""
小猫类 - 游戏主角（特定动画规则）
水平移动：显示cat_head1
跳跃/站立：显示cat_head
"""
import pygame
import sys
from constants import *
from src.ui.font_manager import font_manager  # 导入字体管理器


class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = CAT_WIDTH
        self.height = CAT_HEIGHT
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = 1  # 1=右, -1=左
        self.jumping = False
        self.on_ground = False
        self.screen_x = SCREEN_WIDTH // 2

        # 动画相关属性
        self.current_image = None  # 当前显示的图片
        self.images = {}  # 存储所有加载的图片

        # 新增：猫猫头像状态
        self.head_state = "normal"  # normal, cat_head3
        self.head_state_changed = False  # 状态是否改变

        # 气泡图片相关
        self.bubble_image = None  # 气泡图片
        self.bubble_width = 104  # 气泡宽度
        self.bubble_height = 56  # 气泡高度
        self.bubble_scale = 1.0  # 气泡缩放比例

        # 强制加载小猫图片和气泡图片
        self.load_images()

        # 交互相关
        self.near_object = None
        self.near_character = None
        self.thought_bubble = ""
        self.thought_timer = 0
        self.dialogue_active = False

        # 状态
        self.health = 100
        self.inventory = []

        # 字体相关（仅用于交互提示）
        self.prompt_font = font_manager.get_font(22)  # 提示字体
        self.debug_font = font_manager.get_font(16)  # 调试字体

    def load_images(self):
        """强制加载小猫图片和气泡图片"""
        # 定义要加载的小猫图片
        cat_image_files = ["cat_head.png", "cat_head1.png", "cat_head3.png"]

        # 气泡图片
        bubble_image_files = ["bubblecat.png"]

        # 尝试多个可能的路径前缀
        possible_paths = [
            "assets/images/characters/cat/",
            "assets/images/cat/",
            ""
        ]

        all_cat_images_loaded = True

        # 加载小猫图片
        for filename in cat_image_files:
            print(f"\n尝试加载小猫图片: {filename}")
            image_loaded = False

            for base_path in possible_paths:
                image_path = os.path.join(base_path, filename)

                if os.path.exists(image_path):
                    try:
                        # 加载图片
                        img = pygame.image.load(image_path).convert_alpha()

                        # 缩放图片到游戏尺寸
                        img = pygame.transform.scale(img, (self.width, self.height))
                        print(f"  ✓ {filename} 已缩放为 {self.width}x{self.height}")

                        # 存储图片
                        self.images[filename] = img
                        image_loaded = True
                        break

                    except Exception as e:
                        print(f"  ✗ 无法加载 {filename}: {e}")

            if not image_loaded:
                print(f"  ✗ 未找到图片: {filename}")
                all_cat_images_loaded = False

        # 如果任何必需小猫图片缺失，游戏无法运行
        if not all_cat_images_loaded:
            print("\n游戏无法运行，按任意键退出...")
            input()
            sys.exit(1)

        # 创建镜像版本
        self.create_mirrored_images()

        # 设置默认图片
        self.current_image = self.images["cat_head.png"]
        self.current_mirrored_image = self.mirrored_images["cat_head.png"]

        print(f"\n✅ 小猫图片加载完成:")
        for filename, img in self.images.items():
            print(f"  {filename}: {img.get_width()}x{img.get_height()}")

        # 加载气泡图片（不是必需的）
        self.load_bubble_image(possible_paths)

    def load_bubble_image(self, possible_paths):
        """加载气泡图片（如果存在）"""
        print("\n尝试加载气泡图片: bubblecat.png")

        for base_path in possible_paths:
            bubble_path = os.path.join(base_path, "bubblecat.png")

            if os.path.exists(bubble_path):
                try:
                    # 加载气泡图片
                    self.bubble_image = pygame.image.load(bubble_path).convert_alpha()

                    # 缩放气泡图片到指定大小
                    if self.bubble_width and self.bubble_height:
                        self.bubble_image = pygame.transform.scale(
                            self.bubble_image,
                            (self.bubble_width, self.bubble_height)
                        )
                        print(f"  ✓ 气泡图片已加载，缩放为 {self.bubble_width}x{self.bubble_height}")
                    else:
                        print(
                            f"  ✓ 气泡图片已加载，原始尺寸: {self.bubble_image.get_width()}x{self.bubble_image.get_height()}")

                    print(f"  气泡图片路径: {bubble_path}")
                    return

                except Exception as e:
                    print(f"  ✗ 无法加载气泡图片: {e}")
                    self.bubble_image = None

        print("  ⚠ 未找到气泡图片 bubblecat.png，将不显示气泡")
        print("  气泡图片是可选的，游戏仍可正常运行")

    def set_bubble_size(self, width, height):
        """设置气泡图片大小"""
        self.bubble_width = width
        self.bubble_height = height

        # 如果气泡图片已加载，重新缩放
        if self.bubble_image:
            # 重新加载原始图片再缩放
            for base_path in ["assets/images/characters/cat/", "assets/images/cat/", ""]:
                bubble_path = os.path.join(base_path, "bubblecat.png")
                if os.path.exists(bubble_path):
                    try:
                        original_bubble = pygame.image.load(bubble_path).convert_alpha()
                        self.bubble_image = pygame.transform.scale(
                            original_bubble,
                            (self.bubble_width, self.bubble_height)
                        )
                        print(f"气泡图片重新缩放为: {self.bubble_width}x{self.bubble_height}")
                        break
                    except Exception as e:
                        print(f"重新缩放气泡图片失败: {e}")

    def create_mirrored_images(self):
        """为所有图片创建镜像版本（用于向左移动）"""
        self.mirrored_images = {}

        for filename, img in self.images.items():
            mirrored_img = pygame.transform.flip(img, True, False)
            self.mirrored_images[filename] = mirrored_img

        print("✅ 已创建所有图片的镜像版本")

    def update(self, keys, platforms, dt):
        """更新小猫状态和图片选择"""
        self.handle_input(keys)
        self.apply_physics(dt)
        self.check_collisions(platforms)
        self.update_head_state()
        self.update_thought_bubble(dt)

    def update_head_state(self):
        """根据head_state选择对应的图片"""
        if self.head_state == "cat_head3" and self.head_state_changed:
            # 切换到cat_head3
            if "cat_head3.png" in self.images:
                self.current_image = self.images["cat_head3.png"]
                self.current_mirrored_image = self.mirrored_images["cat_head3.png"]
                self.head_state_changed = False
                print("猫猫头像已切换为cat_head3")
        elif self.head_state == "normal":
            # 正常状态，根据动作选择图片
            if not self.on_ground:
                # 跳跃或下落状态，使用cat_head.png
                image_name = "cat_head.png"
            elif abs(self.velocity_x) > 0.1:
                # 在地面上且水平移动，使用cat_head1.png
                image_name = "cat_head1.png"
            else:
                # 在地面上且静止，使用cat_head.png
                image_name = "cat_head.png"

            # 更新当前图片
            if image_name in self.images:
                self.current_image = self.images[image_name]
                self.current_mirrored_image = self.mirrored_images[image_name]

    def set_head_state(self, state):
        """设置猫猫头像状态"""
        if state != self.head_state:
            self.head_state = state
            self.head_state_changed = True
            print(f"猫猫头像状态设置为: {state}")

    def handle_input(self, keys):
        # 水平移动 - 直接设置速度
        move_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        move_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        if move_left and not move_right:
            self.velocity_x = -CAT_SPEED
            self.direction = -1
        elif move_right and not move_left:
            self.velocity_x = CAT_SPEED
            self.direction = 1
        else:
            # 松开按键立即停止
            self.velocity_x = 0

        # 跳跃
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = CAT_JUMP_POWER
            self.on_ground = False
            self.jumping = True
            self.thought_bubble = "起飞！"
            self.thought_timer = 1.0  # 1秒

    def apply_physics(self, dt):
        """应用物理效果"""
        # 重力
        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, MAX_FALL_SPEED)

        # 更新位置
        self.x += self.velocity_x
        self.y += self.velocity_y

        # 边界检查
        self.x = max(0, min(self.x, WORLD_WIDTH - self.width))

        # 如果掉落到底部，重置位置
        if self.y > SCREEN_HEIGHT:
            self.y = 100
            self.x = 100
            self.velocity_y = 0
            self.thought_bubble = "哎呀，掉出去了！"
            self.thought_timer = 2.0

    def check_collisions(self, platforms):
        """检查与平台的碰撞 - 修改为对空列表也安全"""
        self.on_ground = False

        # 如果平台列表为空，直接返回
        if not platforms:
            # 简单的地面检测
            if self.y >= SCREEN_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - self.height
                self.velocity_y = 0
                self.on_ground = True
                self.jumping = False
            return

        # 原来的碰撞检测逻辑
        for platform in platforms:
            if self.check_collision_with(platform):
                # 确定碰撞方向
                if self.velocity_y > 0:  # 下落中
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumping = False
                elif self.velocity_y < 0:  # 上升中
                    self.y = platform.y + platform.height
                    self.velocity_y = 0
                elif self.velocity_x > 0:  # 向右移动
                    self.x = platform.x - self.width
                elif self.velocity_x < 0:  # 向左移动
                    self.x = platform.x + platform.width

    def check_collision_with(self, platform):
        """检查与特定平台的碰撞"""
        return (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y)

    def update_thought_bubble(self, dt):
        """更新思考气泡"""
        if self.thought_timer > 0:
            self.thought_timer -= dt
            if self.thought_timer <= 0:
                self.thought_bubble = ""

    def draw(self, screen, camera):
        """绘制小猫 - 固定位置绘制"""
        # 小猫在屏幕上始终保持在这个位置
        draw_x = self.screen_x
        draw_y = int(self.y)  # 垂直方向仍然跟随

        # 选择正确的图片（根据方向）
        if self.direction == 1:
            current_image = self.current_image
        else:
            current_image = self.current_mirrored_image

        # 绘制小猫图片
        screen.blit(current_image, (draw_x, draw_y))

        # 绘制气泡图片（如果有气泡图片且需要显示气泡）
        if self.thought_bubble and self.bubble_image:
            self.draw_bubble_image(screen, draw_x, draw_y)

        # 绘制交互提示
        if (self.near_object or self.near_character) and not self.dialogue_active:
            self.draw_interaction_prompt(screen, draw_x, draw_y)

        # 调试信息（可选，按D键显示）
        if False:  # 可以改为True来启用调试信息
            self.draw_debug_info(screen, draw_x, draw_y)

    def draw_debug_info(self, screen, x, y):
        """绘制调试信息"""
        # 使用中文字体管理器获取字体
        font = self.debug_font

        # 确定当前使用的图片
        current_image_name = "未知"
        for name, img in self.images.items():
            if self.direction == 1 and img is self.current_image:
                current_image_name = name
                break
            elif self.direction == -1 and img is self.current_mirrored_image:
                current_image_name = f"{name} (镜像)"
                break

        info = [
            f"当前图片: {current_image_name}",
            f"状态: {'跳跃中' if not self.on_ground else ('移动中' if abs(self.velocity_x) > 0.1 else '站立中')}",
            f"速度: ({self.velocity_x:.1f}, {self.velocity_y:.1f})",
            f"方向: {'右' if self.direction == 1 else '左'}",
            f"在地面: {self.on_ground}",
            f"气泡: {'已加载' if self.bubble_image else '未加载'}",
            f"头像状态: {self.head_state}"  # 新增
        ]

        for i, text in enumerate(info):
            text_surface = font.render(text, True, (255, 255, 255))
            # 半透明背景
            pygame.draw.rect(screen, (0, 0, 0, 128),
                             (x, y + self.height + 5 + i * 15,
                              text_surface.get_width() + 5, text_surface.get_height()))
            screen.blit(text_surface, (x, y + self.height + 5 + i * 15))

    def draw_bubble_image(self, screen, x, y):
        """绘制气泡图片"""
        if not self.bubble_image:
            return

        # 计算气泡位置（在小猫上方）
        bubble_x = x + self.width // 2 - self.bubble_width // 2
        bubble_y = y - self.bubble_height - 10  # 10像素的间距

        # 绘制气泡图片
        screen.blit(self.bubble_image, (bubble_x, bubble_y))

    def draw_interaction_prompt(self, screen, x, y):
        """绘制交互提示（使用中文字体）"""
        prompt_text = "按 E 互动"
        text_surface = self.prompt_font.render(prompt_text, True, YELLOW)

        # 文字背景
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        pygame.draw.rect(screen, (0, 0, 0, 128),
                         (x + self.width // 2 - text_width // 2 - 5,
                          y - 40, text_width + 10, text_height + 5), 0, 3)

        # 绘制文字
        screen.blit(text_surface, (x + self.width // 2 - text_width // 2, y - 38))

    def get_rect(self):
        """获取小猫的矩形区域"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def set_thought(self, text, duration=2.0):
        """设置思考气泡文本和持续时间"""
        self.thought_bubble = text
        self.thought_timer = duration