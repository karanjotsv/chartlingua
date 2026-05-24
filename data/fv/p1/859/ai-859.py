import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=chart_data['categories'],
    y=chart_data['values'],
    marker_color=colors,
    texttemplate='<b>%{y}%</b>',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=16
        )
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=True,
        zerolinecolor='#444444',
        zerolinewidth=1.5,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 105],
        tickvals=[i for i in range(0, 101, 10)],
        tickformat='%{y}%',
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=100, b=80)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")