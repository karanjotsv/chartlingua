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
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
pie_text_labels = [f"<b>{d['label']}</b><br>{d['value']}%" for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=pie_text_labels,
    textinfo='text',
    insidetextfont=dict(
        family='Arial',
        size=16,
        color='white'
    ),
    marker=dict(
        colors=colors,
        line=dict(color='#ffffff', width=1)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=94,
    hoverinfo='label+percent'
))

fig.update_layout(
    title_text=f"<b>{texts['title']}</b>" if texts.get('title') else None,
    title_x=0.5,
    title_y=0.95,
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    margin=dict(t=100, r=50, b=50, l=50),
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=800,
    height=700
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to {output_image_path}")