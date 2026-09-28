vec4 animation(vec2 uv) {
    // Distance from the top-right corner in logical pixels.
    vec2 position = (vec2(1.0, 0.0) - uv) * umbriel_size;

    float distance = length(position);
    float max_distance = length(umbriel_size);
    float normalized_distance = distance / max_distance;

    // 0 -> 1 when entering, 1 -> 0 when leaving.
    float progress = umbriel_clamped_progress;

    if (umbriel_direction < 0.0) {
        progress = 1.0 - progress;
    }

    // Soft reveal boundary.
    const float edge = 0.05;

    float alpha = 1.0 - smoothstep(
        progress - edge,
        progress + edge,
        normalized_distance
    );

    return umbriel_sample(uv) * alpha;
}
