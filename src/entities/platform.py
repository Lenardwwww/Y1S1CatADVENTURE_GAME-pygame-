import pygame
class Platform:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen, camera):
        draw_x = self.x - camera.x
        draw_y = self.y

        # 修改为：
        draw_x = int(self.x - camera.x)  # 转换为整数
        draw_y = int(self.y)  # 转换为整数

        # 绘制平台主体
        pygame.draw.rect(screen, self.color,
                         (draw_x, draw_y, self.width, self.height))