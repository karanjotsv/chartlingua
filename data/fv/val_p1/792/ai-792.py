import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
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

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=100
)

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

layout = go.Layout(
    title=dict(text=full_title if full_title else None),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        x=0.9,
        y=0.9,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=250, t=50, b=20)
)

fig = go.Figure(data=[pie_trace], layout=layout)

base_filename = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")