vec4 animation(vec2 uv) {
    float progress = umbriel_clamped_progress;

    // Smooth pulse: 0 at both endpoints, 1 at the midpoint.
    float pulse = sin(3.14159265 * progress);

    // Keep the window centered while slightly compressing it.
    float scale_x = 1.0 - 0.02 * pulse;
    float scale_y = 1.0 - 0.045 * pulse;

    vec2 centered = uv - vec2(0.5);

    vec2 sample_uv = vec2(
        centered.x / scale_x,
        centered.y / scale_y
    ) + vec2(0.5);

    return umbriel_sample(sample_uv);
}
