import plotly.graph_objects as go
from plotly.subplots import make_subplots


def draw_point(point, ref_point, fig):
    # draw a cube with the point as one of the vertices and the ref_point as the opposite vertex
    fig.add_trace(go.Mesh3d(
        # 8 vertices of a cube
        x=[point[0], point[0], ref_point[0], ref_point[0], point[0], point[0], ref_point[0], ref_point[0]],
        y=[point[1], ref_point[1], ref_point[1], point[1], point[1], ref_point[1], ref_point[1], point[1]],
        z=[point[2], point[2], point[2], point[2], ref_point[2], ref_point[2], ref_point[2], ref_point[2]],
        # i, j and k give the vertices of triangles
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        name='y',
        showscale=True
    ), row=1, col=1)


def visualize_kink_points(points, kink_points, found_point=None):
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'surface'}]])

    # add a scatter plot to the figure
    fig.add_trace(go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(
            size=8,
            color='rgb(160, 160, 160)',
            symbol='circle',
        ),
        name="ref_point"
    ), row=1, col=1)

    for p in points:
        draw_point(p, (0, 0, 0), fig)
        fig.add_trace(go.Scatter3d(
            x=[p[0]],
            y=[p[1]],
            z=[p[2]],
            mode='markers',
            marker=dict(
                size=4,
                color='rgb(0, 0, 0)',
                symbol='x',
                line=dict(
                    color='rgb(0, 0, 0)',
                    width=0.5
                )
            ),
            name=str(p)
        ), row=1, col=1)

    m = max([max([p for p in point]) for point in points])
    eps = m / 100

    for k in kink_points:
        fig.add_trace(go.Scatter3d(
            x=[k[0] + eps],
            y=[k[1] + eps],
            z=[k[2] + eps],
            mode='markers',
            marker=dict(
                size=10,
                color='rgb(0, 0, 0)',
                symbol='circle',
            ),
            name=str(k)
        ), row=1, col=1)

    if found_point is not None:
        fig.add_trace(go.Scatter3d(
            x=[found_point[0]],
            y=[found_point[1]],
            z=[found_point[2]],
            mode='markers',
            marker=dict(
                size=10,
                color='rgb(100, 0, 0)',
                symbol='diamond',
            ),
            name=str(found_point)
        ), row=1, col=1)


    # set axis limits between 0 and 1
    fig.update_layout(scene=dict(
        xaxis=dict(range=[0, 1.1 * m]),
        yaxis=dict(range=[0, 1.1 * m]),
        zaxis=dict(range=[0, 1.1 * m]),
        aspectmode='cube'
    ))

    fig.show()
