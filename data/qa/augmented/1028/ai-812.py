import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0] if colors else None,
    textfont=dict(
        family="Arial",
        size=12
    )
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F5F5F5',
    margin=dict(t=50, r=40, b=100, l=80),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 50],
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickfont=dict(size=11),
        showgrid=True,
        gridcolor='#E0E0E0'
    ),
    showlegend=False
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(
            family="Arial",
            size=12
        )
    )

output_path = json_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2, width=900, height=550)

print(f"Chart saved to {output_path}")