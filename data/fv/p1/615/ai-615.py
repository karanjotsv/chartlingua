import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    textinfo='percent',
    hoverinfo='label+percent',
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=160
))

fig.update_traces(
    textfont=dict(size=14, family="Arial", color='black')
)

fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=20, weight='bold', color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=50, r=50, t=100, b=100),
    paper_bgcolor='#F0F0F8'
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")