import argparse
import colorsys
import json


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    if len(hex_str) != 6:
        raise ValueError(f"Invalid HEX color: {hex_str}")
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


# --- 颜色变换工具 ---


def rotate_hue(hex_str, degree):
    h, s, l = hex_to_hsl(hex_str)
    return hsl_to_hex([(h + degree) % 360, s, l])


def set_lightness(hex_str, lightness):
    h, s, _ = hex_to_hsl(hex_str)
    return hsl_to_hex([h, s, max(0, min(100, lightness))])


def darken(hex_str, amount):
    h, s, l = hex_to_hsl(hex_str)
    return hsl_to_hex([h, s, max(0, l - amount)])


def lighten(hex_str, amount):
    h, s, l = hex_to_hsl(hex_str)
    return hsl_to_hex([h, s, min(100, l + amount)])


def desaturate(hex_str, amount):
    h, s, l = hex_to_hsl(hex_str)
    return hsl_to_hex([h, max(0, s - amount), l])


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


def generate_harmonized_palette(primary_hex):
    h, s, l = hex_to_hsl(primary_hex)

    # 提取基准饱和度，确保语义色不会过淡或过艳
    base_s = max(60.0, min(s, 80.0))

    # 锚定固定语义色相 (Hue)
    # Red: ~5°, Yellow/Amber: ~40°, Green: ~135°, Cyan/Blue: ~200°
    hue_red = 5
    hue_yellow = 40
    hue_green = 135
    hue_cyan = 185

    return {
        "primary": {
            "dark": hsl_to_hex([h, base_s, 68]),
            "light": hsl_to_hex([h, base_s, 42]),
        },
        "primary_fixed": {
            "dark": hsl_to_hex([h, base_s + 10, 82]),
            "light": hsl_to_hex([h, base_s + 10, 88]),
        },
        "primary_container": {
            "dark": hsl_to_hex([h, base_s - 15, 25]),
            "light": hsl_to_hex([h, base_s - 15, 90]),
        },
        "secondary": {
            "dark": hsl_to_hex([(h + 25) % 360, base_s - 10, 65]),
            "light": hsl_to_hex([(h + 25) % 360, base_s - 10, 40]),
        },
        "secondary_fixed": {
            "dark": hsl_to_hex([(h + 25) % 360, base_s, 78]),
            "light": hsl_to_hex([(h + 25) % 360, base_s, 88]),
        },
        "tertiary": {
            "dark": hsl_to_hex([(h - 25) % 360, base_s - 5, 70]),
            "light": hsl_to_hex([(h - 25) % 360, base_s - 5, 45]),
        },
        # 语义固定色定义
        "semantic": {
            "red": {
                "dark": hsl_to_hex([hue_red, base_s, 65]),
                "light": hsl_to_hex([hue_red, base_s + 10, 42]),
            },
            "yellow": {
                "dark": hsl_to_hex([hue_yellow, base_s, 68]),
                "light": hsl_to_hex([hue_yellow, base_s + 15, 38]),
            },
            "green": {
                "dark": hsl_to_hex([hue_green, base_s - 10, 62]),
                "light": hsl_to_hex([hue_green, base_s - 5, 36]),
            },
            "cyan": {
                "dark": hsl_to_hex([hue_cyan, base_s - 5, 66]),
                "light": hsl_to_hex([hue_cyan, base_s, 38]),
            },
        },
        "surface": {
            "dark": hsl_to_hex([h, 8, 11]),
            "light": hsl_to_hex([h, 8, 97]),
        },
        "surface_container_lowest": {
            "dark": hsl_to_hex([h, 10, 8]),
            "light": hsl_to_hex([h, 8, 100]),
        },
        "surface_container_low": {
            "dark": hsl_to_hex([h, 8, 13]),
            "light": hsl_to_hex([h, 8, 94]),
        },
        "surface_container": {
            "dark": hsl_to_hex([h, 8, 16]),
            "light": hsl_to_hex([h, 8, 91]),
        },
        "surface_container_high": {
            "dark": hsl_to_hex([h, 8, 19]),
            "light": hsl_to_hex([h, 8, 87]),
        },
        "surface_container_highest": {
            "dark": hsl_to_hex([h, 8, 23]),
            "light": hsl_to_hex([h, 8, 83]),
        },
        "on_surface": {
            "dark": hsl_to_hex([h, 5, 90]),
            "light": hsl_to_hex([h, 10, 15]),
        },
        "on_surface_variant": {
            "dark": hsl_to_hex([h, 6, 70]),
            "light": hsl_to_hex([h, 8, 38]),
        },
        "outline": {
            "dark": hsl_to_hex([h, 8, 48]),
            "light": hsl_to_hex([h, 8, 52]),
        },
        "outline_variant": {
            "dark": hsl_to_hex([h, 8, 28]),
            "light": hsl_to_hex([h, 8, 75]),
        },
    }


