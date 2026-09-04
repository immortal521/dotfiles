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
    h = (hsl[0] % 360) / 360.0
    s = max(0.0, min(100.0, hsl[1])) / 100.0
    l = max(0.0, min(100.0, hsl[2])) / 100.0
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


def min_dist_hue(target_h, reference_h, weight=0.2):
    """
    计算沿着色相环最短路径向主色 reference_h 偏移后的色相。
    weight 为向主色拉近的权重 (0.0~1.0)，既保持语义认知，又拉近与主色的调性。
    """
    diff = (reference_h - target_h + 180) % 360 - 180
    return (target_h + diff * weight) % 360


def build_dynamic_hue(p_h, offset):
    """根据主色 HSL 的色相，按角度动态偏移出和谐色相"""
    return (p_h + offset) % 360


def build_theme(primary_hex, mode="dark"):
    p_h, p_s, p_l = hex_to_hsl(primary_hex)
    is_dark = mode == "dark"

    # 背景底色基准饱和度
    base_s = max(10.0, min(p_s * 0.3, 20.0))

    p_base = primary_hex
    p_dim = hsl_to_hex([p_h, p_s, p_l - (12 if is_dark else -10)])
    p_bright = hsl_to_hex([p_h, min(100.0, p_s + 15), p_l + (12 if is_dark else -10)])

    hue_analogous_1 = build_dynamic_hue(p_h, -30)
    hue_analogous_2 = build_dynamic_hue(p_h, 30)
    hue_complementary = build_dynamic_hue(p_h, 180)
    hue_triadic_1 = build_dynamic_hue(p_h, 120)
    hue_triadic_2 = build_dynamic_hue(p_h, 240)

    # 动态将标准语义色相向主色（p_h）靠拢 20%
    red_h = min_dist_hue(0, p_h, 0.20)
    orange_h = min_dist_hue(25, p_h, 0.20)
    yellow_h = min_dist_hue(45, p_h, 0.20)
    green_h = min_dist_hue(140, p_h, 0.20)
    cyan_h = min_dist_hue(180, p_h, 0.20)
    blue_h = min_dist_hue(215, p_h, 0.20)
    purple_h = min_dist_hue(270, p_h, 0.20)
    pink_h = min_dist_hue(330, p_h, 0.20)

    if is_dark:
        bg = hsl_to_hex([p_h, base_s, 14])
        bg_dim = hsl_to_hex([p_h, base_s, 17])
        bg_deep = hsl_to_hex([p_h, base_s, 10])
        bg_highlight = hsl_to_hex([p_h, base_s, 22])
        bg_search = hsl_to_hex([p_h, max(p_s, 45.0), 26])

        fg = hsl_to_hex([p_h, 10, 94])
        fg_muted = hsl_to_hex([p_h, 10, 72])
        fg_gutter = hsl_to_hex([p_h, 8, 38])
        fg_dark = hsl_to_hex([p_h, 8, 52])

        border = hsl_to_hex([p_h, base_s, 26])

        red = hsl_to_hex([red_h, 85, 72])
        yellow = hsl_to_hex([yellow_h, 90, 72])
        green = hsl_to_hex([green_h, 75, 68])
        cyan = hsl_to_hex([cyan_h, 75, 70])
        blue = hsl_to_hex([blue_h, 85, 78])
        purple = hsl_to_hex([purple_h, 80, 78])
        orange = hsl_to_hex([orange_h, 88, 70])

        rosewater = hsl_to_hex([hue_analogous_1, 65, 80])
        flamingo = hsl_to_hex([hue_analogous_1, 75, 75])
        mauve = hsl_to_hex([hue_triadic_2, 70, 78])
        maroon = hsl_to_hex([build_dynamic_hue(p_h, 340), 75, 68])
        peach = hsl_to_hex([hue_analogous_2, 80, 75])
        teal = hsl_to_hex([hue_triadic_1, 65, 72])
        sky = hsl_to_hex([hue_complementary, 70, 75])
        sapphire = hsl_to_hex([hue_complementary, 75, 70])
        lavender = hsl_to_hex([hue_triadic_2, 65, 80])

    else:  # Light Mode
        bg = hsl_to_hex([p_h, base_s, 97])
        bg_dim = hsl_to_hex([p_h, base_s, 91])
        bg_deep = hsl_to_hex([p_h, base_s, 85])
        bg_highlight = hsl_to_hex([p_h, base_s, 94])
        bg_search = hsl_to_hex([p_h, max(p_s, 35.0), 88])

        fg = hsl_to_hex([p_h, 20, 12])
        fg_muted = hsl_to_hex([p_h, 15, 38])
        fg_gutter = hsl_to_hex([p_h, 10, 58])
        fg_dark = hsl_to_hex([p_h, 10, 72])

        border = hsl_to_hex([p_h, base_s, 76])

        red = hsl_to_hex([red_h, 85, 42])
        yellow = hsl_to_hex([yellow_h, 100, 30])
        green = hsl_to_hex([green_h, 85, 33])
        cyan = hsl_to_hex([cyan_h, 85, 34])
        blue = hsl_to_hex([blue_h, 85, 42])
        purple = hsl_to_hex([purple_h, 75, 42])
        orange = hsl_to_hex([orange_h, 95, 38])

        rosewater = hsl_to_hex([hue_analogous_1, 75, 42])
        flamingo = hsl_to_hex([hue_analogous_1, 80, 40])
        mauve = hsl_to_hex([hue_triadic_2, 75, 38])
        maroon = hsl_to_hex([build_dynamic_hue(p_h, 340), 80, 38])
        peach = hsl_to_hex([hue_analogous_2, 90, 36])
        teal = hsl_to_hex([hue_triadic_1, 80, 32])
        sky = hsl_to_hex([hue_complementary, 80, 35])
        sapphire = hsl_to_hex([hue_complementary, 85, 36])
        lavender = hsl_to_hex([hue_triadic_2, 70, 44])

    cursor_line = blend(p_base, bg, 0.18 if is_dark else 0.10)
    
    # ---------- 选区颜色优化 ----------
    # 暗色模式下：基色明度由 65.0 提升至 72.0，混合比例 alpha 由 0.38 降低至 0.22
    # 这样生成的选区背景既有主色的柔和色彩感，又更通明亮丽，不显得过于浑浊/深沉。
    p_selection_base = hsl_to_hex([p_h, max(p_s, 70.0), 72.0 if is_dark else 45.0])
    selection = blend(p_selection_base, bg, 0.22 if is_dark else 0.25)

    return {
        "primary": p_base,
        "primary_dim": p_dim,
        "primary_bright": p_bright,
        "bg": bg,
        "bg_dim": bg_dim,
        "bg_deep": bg_deep,
        "bg_highlight": bg_highlight,
        "bg_search": bg_search,
        "fg": fg,
        "fg_muted": fg_muted,
        "fg_gutter": fg_gutter,
        "fg_dark": fg_dark,
        "border": border,
        "border_highlight": p_base,
        "selection": selection,
        "cursor_line": cursor_line,
        "float": {
            "bg": bg_dim,
            "fg": fg,
            "border": border,
        },
        "blue": blue,
        "blue_dim": blend(blue, bg, 0.6),
        "blue_bright": hsl_to_hex([blue_h, 90, 82 if is_dark else 35]),
        "cyan": cyan,
        "green": green,
        "green_bright": hsl_to_hex([green_h, 85, 78 if is_dark else 30]),
        "yellow": yellow,
        "orange": orange,
        "red": red,
        "red_dim": blend(red, bg, 0.6),
        "purple": purple,
        "pink": hsl_to_hex([pink_h, 75, 75 if is_dark else 42]),
        "comment": fg_gutter,
        "terminal_black": hsl_to_hex([p_h, base_s, 26 if is_dark else 75]),
        "rosewater": rosewater,
        "flamingo": flamingo,
        "mauve": mauve,
        "maroon": maroon,
        "peach": peach,
        "teal": teal,
        "sky": sky,
        "sapphire": sapphire,
        "lavender": lavender,
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
            "bg_error": blend(red, bg, 0.18),
            "bg_warn": blend(yellow, bg, 0.18),
            "bg_info": blend(p_base, bg, 0.18),
            "bg_hint": blend(green, bg, 0.18),
        },
        "diff": {
            "add": blend(green, bg, 0.20),
            "change": blend(p_base, bg, 0.20),
            "delete": blend(red, bg, 0.20),
            "text": blend(p_base, bg, 0.45),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate dynamic single-mode JSON palette derived from a primary color."
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
