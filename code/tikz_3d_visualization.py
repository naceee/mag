import plotly.graph_objects as go
import math

from main import get_kink_points

def transform(p, alpha):
    x = math.cos(alpha) * p[0] - math.cos(alpha) * p[1]
    y = math.sin(alpha) * p[0] + math.sin(alpha) * p[1] + p[2]
    return x, y


def get_plot_elements(points, alpha=-math.pi/8, m=None):
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

        for i in range(3):
            neighbouring_kink_points = [p for p in point_kink_points if p[i] != point[i]]

            line_end_point = point[:]
            line_end_point[i] = min(kp[i] for kp in neighbouring_kink_points)
            t_line_end_point = transform(line_end_point, alpha)

            plot_elements["other_points"].append(t_line_end_point)
            plot_elements["lines"].append(t_point + t_line_end_point)

            second_line_points = [p for p in neighbouring_kink_points if
                               sum([p[i] == line_end_point[i] for i in range(3)]) == 2]
            for second_line_point in second_line_points:
                t_second_line_point = transform(second_line_point, alpha)
                plot_elements["lines"].append(t_line_end_point + t_second_line_point)

    if m is None:
        m = max(max(p) for p in points) + 1

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


def plotly_plot(points, alpha=-math.pi / 8):
    plot_elements = get_plot_elements(points, alpha)

    fig = go.Figure()
    all_points = plot_elements["points"] + plot_elements["other_points"] + plot_elements["kink_points"]
    for point in all_points:
        fig.add_trace(go.Scatter(
            x=[point[0]],
            y=[point[1]],
            mode="markers",
            marker=dict(color="black"),
            showlegend=False,
        ))

    for (x1, y1, x2, y2) in plot_elements["lines"]:
        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(color="black"),
            showlegend=False,
        ))

    for (x1, y1, x2, y2) in plot_elements["axes"]:
        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(color="gray"),
            showlegend=False,
        ))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        scaleanchor="x",
        scaleratio=1,
    )

    fig.show()





def tikz_plot(points, alpha=-math.pi / 8, point_color="black", kink_color="gray", show_kink=True):
    plot_elements = get_plot_elements(points, alpha)
    s = "\\begin{tikzpicture}\n"

    s += "    % lines:\n"
    for (x1, y1, x2, y2) in plot_elements["lines"]:
        s += f"    \\draw ({round(x1, 4)},{round(y1, 4)}) -- ({round(x2, 4)},{round(y2, 4)});\n"

    s += "    % points:\n"
    for i, (x, y) in enumerate(plot_elements["points"]):
        s += (f"    \\fill[{point_color}] ({x},{y}) circle (2pt) "
              f"node[below left] {{\\( p_{{{i+1}}} \\)}};\n")

    if show_kink:
        s += "    % kink points:\n"
        for i, (x, y) in enumerate(plot_elements["kink_points"]):
            s += (f"    \\fill[{kink_color}] ({x},{y}) circle (2pt) "
                  f"node[above left] {{\\( v_{{{i+1}}} \\)}};\n")

    s += "    % axes:\n"
    for i, ((x1, y1, x2, y2), position) in enumerate(zip(plot_elements["axes"], ["below", "below", "right"])):
        s += (f"    \\draw[->] ({round(x1, 4)},{round(y1, 4)}) -- ({round(x2, 4)},{round(y2, 4)}) "
              f"node[midway, {position}] {{\\( f_{i+1} \\)}};\n")

    s += "\\end{tikzpicture}"
    print(s)





if __name__ == '__main__':
    pts = [[2, 3, 5], [4, 1, 4], [3, 2, 2], [5, 5, 1]]
    # plotly_plot(pts)
    tikz_plot(pts, show_kink=True)
