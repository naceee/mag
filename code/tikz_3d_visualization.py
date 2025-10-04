import plotly.graph_objects as go
import math
import pandas as pd

from point_sampling import remove_dominated_points, get_non_dominated_points, epsilon_net, epsilon_net_from_square
from main import get_kink_points

def transform(p, alpha):
    x = math.cos(alpha) * p[0] - math.cos(alpha) * p[1]
    y = math.sin(alpha) * p[0] + math.sin(alpha) * p[1] + p[2]
    return x, y


def get_plot_elements_3d(points, alpha=-math.pi / 8, m=None):
    kink_points = get_kink_points([tuple(p) for p in points], 3)

    plot_elements = {
        "points": [],
        "axes": [],
        "kink_points": [transform(p, alpha) for p in kink_points],
        "other_points": [],
        "lines": []
    }

    for point in points:
        t_point = transform(point, alpha)
        plot_elements["points"].append(t_point)

        point_kink_points = [p for p in kink_points if any([point[i] == p[i] for i in range(3)])]
        point_points = [p for p in points if any([point[i] == p[i] for i in range(3)])]

        for i in range(3):
            neighbouring_kink_points = [p for p in point_kink_points if p[i] != point[i]]
            neighbouring_points = [p for p in point_points if p[i] != point[i]]

            line_end_point = point[:]
            line_end_i_kink = min(kp[i] for kp in neighbouring_kink_points)
            if len(neighbouring_points) > 0:
                line_end_i_points = max(kp[i] for kp in neighbouring_points)
                if line_end_i_points < line_end_point[i]:
                    line_end_point[i] = max(line_end_i_kink, line_end_i_points)
                else:
                    line_end_point[i] = line_end_i_kink
            else:
                line_end_point[i] = line_end_i_kink
            t_line_end_point = transform(line_end_point, alpha)

            plot_elements["other_points"].append(t_line_end_point)
            plot_elements["lines"].append(t_point + t_line_end_point)

            second_line_points = [p for p in neighbouring_kink_points if
                               sum([p[i] == line_end_point[i] for i in range(3)]) == 2]
            for second_line_point in second_line_points:
                t_second_line_point = transform(second_line_point, alpha)
                plot_elements["lines"].append(t_line_end_point + t_second_line_point)

    if m is None:
        m = max(max(p) for p in points) + 0.5

    for i in range(3):
        other_axes = [(i + 1) % 3, (i + 2) % 3]
        axes_point = [p for p in kink_points if p[other_axes[0]] == 0 and p[other_axes[1]] == 0]
        if len(axes_point) > 0:
            ax_start = axes_point[0]
        else:
            ax_start = 0
        ax_end = [0] * i + [m] + [0] * (2 - i)
        plot_elements["axes"].append(transform(ax_start, alpha) + transform(ax_end, alpha))

    return plot_elements

def get_plot_elements_2d(points, m=None):
    points = sorted(points, key=lambda p: p[0])
    points = [p[:2] for p in points]
    if m is None:
        m = max(max(p) for p in points) + 1
    points2 = [[0, m]] + points + [[m, 0]]
    print(points2)
    kink_points = [(p1[0], p2[1]) for (p1, p2) in zip(points2, points2[1:])]

    plot_elements = {
        "points": points,
        "axes": [(0, 0, m, 0), (0, 0, 0, m)],
        "kink_points": kink_points,
        "other_points": [],
        "lines": []
    }

    for i, p in enumerate(points):
        plot_elements["lines"].append(kink_points[i] + tuple(p))
        plot_elements["lines"].append(tuple(p) + kink_points[i+1])

    return plot_elements


def get_sweep_plots_2d(points, m=None):
    for i, _ in enumerate(points):
        f_name = f"../tikz_plots/sweep_{i + 1}.tex"
        print(m)
        plot_elements = get_plot_elements_2d(remove_dominated_points(points[:i + 1]), m)
        print(plot_elements)
        s = tikz_plot(plot_elements, axes_positions=("below", "left"), point_pos="above right")

        # save the string s in file f_name
        with open(f_name, "w") as f:
            f.write(s)

