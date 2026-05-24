import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=7, line=dict(width=1, color='white')),
        name=series['name']
    ))

    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        showarrow=True,
        arrowhead=0,
        ax=40,
        ay=0,
        xanchor="left",
        yanchor="middle",
        font=dict(family="Arial", size=12, color="black"),
        bgcolor="white",
        bordercolor=colors[i],
        borderwidth=0.5,
        borderpad=4
    )


title_text = f"<span style='font-size:24px;'><b>{texts['title']}</b></span><br><span style='font-size:16px;color:#555555'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12, color='#555555')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='white',
        zeroline=False,
        range=[65, 115],
        tickvals=[70, 75, 80, 85, 90, 95, 100, 105, 110],
        tickfont=dict(size=12, color='#555555')
    ),
    font=dict(family="Arial"),
    plot_bgcolor='#eef3f7',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=100, t=120, b=40)
)


fig.add_shape(
    type="line",
    x0=0, y0=112.5, x1=1, y1=112.5,
    xref="paper", yref="y",
    line=dict(color="#3793cb", width=2)
)

fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0.99, y=1.07,
    xanchor='right', yanchor='bottom',
    showarrow=False,
    font=dict(size=12, color="#555555")
)


output_filename = json_file_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")