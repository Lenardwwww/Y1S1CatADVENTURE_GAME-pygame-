def create_test_background(width, height, filename=None):
    """创建一个测试用的长背景"""
    import pygame
    import random

    surface = pygame.Surface((width, height))

    # 天空渐变 - 修复颜色计算
    for y in range(height):
        # 确保颜色值在0-255范围内
        blue = min(255, 200 + int(55 * y / height))
        green = min(255, 180 + int(75 * y / height))
        color = (100, green, blue)  # 现在颜色值安全了
        pygame.draw.line(surface, color, (0, y), (width, y))

    # 地面
    ground_y = height - 150
    pygame.draw.rect(surface, (120, 80, 40), (0, ground_y, width, 150))

    # 草地
    grass_y = ground_y - 20
    for x in range(0, width, 50):
        height_var = random.randint(10, 30)
        pygame.draw.rect(surface, (60, 180, 75),
                         (x, grass_y - height_var, 40, height_var))

    # 云朵
    for i in range(15):
        cloud_x = random.randint(0, width)
        cloud_y = random.randint(50, 200)
        cloud_size = random.randint(40, 80)
        pygame.draw.ellipse(surface, (240, 240, 255),
                            (cloud_x, cloud_y, cloud_size, cloud_size // 2))

    # 分区域标记（用于测试）
    font = pygame.font.Font(None, 36)
    regions = [
        (500, "起始草地"),
        (1500, "神秘小院"),
        (2500, "遗忘角落"),
        (3500, "危险边缘"),
        (4500, "烟囱之谜")
    ]

    for x, text in regions:
        text_surface = font.render(text, True, (255, 255, 255))
        surface.blit(text_surface, (x, 50))
        pygame.draw.line(surface, (255, 255, 0), (x, 0), (x, height), 2)

    # 保存图片
    if filename:
        pygame.image.save(surface, filename)
        print(f"背景图片已保存: {filename}")

    return surface