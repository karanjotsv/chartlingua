import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
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

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='inside',
    insidetextanchor='start',
    texttemplate='%{text:.2f}',
    textfont=dict(
        family="Arial",
        size=14,
        color='white',
        weight='bold'
    )
))

title_text = texts.get('title')
full_title_text = f"<b>{title_text}</b>" if title_text else ""

fig.update_layout(
    title_text=full_title_text,
    title_x=0.05,
    title_font=dict(family="Arial", size=18, color='black'),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12, color='#333333'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1.8],
        dtick=0.25,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            x=1,
            y=-0.2,
            xref="paper",
            yref="paper",
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")