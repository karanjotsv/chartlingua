import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file {json_file_path}")
    sys.exit(1)

output_filename_base = os.path.splitext(os.path.basename(json_file_path))[0]

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', {})

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors.get('bar_color', ['#1f77b4'])[0],
    text=[f'{y:.2f}%' for y in y_values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    title_text=texts.get('title', ''),
    yaxis=dict(
        title_text=texts.get('y_axis_title', ''),
        range=[0, 60],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        title_standoff=15
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title', ''),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#7f7f7f')
        )
    ]
)

output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")