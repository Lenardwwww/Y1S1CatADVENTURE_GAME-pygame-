# src/ui/hint_system.py - 修改使用中文字体
import pygame
from src.ui.font_manager import font_manager
from constants import YELLOW


class HintSystem:
    def __init__(self):
        # 使用字体管理器获取中文字体
        self.font = font_manager.get_font(20)
        self.hints = [
            "提示：按 E 键与物体和角色交互",
            "提示：按住空格键可以跳得更高",
            "提示：向右走探索烟囱的奥秘",
            "提示：注意观察环境中的线索",
            "提示：每个角色都有自己的故事"
        ]
        self.current_hint_index = 0
        self.hint_timer = 0
        self.hint_interval = 300  # 每300帧切换一次提示

    def update(self, dt):
        self.hint_timer += 1
        if self.hint_timer >= self.hint_interval:
            self.current_hint_index = (self.current_hint_index + 1) % len(self.hints)
            self.hint_timer = 0

    def draw(self, screen):
        current_hint = self.hints[self.current_hint_index]
        hint_text = self.font.render(current_hint, True, YELLOW)

        # 在屏幕底部居中显示提示
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        text_rect = hint_text.get_rect(center=(screen_width // 2, screen_height - 20))

        # 绘制半透明背景
        bg_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5,
                              text_rect.width + 20, text_rect.height + 10)
        s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))  # 半透明黑色
        screen.blit(s, bg_rect)

        screen.blit(hint_text, text_rect)