import pygame
import random
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TtkTicTacToe:
    """井字棋游戏类（带ttk前缀避免冲突）"""

    def __init__(self, screen_width, screen_height, font_manager):
        self.ttk_board = None
        self.ttk_winning_line = None
        self.ttk_current_player = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.ttk_reset_game()

        # 游戏状态
        self.ttk_game_over = False
        self.ttk_winner = None  # "player", "doll", "draw"

        # 娃娃AI
        self.ttk_doll_thinking = False
        self.ttk_doll_think_timer = 0  # 娃娃思考计时器
        self.ttk_doll_think_delay = 2000  # 娃娃思考延迟时间（毫秒）

        # 绘制相关
        self.ttk_cell_size = 100
        self.ttk_board_offset_x = (screen_width - 3 * self.ttk_cell_size) // 2
        self.ttk_board_offset_y = (screen_height - 3 * self.ttk_cell_size) // 2 + 80  # 向下移动80像素，为标题腾出空间

        # 颜色定义
        self.ttk_BOARD_COLOR = (200, 200, 200)
        self.ttk_LINE_COLOR = (50, 50, 50)
        self.ttk_PLAYER_COLOR = (66, 134, 244)  # 蓝色
        self.ttk_DOLL_COLOR = (244, 66, 66)  # 红色
        self.ttk_TEXT_COLOR = (255, 255, 255)
        self.ttk_HIGHLIGHT_COLOR = (255, 255, 100, 100)

    def ttk_reset_game(self):
        """重置游戏"""
        # 3x3棋盘，0=空，1=玩家(X)，2=娃娃(O)
        self.ttk_board = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
        self.ttk_current_player = 1  # 玩家先手
        self.ttk_game_over = False
        self.ttk_winner = None
        self.ttk_winning_line = None
        self.ttk_doll_thinking = False
        self.ttk_doll_think_timer = 0
        print("井字棋游戏已重置")

    def ttk_handle_click(self, mouse_pos):
        """处理玩家点击"""
        if self.ttk_game_over or self.ttk_current_player != 1:
            return False

        x, y = mouse_pos

        # 转换为棋盘坐标
        board_x = (x - self.ttk_board_offset_x) // self.ttk_cell_size
        board_y = (y - self.ttk_board_offset_y) // self.ttk_cell_size

        # 检查是否在棋盘内
        if 0 <= board_x < 3 and 0 <= board_y < 3:
            # 检查格子是否为空
            if self.ttk_board[board_y][board_x] == 0:
                self.ttk_board[board_y][board_x] = 1
                print(f"玩家落子: ({board_x}, {board_y})")

                # 检查游戏是否结束
                self.ttk_check_game_over()

                # 如果不是游戏结束，开始娃娃思考计时器
                if not self.ttk_game_over:
                    self.ttk_current_player = 2
                    self.ttk_doll_thinking = True  # 娃娃开始思考
                    # 设置随机思考时间（1000-2000毫秒）
                    self.ttk_doll_think_delay = random.randint(1000, 2000)
                    self.ttk_doll_think_timer = pygame.time.get_ticks() + self.ttk_doll_think_delay

                return True

        return False

    def ttk_doll_move(self):
        """娃娃的回合（使用计时器而不是延迟）"""
        # 找出所有空位
        empty_cells = []
        for y in range(3):
            for x in range(3):
                if self.ttk_board[y][x] == 0:
                    empty_cells.append((x, y))

        if empty_cells:
            # 随机选择一个空位
            x, y = random.choice(empty_cells)
            self.ttk_board[y][x] = 2
            print(f"娃娃落子: ({x}, {y})")

            # 检查游戏是否结束
            self.ttk_check_game_over()

            # 如果不是游戏结束，轮到玩家
            if not self.ttk_game_over:
                self.ttk_current_player = 1

        self.ttk_doll_thinking = False
        return True

    def ttk_check_game_over(self):
        """检查游戏是否结束"""
        # 检查所有行
        for y in range(3):
            if self.ttk_board[y][0] == self.ttk_board[y][1] == self.ttk_board[y][2] != 0:
                self.ttk_winner = "player" if self.ttk_board[y][0] == 1 else "doll"
                self.ttk_winning_line = ("row", y)
                self.ttk_game_over = True
                return

        # 检查所有列
        for x in range(3):
            if self.ttk_board[0][x] == self.ttk_board[1][x] == self.ttk_board[2][x] != 0:
                self.ttk_winner = "player" if self.ttk_board[0][x] == 1 else "doll"
                self.ttk_winning_line = ("col", x)
                self.ttk_game_over = True
                return

        # 检查对角线
        if self.ttk_board[0][0] == self.ttk_board[1][1] == self.ttk_board[2][2] != 0:
            self.ttk_winner = "player" if self.ttk_board[0][0] == 1 else "doll"
            self.ttk_winning_line = ("diag", 0)
            self.ttk_game_over = True
            return

        if self.ttk_board[0][2] == self.ttk_board[1][1] == self.ttk_board[2][0] != 0:
            self.ttk_winner = "player" if self.ttk_board[0][2] == 1 else "doll"
            self.ttk_winning_line = ("diag", 1)
            self.ttk_game_over = True
            return

        # 检查平局
        if all(self.ttk_board[y][x] != 0 for y in range(3) for x in range(3)):
            self.ttk_winner = "draw"
            self.ttk_game_over = True
            return

    def ttk_update(self):
        """更新游戏状态"""
        if self.ttk_doll_thinking and not self.ttk_game_over:
            # 检查思考时间是否到了
            current_time = pygame.time.get_ticks()
            if current_time >= self.ttk_doll_think_timer:
                # 思考时间到，娃娃落子
                self.ttk_doll_move()

    def ttk_draw(self, screen):
        """绘制井字棋"""
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # 绘制标题（位置调整）
        title_font = self.font_manager.get_font(48, bold=True)
        title_text = title_font.render("井 字 棋", True, self.ttk_TEXT_COLOR)
        screen.blit(title_text, (self.screen_width // 2 - 80, 30))  # 向上移动到30

        # 绘制当前玩家提示（位置调整）
        status_font = self.font_manager.get_font(24)
        if self.ttk_game_over:
            if self.ttk_winner == "player":
                status_text = "玩家胜利！按 ESC 退出"
            elif self.ttk_winner == "doll":
                status_text = "娃娃胜利！按 ESC 退出"
            else:
                status_text = "平局！按 ESC 退出"
        else:
            if self.ttk_current_player == 1:
                status_text = "轮到你了 (X)"
            else:
                status_text = "娃娃思考中... (O)"

        status_surface = status_font.render(status_text, True, self.ttk_TEXT_COLOR)
        screen.blit(status_surface, (self.screen_width // 2 - 100, 80))  # 向上移动到80

        # 绘制棋盘背景
        board_width = 3 * self.ttk_cell_size
        board_height = 3 * self.ttk_cell_size
        pygame.draw.rect(screen, self.ttk_BOARD_COLOR,
                         (self.ttk_board_offset_x, self.ttk_board_offset_y,
                          board_width, board_height))

        # 绘制网格线
        for i in range(1, 3):
            # 垂直线
            pygame.draw.line(screen, self.ttk_LINE_COLOR,
                             (self.ttk_board_offset_x + i * self.ttk_cell_size, self.ttk_board_offset_y),
                             (self.ttk_board_offset_x + i * self.ttk_cell_size,
                              self.ttk_board_offset_y + board_height), 4)
            # 水平线
            pygame.draw.line(screen, self.ttk_LINE_COLOR,
                             (self.ttk_board_offset_x, self.ttk_board_offset_y + i * self.ttk_cell_size),
                             (self.ttk_board_offset_x + board_width,
                              self.ttk_board_offset_y + i * self.ttk_cell_size), 4)

        # 绘制胜利线（如果有）
        if self.ttk_winning_line:
            self.ttk_draw_winning_line(screen)

        # 绘制棋子
        for y in range(3):
            for x in range(3):
                cell_x = self.ttk_board_offset_x + x * self.ttk_cell_size + self.ttk_cell_size // 2
                cell_y = self.ttk_board_offset_y + y * self.ttk_cell_size + self.ttk_cell_size // 2

                if self.ttk_board[y][x] == 1:  # 玩家
                    pygame.draw.line(screen, self.ttk_PLAYER_COLOR,
                                     (cell_x - 30, cell_y - 30),
                                     (cell_x + 30, cell_y + 30), 8)
                    pygame.draw.line(screen, self.ttk_PLAYER_COLOR,
                                     (cell_x + 30, cell_y - 30),
                                     (cell_x - 30, cell_y + 30), 8)
                elif self.ttk_board[y][x] == 2:  # 娃娃
                    pygame.draw.circle(screen, self.ttk_DOLL_COLOR,
                                       (cell_x, cell_y), 35, 6)

        # 绘制游戏说明（位置调整到棋盘下方）
        instruction_font = self.font_manager.get_font(18)
        instruction_text = [
            "规则: 点击格子放置 X，三个连成一线获胜",
            "娃娃会自动放置 O",
            "按 ESC 键退出游戏"
        ]

        for i, text in enumerate(instruction_text):
            instruction_surface = instruction_font.render(text, True, self.ttk_TEXT_COLOR)
            # 调整到棋盘下方
            screen.blit(instruction_surface, (7, 590 + i * 30))  # 向下移动到500

        # 如果娃娃正在思考，显示思考动画（位置调整）
        if self.ttk_doll_thinking:
            self.ttk_draw_thinking_animation(screen)

    def ttk_draw_winning_line(self, screen):
        """绘制胜利线"""
        line_type, index = self.ttk_winning_line

        if line_type == "row":
            y = self.ttk_board_offset_y + index * self.ttk_cell_size + self.ttk_cell_size // 2
            start_x = self.ttk_board_offset_x + 20
            end_x = self.ttk_board_offset_x + 3 * self.ttk_cell_size - 20
            pygame.draw.line(screen, self.ttk_HIGHLIGHT_COLOR,
                             (start_x, y), (end_x, y), 10)
        elif line_type == "col":
            x = self.ttk_board_offset_x + index * self.ttk_cell_size + self.ttk_cell_size // 2
            start_y = self.ttk_board_offset_y + 20
            end_y = self.ttk_board_offset_y + 3 * self.ttk_cell_size - 20
            pygame.draw.line(screen, self.ttk_HIGHLIGHT_COLOR,
                             (x, start_y), (x, end_y), 10)
        elif line_type == "diag":
            if index == 0:  # 主对角线
                start_x = self.ttk_board_offset_x + 20
                start_y = self.ttk_board_offset_y + 20
                end_x = self.ttk_board_offset_x + 3 * self.ttk_cell_size - 20
                end_y = self.ttk_board_offset_y + 3 * self.ttk_cell_size - 20
            else:  # 副对角线
                start_x = self.ttk_board_offset_x + 3 * self.ttk_cell_size - 20
                start_y = self.ttk_board_offset_y + 20
                end_x = self.ttk_board_offset_x + 20
                end_y = self.ttk_board_offset_y + 3 * self.ttk_cell_size - 20
            pygame.draw.line(screen, self.ttk_HIGHLIGHT_COLOR,
                             (start_x, start_y), (end_x, end_y), 10)

    def ttk_draw_thinking_animation(self, screen):
        """绘制娃娃思考动画"""
        center_x = self.screen_width // 2
        center_y = 180  # 向上移动到150，避免与棋盘重叠

        # 绘制思考气泡
        think_font = self.font_manager.get_font(20)
        think_text = think_font.render("娃娃思考中...", True, (255, 255, 200))

        # 气泡背景
        bubble_width = think_text.get_width() + 20
        bubble_height = think_text.get_height() + 10
        bubble_rect = pygame.Rect(center_x - bubble_width // 2, center_y - bubble_height,
                                  bubble_width, bubble_height)

        pygame.draw.rect(screen, (0, 0, 0, 150), bubble_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), bubble_rect, 2, border_radius=10)
        screen.blit(think_text, (center_x - think_text.get_width() // 2, center_y - bubble_height + 5))

        # 绘制跳动的点
        time_ms = pygame.time.get_ticks()
        for i in range(3):
            offset = (time_ms // 200 + i) % 4 - 1
            y_offset = offset * 3
            pygame.draw.circle(screen, (255, 255, 200),
                               (center_x - 30 + i * 30, center_y + 20 + y_offset), 5)