import math, itertools


def lines_intersection(k1: float, c1: float, k2: float, c2: float) -> tuple | None:
    """

    :param k1:
    :param c1:
    :param k2:
    :param c2:
    :return:

    Ця функція приймає чотири числа (кожне з чисел ціле або з плаваючою комою) та
    повертає кортеж з двох чисел з плаваючою комою - значення кординат (x,y)
    точки перетину двох прямих (числа заокруглені до 2 знаків після коми).
    Якщо прямі паралельні, або співпадають, функція повинна повернути None.
    """

    if k1 == k2:
        return None
    return round(x := (c2 - c1) / (k1 - k2), 10), round(k1 * x + c1, 10)


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:

    Ця функція приймає чотири числа (кожне з чисел ціле або з плаваючою комою),
    що є координатами двох точок. Функція повертає відстань між цими точками
    (число з плаваючою комою заокруглене до 2-х знаків після коми).
    """

    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)


def collinearity_check(point1, point2, point3):

    # here we use the requested in the instructions function distance()
    side1 = distance(*point1, *point2)
    side2 = distance(*point1, *point3)
    side3 = distance(*point2, *point3)

    s = (side1 + side2 + side3) / 2    # semi perimeter
    area_squared = s * (s - side1) * (s - side2) * (s - side3)    # heron's formula

    if area_squared < 0 or math.sqrt(area_squared) < 0.5:
        return True

    return False


def is_quadrilateral(vertice1, vertice2, vertice3, vertice4):
    for points_to_check_for_collinearity in itertools.combinations([vertice1, vertice2, vertice3, vertice4], 3):
        if collinearity_check(*points_to_check_for_collinearity):
            return False
    return True


def area_sign(x1, y1, x2, y2, x3, y3):
    return x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)


def is_convex_quadrilateral(point1, point2, point3, point4):
    sign1 = area_sign(point1[0], point1[1], point2[0], point2[1], point3[0], point3[1])
    sign2 = area_sign(point2[0], point2[1], point3[0], point3[1], point4[0], point4[1])
    sign3 = area_sign(point3[0], point3[1], point4[0], point4[1], point1[0], point1[1])
    sign4 = area_sign(point4[0], point4[1], point1[0], point1[1], point2[0], point2[1])

    return (sign1 > 0 and sign2 > 0 and sign3 > 0 and sign4 > 0) or \
        (sign1 < 0 and sign2 < 0 and sign3 < 0 and sign4 < 0)


def four_lines_area(k1: float, c1: float, k2: float, c2: float, k3: float, c3: float, k4: float, c4: float):
    """

    :param k1:
    :param c1:
    :param k2:
    :param c2:
    :param k3:
    :param c3:
    :param k4:
    :param c4:
    :return:

    >>> four_lines_area(-0.5, 5, 0.5, 5, 1, -4, -1, -4)
    [54.0, 243.0, 288.0]
    """

    coefficients = [k1, k2, k3, k4]
    intercepts = [c1, c2, c3, c4]
    line_functions = list(zip(coefficients, intercepts))
    intersection_points = []

    for i, line_function1 in enumerate(line_functions):
        # check if 3 or more lines are parallel, if so return 0 as they do not form a quadrangle
        if coefficients.count(coefficients[i]) >= 3:
            return 0

        # find all possible intersections, do not append duplicates
        for line_function2 in line_functions:
            if (intersection := lines_intersection(*line_function1, *line_function2)) not in intersection_points:
                intersection_points.append(intersection)

    # remove all None elements received from trying to find the intersection of two parallel lines
    intersection_points.remove(None)

    quadrilaterals = []

    for four_points in itertools.combinations(intersection_points, 4):
        if is_quadrilateral(*four_points):
            quadrilaterals.append(order_points(four_points))

    areas = []

    for quadrilateral in quadrilaterals:
        areas.append(shoelace_formula(*quadrilateral))

    print("The interception points of the four lines you provided create the following quadrilaterals:\n")
    for i, quadrilateral in enumerate(quadrilaterals):
        print(f"Quadrilateral №{i + 1} | vertices: {quadrilateral} | area: {areas[i]}")

    return list(areas)


def order_points(points):
    centroid_x = 0
    centroid_y = 0

    # this code adds every x and y value and then divides the sum by the quantity of points,
    # effectively providing us with arithmetic means of x and y values which form a centroid
    for x, y in points:
        centroid_x += x
        centroid_y += y

    centroid_x /= len(points)
    centroid_y /= len(points)

    # then we calculate the angle between any given point and the centroid
    def angle_from_centroid(point):
        return math.atan2(point[1] - centroid_y, point[0] - centroid_x)

    # and sort the points by their angle relative to the centroid
    return sorted(points, key=angle_from_centroid)


def shoelace_formula(point1, point2, point3, point4):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    return round(0.5 * abs(x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1 - (y1 * x2 + y2 * x3 + y3 * x4 + y4 * x1)), 2)


def quadrangle_area(a: float, b: float, c: float, d: float, f1: float, f2: float) -> float | None:
    """

    :param a:
    :param b:
    :param c:
    :param d:
    :param f1:
    :param f2:
    :return:

    Ця функція приймає шість чисел (кожне з чисел ціле або з плаваючою комою),
    які представляють довжини сторін та довжини діагоналей чотирикутника і
    повертає площу чотирикутника (число заокруглене до 2 знаків після коми).
    Якщо такого чотирикутника не існує, то функція повертає None.
    """
    if (area_squared := 4 * f1 ** 2 * f2 ** 2 - math.pow(b ** 2 + d ** 2 - a ** 2 - c ** 2, 2)) < 0:
        return None
    return round(math.sqrt(area_squared))
