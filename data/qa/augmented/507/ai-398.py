import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors[0] if colors else None,
    cliponaxis=False
))

annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(size=12, color='#666666')
    ))

if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(size=12, color='#666666')
    ))

fig.update_layout(
    font_family="Arial",
    title=texts.get('title'),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        range=[-5, 35]
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    showlegend=False,
    annotations=annotations
)

output_filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_directory = os.path.dirname(json_file_path)
output_png_path = os.path.join(output_directory, f"{output_filename_base}.png")


fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")