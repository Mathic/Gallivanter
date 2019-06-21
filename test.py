import sys
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

def main():
    pygame.init()
    size = [500, 500]
    screen = pygame.display.set_mode(size)
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Spinning Planet")
    clock = pygame.time.Clock()
    image_orig = pygame.image.load('spd1_bk1.gif').convert()
    image = image_orig.copy()
    image_rect = image_orig.get_rect(center=screen_rect.center)
    angle = 0
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        image = pygame.transform.rotate(image_orig, angle)
        image_rect = image.get_rect(center=image_rect.center)
        # screen.fill(BLACK)
        screen.blit(image, image_rect)
        pygame.display.flip()
        clock.tick(60)
        angle += 1

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
