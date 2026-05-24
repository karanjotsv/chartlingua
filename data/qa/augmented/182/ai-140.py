import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Create background shapes to mimic the vertical bands
shapes = []
for i, cat in enumerate(categories):
    if i % 2 != 0:
        shapes.append(go.layout.Shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=i - 0.5,
            y0=0,
            x1=i + 0.5,
            y1=1,
            fillcolor="#f5f5f5",
            layer="below",
            line_width=0,
        ))

# Create annotations for source text
annotations = []
if texts.get('source_left'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.0, y=-0.15,
            xanchor="left", yanchor="top",
            text=texts['source_left'],
            showarrow=False,
            font=dict(family="Arial", size=11, color="#666666")
        )
    )

if texts.get('source_right_main'):
     annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.85, y=-0.15,
            xanchor="right", yanchor="top",
            text=texts['source_right_main'],
            showarrow=False,
            font=dict(family="Arial", size=11, color="#666666")
        )
    )

if texts.get('source_right_secondary'):
     annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.98, y=-0.15,
            xanchor="right", yanchor="top",
            text=texts['source_right_secondary'],
            showarrow=False,
            font=dict(family="Arial", size=11, color="#666666")
        )
    )

# Update layout
fig.update_layout(
    title_text=texts.get('title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=70, r=20, t=40, b=100),
    yaxis=dict(
        range=[0, 15],
        tickmode='array',
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15],
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False
    ),
    shapes=shapes,
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=800, height=550)

print(f"Chart saved to {output_filename}")