def get_images_3d(points, f_name="points3d"):
    elements = get_plot_elements_3d(points)
    s1 = tikz_plot(elements, show_kink=True)
    # s2 = tikz_plot(elements, show_kink=True)

    with open(f"../tikz_plots/{f_name}.tex", "w") as f:
        f.write(s1)
    # with open(f"../tikz_plots/{f_name}_with_kink.tex", "w") as f:
    #     f.write(s2)

def get_front_tikz_elements_2d(points):
    m = 4
    plot_elements = {
        "points": [],
        "unnamed_points": points,
        "axes": [(0, 0, m, 0), (0, 0, 0, m)],
        "kink_points": [],
        "other_points": [],
        "lines": []
    }
    return plot_elements


def get_front_tikz_elements_3d(points):
    m = 3.5
    alpha = -math.pi / 8
    ax_start = transform((0, 0, 0), alpha)
    plot_elements = {
        "points": [],
        "unnamed_points": [transform(p, alpha) for p in points],
        "axes": [ax_start + transform((m, 0, 0), alpha),
                 ax_start + transform((0, m, 0), alpha),
                 ax_start + transform((0, 0, m), alpha)],
        "kink_points": [],
        "other_points": [],
        "lines": []
    }
    return plot_elements


def plane_intersections():
    alpha = -math.pi / 8
    max_x, max_y = 5, 5
    min_x, min_y = 0, 0
    mid_points = [
        [(min_x, min_y, -0.5)],
        [(4, min_x, 0.5), (4, 3, 0.5), (2, 3, 0.5), (2, 4, 0.5), (min_y, 4, 0.5)],
        [(4, min_x, 1.5), (4, 3, 1.5), (min_y, 3, 1.5)],
        [(3, min_x, 2.5), (3, 1, 2.5), (1, 1, 2.5), (1, 3, 2.5), (min_y, 3, 2.5)],
        [(1, min_x, 3.5), (1, 3, 3.5), (min_y, 3, 3.5)],
        [(min_x, min_y, 4.5)]
    ]

    for i, z in enumerate([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]):

        pts_out = [(max_x, max_y, z), (max_x, min_y, z)] + mid_points[i] + [(min_x, max_y, z)]

        pts_in = [(min_x, min_y, z)] + mid_points[i]
        for p1, p2 in zip(pts_in[1:], pts_in[2:]):
            print(f"    \draw[gray, dashed] {transform(p1, alpha)} -- {transform(p2, alpha)};")


        for op, pts in zip([0.5, 0.75], [pts_in, pts_out]):
            t_pts = [str(transform(p, alpha)) for p in pts]
            s = f"    \\fill[fillcol, opacity={op}] " + " -- ".join(t_pts) + " -- cycle;"
            print(s)


        print()

def hyperplane():
    alpha = -math.pi / 8
    pts = [(3, 0, 0), (3, 3, 0), (0, 3, 0), (0, 3, 3), (0, 0, 3), (3, 0, 3)]
    lines = [(3, 3, 0), (0, 3, 3), (3, 0, 3)]

    t_pts = [str(transform(p, alpha)) for p in pts]
    s = f"    \\fill[fillcol, opacity=0.8] " + " -- ".join(t_pts) + " -- cycle;"
    print(s)

    for l in lines:
        print(f"    \draw[gray, dashed] {transform(l, alpha)} -- {transform((3, 3, 3), alpha)};")

    print()



def get_front_visualizations():
    for front in ["spherical", "linear", "worst_case"]:
        points = get_non_dominated_points(20, 2, front, distance=3)
        points_df = pd.DataFrame(points, columns=["x", "y"])
        points_df.to_csv(f"../csv/points_{front}_2D.csv", index=False)

        elements = get_front_tikz_elements_2d(points)
        s2d = tikz_plot(elements, show_kink=False, axes_positions=("below", "left"))

        with open(f"../tikz_plots/front_{front}_2d.tex", "w") as f:
            f.write(s2d)

        points = get_non_dominated_points(200, 3, front, distance=3)
        points_df = pd.DataFrame(points, columns=["x", "y", "z"])
        points_df.to_csv(f"../csv/points_{front}_3D.csv", index=False)
        elements = get_front_tikz_elements_3d(points)
        s3d = tikz_plot(elements, show_kink=False)

        with open(f"../tikz_plots/front_{front}_3d.tex", "w") as f:
            f.write(s3d)


