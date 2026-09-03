import argparse
import colorsys
import json


# --- HSL/RGB 基础转换 ---


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


# --- 链式颜色变换 ---


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


# --- 调色板生成 ---


def generate_harmonized_palette(primary_hex):
    h, s, l = hex_to_hsl(primary_hex)

    base_s = max(55.0, min(s, 75.0))

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
        "error": {
            "dark": "#E56B6B",
            "light": "#C53030",
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
            "statusline": {
                "bg": c["surface_container_low"]["dark"],
                "fg": c["on_surface_variant"]["dark"],
                "active": c["on_surface"]["dark"],
                "inactive": c["outline"]["dark"],
            },
            "blue": c["primary"]["dark"],
            "blue_dim": desaturate(
                darken(c["primary"]["dark"], 15),
                10,
            ),
            "blue_bright": c["primary_fixed"]["dark"],
            "cyan": c["tertiary"]["dark"],
            "green": c["secondary"]["dark"],
            "green_bright": c["secondary_fixed"]["dark"],
            "yellow": lighten(
                rotate_hue(c["tertiary"]["dark"], -20),
                8,
            ),
            "orange": rotate_hue(c["error"]["dark"], 20),
            "red": c["error"]["dark"],
            "red_dim": darken(c["error"]["dark"], 15),
            "purple": rotate_hue(c["primary"]["dark"], 20),
            "pink": rotate_hue(c["tertiary"]["dark"], 15),
            "comment": c["outline"]["dark"],
            "terminal_black": c["surface_container_highest"]["dark"],
            "git": {
                "add": c["secondary"]["dark"],
                "change": c["primary"]["dark"],
                "delete": c["error"]["dark"],
            },
            "diag": {
                "error": c["error"]["dark"],
                "warn": rotate_hue(c["tertiary"]["dark"], -20),
                "info": c["primary"]["dark"],
                "hint": c["secondary"]["dark"],
                "bg_error": blend(
                    c["error"]["dark"],
                    c["surface"]["dark"],
                    0.15,
                ),
                "bg_warn": blend(
                    rotate_hue(c["tertiary"]["dark"], -20),
                    c["surface"]["dark"],
                    0.15,
                ),
                "bg_info": blend(
                    c["primary"]["dark"],
                    c["surface"]["dark"],
                    0.15,
                ),
                "bg_hint": blend(
                    c["secondary"]["dark"],
                    c["surface"]["dark"],
                    0.15,
                ),
            },
            "diff": {
                "add": blend(
                    c["secondary"]["dark"],
                    c["surface"]["dark"],
                    0.20,
                ),
                "change": blend(
                    c["primary"]["dark"],
                    c["surface"]["dark"],
                    0.20,
                ),
                "delete": blend(
                    c["error"]["dark"],
                    c["surface"]["dark"],
                    0.20,
                ),
                "text": blend(
                    c["primary"]["dark"],
                    c["surface"]["dark"],
                    0.40,
                ),
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
            "statusline": {
                "bg": c["surface_container_low"]["light"],
                "fg": c["on_surface_variant"]["light"],
                "active": c["on_surface"]["light"],
                "inactive": c["outline"]["light"],
            },
            "blue": set_lightness(c["primary"]["light"], 40),
            "blue_dim": set_lightness(c["primary"]["light"], 30),
            "blue_bright": set_lightness(c["primary"]["light"], 48),
            "cyan": set_lightness(c["tertiary"]["light"], 38),
            "green": set_lightness(c["secondary"]["light"], 36),
            "green_bright": set_lightness(c["secondary"]["light"], 30),
            "yellow": set_lightness(
                rotate_hue(c["tertiary"]["light"], -20),
                40,
            ),
            "orange": set_lightness(
                rotate_hue(c["error"]["light"], 20),
                38,
            ),
            "red": set_lightness(c["error"]["light"], 42),
            "red_dim": set_lightness(c["error"]["light"], 32),
            "purple": set_lightness(
                rotate_hue(c["primary"]["light"], 20),
                40,
            ),
            "pink": set_lightness(
                rotate_hue(c["tertiary"]["light"], 15),
                42,
            ),
            "comment": c["outline"]["light"],
            "terminal_black": c["outline_variant"]["light"],
            "git": {
                "add": set_lightness(c["secondary"]["light"], 36),
                "change": set_lightness(c["primary"]["light"], 40),
                "delete": set_lightness(c["error"]["light"], 42),
            },
            "diag": {
                "error": set_lightness(c["error"]["light"], 42),
                "warn": set_lightness(
                    rotate_hue(c["tertiary"]["light"], -20),
                    40,
                ),
                "info": set_lightness(c["primary"]["light"], 38),
                "hint": set_lightness(c["secondary"]["light"], 36),
                "bg_error": blend(
                    set_lightness(c["error"]["light"], 42),
                    c["surface"]["light"],
                    0.12,
                ),
                "bg_warn": blend(
                    set_lightness(
                        rotate_hue(c["tertiary"]["light"], -20),
                        40,
                    ),
                    c["surface"]["light"],
                    0.12,
                ),
                "bg_info": blend(
                    set_lightness(c["primary"]["light"], 38),
                    c["surface"]["light"],
                    0.12,
                ),
                "bg_hint": blend(
                    set_lightness(c["secondary"]["light"], 36),
                    c["surface"]["light"],
                    0.12,
                ),
            },
            "diff": {
                "add": blend(
                    set_lightness(c["secondary"]["light"], 36),
                    c["surface"]["light"],
                    0.15,
                ),
                "change": blend(
                    set_lightness(c["primary"]["light"], 40),
                    c["surface"]["light"],
                    0.15,
                ),
                "delete": blend(
                    set_lightness(c["error"]["light"], 42),
                    c["surface"]["light"],
                    0.15,
                ),
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
        description="Generate a harmonized dark/light theme from a primary HEX color."
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
        # 提前验证颜色
        hex_to_rgb(args.primary)

        theme = build_theme(args.primary)

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(theme, f, indent=2, ensure_ascii=False)
            f.write("\n")

    except ValueError as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
