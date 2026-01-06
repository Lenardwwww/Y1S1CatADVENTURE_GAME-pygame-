# src/ui/fullscreen_dialogue.py
import pygame
import os
from src.ui.font_manager import font_manager


class FullscreenDialogue:
    """极简全屏对话框 - Pygame会自动缩放图片"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dialogues = {}
        self.active = False
        self.current_dialogue = None
        self.current_dialogue_key = None

        # 对话序列管理（用于连续播放多个对话）
        self.dialogue_sequence = []  # 存储要连续播放的对话键列表
        self.sequence_index = 0  # 当前播放到序列中的第几个
        self.in_sequence = False  # 是否正在播放序列

        # 猫猫状态跟踪
        self.cat_head_state = "normal"  # normal, cat_head3

        # 触发区域
        self.trigger_areas = [
            # 原有的 mydialogue1（井字棋触发）
            (3752, 434, 154, 119, "mydialogue1"),

            # 新增：小鱼干奖励CG（需要条件检查cat_head3状态）
            (5285, 308, 301, 245, "mydialogue5"),

            # 新增：日记
            (812, 385, 189, 168, "mydialogue8"),

            # 新增：闹钟介绍娃娃
            (3374, 252, 189, 168, "mydialogue9"),

            # 新增：断线风筝
            (4074, 329, 280, 196, "mydialogue10"),

            # 新增：幸福壁画
            (4760, 154, 336, 168, "mydialogue11"),
        ]

        # 定义对话序列
        self.sequences = {
            "special_cg": ["mydialogue5", "mydialogue6", "mydialogue7"]  # 特殊CG连续播放
        }

        # 加载对话框图片
        self.load_dialogues()

    def set_cat_head_state(self, state):
        """设置猫猫头像状态"""
        self.cat_head_state = state
        print(f"对话系统：猫猫状态更新为: {state}")

    def load_dialogues(self):
        """加载所有对话框图片，Pygame会自动缩放到屏幕大小"""
        dialogues_dir = os.path.join("assets", "images", "dialogues")
        if not os.path.exists(dialogues_dir):
            print(f"✗ 对话框目录不存在: {dialogues_dir}")
            print("⚠ 使用默认对话框")
            self.create_default_dialogues()
            return

        # 要加载的对话框图片列表（包括所有新增的）
        dialogue_files = [
            "mydialogue1.png",
            "mydialogue2.png",
            "mydialogue3.png",
            "mydialogue5.png",  # 新增
            "mydialogue6.png",  # 新增
            "mydialogue7.png",  # 新增
            "mydialogue8.png",  # 新增
            "mydialogue9.png",  # 新增
            "mydialogue10.png",  # 新增
            "mydialogue11.png",  # 新增
        ]

        for filename in dialogue_files:
            dialogue_path = os.path.join(dialogues_dir, filename)

            if os.path.exists(dialogue_path):
                try:
                    # 1. 加载原始图片
                    original_image = pygame.image.load(dialogue_path).convert_alpha()

                    # 2. 让Pygame自动缩放到屏幕大小！
                    scaled_image = pygame.transform.scale(original_image,
                                                          (self.screen_width, self.screen_height))

                    # 3. 保存缩放后的图片（使用文件名去掉扩展名作为键）
                    dialogue_key = filename.replace(".png", "")
                    self.dialogues[dialogue_key] = scaled_image
                    print(f"✓ 加载对话框图片: {filename}")

                except Exception as e:
                    print(f"✗ 加载对话框图片失败 {filename}: {e}")
            else:
                print(f"⚠ 对话框图片不存在: {dialogue_path}")

        # 如果没有加载到任何图片，创建默认对话框
        if not self.dialogues:
            print("⚠ 未找到任何对话框图片，使用默认对话框")
            self.create_default_dialogues()

    def create_default_dialogues(self):
        """创建默认对话框（使用中文字体）"""
        default_surface = pygame.Surface((self.screen_width, self.screen_height))
        default_surface.fill((40, 40, 60))

        # 使用字体管理器获取中文字体
        title_font = font_manager.get_font(48, bold=True)
        title = title_font.render("全屏对话框", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        default_surface.blit(title, title_rect)

        font_small = font_manager.get_font(24)
        instructions = [
            "这是一个全屏对话框示例",
            "按 ESC 键退出对话框",
            "按 E 键可以切换到下一个对话框",
            "如果看到此界面，说明图片加载失败"
        ]

        for i, text in enumerate(instructions):
            text_surface = font_small.render(text, True, (200, 200, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, 200 + i * 40))
            default_surface.blit(text_surface, text_rect)

        # 添加图片加载提示
        tip_font = font_manager.get_font(20)
        tip_text = tip_font.render("请将对话框图片放在 assets/images/dialogues/ 目录下",
                                   True, (255, 200, 200))
        tip_rect = tip_text.get_rect(center=(self.screen_width // 2, 400))
        default_surface.blit(tip_text, tip_rect)

        # 创建所有默认对话框
        self.dialogues["default"] = default_surface
        self.dialogues["mydialogue1"] = default_surface
        self.dialogues["mydialogue2"] = default_surface
        self.dialogues["mydialogue3"] = default_surface
        self.dialogues["mydialogue5"] = default_surface
        self.dialogues["mydialogue6"] = default_surface
        self.dialogues["mydialogue7"] = default_surface
        self.dialogues["mydialogue8"] = default_surface
        self.dialogues["mydialogue9"] = default_surface
        self.dialogues["mydialogue10"] = default_surface
        self.dialogues["mydialogue11"] = default_surface

    def check_triggers(self, cat_x, cat_y, cat_width=40, cat_height=40):
        """检查小猫是否在触发区域内，返回对应的对话键"""
        # 创建小猫的碰撞矩形
        cat_rect = pygame.Rect(cat_x, cat_y, cat_width, cat_height)

        for x, y, width, height, dialogue_key in self.trigger_areas:
            # 创建触发区域的矩形
            trigger_rect = pygame.Rect(x, y, width, height)

            # 使用Pygame的矩形碰撞检测
            if cat_rect.colliderect(trigger_rect):
                # 特殊处理：小鱼干奖励CG需要猫猫处于cat_head3状态
                if dialogue_key == "mydialogue5":
                    if self.cat_head_state == "cat_head3":
                        # 返回序列标识，而不是单个对话键
                        return "special_cg"
                    else:
                        # 猫猫不是cat_head3状态，不触发
                        continue

                return dialogue_key

        return None

    def show(self, dialogue_key="mydialogue1"):
        """显示对话框或对话序列"""
        # 检查是否是对话序列
        if dialogue_key in self.sequences:
            sequence = self.sequences[dialogue_key]

            # 检查序列中的所有对话图片是否都已加载
            for seq_key in sequence:
                if seq_key not in self.dialogues:
                    print(f"⚠ 对话序列中的图片未加载: {seq_key}")
                    return False

            # 设置序列播放
            self.dialogue_sequence = sequence
            self.sequence_index = 0
            self.in_sequence = True

            # 显示序列中的第一个对话
            self.current_dialogue_key = sequence[0]
            self.current_dialogue = self.dialogues[sequence[0]]
            self.active = True

            print(f"开始播放对话序列: {sequence}")
            return True

        # 单个对话
        if dialogue_key in self.dialogues:
            self.current_dialogue = self.dialogues[dialogue_key]
            self.current_dialogue_key = dialogue_key
            self.active = True
            return True

        return False

    def hide(self):
        """隐藏对话框"""
        self.active = False
        self.current_dialogue = None
        self.current_dialogue_key = None

        # 重置序列状态
        self.in_sequence = False
        self.dialogue_sequence = []
        self.sequence_index = 0

    def next_in_sequence(self):
        """播放序列中的下一个对话"""
        if not self.in_sequence or not self.dialogue_sequence:
            return False

        self.sequence_index += 1

        # 检查是否还有下一个对话
        if self.sequence_index < len(self.dialogue_sequence):
            next_key = self.dialogue_sequence[self.sequence_index]
            if next_key in self.dialogues:
                self.current_dialogue_key = next_key
                self.current_dialogue = self.dialogues[next_key]
                print(f"切换到序列中的下一个对话: {next_key}")
                return True
            else:
                print(f"⚠ 序列中的对话图片未加载: {next_key}")
                self.hide()
                return False
        else:
            # 序列播放完毕
            print("对话序列播放完毕")
            self.hide()
            return False

    def update(self):
        """更新（空方法，保持接口一致）"""
        pass

    def draw(self, screen):
        """绘制对话框"""
        if self.active and self.current_dialogue:
            # 直接绘制缩放后的图片
            screen.blit(self.current_dialogue, (0, 0))

            # 根据当前对话框显示不同的按键提示
            prompt_font = font_manager.get_font(24)

            if self.in_sequence:
                # 在序列中
                if self.sequence_index < len(self.dialogue_sequence) - 1:
                    # 不是最后一个，提示继续
                    prompt_text = "按 D 键继续"
                    prompt_color = (255, 200, 100)  # 橙色
                else:
                    # 最后一个，提示退出
                    prompt_text = "按 D 键退出"
                    prompt_color = (255, 100, 100)  # 红色

            elif self.current_dialogue_key == "mydialogue1":
                # 触发井字棋的对话
                prompt_text = "按 F 键开始井字棋 | 按 ESC 键退出"
                prompt_color = (100, 255, 100)  # 绿色

            elif self.current_dialogue_key in ["mydialogue2", "mydialogue3"]:
                # 井字棋结果对话
                prompt_text = "按 D 键退出对话"
                prompt_color = (255, 100, 100)  # 红色

            elif self.current_dialogue_key in ["mydialogue8", "mydialogue9", "mydialogue10", "mydialogue11"]:
                # 其他新增对话
                prompt_text = "按 D 键退出对话"
                prompt_color = (200, 200, 255)  # 蓝色

            else:
                prompt_text = "按 ESC 键退出"
                prompt_color = (255, 255, 255)  # 白色

            # 绘制按键提示
            prompt = prompt_font.render(prompt_text, True, prompt_color)
            prompt_rect = prompt.get_rect(bottomright=(self.screen_width - 20, self.screen_height - 20))

            # 添加半透明背景
            bg_rect = pygame.Rect(prompt_rect.left - 10, prompt_rect.top - 5,
                                  prompt_rect.width + 20, prompt_rect.height + 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 150))
            screen.blit(bg_surface, bg_rect)

            screen.blit(prompt, prompt_rect)

    def handle_key_event(self, event):
        """处理键盘事件"""
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 按ESC退出任何对话框
                self.hide()
                return "exit"

            elif event.key == pygame.K_f and self.current_dialogue_key == "mydialogue1":
                # 按F键开始井字棋
                self.hide()
                return "start_tic_tac_toe"

            elif event.key == pygame.K_d:
                # 按D键
                if self.in_sequence:
                    # 在序列中，切换到下一个
                    if not self.next_in_sequence():
                        # 序列结束
                        return "exit_dialogue"
                    return None
                else:
                    # 不在序列中，退出对话
                    self.hide()
                    return "exit_dialogue"

        return None