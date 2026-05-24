import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
pull = [item.get('explode', 0) for item in chart_data]

# Only show values for the 5 largest slices, as in the original image
text_labels = [str(v) if v >= 10528 else '' for v in values]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    pull=pull,
    text=text_labels,
    textinfo='text',
    insidetextfont=dict(family="Arial", size=16, color='white'),
    hoverinfo='label+percent+value',
    sort=False,
    direction='clockwise'
)])

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=True,
    legend=dict(
        x=0.9,
        y=0.9,
        xanchor='left',
        yanchor='top',
        traceorder='normal'
    ),
    margin=dict(l=20, r=200, t=100, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")