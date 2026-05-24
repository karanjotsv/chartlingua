import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name=''
))

fig.update_layout(
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    showlegend=False,
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis=dict(
        range=[0, 800],
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False
    ),
    margin=dict(l=80, r=20, t=40, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{output_filename_base}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")