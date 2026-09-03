import argparse
import colorsys
import json


# --- 颜色转换基础函数 ---


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    r, g, b = [max(0, min(255, int(round(x * 255)))) for x in rgb]
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_hsl(hex_str):
    r, g, b = hex_to_rgb(hex_str)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return [h * 360, s * 100, l * 100]


def hsl_to_hex(hsl):
    h, s, l = hsl[0] / 360.0, hsl[1] / 100.0, hsl[2] / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex((r, g, b))


def blend(hex_str1, hex_str2, alpha):
    r1, g1, b1 = hex_to_rgb(hex_str1)
    r2, g2, b2 = hex_to_rgb(hex_str2)
    return rgb_to_hex(
        (
            r1 * alpha + r2 * (1 - alpha),
            g1 * alpha + g2 * (1 - alpha),
            b1 * alpha + b2 * (1 - alpha),
        )
    )


# --- 核心：解耦基调色与标准颜色 ---


def build_theme(primary_hex):
    p_h, p_s, p_l = hex_to_hsl(primary_hex)

    # 1. 提取基调色（Primary / Accent）及其变体
    # 暗色模式下的主色变体
    p_dark_base = hsl_to_hex([p_h, max(50.0, p_s), 75])
    p_dark_dim = hsl_to_hex([p_h, max(40.0, p_s * 0.8), 58])
    p_dark_bright = hsl_to_hex([p_h, max(60.0, p_s), 85])

    # 亮色模式下的主色变体
    p_light_base = hsl_to_hex([p_h, max(50.0, p_s), 45])
    p_light_dim = hsl_to_hex([p_h, max(40.0, p_s * 0.8), 35])
    p_light_bright = hsl_to_hex([p_h, max(60.0, p_s), 55])

    # 2. 独立的标准语义色彩（标准 Hue，不受 primary 拖累）
    hue_blue = 210
    hue_cyan = 185
    hue_green = 135
    hue_yellow = 40
    hue_orange = 25
    hue_red = 5
    hue_purple = 270
    hue_pink = 330

    return {
        "dark": {
            # ===== 新增：专门围绕基调色的字段 =====
            "primary": p_dark_base,
            "primary_dim": p_dark_dim,
            "primary_bright": p_dark_bright,
            # ===== 背景与基础 UI =====
            "bg": hsl_to_hex([p_h, 10, 11]),  # 微微带有基调色调的深暗背景
            "bg_dim": hsl_to_hex([p_h, 10, 13]),
            "bg_deep": hsl_to_hex([p_h, 10, 8]),
            "bg_highlight": hsl_to_hex([p_h, 10, 19]),
            "bg_search": hsl_to_hex([p_h, 30, 20]),
            "fg": hsl_to_hex([p_h, 5, 90]),
            "fg_muted": hsl_to_hex([p_h, 5, 70]),
            "fg_gutter": hsl_to_hex([p_h, 5, 30]),
            "fg_dark": hsl_to_hex([p_h, 5, 48]),
            "border": hsl_to_hex([p_h, 8, 20]),
            "border_highlight": p_dark_base,
            "selection": hsl_to_hex([p_h, 10, 23]),
            "cursor_line": hsl_to_hex([p_h, 10, 16]),
            "float": {
                "bg": hsl_to_hex([p_h, 10, 13]),
                "fg": hsl_to_hex([p_h, 5, 90]),
                "border": hsl_to_hex([p_h, 5, 30]),
            },
            # ===== 真正标准的颜色（blue 回归蓝色） =====
            "blue": hsl_to_hex([hue_blue, 65, 75]),
            "blue_dim": hsl_to_hex([hue_blue, 50, 60]),
            "blue_bright": hsl_to_hex([hue_blue, 80, 85]),
            "cyan": hsl_to_hex([hue_cyan, 55, 68]),
            "green": hsl_to_hex([hue_green, 50, 65]),
            "green_bright": hsl_to_hex([hue_green, 60, 75]),
            "yellow": hsl_to_hex([hue_yellow, 60, 70]),
            "orange": hsl_to_hex([hue_orange, 60, 70]),
            "red": hsl_to_hex([hue_red, 65, 68]),
            "red_dim": hsl_to_hex([hue_red, 60, 50]),
            "purple": hsl_to_hex([hue_purple, 50, 72]),
            "pink": hsl_to_hex([hue_pink, 55, 72]),
            "comment": hsl_to_hex([p_h, 5, 48]),
            "terminal_black": hsl_to_hex([p_h, 10, 23]),
            "rosewater": hsl_to_hex([15, 45, 75]),
            "flamingo": hsl_to_hex([20, 50, 72]),
            "mauve": hsl_to_hex([260, 45, 75]),
            "maroon": hsl_to_hex([350, 55, 60]),
            "peach": hsl_to_hex([30, 60, 72]),
            "teal": hsl_to_hex([165, 40, 68]),
            "sky": hsl_to_hex([195, 45, 72]),
            "sapphire": hsl_to_hex([200, 45, 68]),
            "lavender": hsl_to_hex([230, 45, 75]),
            "git": {
                "add": hsl_to_hex([hue_green, 50, 65]),
                "change": p_dark_base,  # Git 修改使用基调色
                "delete": hsl_to_hex([hue_red, 65, 68]),
            },
            "diag": {
                "error": hsl_to_hex([hue_red, 65, 68]),
                "warn": hsl_to_hex([hue_yellow, 60, 70]),
                "info": p_dark_base,  # 诊断 Info 使用基调色
                "hint": hsl_to_hex([hue_green, 50, 65]),
                "bg_error": blend(
                    hsl_to_hex([hue_red, 65, 68]), hsl_to_hex([p_h, 10, 11]), 0.2
                ),
                "bg_warn": blend(
                    hsl_to_hex([hue_yellow, 60, 70]),
                    hsl_to_hex([p_h, 10, 11]),
                    0.2,
                ),
                "bg_info": blend(p_dark_base, hsl_to_hex([p_h, 10, 11]), 0.2),
                "bg_hint": blend(
                    hsl_to_hex([hue_green, 50, 65]),
                    hsl_to_hex([p_h, 10, 11]),
                    0.2,
                ),
            },
            "diff": {
                "add": blend(
                    hsl_to_hex([hue_green, 50, 65]),
                    hsl_to_hex([p_h, 10, 11]),
                    0.25,
                ),
                "change": blend(p_dark_base, hsl_to_hex([p_h, 10, 11]), 0.25),
                "delete": blend(
                    hsl_to_hex([hue_red, 65, 68]), hsl_to_hex([p_h, 10, 11]), 0.25
                ),
                "text": blend(p_dark_base, hsl_to_hex([p_h, 10, 11]), 0.50),
            },
        },
        "light": {
            # ===== 亮色模式基调色 =====
            "primary": p_light_base,
            "primary_dim": p_light_dim,
            "primary_bright": p_light_bright,
            # ===== 背景与基础 UI =====
            "bg": hsl_to_hex([p_h, 8, 97]),
            "bg_dim": hsl_to_hex([p_h, 8, 88]),
            "bg_deep": hsl_to_hex([p_h, 8, 83]),
            "bg_highlight": hsl_to_hex([p_h, 8, 94]),
            "bg_search": hsl_to_hex([p_h, 25, 90]),
            "fg": hsl_to_hex([p_h, 10, 15]),
            "fg_muted": hsl_to_hex([p_h, 8, 38]),
            "fg_gutter": hsl_to_hex([p_h, 8, 52]),
            "fg_dark": hsl_to_hex([p_h, 8, 75]),
            "border": hsl_to_hex([p_h, 8, 75]),
            "border_highlight": p_light_base,
            "selection": hsl_to_hex([p_h, 8, 88]),
            "cursor_line": hsl_to_hex([p_h, 8, 100]),
            "float": {
                "bg": hsl_to_hex([p_h, 8, 94]),
                "fg": hsl_to_hex([p_h, 10, 15]),
                "border": hsl_to_hex([p_h, 8, 75]),
            },
            # ===== 真正标准的颜色 =====
            "blue": hsl_to_hex([hue_blue, 50, 42]),
            "blue_dim": hsl_to_hex([hue_blue, 40, 32]),
            "blue_bright": hsl_to_hex([hue_blue, 65, 50]),
            "cyan": hsl_to_hex([hue_cyan, 50, 38]),
            "green": hsl_to_hex([hue_green, 50, 36]),
            "green_bright": hsl_to_hex([hue_green, 60, 30]),
            "yellow": hsl_to_hex([hue_yellow, 65, 38]),
            "orange": hsl_to_hex([hue_orange, 60, 42]),
            "red": hsl_to_hex([hue_red, 60, 42]),
            "red_dim": hsl_to_hex([hue_red, 60, 32]),
            "purple": hsl_to_hex([hue_purple, 45, 42]),
            "pink": hsl_to_hex([hue_pink, 50, 44]),
            "comment": hsl_to_hex([p_h, 8, 52]),
            "terminal_black": hsl_to_hex([p_h, 8, 75]),
            "rosewater": hsl_to_hex([15, 45, 47]),
            "flamingo": hsl_to_hex([20, 50, 47]),
            "mauve": hsl_to_hex([260, 45, 42]),
            "maroon": hsl_to_hex([350, 55, 38]),
            "peach": hsl_to_hex([30, 60, 43]),
            "teal": hsl_to_hex([165, 40, 38]),
            "sky": hsl_to_hex([195, 45, 42]),
            "sapphire": hsl_to_hex([200, 45, 40]),
            "lavender": hsl_to_hex([230, 45, 44]),
            "git": {
                "add": hsl_to_hex([hue_green, 50, 36]),
                "change": p_light_base,
                "delete": hsl_to_hex([hue_red, 60, 42]),
            },
            "diag": {
                "error": hsl_to_hex([hue_red, 60, 42]),
                "warn": hsl_to_hex([hue_yellow, 65, 38]),
                "info": p_light_base,
                "hint": hsl_to_hex([hue_green, 50, 36]),
                "bg_error": blend(
                    hsl_to_hex([hue_red, 60, 42]), hsl_to_hex([p_h, 8, 97]), 0.15
                ),
                "bg_warn": blend(
                    hsl_to_hex([hue_yellow, 65, 38]),
                    hsl_to_hex([p_h, 8, 97]),
                    0.15,
                ),
                "bg_info": blend(p_light_base, hsl_to_hex([p_h, 8, 97]), 0.15),
                "bg_hint": blend(
                    hsl_to_hex([hue_green, 50, 36]),
                    hsl_to_hex([p_h, 8, 97]),
                    0.15,
                ),
            },
            "diff": {
                "add": blend(
                    hsl_to_hex([hue_green, 50, 36]),
                    hsl_to_hex([p_h, 8, 97]),
                    0.18,
                ),
                "change": blend(p_light_base, hsl_to_hex([p_h, 8, 97]), 0.18),
                "delete": blend(
                    hsl_to_hex([hue_red, 60, 42]), hsl_to_hex([p_h, 8, 97]), 0.18
                ),
                "text": blend(p_light_base, hsl_to_hex([p_h, 8, 97]), 0.35),
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate json palette with dedicated primary fields."
    )
    parser.add_argument("primary", help="Primary color in HEX format")
    parser.add_argument("output", help="Output JSON path")
    args = parser.parse_args()

    theme = build_theme(args.primary)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
