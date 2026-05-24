import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#2175D9',
    text=y_values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    )

if texts.get('additional_info'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0.0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['additional_info'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#2175D9')
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 60],
        dtick=10,
        gridcolor='#EAEAEA',
        showline=False,
        tickfont=dict(size=12),
        zeroline=False
    ),
    margin=dict(l=60, r=40, t=50, b=100),
    annotations=annotations
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")