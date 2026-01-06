# src/ui/dialogue_box.py - 修改使用中文字体
import pygame
from src.ui.font_manager import font_manager
from constants import WHITE, YELLOW

# 注意：在constants.py中添加LIGHT_BLUE颜色，如果没有的话
# LIGHT_BLUE = (173, 216, 230)  # 添加到constants.py


class DialogueBox:
    def __init__(self):
        # 使用字体管理器获取中文字体
        self.font = font_manager.get_font(24)  # 24号字体
        self.text = ""
        self.visible = False
        self.name = ""
        self.funny_name = ""
        self.line_height = 30

    def show(self, text, name="", funny_name=""):
        self.text = text
        self.name = name
        self.funny_name = funny_name if funny_name else name
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # 绘制对话框背景
        dialogue_height = 180
        dialogue_y = screen_height - dialogue_height

        # 半透明背景
        s = pygame.Surface((screen_width, dialogue_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))  # 黑色半透明
        screen.blit(s, (0, dialogue_y))

        # 边框
        pygame.draw.rect(screen, WHITE, (0, dialogue_y, screen_width, dialogue_height), 2)

        # 如果有名字，显示名字
        if self.funny_name:
            # 使用字体管理器获取加粗字体
            name_font = font_manager.get_font(28, bold=True)
            name_text = name_font.render(self.funny_name, True, YELLOW)
            screen.blit(name_text, (20, dialogue_y + 10))

        # 分割文本为多行
        lines = self._split_text(self.text, screen_width - 40)

        # 显示文本行
        text_y = dialogue_y + 50
        for line in lines:
            line_text = self.font.render(line, True, WHITE)
            screen.blit(line_text, (20, text_y))
            text_y += self.line_height

        # 显示继续提示
        continue_font = font_manager.get_font(20)
        continue_text = continue_font.render("按空格键继续...", True, (173, 216, 230))  # LIGHT_BLUE
        screen.blit(continue_text, (screen_width - 150, screen_height - 40))

    def _split_text(self, text, max_width):
        """将文本分割为多行以适应宽度"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            # 测试当前行加上新单词是否超过宽度
            test_line = ' '.join(current_line + [word])
            if self.font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines