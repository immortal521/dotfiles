vec4 animation(vec2 uv) {
    float progress = umbriel_direction > 0.0
        ? umbriel_clamped_progress
        : 1.0 - umbriel_clamped_progress;

    // Convert normalized coordinates to logical coordinates.
    // This keeps the reveal circular regardless of window aspect ratio.
    vec2 p = (vec2(1.0, 0.0) - uv) * umbriel_size;

    // Distance from the top-right corner.
    float distance = length(p);

    // Maximum distance needed to cover the whole window.
    float max_distance = length(umbriel_size);

    float normalized_distance = distance / max_distance;

    // Soft reveal edge.
    float edge = 0.05;

    float alpha = 1.0 - smoothstep(
        progress - edge,
        progress + edge,
        normalized_distance
    );

    return umbriel_sample(uv) * alpha;
}