def get_epsilon_net_visualizations():
    points = epsilon_net_from_square(3, 0.3, 2)
    points_df = pd.DataFrame(points, columns=["x", "y"])
    points_df.to_csv(f"../csv/epsilon_net_2D.csv", index=False)

    elements = get_front_tikz_elements_2d(points)
    s2d = tikz_plot(elements, show_kink=False, axes_positions=("below", "left"))

    with open(f"../tikz_plots/epsilon_net_2d.tex", "w") as f:
        f.write(s2d)

    points = epsilon_net_from_square(3, 0.3, 3)
    points_df = pd.DataFrame(points, columns=["x", "y", "z"])
    points_df.to_csv(f"../csv/epsilon_net_3D.csv", index=False)

    elements = get_front_tikz_elements_3d(points)
    s3d = tikz_plot(elements, show_kink=False)
    with open(f"../tikz_plots/epsilon_net_3d.tex", "w") as f:
        f.write(s3d)




def tikz_plot(plot_elements, point_color="black", kink_color="nodecol", show_kink=True,
              axes_positions=("below", "below", "right"), point_pos="below left"):

    s = "\\begin{tikzpicture}\n"

    s += "    % lines:\n"
    for (x1, y1, x2, y2) in plot_elements["lines"]:
        s += f"    \\draw ({round(x1, 4)},{round(y1, 4)}) -- ({round(x2, 4)},{round(y2, 4)});\n"

    s += "    % points:\n"
    for i, (x, y) in enumerate(plot_elements["points"]):
        s += (f"    \\fill[{point_color}] ({x},{y}) circle (2pt) "
              # f"node[{point_pos}] {{\\( \\textbf{{p}}^{{{i+1}}} \\)}}
              f";\n")

    for i, (x, y) in enumerate(plot_elements.get("unnamed_points", [])):
        s += (f"    \\fill[{point_color}] ({x},{y}) circle (2pt) "
              f"node[{point_pos}] {{\\(  \\)}};\n")

    if show_kink:
        s += "    % kink points:\n"
        for i, (x, y) in enumerate(plot_elements["kink_points"]):
            s += (f"    \\fill[{kink_color}] ({x},{y}) circle (2pt) "
                  # f"node[above left] {{\\( v^{{{i + 1}}} \\)}};\n")
                  f";\n")

    s += "    % axes:\n"
    for i, ((x1, y1, x2, y2), position) in enumerate(zip(plot_elements["axes"], axes_positions)):
        s += (f"    \\draw[->] ({round(x1, 4)},{round(y1, 4)}) -- ({round(x2, 4)},{round(y2, 4)}) "
              f"node[midway, {position}] {{\\( f_{i+1} \\)}};\n")

    s += "\\end{tikzpicture}"
    # print(s)
    return s


if __name__ == '__main__':
    """
    pts = [[0.65, 2.6, 3.25], [1.3, 1.95, 3], [1.95, 1.3, 2.75], [2.6, 0.65, 2.5],
           [3.25, 3.25, 0.8], [3, 3, 1.6]]
    p = 6
    pts = [[i + 1, p / 2 - i, p - i] for i in range(3)] + \
          [[p - i, p - i, i + 1] for i in range(3)]
    pts = [[x / 2 for x in p] for p in pts]

    get_images_3d(pts[:3], f_name="example4d_1")
    get_images_3d(pts[:4], f_name="example4d_2")
    get_images_3d(pts[:5], f_name="example4d_3")
    get_images_3d(pts[:6], f_name="example4d_4")
    """
    # get_sweep_plots_2d(pts, m=5)
    # plane_intersections()
    hyperplane()
    # get_epsilon_net_visualizations()
