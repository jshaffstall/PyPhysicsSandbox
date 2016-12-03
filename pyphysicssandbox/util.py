def to_pygame(p):
    # Converts pymunk body position into pygame coordinate tuple
    return int(p.x), int(p.y)


def poly_centroid(vertices):
    centroid = [0, 0]
    area = 0.0

    for i in range(len(vertices)):
        x0, y0 = vertices[i]

        if i == len(vertices) - 1:
            x1, y1 = vertices[0]
        else:
            x1, y1 = vertices[i + 1]

        a = (x0 * y1 - x1 * y0)
        area += a
        centroid[0] += (x0 + x1) * a
        centroid[1] += (y0 + y1) * a

    area *= 0.5
    centroid[0] /= (6.0 * area)
    centroid[1] /= (6.0 * area)

    return centroid


