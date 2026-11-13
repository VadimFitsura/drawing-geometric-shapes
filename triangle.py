import tkinter as tk
import math

RAINBOW = [
    ("красный",    "#FF0000"),
    ("оранжевый",  "#FF7F00"),
    ("жёлтый",     "#FFFF00"),
    ("зелёный",    "#00C000"),
    ("голубой",    "#00BFFF"),
    ("синий",      "#0000FF"),
    ("фиолетовый", "#8B00FF"),
]

ANGLE       = 15
CANVAS_SIZE = 600
CENTER      = CANVAS_SIZE / 2
MARGIN      = 20
MAX_RADIUS  = CENTER - MARGIN

def centroid(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def rotate(pts, angle_deg):
    cx, cy = centroid(pts)
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa,
             cy + (x - cx) * sa + (y - cy) * ca)
            for x, y in pts]

def ask_vertices():
    print("=" * 60)
    print("Введите координаты трёх вершин треугольника.")
    print("Формат:  x1 y1 x2 y2 x3 y3 ")
    print("Пример:  150 100 100 300 300 300")
    print("=" * 60)
    while True:
        raw = input("Координаты: ").strip().replace(",", " ").split()
        try:
            nums = [float(v) for v in raw]
        except ValueError:
            print("Ошибка: нужны числа. Попробуйте ещё раз.\n")
            continue
        if len(nums) != 6:
            print(f"Ошибка: введено {len(nums)} чисел, а нужно 6.\n")
            continue
        pts = [(nums[0], nums[1]),
               (nums[2], nums[3]),
               (nums[4], nums[5])]
        # проверка: точки не должны лежать на одной прямой
        area = abs((pts[1][0] - pts[0][0]) * (pts[2][1] - pts[0][1])
                 - (pts[2][0] - pts[0][0]) * (pts[1][1] - pts[0][1])) / 2
        if area < 1e-6:
            print("Ошибка: точки лежат на одной прямой — треугольника не будет.\n")
            continue
        return pts

def ask_color():
    print("\n" + "=" * 60)
    print("Выберите начальный цвет закраски.")
    print("Доступны цвета радуги:")
    for i, (name, hx) in enumerate(RAINBOW, 1):
        print(f"  {i}. {name:<12s}")
    print("=" * 60)
    while True:
        s = input("Цвет: ").strip()
        if not s:
            print("Введите цвет.")
            continue

        if s.isdigit():
            n = int(s)
            if 1 <= n <= len(RAINBOW):
                return RAINBOW[n - 1][1], n - 1
            print(f"Номер должен быть от 1 до {len(RAINBOW)}.\n")
            continue


vertices = ask_vertices()
current_color, idx  = ask_color()

cx0, cy0 = centroid(vertices)
R = max(math.hypot(x - cx0, y - cy0) for x, y in vertices)
scale = MAX_RADIUS / R if R > MAX_RADIUS else 1.0
vertices = [((x - cx0) * scale + CENTER,
             (y - cy0) * scale + CENTER) for x, y in vertices]

root = tk.Tk()
root.title("Вращающийся треугольник")
canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
canvas.pack()
tk.Label(root,
         text="R — по часовой, L — против часовой, Enter — следующий цвет радуги"
         ).pack()


def draw():
    canvas.delete("all")
    flat = [c for p in vertices for c in p]
    canvas.create_polygon(flat, fill=current_color, outline="black", width=2)


def on_key(event):
    global vertices, current_color, idx
    kc = event.keycode

    if kc == 82:
        vertices = rotate(vertices, ANGLE)
        draw()
    elif kc == 76:
        vertices = rotate(vertices, -ANGLE)
        draw()
    elif kc == 13:
        idx = (idx + 1) % len(RAINBOW)
        current_color = RAINBOW[idx][1]
        draw()


root.bind("<Key>", on_key)

draw()
root.mainloop()