import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

fig = go.Figure()

data = chart_data['chart_data'][0]
colors = chart_data['colors']
texts = chart_data['texts']

fig.add_trace(go.Scatter(
    x=data['x'],
    y=data['y'],
    mode='lines+markers+text',
    text=data['text'],
    textposition='top center',
    textfont=dict(family="Arial", size=11, color='black'),
    marker=dict(color=colors[0], size=7),
    line=dict(color=colors[0], width=2.5),
    hoverinfo='none',
    name=data.get('name', '')
))

for year in range(1986, 2026, 4):
    fig.add_shape(
        type="rect",
        xref="x", yref="paper",
        x0=year, y0=0,
        x1=year + 2, y1=1,
        fillcolor="#f5f5f5",
        layer="below",
        line_width=0,
        opacity=1
    )

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickvals=chart_data['x_axis_config']['tickvals'],
        ticktext=chart_data['x_axis_config']['ticktext'],
        tickangle=chart_data['x_axis_config']['tickangle'],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=chart_data['y_axis_config']['range'],
        ticksuffix=chart_data['y_axis_config']['ticksuffix'],
        dtick=chart_data['y_axis_config']['dtick'],
        showgrid=True,
        gridcolor='#e1e1e1',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            text=texts.get('additional_info', ''),
            showarrow=False,
            font=dict(size=12, color='#3366cc')
        ),
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.25,
            xanchor='right', yanchor='top',
            text=texts.get('source', ''),
            showarrow=False,
            font=dict(size=12)
        ),
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.32,
            xanchor='right', yanchor='top',
            text=texts.get('note', ''),
            showarrow=False,
            font=dict(size=12, color='#3366cc')
        )
    ]
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")