import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from point_sampling import epsilon_net


def pareto_front(add_kink_points=True, add_cones=False):
    points = [[1, 9], [2, 8], [3, 5], [6, 4], [8, 2], [10, 1]]
    m = max([max([p for p in point]) for point in points])
    points = [[0, m + 1]] + points + [[m + 1, 0]]
    kink_points = [[x1[0], x2[1]] for x1, x2 in zip(points[:-1], points[1:])]

    fig = go.Figure()

    # pareto front line
    interleaved = [item for pair in zip(points, kink_points) for item in pair] + [points[-1]]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in interleaved],
        y=[p[1] for p in interleaved],
        mode='lines',
        line=dict(width=2, color="red"),
        showlegend=False,
    ))

    # plot the points
    fig.add_trace(go.Scatter(
        x=[p[0] for p in points[1:-1]],
        y=[p[1] for p in points[1:-1]],
        mode='markers',
        marker=dict(size=8, color="black", symbol="circle"),
        showlegend=False,
    ))
    if add_kink_points:
        fig.add_trace(go.Scatter(
            x=[p[0] for p in kink_points],
            y=[p[1] for p in kink_points],
            mode='markers',
            marker=dict(size=8, color="blue", symbol="square"),
            showlegend=False,
        ))
    if add_cones:
        for kp in kink_points:
            fig.add_trace(go.Scatter(
                x=[kp[0], m + 1, m + 1, kp[0], kp[0]],
                y=[kp[1], kp[1], m + 1, m + 1, kp[1]],
                fill='toself',
                mode='none',
                fillcolor="grey",
                opacity=0.5,
                showlegend=False,
            ))
    # update the layout and axes
    fig.update_layout(
        xaxis=dict(range=[0, m + 1]),
        yaxis=dict(range=[0, m + 1]),
        height=500,
        width=500,
        plot_bgcolor="white",
    )
    x_name = "Kriterij 1"
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        title_text=x_name,
        showticklabels=False,
    )

    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        title_text="Kriterij 2",
        showticklabels=False,
    )

    fig.show()
    if not add_kink_points:
        export_to_pdf(fig, "pareto_front")
    elif not add_cones:
        export_to_pdf(fig, "pareto_front_with_kink_points")
    else:
        export_to_pdf(fig, "pareto_front_with_cones")


def non_dominated_points():
    non_dom_points = [[1, 11], [3, 9], [7, 8], [11, 7], [12, 2]]
    dom_points = [[1, 2], [4, 8], [4, 5], [5, 2], [8, 4], [9, 1]]
    ma = max([max([p for p in point]) for point in non_dom_points + dom_points])

    fig = go.Figure()
    # plot the points
    fig.add_trace(go.Scatter(
        x=[p[0] for p in non_dom_points],
        y=[p[1] for p in non_dom_points],
        mode='markers',
        marker=dict(size=8, color="black", symbol="circle"),
        showlegend=False,
    ))

    fig.add_trace(go.Scatter(
        x=[p[0] for p in dom_points],
        y=[p[1] for p in dom_points],
        mode='markers',
        marker=dict(size=8, color="blue", symbol="square"),
        showlegend=False,
    ))

    # update the layout and axes
    fig.update_layout(
        xaxis=dict(range=[-1, ma + 1]),
        yaxis=dict(range=[-1, ma + 1]),
        height=500,
        width=500,
        plot_bgcolor="white",
    )
    x_name = "Kriterij 1"
    fig.update_xaxes(
        showline=False,
        linewidth=1,
        linecolor='black',
        title_text=x_name,
        showticklabels=False,
    )

    fig.update_yaxes(
        showline=False,
        linewidth=1,
        linecolor='black',
        title_text="Kriterij 2",
        showticklabels=False,
    )

    # add arrow on x-axis
    arrow_settings = dict(
        xref="x",
        yref="y",
        axref='x',
        ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowsize=2,
        arrowwidth=1,
        arrowcolor="gray",
        opacity=1.0
    )
    fig.add_annotation(
        x=ma + 1,
        y=0,
        ax=-1,
        ay=0,
        **arrow_settings
    )
    fig.add_annotation(
        x=0,
        y=ma + 1,
        ax=0,
        ay=-1,
        **arrow_settings
    )

    fig.show()
    export_to_pdf(fig, "non_dominated_points")


