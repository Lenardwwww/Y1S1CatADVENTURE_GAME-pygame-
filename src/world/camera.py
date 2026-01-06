"""
相机类
"""
import pygame
from constants import *


class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 相机位置
        self.x = 0
        self.y = 0

        # 平滑移动
        self.target_x = 0
        self.target_y = 0

        # 死区（小猫移动超过此范围相机才跟随）
        self.deadzone = CAMERA_DEADZONE

        # 是否垂直跟随
        self.vertical_follow = CAMERA_VERTICAL_FOLLOW

    def update(self, target_x, target_y, dt=1.0):
        """
        更新相机位置

        Args:
            target_x: 目标x坐标（通常是小猫）
            target_y: 目标y坐标
            dt: 时间增量（用于平滑移动）
        """
        # 计算目标相机位置（让目标在屏幕中心）
        target_cam_x = target_x - self.screen_width // 2

        # 水平跟随（带死区）
        distance_x = abs(target_cam_x - self.x)
        if distance_x > self.deadzone:
            # 平滑移动到目标位置
            lerp_factor = min(CAMERA_SMOOTHNESS * dt * 60, 1.0)
            self.x += (target_cam_x - self.x) * lerp_factor

        # 垂直跟随（可选）
        if self.vertical_follow:
            target_cam_y = target_y - self.screen_height // 2
            self.y += (target_cam_y - self.y) * CAMERA_SMOOTHNESS * dt * 60

        # 限制相机范围
        self.clamp_position()

    def clamp_position(self):
        """限制相机位置在世界范围内"""
        self.x = max(0, min(self.x, self.world_width - self.screen_width))
        self.y = max(0, min(self.y, self.world_height - self.screen_height))

    def apply(self, entity):
        """
        将世界坐标转换为屏幕坐标

        Args:
            entity: 实体对象（需要有x, y属性）
        Returns:
            (screen_x, screen_y): 屏幕坐标
        """
        screen_x = entity.x - self.x
        screen_y = entity.y - self.y
        return screen_x, screen_y

    def apply_to_point(self, world_x, world_y):
        """将世界坐标点转换为屏幕坐标点"""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return screen_x, screen_y

    def apply_to_rect(self, rect):
        """将世界坐标矩形转换为屏幕坐标矩形"""
        screen_rect = rect.copy()
        screen_rect.x -= self.x
        screen_rect.y -= self.y
        return screen_rect

    def is_visible(self, entity, margin=100):
        """
        检查实体是否在相机视野内（带边距）

        Args:
            entity: 实体对象
            margin: 视野边距（实体在视野外margin像素内也算可见）
        Returns:
            bool: 是否可见
        """
        screen_x, screen_y = self.apply(entity)

        return (screen_x + entity.width > -margin and
                screen_x < self.screen_width + margin and
                screen_y + entity.height > -margin and
                screen_y < self.screen_height + margin)

    def get_view_rect(self):
        """获取相机视野的矩形（世界坐标）"""
        return pygame.Rect(self.x, self.y, self.screen_width, self.screen_height)

    def shake(self, intensity=10, duration=0.5):
        """相机震动效果（可选功能）"""
        # 可以扩展这个功能
        pass