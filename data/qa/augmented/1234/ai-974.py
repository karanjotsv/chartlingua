import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0] if colors else '#2B79C2',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#337ab7")
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=150),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        showgrid=False,
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 150],
        tickvals=[0, 25, 50, 75, 100, 125, 150],
        gridcolor='#e9e9e9',
        showgrid=True,
        showline=False,
        zeroline=True,
        zerolinecolor='#e9e9e9'
    ),
    annotations=annotations
)

base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart generated and saved to {output_filename}")