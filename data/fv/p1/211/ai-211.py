import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

chart_data = data.get('chart_data', [])
colors = data.get('colors', [])
text_font_colors = data.get('text_font_colors', [])
text_font_sizes = data.get('text_font_sizes', [])

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
texts = [item['text'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=texts,
    hoverinfo='label+percent',
    textinfo='text',
    insidetextorientation='horizontal',
    insidetextfont=dict(
        family="Arial",
        size=text_font_sizes,
        color=text_font_colors
    ),
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1.5)
    ),
    sort=False,
    direction='clockwise',
    rotation=158
))

fig.update_layout(
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(t=20, b=20, l=20, r=20),
    font=dict(family="Arial")
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")