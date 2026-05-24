import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data_series = chart_info['chart_data']
texts = chart_info['texts']
color_map = chart_info['colors']

fig = go.Figure()

# The outer ring must be added first to be in the background.
# The data is structured with the inner ring at index 0 and outer at index 1.
outer_ring = data_series[1]
outer_colors = [color_map.get(label) for label in outer_ring['labels']]
fig.add_trace(go.Pie(
    labels=outer_ring['labels'],
    values=outer_ring['values'],
    marker=dict(colors=outer_colors, line=dict(color='white', width=4)),
    textinfo='percent',
    texttemplate='%{value}%',
    textposition='outside',
    textfont=dict(size=16, family="Arial", color='black'),
    domain={'x': [0, 1], 'y': [0, 1]},
    sort=False,
    direction='clockwise',
    rotation=90,
    showlegend=False
))

inner_ring = data_series[0]
inner_colors = [color_map.get(label) for label in inner_ring['labels']]
fig.add_trace(go.Pie(
    labels=inner_ring['labels'],
    values=inner_ring['values'],
    marker=dict(colors=inner_colors, line=dict(color='white', width=4)),
    textinfo='percent',
    texttemplate='%{value}%',
    textposition='inside',
    insidetextorientation='horizontal',
    textfont=dict(size=16, family="Arial", color='white'),
    domain={'x': [0.18, 0.82], 'y': [0.18, 0.82]},
    sort=False,
    direction='clockwise',
    rotation=90,
    showlegend=False
))

# Create a custom legend to match the original chart's style and order.
legend_order = ["Like", "No opinion", "Dislike"]
for label in legend_order:
    if label in color_map:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(symbol='square', size=15, color=color_map[label]),
            name=label,
            showlegend=True
        ))

fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        y=0.97,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18, family="Arial")
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="left",
        x=0.1,
        font=dict(family="Arial", size=14),
        traceorder='normal'
    ),
    margin=dict(l=40, r=40, t=140, b=140),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=True,
    shapes=[dict(
        type="circle",
        xref="paper", yref="paper",
        x0=0.36, y0=0.36, x1=0.64, y1=0.64,
        line_color="white",
        fillcolor="white"
    )],
    annotations=[
        dict(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.1,
            y=-0.22,
            font=dict(family="Arial", size=14)
        )
    ]
)

fig.write_image(str(output_path), scale=2)
print(f"Chart saved to {output_path}")