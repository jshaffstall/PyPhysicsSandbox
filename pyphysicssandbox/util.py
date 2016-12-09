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


def poly_area(vertices):
    n = len(vertices)  # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result
