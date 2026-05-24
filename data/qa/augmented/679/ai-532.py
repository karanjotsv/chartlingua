import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [item['category'] for item in data]
y_values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#2B78D6',
    text=y_values,
    textposition='outside',
    texttemplate='%{text:.1f}',
    cliponaxis=False
))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(texts['subtitle'])
full_title = "<br>".join(title_parts)

fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_font_family="Arial",
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickmode='linear'
    ),
    yaxis=dict(
        range=[0, 18],
        dtick=2.5,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        showline=False,
        zeroline=False
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=10)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")