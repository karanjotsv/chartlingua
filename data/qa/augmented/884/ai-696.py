import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
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

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    hoverinfo='none',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e9e9e9',
        range=[0, max(y_values) * 1.12],
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35],
        showline=False,
        zeroline=False
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        tickmode='array',
        tickvals=x_values,
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        zeroline=False
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.20,
            xanchor='right',
            yanchor='top'
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")