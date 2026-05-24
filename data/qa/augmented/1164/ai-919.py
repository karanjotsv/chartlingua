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
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

# Add traces from JSON data
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        mode='lines+markers',
        line=dict(color=chart_data['colors'][i], width=2.5),
        marker=dict(color=chart_data['colors'][i], size=7)
    ))

# Create vertical bands for background
shapes = []
for i, _ in enumerate(chart_data['chart_data'][0]['x']):
    if i % 2 != 0:
        shape = go.layout.Shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=i - 0.5,
            y0=0,
            x1=i + 0.5,
            y1=1,
            fillcolor="#f0f0f0",
            layer="below",
            line_width=0
        )
        shapes.append(shape)

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    shapes=shapes,
    annotations=[
        dict(
            text=chart_data['texts']['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='top',
            font=dict(color="#337ab7")
        ),
        dict(
            text=chart_data['texts']['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            font=dict(color="#6c757d")
        )
    ]
)

# Update axes
fig.update_xaxes(
    showgrid=False,
    tickfont=dict(size=12)
)

fig.update_yaxes(
    title_text=chart_data['texts']['y_axis_title'],
    title_font=dict(size=14),
    gridcolor='#e0e0e0',
    range=[70, 106],
    dtick=5,
    tickfont=dict(size=12)
)

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")