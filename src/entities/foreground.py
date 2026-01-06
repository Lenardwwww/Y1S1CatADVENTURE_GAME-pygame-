# src/entities/foreground.py
import pygame
import os


class ForegroundObject:
    """前景对象类，用于创建遮挡效果的前景元素"""

    def __init__(self, image_path, x, y, scale=1.0, alpha=255, special_scale=None):
        """
        初始化前景对象

        Args:
            image_path: 图片路径
            x: x坐标（世界坐标）
            y: y坐标（世界坐标）
            scale: 缩放比例
            alpha: 透明度 (0-255, 255为完全不透明)
            special_scale: 特殊缩放比例，如果指定，会覆盖scale参数
        """
        self.x = x
        self.y = y
        self.scale = scale
        self.special_scale = special_scale
        self.alpha = alpha
        self.image = None
        self.original_image = None
        self.width = 0
        self.height = 0

        # 加载图片
        self.load_image(image_path)

    def load_image(self, image_path):
        """加载并处理图片"""
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"✗ 前景图片不存在: {image_path}")
                return

            # 加载图片
            self.original_image = pygame.image.load(image_path).convert_alpha()

            # 应用特殊缩放
            if self.special_scale is not None:
                # 使用特殊缩放比例
                new_width = int(self.original_image.get_width() * self.special_scale)
                new_height = int(self.original_image.get_height() * self.special_scale)
                print(f"应用特殊缩放: {self.special_scale}倍, 新尺寸: {new_width}x{new_height}")
                self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
            # 应用普通缩放
            elif self.scale != 1.0:
                new_width = int(self.original_image.get_width() * self.scale)
                new_height = int(self.original_image.get_height() * self.scale)
                self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
            else:
                self.image = self.original_image

            # 应用透明度
            if self.alpha < 255:
                self.image.set_alpha(self.alpha)

            # 获取尺寸
            self.width = self.image.get_width()
            self.height = self.image.get_height()

            print(f"✓ 加载前景图片: {image_path}")
            print(f"  原始尺寸: {self.original_image.get_width()}x{self.original_image.get_height()}")
            print(f"  缩放后尺寸: {self.width}x{self.height}")

        except Exception as e:
            print(f"✗ 加载前景图片失败 {image_path}: {e}")

    def draw(self, screen, camera_x):
        """绘制前景对象"""
        if self.image:
            # 计算屏幕坐标（考虑相机偏移）
            screen_x = self.x - camera_x
            screen_y = self.y

            # 绘制图片
            screen.blit(self.image, (screen_x, screen_y))