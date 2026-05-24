import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Error: A path to a JSON file is required as a command-line argument.")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' contains invalid JSON.")
    sys.exit(1)

output_filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{output_filename_base}.png"

data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    hoverinfo='none',
    name=''
))

title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text += f"<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    title_text=title_text,
    title_x=0.05,
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=80),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[0, 25000],
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        zeroline=False
    )
)

fig.add_annotation(
    text=texts.get('source'),
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.99,
    y=-0.15,
    xanchor='right',
    yanchor='top',
    font=dict(size=10)
)

fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")