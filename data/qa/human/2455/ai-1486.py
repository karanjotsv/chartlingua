import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
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

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    textinfo='label+percent',
    textposition='outside'
)])

title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=0,
            xanchor='right',
            yanchor='bottom'
        )
    )

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(family="Arial", size=12),
    showlegend=False,
    margin=dict(l=80, r=80, t=80, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations
)

output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)
print(f"Chart saved to {output_png_path}")