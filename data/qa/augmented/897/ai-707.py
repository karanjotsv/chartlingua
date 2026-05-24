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
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

bar_texts = []
for item in chart_data:
    y_val = item['y']
    if y_val == int(y_val):
        bar_texts.append(str(int(y_val)))
    else:
        bar_texts.append(f"{y_val:.2f}")

fig.add_trace(go.Bar(
    x=[d['x'] for d in chart_data],
    y=[d['y'] for d in chart_data],
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False 
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 6.1],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        tickangle=0
    ),
    margin=dict(l=100, r=40, t=40, b=100)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color="#808080")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")