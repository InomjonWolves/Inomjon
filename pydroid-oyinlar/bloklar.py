# Bloklar — tushayotgan bloklar oʻyini (Pydroid 3 uchun, pygame)
# Pydroid 3: faylni oching → ▶ (Run). pygame Pydroid'da oldindan bor.
# Telefonda: pastdagi tugmalar. Kompyuterda: ← → ↓, ↑ (burish), Probel (tashlash), P (pauza).
import random
import sys

import pygame

COLS, ROWS = 10, 20
SHAPES = {  # har shakl: burilish holatlari (x, y) kataklar
    "I": [(0, 1), (1, 1), (2, 1), (3, 1)],
    "O": [(1, 0), (2, 0), (1, 1), (2, 1)],
    "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
    "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "J": [(0, 0), (0, 1), (1, 1), (2, 1)],
    "L": [(2, 0), (0, 1), (1, 1), (2, 1)],
}
COLORS = {
    "I": (64, 200, 230), "O": (245, 200, 60), "T": (170, 90, 220),
    "S": (90, 200, 110), "Z": (230, 80, 80), "J": (70, 110, 230), "L": (245, 145, 50),
}
BG, GRID, PANEL, TEXT = (18, 20, 38), (36, 40, 66), (28, 31, 56), (235, 235, 245)
SCORES = [0, 100, 300, 500, 800]  # 0–4 qator uchun ochko


def rotate(cells, kind):
    if kind == "O":
        return cells
    n = 4 if kind == "I" else 3
    return [(n - 1 - y, x) for x, y in cells]


class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.cells = list(SHAPES[kind])
        self.x, self.y = 3, -1 if kind == "I" else 0

    def blocks(self, dx=0, dy=0, cells=None):
        return [(self.x + x + dx, self.y + y + dy) for x, y in (cells or self.cells)]


