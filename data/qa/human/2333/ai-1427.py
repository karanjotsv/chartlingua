import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

fig = go.Figure()

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=[f'{val:g}' for val in series['data']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=14,
            color='white'
        )
    ))

title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1.5
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 6000],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    margin=dict(l=90, r=30, t=60, b=150),
    width=800,
    height=600
)

if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.28,
        xanchor='right',
        yanchor='bottom',
        font=dict(
            family="Arial",
            size=10,
            color='grey'
        )
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")