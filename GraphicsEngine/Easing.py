# pylint: disable=W,R,C,import-error



import math

def linear(x: float) -> float:
    return x

def easeInSine(x: float) -> float:
    return 1 - math.cos((x * math.pi) / 2)

def easeOutSine(x: float) -> float:
    return math.sin((x * math.pi) / 2)

def easeInOutSine(x: float) -> float:
    return -0.5 * (math.cos(math.pi * x) - 1)

def easeInOutQuad(x: float) -> float:
    if x < 0.5:
        return 2 * x * x
    else:
        return 1 - (((-2 * x + 2) ** 2) / 2)

def easeInOutCubic(x: float) -> float:
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - (-2 * x + 2) ** 3 / 2


def easeInOutQuart(x: float) -> float:
    if x < 0.5:
        return 8 * x * x * x * x
    else:
        return 1 - (-2 * x + 2) ** 4 / 2


def easeInOutQuint(x: float) -> float:
    if x < 0.5:
        return 16 * x * x * x * x * x
    else:
        return 1 - (-2 * x + 2) ** 5 / 2

def easeInExpo(x: float) -> float:
    return math.pow(2, 10 * x - 10)

def easeOutExpo(x: float) -> float:
    return 1 - math.pow(2, -10 * x)

def easeInOutExpo(x: float) -> float:
    if x == 0:
        return 0
    elif x == 1:
        return 1
    elif x < 0.5:
        return math.pow(2, 20 * x - 10) / 2
    else:
        return (2 - math.pow(2, -20 * x + 10)) / 2


def easeInCirc(x: float) -> float:
    return 1 - math.sqrt(1 - x ** 2)

def easeOutCirc(x: float) -> float:
    return math.sqrt(1 - (x - 1) ** 2)

def easeInOutCirc(x: float) -> float:
    if x < 0.5:
        return (1 - math.sqrt(1 - (2 * x) ** 2)) / 2
    else:
        return (math.sqrt(1 - (-2 * x + 2) ** 2) + 1) / 2

def interpolate2D(a:tuple[float, float], b:tuple[float, float], t:float) -> tuple[float, float]:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)



# def rectangularEase(x:float, a:float, b:float, easing) -> float:
#     perimeter_length = 2*a + 2*b
    
#     target = perimeter_length * easing(x)
    
#     if target <= b/2: # right side (bottom half)
#         _x = (a/2)
#         _y = target
#     elif target <= (b/2) + a: # bottom side
#         _x = (a/2) - (target - (b/2))
#         _y = (b/2)
#     elif target <= (b/2) + a + b: # left side
#         _x = -(a/2)
#         _y = (b/2) - (target - (b/2) - a)
#     elif target <= perimeter_length - (b/2): # top side
#         _y = -(b/2)
#         _x = (a/2) - (target - (b/2) - a - b)
#     else: # right side (top half)
#         _x = (a/2)
#         _y = (b/2) - (target - (perimeter_length - (b/2)))

#     print(f" {target} ({_x}, {_y})")

#     out = (math.degrees(math.atan2(_y, _x)) % 360) / (360*2)
#     print(out*360)
#     return out
