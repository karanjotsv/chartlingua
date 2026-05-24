import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=series['y'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color='white'
        )
    ))

title_text = texts.get('title') if texts.get('title') else ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    barmode='stack',
    title_text=title_text,
    title_x=0.05,
    font_family='Arial',
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='lightgray'
    ),
    xaxis=dict(
        showline=False,
        linecolor='black',
        tickfont=dict(family='Arial', size=12)
    ),
    plot_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        font=dict(family='Arial', size=11)
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family='Arial', size=10, color='grey')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")