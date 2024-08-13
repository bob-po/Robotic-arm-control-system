# 初始化 Pygame
import pygame

pygame.init()
# 设置屏幕大小和标题
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
print(screen_width, screen_height)