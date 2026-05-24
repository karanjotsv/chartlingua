import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [item['category'] for item in chart_data]
y_values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0],
    hoverinfo='none',
    textfont=dict(
        family="Arial",
        size=11,
        color='black'
    )
))

fig.update_layout(
    template='plotly_white',
    font=dict(family="Arial", size=12),
    yaxis_title=texts.get('y_axis_title'),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    yaxis=dict(
        range=[0, 85],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickmode='array',
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80]
    ),
    xaxis=dict(
        showgrid=False
    ),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper", yref="paper",
            x=1.0, y=-0.22,
            xanchor='right', yanchor='top',
            align='right'
        )
    ]
)

output_filename_base = os.path.splitext(json_file_path)[0]
output_image_path = f"{output_filename_base}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")