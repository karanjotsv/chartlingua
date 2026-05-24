import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)

if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path_str}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path_str}")
    sys.exit(1)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']
categories = chart_data['categories']
series_list = chart_data['series']

fig = go.Figure()

max_y_value = 0
for s in series_list:
    current_max = max(s['data'])
    if current_max > max_y_value:
        max_y_value = current_max

for i, series in enumerate(series_list):
    text_labels = [f'{val:,}'.replace(',', ' ') for val in series['data']]
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['data'],
        marker_color=colors[i],
        text=text_labels,
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12)
    ))

fig.update_layout(
    barmode='group',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title') or None,
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        showline=False,
        showticklabels=False,
        range=[0, max_y_value * 1.20]
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, t=50, b=140),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")