import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON file.")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
pie_text_labels = [f"{d['label']} {d['value']}%" for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=pie_text_labels,
    textinfo='none',
    textposition='outside',
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
)])

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(family="Arial", size=18, color="#FF0000"),
    font=dict(family="Arial", size=12),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=60, r=60, t=100, b=60)
)

output_filename_base = pathlib.Path(json_path).stem
output_filename_png = f"{output_filename_base}.png"

try:
    fig.write_image(output_filename_png, scale=2)
    print(f"Chart saved to {output_filename_png}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)