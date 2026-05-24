import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python your_script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[f'{y:.2f}' if y % 1 != 0 and str(y)[-2] != '0' else f'{y:.1f}' if y % 1 != 0 else f'{int(y)}' for y in y_values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='rgb(248, 249, 250)',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    yaxis_title=texts['y_axis_title'],
    xaxis=dict(
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 60],
        dtick=10,
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

base_filename, _ = os.path.splitext(json_file_path)
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")