class Game:
    def __init__(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.bag = []
        self.cur, self.nxt = Piece(self.take()), Piece(self.take())
        self.score = self.lines = 0
        self.level = 1
        self.over = self.paused = False
        self.timer = 0
        self.flash = []  # tozalanayotgan qatorlar (animatsiya)
        self.flash_t = 0

    def take(self):  # «7 talik qop»: har 7 shaklda har biri bir marta
        if not self.bag:
            self.bag = list(SHAPES)
            random.shuffle(self.bag)
        return self.bag.pop()

    def free(self, blocks):
        for x, y in blocks:
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and self.board[y][x]:
                return False
        return True

    def move(self, dx, dy):
        if self.free(self.cur.blocks(dx, dy)):
            self.cur.x += dx
            self.cur.y += dy
            return True
        return False

    def turn(self):
        new = rotate(self.cur.cells, self.cur.kind)
        for kick in (0, -1, 1, -2, 2):  # devorga tegsa biroz suriladi
            if self.free(self.cur.blocks(kick, 0, new)):
                self.cur.cells = new
                self.cur.x += kick
                return

    def ghost_dy(self):
        dy = 0
        while self.free(self.cur.blocks(0, dy + 1)):
            dy += 1
        return dy

    def drop(self):
        dy = self.ghost_dy()
        self.cur.y += dy
        self.score += 2 * dy
        self.lock()

    def lock(self):
        for x, y in self.cur.blocks():
            if y < 0:
                self.over = True
                return
            self.board[y][x] = self.cur.kind
        full = [y for y in range(ROWS) if all(self.board[y])]
        if full:
            self.flash, self.flash_t = full, 180
        self.cur, self.nxt = self.nxt, Piece(self.take())
        if not self.free(self.cur.blocks()):
            self.over = True

    def clear(self):
        n = len(self.flash)
        for y in self.flash:
            del self.board[y]
            self.board.insert(0, [None] * COLS)
        self.flash = []
        self.lines += n
        self.score += SCORES[n] * self.level
        self.level = 1 + self.lines // 10

    def speed(self):  # ms har qadamda
        return max(70, 800 - (self.level - 1) * 70)

    def update(self, dt):
        if self.over or self.paused:
            return
        if self.flash:
            self.flash_t -= dt
            if self.flash_t <= 0:
                self.clear()
            return
        self.timer += dt
        if self.timer >= self.speed():
            self.timer = 0
            if not self.move(0, 1):
                self.lock()


class Button:
    def __init__(self, rect, kind, repeat=False):
        self.rect, self.kind, self.repeat = pygame.Rect(rect), kind, repeat
        self.down, self.hold = False, 0

    def draw(self, s):
        col = (70, 78, 130) if self.down else (52, 58, 100)
        pygame.draw.rect(s, col, self.rect, border_radius=18)
        pygame.draw.rect(s, (90, 100, 160), self.rect, 3, border_radius=18)
        cx, cy = self.rect.center
        r = min(self.rect.w, self.rect.h) // 4
        w = (235, 235, 245)
        if self.kind == "left":
            pygame.draw.polygon(s, w, [(cx - r, cy), (cx + r // 2, cy - r), (cx + r // 2, cy + r)])
        elif self.kind == "right":
            pygame.draw.polygon(s, w, [(cx + r, cy), (cx - r // 2, cy - r), (cx - r // 2, cy + r)])
        elif self.kind == "down":
            pygame.draw.polygon(s, w, [(cx, cy + r), (cx - r, cy - r // 2), (cx + r, cy - r // 2)])
        elif self.kind == "drop":
            for k in (-r // 2, r // 2):
                pygame.draw.polygon(s, w, [(cx, cy + k + r // 2), (cx - r, cy + k - r // 2), (cx + r, cy + k - r // 2)])
        elif self.kind == "turn":
            pygame.draw.arc(s, w, (cx - r, cy - r, 2 * r, 2 * r), 0.6, 5.6, max(4, r // 4))
            pygame.draw.polygon(s, w, [(cx + r, cy - r // 3), (cx + r + r // 2, cy - r), (cx + r // 2, cy - r)])


def main():
    pygame.init()
    info = pygame.display.Info()
    if info.current_w < info.current_h:  # telefon — butun ekran
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:  # kompyuter — tik oyna
        screen = pygame.display.set_mode((480, 840))
    pygame.display.set_caption("Bloklar")
    W, H = screen.get_size()

    pad = W // 30
    btn_h = H // 9
    top = H // 12  # yuqori panel (ochko)
    cell = min((W - 2 * pad) * 0.72 / COLS, (H - top - btn_h * 2 - 3 * pad) / ROWS)
    cell = int(cell)
    bx, by = pad, top + pad
    side_x = bx + COLS * cell + pad
    side_w = W - side_x - pad

    font = pygame.font.Font(None, max(24, H // 26))
    big = pygame.font.Font(None, max(40, H // 14))

    # tugmalar: yuqori qator ← ⟳ →, pastki qator ↓ ⤓
    gy = by + ROWS * cell + pad
    bw = (W - 4 * pad) // 3
    buttons = [
        Button((pad, gy, bw, btn_h), "left", True),
        Button((2 * pad + bw, gy, bw, btn_h), "turn"),
        Button((3 * pad + 2 * bw, gy, bw, btn_h), "right", True),
        Button((pad, gy + btn_h + pad // 2, (W - 3 * pad) // 2, btn_h), "down", True),
        Button((2 * pad + (W - 3 * pad) // 2, gy + btn_h + pad // 2, (W - 3 * pad) // 2, btn_h), "drop"),
    ]
    pause_rect = pygame.Rect(side_x, by + ROWS * cell - side_w // 2, side_w, side_w // 2)

    game = Game()
    clock = pygame.time.Clock()
    pointers = {}  # barmoq / sichqoncha → tugma

    def act(kind):
        if game.over or game.paused or game.flash:
            return
        if kind == "left":
            game.move(-1, 0)
        elif kind == "right":
            game.move(1, 0)
        elif kind == "down":
            if game.move(0, 1):
                game.score += 1
        elif kind == "turn":
            game.turn()
        elif kind == "drop":
            game.drop()

    def press(pid, pos):
        nonlocal game
        if game.over:
            game = Game()
            return
        if pause_rect.collidepoint(pos):
            game.paused = not game.paused
            return
        if game.paused:
            game.paused = False
            return
        for b in buttons:
            if b.rect.collidepoint(pos):
                b.down, b.hold = True, -170  # birinchi qaytarishgacha kutish
                pointers[pid] = b
                act(b.kind)

    def release(pid):
        b = pointers.pop(pid, None)
        if b:
            b.down = False

    def cell_rect(x, y):
        return pygame.Rect(bx + x * cell, by + y * cell, cell, cell)

    def draw_block(x, y, col, surf=None, alpha=None):
        r = cell_rect(x, y).inflate(-2, -2)
        if alpha:
            pygame.draw.rect(screen, col, r, 2, border_radius=cell // 5)
            return
        pygame.draw.rect(screen, col, r, border_radius=cell // 5)
        hi = tuple(min(255, c + 50) for c in col)
        pygame.draw.rect(screen, hi, (r.x + 3, r.y + 3, r.w - 6, max(2, r.h // 5)), border_radius=cell // 6)

    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.FINGERDOWN:
                press(("f", e.finger_id), (e.x * W, e.y * H))
            elif e.type == pygame.FINGERUP:
                release(("f", e.finger_id))
            elif e.type == pygame.MOUSEBUTTONDOWN and not getattr(e, "touch", False):
                press("m", e.pos)
            elif e.type == pygame.MOUSEBUTTONUP and not getattr(e, "touch", False):
                release("m")
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_AC_BACK):
                    pygame.quit()
                    sys.exit()
                if game.over:
                    game = Game()
                elif e.key == pygame.K_p:
                    game.paused = not game.paused
                else:
                    act({pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down",
                         pygame.K_UP: "turn", pygame.K_SPACE: "drop"}.get(e.key, ""))

        for b in pointers.values():  # bosib turilsa takrorlanadi
            if b.repeat:
                b.hold += dt
                if b.hold >= 55:
                    b.hold = 0
                    act(b.kind)

        game.update(dt)

        # ---- chizish
        screen.fill(BG)
        screen.blit(big.render(f"{game.score}", True, TEXT), (pad, (top - big.get_height()) // 2 + pad // 2))
        lv = font.render(f"Daraja {game.level}   Qator {game.lines}", True, (170, 175, 210))
        screen.blit(lv, (W - pad - lv.get_width(), (top - lv.get_height()) // 2 + pad // 2))

        pygame.draw.rect(screen, PANEL, (bx - 4, by - 4, COLS * cell + 8, ROWS * cell + 8), border_radius=10)
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(screen, GRID, cell_rect(x, y), 1)
                k = game.board[y][x]
                if k:
                    col = (255, 255, 255) if y in game.flash else COLORS[k]
                    draw_block(x, y, col)

        if not game.over and not game.flash:
            g = game.ghost_dy()
            for x, y in game.cur.blocks(0, g):
                if y >= 0:
                    draw_block(x, y, COLORS[game.cur.kind], alpha=True)
            for x, y in game.cur.blocks():
                if y >= 0:
                    draw_block(x, y, COLORS[game.cur.kind])

        # keyingi shakl
        screen.blit(font.render("Keyingi", True, (170, 175, 210)), (side_x, by))
        nc = side_w // 5
        ny = by + font.get_height() + pad // 2
        pygame.draw.rect(screen, PANEL, (side_x, ny, side_w, nc * 3), border_radius=10)
        cells = game.nxt.cells
        mw = max(x for x, _ in cells) + 1
        mh = max(y for _, y in cells) + 1
        ox = side_x + (side_w - mw * nc) // 2
        oy = ny + (nc * 3 - (mh - min(y for _, y in cells)) * nc) // 2 - min(y for _, y in cells) * nc
        for x, y in cells:
            pygame.draw.rect(screen, COLORS[game.nxt.kind], (ox + x * nc + 1, oy + y * nc + 1, nc - 2, nc - 2), border_radius=nc // 5)

        # pauza tugmasi
        pygame.draw.rect(screen, (52, 58, 100), pause_rect, border_radius=12)
        bw2 = max(4, pause_rect.h // 7)
        cx, cy = pause_rect.center
        for k in (-bw2, bw2):
            pygame.draw.rect(screen, TEXT, (cx + k - bw2 // 2, cy - pause_rect.h // 4, bw2, pause_rect.h // 2))

        for b in buttons:
            b.draw(screen)

        if game.over or game.paused:
            veil = pygame.Surface((W, H), pygame.SRCALPHA)
            veil.fill((10, 10, 25, 190))
            screen.blit(veil, (0, 0))
            t1 = big.render("O'yin tugadi" if game.over else "Pauza", True, TEXT)
            t2 = font.render("Qayta boshlash uchun bosing" if game.over else "Davom etish uchun bosing", True, (190, 195, 225))
            screen.blit(t1, ((W - t1.get_width()) // 2, H // 2 - t1.get_height()))
            if game.over:
                t3 = font.render(f"Ochko: {game.score}", True, (245, 200, 60))
                screen.blit(t3, ((W - t3.get_width()) // 2, H // 2 + 6))
            screen.blit(t2, ((W - t2.get_width()) // 2, H // 2 + 6 + font.get_height() * 1.4))

        pygame.display.flip()


if __name__ == "__main__":
    main()
