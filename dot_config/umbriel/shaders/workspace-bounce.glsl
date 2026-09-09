vec4 animation(vec2 uv) {
    float progress = umbriel_clamped_progress;

    // Small overshoot near the end of the transition.
    float overshoot = sin(3.14159265 * progress);

    // Make the overshoot happen after the main movement.
    overshoot *= smoothstep(0.55, 0.9, progress);

    float direction = umbriel_direction > 0.0 ? 1.0 : -1.0;

    vec2 sample_uv = uv;
    sample_uv.x += direction * overshoot * 0.015;

    return umbriel_sample(sample_uv);
}