def dominated_area():
    fig = go.Figure()
    # plot the points

    points = [[0, 0], [1, 4], [-3, -2], [-2, 1]]
    colors = ["black", "green", "blue", "gray"]
    names = ["$p$", "$q$", "$r$", "$s$"]

    for p, c, n in zip(points, colors, names):
        fig.add_trace(go.Scatter(
            x=[p[0]],
            y=[p[1]],
            mode='markers',
            marker=dict(size=8, color=c, symbol="circle"),
            showlegend=False,
        ))
        fig.add_annotation(
            x=p[0],
            y=p[1],
            xshift=6,
            yshift=0,
            text=n,
            showarrow=False,
            xanchor="left",
            yanchor="top",
            font=dict(size=12, color="black"),
        )

    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=-5, y1=-5,
        line=dict(
            color="blue",
            width=2,
        ),
        fillcolor="blue",
        opacity=0.4,
        )
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=5, y1=5,
        line=dict(
            color="green",
            width=2,
        ),
        fillcolor="green",
        opacity=0.4,
        )


    fig.update_layout(
        xaxis=dict(range=[-5, 5]),
        yaxis=dict(range=[-5, 5]),
        height=500,
        width=500,
        plot_bgcolor="white",
    )
    fig.update_xaxes(
        showline=False,
        showticklabels=False,
    )

    fig.update_yaxes(
        showline=False,
        showticklabels=False,
    )

    fig.show()
    export_to_pdf(fig, "dominated_area")


def test_visualization():
    points = [(1, 9), (2, 8), (3, 5), (6, 4), (8, 2), (10, 1)]
    m = max([max([p for p in point]) for point in points])
    points = [[0, m + 1]] + points + [[m + 1, 0]]
    kink_points = [[x1[0], x2[1]] for x1, x2 in zip(points[:-1], points[1:])]

    dom_point = (1, 2)
    dist = math.sqrt(8)
    delta = 0.1
    epsilon = 0.1
    net_big = epsilon_net(dist + delta, epsilon, 2)
    net_big = [[p[0] + dom_point[0], p[1] + dom_point[1]] for p in net_big]

    net_small = epsilon_net(dist - delta, epsilon, 2)
    net_small = [[p[0] + dom_point[0], p[1] + dom_point[1]] for p in net_small]


    fig = go.Figure()

    # pareto front line
    interleaved = [item for pair in zip(points, kink_points) for item in pair] + [points[-1]]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in interleaved],
        y=[p[1] for p in interleaved],
        mode='lines',
        line=dict(width=2, color="black"),
        showlegend=False,
    ))
    # plot the points
    fig.add_trace(go.Scatter(
        x=[p[0] for p in points[1:-1]],
        y=[p[1] for p in points[1:-1]],
        mode='markers',
        marker=dict(size=8, color="black", symbol="circle"),
        showlegend=False,
    ))

    fig.add_trace(go.Scatter(
        x=[dom_point[0]],
        y=[dom_point[1]],
        mode='markers',
        line=dict(width=2, color="red"),
        showlegend=False,
    ))

    fig.add_trace(go.Scatter(
        x=[p[0] for p in net_big],
        y=[p[1] for p in net_big],
        mode='lines',
        line=dict(width=1, color="green"),
        showlegend=False,
    ))

    fig.add_trace(go.Scatter(
        x=[p[0] for p in net_small],
        y=[p[1] for p in net_small],
        mode='lines',
        line=dict(width=1, color="red"),
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=[dom_point[0], dom_point[0], dom_point[0] + dist + delta],
        y=[dom_point[1] + dist + delta, dom_point[1], dom_point[1]],
        mode='lines',
        line=dict(width=1, color="black", dash="dot"),
        showlegend=False,
    ))

    # update the layout and axes
    fig.update_layout(
        xaxis=dict(range=[0, m + 1]),
        yaxis=dict(range=[0, m + 1]),
        height=500,
        width=500,
        plot_bgcolor="white",
    )
    x_name = "Kriterij 1"
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        title_text=x_name,
        showticklabels=False,
    )

    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        title_text="Kriterij 2",
        showticklabels=False,
    )

    fig.show()
    export_to_pdf(fig, "test_visualization")



def export_to_pdf(fig, name):
    print(f"Exporting {name} to PDF...", end="")
    fig.write_image(f"../images/{name}.pdf")
    print("done")


if __name__ == "__main__":
    pareto_front(add_kink_points=False)
    pareto_front(add_cones=False)
    pareto_front(add_cones=True)
    # non_dominated_points()
    # dominated_area()
    # test_visualization()
