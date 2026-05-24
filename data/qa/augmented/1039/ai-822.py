import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

x_values = [d['category'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=[f'{v:.1f}' for v in y_values],
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickangle=-45,
        linecolor='black',
        linewidth=1,
        showline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 7],
        dtick=1,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='lightgrey',
        showline=False
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10, color="#666666")
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")