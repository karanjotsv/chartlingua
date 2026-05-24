import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

filename_base = json_path.stem

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
categories = chart_info['categories']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=[f"{v}%" for v in series['values']],
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_font=dict(size=14),
        tickfont=dict(size=12),
        range=[0, 105],
        dtick=20,
        ticksuffix='%',
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1.5
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    ]
)

output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")