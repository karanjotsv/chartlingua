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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=160, r=60, t=30, b=80),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        tickcolor='#D3D3D3',
        range=[0, max(values) * 1.25]
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        showline=True,
        linecolor='black',
        linewidth=1,
        autorange='reversed'
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(
            family="Arial",
            size=10,
            color="grey"
        )
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")