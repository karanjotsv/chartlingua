import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series_list = chart_data['series']

fig = go.Figure()

max_x_value = 0
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['data'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i]),
        text=[f"{val}%" for val in series['data']],
        textposition='outside',
        textfont=dict(size=12),
        cliponaxis=False
    ))
    current_max = max(series['data'])
    if current_max > max_x_value:
        max_x_value = current_max

fig.update_layout(
    barmode='group',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=130, r=40, b=110, t=40),
    xaxis=dict(
        title=texts['x_axis_title'],
        title_standoff=10,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticksuffix='%',
        range=[0, max_x_value * 1.15]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        categoryorder='array',
        categoryarray=categories
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")