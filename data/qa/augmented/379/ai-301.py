import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to display from top to bottom as in the original image
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    hoverinfo='none'
))

# Add data labels as annotations for precise placement
annotations = []
for i in range(len(categories)):
    annotations.append(
        dict(
            x=values[i],
            y=categories[i],
            text=str(values[i]),
            font=dict(family="Arial", size=12, color='black'),
            showarrow=False,
            xanchor='left',
            xshift=5,
            yanchor='middle'
        )
    )

# Combine main title and subtitle
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += title_text
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Add source text as a layout annotation
source_text = texts.get('source')
if source_text:
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.12,
            xanchor='right', yanchor='top',
            text=source_text,
            showarrow=False,
            font=dict(family="Arial", size=11, color='grey')
        )
    )

fig.update_layout(
    title_text=full_title if full_title else None,
    xaxis_title_text=texts.get('xaxis_title'),
    yaxis_title_text=texts.get('yaxis_title'),
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=160, r=80, t=40, b=80),
    xaxis=dict(
        showgrid=False,
        tickformat=' ',  # Use space as thousands separator
        range=[0, max(values) * 1.2]  # Auto-adjust range to fit labels
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1
    ),
    annotations=annotations
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")