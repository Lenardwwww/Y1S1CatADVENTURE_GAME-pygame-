"""
强制要求必须有背景图片，否则游戏无法运行
"""
import pygame
import os
import sys
from constants import *

class StrictBackground:
    def __init__(self, image_path, target_width, target_height):
        """
        初始化背景类 - 必须要有图片

        Args:
            image_path: 背景图片路径
            target_width: 目标宽度（7000）
            target_height: 目标高度（700）
        """
        self.target_width = target_width
        self.target_height = target_height

        # 尝试加载背景图片
        print("正在加载背景图片...")
        print(f"图片路径: {image_path}")

        if not os.path.exists(image_path):
            print("\n游戏无法运行，按任意键退出...")
            input()  # 等待用户按键
            sys.exit(1)  # 退出程序

        try:
            # 加载原始图片
            original_image = pygame.image.load(image_path).convert_alpha()
            original_width = original_image.get_width()
            original_height = original_image.get_height()

            # 等比例缩放到目标尺寸
            self.image = pygame.transform.scale(original_image, (target_width, target_height))

            print(f"✓ 背景图片已成功缩放到 {target_width}x{target_height}")
            print(f"  缩放比例: 宽度×{target_width/original_width:.1f}, 高度×{target_height/original_height:.1f}")

        except Exception as e:
            print("游戏无法运行，按任意键退出...")
            input()
            sys.exit(1)

    def draw(self, screen, camera_x):
        """
        绘制背景

        Args:
            screen: 目标Surface
            camera_x: 相机x坐标
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # 确保相机位置在有效范围内
        max_camera_x = self.target_width - screen_width
        camera_x = max(0, min(camera_x, max_camera_x))

        # 计算源矩形（背景图片的哪部分应该显示）
        src_rect = pygame.Rect(camera_x, 0, screen_width, screen_height)

        # 绘制背景
        screen.blit(self.image, (0, 0), src_rect)