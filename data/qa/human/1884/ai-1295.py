import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

categories = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#1A73E8'),
    text=[f'{v}%' for v in values],
    textposition='outside',
    textfont=dict(size=12, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    margin=dict(l=260, r=40, t=30, b=80),
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, max(values) * 1.3 if values else 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")