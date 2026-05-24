import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=chart_data['x_values'],
    y=chart_data['y_values'],
    mode='lines+markers',
    line=dict(color=colors['line'], width=3),
    marker=dict(color=colors['line'], size=8),
    showlegend=False
))

for x, y, label in zip(chart_data['x_values'], chart_data['y_values'], chart_data['labels']):
    if label:
        fig.add_annotation(
            x=x,
            y=y,
            text=label,
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors['text_main']),
            yshift=15
        )

fig.update_layout(
    title=texts['title'],
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color=colors['text_main']),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[6, 18],
        dtick=2,
        ticksuffix='%',
        gridcolor=colors['grid'],
        zeroline=False
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=chart_data['x_values'],
        ticktext=[str(year) for year in chart_data['x_values']],
        showgrid=True,
        gridcolor=colors['grid'],
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.25,
            xanchor='left', yanchor='bottom',
            text=texts['source_left'],
            font=dict(family="Arial", size=12, color=colors['source_left_text']),
            showarrow=False
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.25,
            xanchor='right', yanchor='bottom',
            text=texts['source_right'],
            align='right',
            font=dict(family="Arial", size=12, color=colors['text_main']),
            showarrow=False
        )
    ]
)

output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")