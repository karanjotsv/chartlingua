import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=series['data'],
        textposition='auto',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='group',
    title_text=title_text if title_text else None,
    xaxis_title_text=texts['x_axis_title'],
    yaxis_title_text=texts['y_axis_title'],
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        tickangle=0
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#dddddd',
        range=[0, 1050],
        tickvals=[0, 250, 500, 750, 1000]
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=160, t=50),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.45,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(
                family="Arial",
                size=12
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")