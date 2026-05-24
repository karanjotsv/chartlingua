import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

x_values = [d['year'] for d in data]
y_values = [d['value'] for d in data]

fig = go.Figure()

# Add the main line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=7),
    showlegend=False
))

# Add data labels as annotations
for point in data:
    if point.get('label'):
        yshift = 15 if point['position'] == 'above' else -15
        fig.add_annotation(
            x=point['year'],
            y=point['value'],
            text=point['label'],
            showarrow=False,
            font=dict(family="Arial", size=11),
            yshift=yshift
        )

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=2000,
        dtick=1,
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[44000, 54000],
        dtick=2000,
        showgrid=True,
        gridcolor='#EAEAEA',
        tickformat=',d',
        separatethousands=True,
        linecolor='black'
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=30, t=50, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=11)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_path = f"{base_filename}.png"

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")