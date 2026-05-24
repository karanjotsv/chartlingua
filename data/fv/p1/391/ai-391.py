import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.isfile(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
y_axis_title_color = texts.get('y_axis_title_color', '#000000')

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i] if i < len(colors) else None
    ))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        font=dict(size=32),
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=[1950, 1960, 1970, 1980, 1990, 2000, 2010],
        tickfont=dict(size=18),
        showgrid=True,
        gridcolor='#CCCCCC',
        gridwidth=1,
        linecolor='black',
        linewidth=1,
        mirror=True
    ),
    yaxis=dict(
        title=dict(
            text=texts.get('y_axis_title'),
            font=dict(
                size=22,
                color=y_axis_title_color
            )
        ),
        range=[0, 600],
        tickvals=[0, 100, 200, 300, 400, 500, 600],
        tickfont=dict(size=18),
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dash',
        linecolor='black',
        linewidth=1,
        mirror=True,
        zeroline=False
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.25,
    margin=dict(l=100, r=20, t=120, b=80)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart successfully generated and saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)