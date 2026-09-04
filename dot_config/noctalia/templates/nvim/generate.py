import argparse
import colorsys
import json


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    r, g, b = [max(0, min(255, round(x * 255))) for x in rgb]
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


def adjust_lightness(p_h, p_s, target_l):
    """根据主色的色相/饱和度调整亮度"""
    return hsl_to_hex([p_h, p_s, max(0.0, min(100.0, target_l))])


def build_theme(primary_hex, mode="dark"):
    p_h, p_s, p_l = hex_to_hsl(primary_hex)

    # 保持主色与输入的源主色一致
    p_base = primary_hex

    hue_blue = 210
    hue_cyan = 185
    hue_green = 135
    hue_yellow = 40
    hue_orange = 25
    hue_red = 5
    hue_purple = 270
    hue_pink = 330

    if mode == "dark":
        p_dim = adjust_lightness(p_h, p_s, p_l - 12)
        p_bright = adjust_lightness(p_h, p_s, p_l + 12)

        bg = hsl_to_hex([p_h, 10, 11])
        red = hsl_to_hex([hue_red, 65, 68])
        yellow = hsl_to_hex([hue_yellow, 60, 70])
        green = hsl_to_hex([hue_green, 50, 65])

        # 关联主色的 cursor_line 与 selection
        # cursor_line: 在背景色基础上融入约 8% 的主色高亮
        cursor_line = blend(p_base, bg, 0.08)
        # selection: 融入约 25% 的主色，提供协调且清晰的选中效果
        selection = blend(p_base, bg, 0.25)

        return {
            "primary": p_base,
            "primary_dim": p_dim,
            "primary_bright": p_bright,
            "bg": bg,
            "bg_dim": hsl_to_hex([p_h, 10, 13]),
            "bg_deep": hsl_to_hex([p_h, 10, 8]),
            "bg_highlight": hsl_to_hex([p_h, 10, 19]),
            "bg_search": hsl_to_hex([p_h, 30, 20]),
            "fg": hsl_to_hex([p_h, 5, 90]),
            "fg_muted": hsl_to_hex([p_h, 5, 70]),
            "fg_gutter": hsl_to_hex([p_h, 5, 30]),
            "fg_dark": hsl_to_hex([p_h, 5, 48]),
            "border": hsl_to_hex([p_h, 8, 20]),
            "border_highlight": p_base,
            "selection": selection,
            "cursor_line": cursor_line,
            "float": {
                "bg": hsl_to_hex([p_h, 10, 13]),
                "fg": hsl_to_hex([p_h, 5, 90]),
                "border": hsl_to_hex([p_h, 5, 30]),
            },
            "blue": hsl_to_hex([hue_blue, 65, 75]),
            "blue_dim": hsl_to_hex([hue_blue, 50, 60]),
            "blue_bright": hsl_to_hex([hue_blue, 80, 85]),
            "cyan": hsl_to_hex([hue_cyan, 55, 68]),
            "green": green,
            "green_bright": hsl_to_hex([hue_green, 60, 75]),
            "yellow": yellow,
            "orange": hsl_to_hex([hue_orange, 60, 70]),
            "red": red,
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
                "add": green,
                "change": p_base,
                "delete": red,
            },
            "diag": {
                "error": red,
                "warn": yellow,
                "info": p_base,
                "hint": green,
                "bg_error": blend(red, bg, 0.2),
                "bg_warn": blend(yellow, bg, 0.2),
                "bg_info": blend(p_base, bg, 0.2),
                "bg_hint": blend(green, bg, 0.2),
            },
            "diff": {
                "add": blend(green, bg, 0.25),
                "change": blend(p_base, bg, 0.25),
                "delete": blend(red, bg, 0.25),
                "text": blend(p_base, bg, 0.50),
            },
        }

    else:  # mode == "light"
        p_dim = adjust_lightness(p_h, p_s, p_l - 10)
        p_bright = adjust_lightness(p_h, p_s, p_l + 10)

        bg = hsl_to_hex([p_h, 8, 97])
        red = hsl_to_hex([hue_red, 60, 42])
        yellow = hsl_to_hex([hue_yellow, 65, 38])
        green = hsl_to_hex([hue_green, 50, 36])

        # 亮色模式下同样融入主色
        # cursor_line: 极轻微的主色着色（约 5% 透明度）
        cursor_line = blend(p_base, bg, 0.05)
        # selection: 柔和的浅主色选中区（约 18% 透明度）
        p_selection_base = hsl_to_hex([p_h, max(p_s, 65.0), min(p_l, 50.0)])
        selection = blend(p_selection_base, bg, 0.32)

        return {
            "primary": p_base,
            "primary_dim": p_dim,
            "primary_bright": p_bright,
            "bg": bg,
            "bg_dim": hsl_to_hex([p_h, 8, 88]),
            "bg_deep": hsl_to_hex([p_h, 8, 83]),
            "bg_highlight": hsl_to_hex([p_h, 8, 94]),
            "bg_search": hsl_to_hex([p_h, 25, 90]),
            "fg": hsl_to_hex([p_h, 10, 15]),
            "fg_muted": hsl_to_hex([p_h, 8, 38]),
            "fg_gutter": hsl_to_hex([p_h, 8, 52]),
            "fg_dark": hsl_to_hex([p_h, 8, 75]),
            "border": hsl_to_hex([p_h, 8, 75]),
            "border_highlight": p_base,
            "selection": selection,
            "cursor_line": cursor_line,
            "float": {
                "bg": hsl_to_hex([p_h, 8, 94]),
                "fg": hsl_to_hex([p_h, 10, 15]),
                "border": hsl_to_hex([p_h, 8, 75]),
            },
            "blue": hsl_to_hex([hue_blue, 50, 42]),
            "blue_dim": hsl_to_hex([hue_blue, 40, 32]),
            "blue_bright": hsl_to_hex([hue_blue, 65, 50]),
            "cyan": hsl_to_hex([hue_cyan, 50, 38]),
            "green": green,
            "green_bright": hsl_to_hex([hue_green, 60, 30]),
            "yellow": yellow,
            "orange": hsl_to_hex([hue_orange, 60, 42]),
            "red": red,
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
                "add": green,
                "change": p_base,
                "delete": red,
            },
            "diag": {
                "error": red,
                "warn": yellow,
                "info": p_base,
                "hint": green,
                "bg_error": blend(red, bg, 0.15),
                "bg_warn": blend(yellow, bg, 0.15),
                "bg_info": blend(p_base, bg, 0.15),
                "bg_hint": blend(green, bg, 0.15),
            },
            "diff": {
                "add": blend(green, bg, 0.18),
                "change": blend(p_base, bg, 0.18),
                "delete": blend(red, bg, 0.18),
                "text": blend(p_base, bg, 0.35),
            },
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate single-mode JSON palette derived from a primary color."
    )
    parser.add_argument("primary", help="Primary color in HEX format (e.g. #7aa2f7)")
    parser.add_argument("output", help="Output JSON file path")
    parser.add_argument(
        "--mode",
        choices=["dark", "light"],
        default="dark",
        help="Generate mode: 'dark' or 'light' (default: dark)",
    )
    args = parser.parse_args()

    palette = build_theme(args.primary, mode=args.mode)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(palette, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
