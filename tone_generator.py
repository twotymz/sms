import pygame
from psg import PSG


CLOCK_RATE = 3579545        # Hz
TICKS_PER_MS = CLOCK_RATE / 1000.0


def _hz_to_reg(hz):
    return int(CLOCK_RATE / (32 * hz))


def _main():
    psg = PSG()
    pygame.init()

    pygame.mixer.init()
    pygame.display.set_caption('SN76489 Tone Generator')

    screen = pygame.display.set_mode(
        (640, 480),
        0,
        24
    )

    running = True
    clock = pygame.time.Clock()
    latched_channel = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    latched_channel = 0

                elif event.key == pygame.K_2:
                    latched_channel = 1

                elif event.key == pygame.K_3:
                    latched_channel = 2

                elif event.key == pygame.K_4:
                    latched_channel = 3

                elif event.key == pygame.K_UP:
                    volume = psg.get_channel(latched_channel).volume.register
                    if volume >= 0x1:
                        latch = (1 << 7) | (latched_channel << 5) | (1 << 4) | ((volume - 1) & 0xF)
                        psg.write(latch)

                elif event.key == pygame.K_DOWN:
                    volume = psg.get_channel(latched_channel).volume.register
                    if volume <= 0xE:
                        latch = (1 << 7) | (latched_channel << 5) | (1 << 4) | ((volume + 1) & 0xF)
                        psg.write(latch)

                elif event.key == pygame.K_a:
                    reg = _hz_to_reg(440)
                    latch = (1 << 7) | (latched_channel << 5) | (0 << 4) | (reg & 0xF)
                    data = (reg >> 4) & 0x2F
                    psg.write(latch)
                    psg.write(data)

        cycles = int(clock.get_time() * TICKS_PER_MS)
        psg.run(cycles)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    _main()
