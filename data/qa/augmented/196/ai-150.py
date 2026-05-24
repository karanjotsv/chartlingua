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
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to match the visual order (top-to-bottom in the image)
categories.reverse()
values.reverse()
colors.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker_color=colors,
    text=values,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        ticks='outside',
        showline=False,
        range=[0, max(values) * 1.2]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    margin=dict(l=120, r=40, t=30, b=80),
    showlegend=False
)

if texts.get('source'):
    fig.add_annotation(
        xref='paper', yref='paper',
        x=0.98, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family='Arial', size=10, color='grey')
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")