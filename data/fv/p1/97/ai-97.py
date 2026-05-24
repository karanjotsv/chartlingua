import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

fig = go.Figure()

chart_data = data.get('chart_data', [])
if not chart_data:
    print("Error: 'chart_data' not found in JSON.")
    sys.exit(1)

# Add bar trace, taking data from the first series
series = chart_data[0]
fig.add_trace(go.Bar(
    y=series.get('categories', []),
    x=series.get('values', []),
    orientation='h',
    marker_color=data.get('colors', [])[0]
))

texts = data.get('texts', {})
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.99,
        yanchor='top',
        font=dict(size=14)
    ),
    xaxis=dict(
        side='top',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title')
    ),
    font=dict(
        family="Arial",
        size=10
    ),
    plot_bgcolor='white',
    showlegend=False,
    height=2400,
    width=700,
    margin=dict(l=150, r=40, t=100, b=40)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)