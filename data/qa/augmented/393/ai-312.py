import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {pathlib.Path(sys.argv[0]).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]
bar_texts = [f"{d['y']:,}".replace(',', ' ') for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='#333333')
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        type='category',
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 35000],
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickvals=[0, 5000, 10000, 15000, 20000, 25000, 30000, 35000],
        ticktext=['0', '5 000', '10 000', '15 000', '20 000', '25 000', '30 000', '35 000'],
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color="#666666")
        )
    ]
)

output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")