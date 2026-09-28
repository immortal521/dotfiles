vec4 animation(vec2 uv) {
    // 0 -> 1 for the entire animation.
    float progress = umbriel_clamped_progress;

    // Smooth pulse:
    // 0 at the beginning/end, 1 at the midpoint.
    float pulse = sin(3.14159265 * progress);

    // Slightly compress the window horizontally and vertically.
    float scale_x = 1.0 - 0.02 * pulse;
    float scale_y = 1.0 - 0.045 * pulse;

    // Transform around the center of the window.
    vec2 centered = uv - vec2(0.5);

    vec2 sample_uv = centered / vec2(scale_x, scale_y) + vec2(0.5);

    return umbriel_sample(sample_uv);
}
