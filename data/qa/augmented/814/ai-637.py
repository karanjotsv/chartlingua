import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False
))

fig.update_layout(
    title_text=texts.get('title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 5],
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts.get('source_left', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='bottom',
            align='left'
        ),
        dict(
            text=texts.get('source_right', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.22,
            xanchor='right', yanchor='bottom',
            align='right'
        )
    ]
)

fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none'
)

output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")