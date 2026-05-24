import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='label+percent',
    textposition='outside',
    sort=False,
    direction='clockwise'
)])

fig.update_traces(textfont=dict(size=16, family="Arial"))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: 16px;'>{texts['subtitle']}</span>")
full_title = '<br>'.join(title_parts)

fig.update_layout(
    title_text=full_title if full_title else None,
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial", size=14, color="black"),
    margin=dict(l=80, r=80, t=80, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=0,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color="grey")
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")