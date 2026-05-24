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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for Plotly's bottom-to-top rendering
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.15] # Add padding for text labels
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    margin=dict(l=120, r=40, t=40, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=10, color="grey")
        )
    ]
)

base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")