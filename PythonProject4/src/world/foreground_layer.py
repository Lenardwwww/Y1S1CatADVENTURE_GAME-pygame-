# src/world/foreground_layer.py
import pygame
import os


class ForegroundLayer:
    """前景层类"""

    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.foreground_objects = []
        self.debug_mode = False

    def add_foreground(self, image_path, x, y, scale=1.0, alpha=255, special_scale=None):
        """添加前景对象"""
        # 加载图片
        if not os.path.exists(image_path):
            print(f"✗ 前景图片不存在: {image_path}")
            return None

        try:
            original_image = pygame.image.load(image_path).convert_alpha()

            # 应用缩放
            if special_scale is not None:
                new_width = int(original_image.get_width() * special_scale)
                new_height = int(original_image.get_height() * special_scale)
                print(f"应用特殊缩放: {special_scale}倍, 新尺寸: {new_width}x{new_height}")
                image = pygame.transform.scale(original_image, (new_width, new_height))
            elif scale != 1.0:
                new_width = int(original_image.get_width() * scale)
                new_height = int(original_image.get_height() * scale)
                image = pygame.transform.scale(original_image, (new_width, new_height))
            else:
                image = original_image

            if alpha < 255:
                image.set_alpha(alpha)

            # 创建前景对象
            fg_obj = {
                'image': image,
                'x': x,
                'y': y,
                'width': image.get_width(),
                'height': image.get_height()
            }

            self.foreground_objects.append(fg_obj)
            print(f"✓ 添加前景对象: {os.path.basename(image_path)}")
            return fg_obj

        except Exception as e:
            print(f"✗ 加载前景图片失败: {e}")
            return None

    def draw(self, screen, camera_x):
        """绘制所有前景对象"""
        for fg_obj in self.foreground_objects:
            # 计算屏幕坐标
            screen_x = fg_obj['x'] - camera_x
            screen_y = fg_obj['y']

            # 绘制前景图片
            screen.blit(fg_obj['image'], (screen_x, screen_y))

            # 调试模式：显示边框
            if self.debug_mode:
                pygame.draw.rect(screen, (255, 0, 0),
                                 (screen_x, screen_y, fg_obj['width'], fg_obj['height']), 1)

                # 显示坐标信息
                font = pygame.font.Font(None, 16)
                coord_text = font.render(f"({fg_obj['x']}, {fg_obj['y']})", True, (255, 255, 255))
                screen.blit(coord_text, (screen_x, screen_y - 20))