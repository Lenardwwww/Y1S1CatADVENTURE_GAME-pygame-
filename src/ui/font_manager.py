# src/ui/font_manager.py - 确保正确实现
import pygame
import os


class FontManager:
    """字体管理器，负责加载和管理游戏字体"""
    def __init__(self):
        self.fonts = {}

    def load_font(self, size=24, bold=False, italic=False, font_name="myfont.ttf"):
        """加载指定大小的字体"""
        # 字体文件路径
        font_dir = os.path.join("assets", "fonts")
        font_path = os.path.join(font_dir, font_name)

        # 检查字体文件是否存在
        if not os.path.exists(font_path):
            print(f"⚠ 警告: 字体文件不存在: {font_path}")
            print("将使用系统默认字体，中文可能无法显示")
            # 回退到系统字体
            font = pygame.font.Font(None, size)
            if bold:
                font.set_bold(True)
            if italic:
                font.set_italic(True)
            return font

        # 创建字体缓存键
        font_key = f"{font_name}_{size}_{bold}_{italic}"

        # 如果字体已加载，直接返回
        if font_key in self.fonts:
            return self.fonts[font_key]

        # 加载新字体
        try:
            font = pygame.font.Font(font_path, size)
            if bold:
                font.set_bold(True)
            if italic:
                font.set_italic(True)
            self.fonts[font_key] = font
            print(f"✓ 加载字体: {font_name}, 大小: {size}")
            return font
        except Exception as e:
            print(f"✗ 加载字体失败: {e}")
            # 回退到系统字体
            font = pygame.font.Font(None, size)
            if bold:
                font.set_bold(True)
            if italic:
                font.set_italic(True)
            return font

    def get_font(self, size=24, bold=False, italic=False):
        """获取字体对象（简单封装）"""
        return self.load_font(size, bold, italic)

    def clear_cache(self):
        """清除字体缓存"""
        self.fonts.clear()


# 创建全局字体管理器实例
font_manager = FontManager()