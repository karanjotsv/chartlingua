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
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.5,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1.5)
    ),
    texttemplate='%{label}<br>%{value}%',
    textposition='outside',
    textfont=dict(size=12, color='#000000'),
    sort=False,
    direction='clockwise',
    rotation=115
)])

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.95,
    title_font=dict(size=18, color='#000000'),
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=50, l=50, r=50)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)