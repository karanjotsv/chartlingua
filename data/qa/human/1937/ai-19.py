import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    sort=False,
    direction='clockwise',
    texttemplate='%{label} %{value}%',
    textposition='outside',
    hoverinfo='label+percent',
    textfont=dict(size=14)
)])

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            showarrow=False,
            text=texts['source'],
            xref="paper",
            yref="paper",
            x=0.99,
            y=0.01,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12, color="#555555")
        )
    )

fig.update_layout(
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=80, r=80, t=50, b=60),
    annotations=annotations
)

output_filename_base = os.path.splitext(json_path)[0]
output_filename_png = f"{output_filename_base}.png"
fig.write_image(output_filename_png, scale=2)

print(f"Chart saved to {output_filename_png}")