def build_theme(primary_hex):
    c = generate_harmonized_palette(primary_hex)

    # 快捷别名提取语义色彩
    sem = c["semantic"]

    red_d, red_l = sem["red"]["dark"], sem["red"]["light"]
    yellow_d, yellow_l = sem["yellow"]["dark"], sem["yellow"]["light"]
    green_d, green_l = sem["green"]["dark"], sem["green"]["light"]
    cyan_d, cyan_l = sem["cyan"]["dark"], sem["cyan"]["light"]

    return {
        "dark": {
            "bg": c["surface"]["dark"],
            "bg_dim": c["surface_container_low"]["dark"],
            "bg_deep": c["surface_container_lowest"]["dark"],
            "bg_highlight": c["surface_container_high"]["dark"],
            "bg_search": blend(
                c["primary_container"]["dark"],
                c["surface"]["dark"],
                0.6,
            ),
            "fg": c["on_surface"]["dark"],
            "fg_muted": c["on_surface_variant"]["dark"],
            "fg_gutter": c["outline_variant"]["dark"],
            "fg_dark": c["outline"]["dark"],
            "border": blend(
                c["outline_variant"]["dark"],
                c["surface"]["dark"],
                0.5,
            ),
            "border_highlight": c["primary"]["dark"],
            "selection": c["surface_container_highest"]["dark"],
            "cursor_line": c["surface_container"]["dark"],
            "float": {
                "bg": c["surface_container_low"]["dark"],
                "fg": c["on_surface"]["dark"],
                "border": c["outline_variant"]["dark"],
            },
            # Standard Colors
            "blue": c["primary"]["dark"],
            "blue_dim": desaturate(darken(c["primary"]["dark"], 15), 10),
            "blue_bright": c["primary_fixed"]["dark"],
            "cyan": cyan_d,
            "green": green_d,
            "green_bright": lighten(green_d, 10),
            "yellow": yellow_d,
            "orange": rotate_hue(red_d, 25),
            "red": red_d,
            "red_dim": darken(red_d, 15),
            "purple": rotate_hue(c["primary"]["dark"], 25),
            "pink": rotate_hue(red_d, 330),
            "comment": c["outline"]["dark"],
            "terminal_black": c["surface_container_highest"]["dark"],
            # Extended Palette (Catppuccin Style)
            "rosewater": rotate_hue(red_d, 15),
            "flamingo": rotate_hue(red_d, 25),
            "mauve": rotate_hue(c["primary"]["dark"], 30),
            "maroon": darken(red_d, 10),
            "peach": rotate_hue(yellow_d, -15),
            "teal": rotate_hue(green_d, 30),
            "sky": rotate_hue(cyan_d, 15),
            "sapphire": rotate_hue(c["primary"]["dark"], -10),
            "lavender": rotate_hue(c["primary"]["dark"], 15),
            "git": {
                "add": green_d,
                "change": c["primary"]["dark"],
                "delete": red_d,
            },
            # 强化强固定的 Diagnostcs (Error=红, Warn=黄, Info=蓝/主色, Hint=绿)
            "diag": {
                "error": red_d,
                "warn": yellow_d,
                "info": c["primary"]["dark"],
                "hint": green_d,
                "bg_error": blend(red_d, c["surface"]["dark"], 0.15),
                "bg_warn": blend(yellow_d, c["surface"]["dark"], 0.15),
                "bg_info": blend(c["primary"]["dark"], c["surface"]["dark"], 0.15),
                "bg_hint": blend(green_d, c["surface"]["dark"], 0.15),
            },
            "diff": {
                "add": blend(green_d, c["surface"]["dark"], 0.20),
                "change": blend(c["primary"]["dark"], c["surface"]["dark"], 0.20),
                "delete": blend(red_d, c["surface"]["dark"], 0.20),
                "text": blend(c["primary"]["dark"], c["surface"]["dark"], 0.40),
            },
        },
        "light": {
            "bg": c["surface"]["light"],
            "bg_dim": c["surface_container_high"]["light"],
            "bg_deep": c["surface_container_highest"]["light"],
            "bg_highlight": c["surface_container_low"]["light"],
            "bg_search": c["primary_container"]["light"],
            "fg": c["on_surface"]["light"],
            "fg_muted": c["on_surface_variant"]["light"],
            "fg_gutter": c["outline"]["light"],
            "fg_dark": c["outline_variant"]["light"],
            "border": c["outline_variant"]["light"],
            "border_highlight": c["primary"]["light"],
            "selection": c["surface_container_high"]["light"],
            "cursor_line": c["surface_container_lowest"]["light"],
            "float": {
                "bg": c["surface_container_low"]["light"],
                "fg": c["on_surface"]["light"],
                "border": c["outline_variant"]["light"],
            },
            # Standard Colors
            "blue": set_lightness(c["primary"]["light"], 40),
            "blue_dim": set_lightness(c["primary"]["light"], 30),
            "blue_bright": set_lightness(c["primary"]["light"], 48),
            "cyan": cyan_l,
            "green": green_l,
            "green_bright": set_lightness(green_l, 30),
            "yellow": yellow_l,
            "orange": rotate_hue(red_l, 25),
            "red": red_l,
            "red_dim": set_lightness(red_l, 32),
            "purple": set_lightness(rotate_hue(c["primary"]["light"], 25), 40),
            "pink": set_lightness(rotate_hue(red_l, 330), 42),
            "comment": c["outline"]["light"],
            "terminal_black": c["outline_variant"]["light"],
            # Extended Palette (Catppuccin Style)
            "rosewater": rotate_hue(red_l, 15),
            "flamingo": rotate_hue(red_l, 25),
            "mauve": set_lightness(rotate_hue(c["primary"]["light"], 30), 40),
            "maroon": set_lightness(red_l, 35),
            "peach": rotate_hue(yellow_l, -15),
            "teal": rotate_hue(green_l, 30),
            "sky": rotate_hue(cyan_l, 15),
            "sapphire": set_lightness(rotate_hue(c["primary"]["light"], -10), 38),
            "lavender": set_lightness(rotate_hue(c["primary"]["light"], 15), 42),
            "git": {
                "add": green_l,
                "change": set_lightness(c["primary"]["light"], 40),
                "delete": red_l,
            },
            # 强化强固定的 Diagnostcs (Error=红, Warn=黄, Info=蓝色/主色, Hint=绿)
            "diag": {
                "error": red_l,
                "warn": yellow_l,
                "info": set_lightness(c["primary"]["light"], 38),
                "hint": green_l,
                "bg_error": blend(red_l, c["surface"]["light"], 0.12),
                "bg_warn": blend(yellow_l, c["surface"]["light"], 0.12),
                "bg_info": blend(
                    set_lightness(c["primary"]["light"], 38),
                    c["surface"]["light"],
                    0.12,
                ),
                "bg_hint": blend(green_l, c["surface"]["light"], 0.12),
            },
            "diff": {
                "add": blend(green_l, c["surface"]["light"], 0.15),
                "change": blend(
                    set_lightness(c["primary"]["light"], 40),
                    c["surface"]["light"],
                    0.15,
                ),
                "delete": blend(red_l, c["surface"]["light"], 0.15),
                "text": blend(
                    set_lightness(c["primary"]["light"], 40),
                    c["surface"]["light"],
                    0.30,
                ),
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate a harmonized dark/light theme with strict semantic colors from a primary HEX color."
    )

    parser.add_argument(
        "primary",
        help="Primary color in HEX format, e.g. #ffb4a7",
    )

    parser.add_argument(
        "output",
        help="Output JSON file path, e.g. ./theme.json",
    )

    args = parser.parse_args()

    try:
        hex_to_rgb(args.primary)
        theme = build_theme(args.primary)

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(theme, f, indent=2, ensure_ascii=False)
            f.write("\n")

    except ValueError as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
