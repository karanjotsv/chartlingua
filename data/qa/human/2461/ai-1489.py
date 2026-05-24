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

# Format numbers with spaces as thousand separators for text labels
formatted_text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=formatted_text_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text labels from being clipped by the plot area
))

# Combine title and subtitle using HTML for proper formatting
title_text = ""
if texts.get("title") and texts['title']:
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle") and texts['subtitle']:
    if title_text:
        title_text += "<br>"
    title_text += f"<sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        range=[0, max(values) * 1.2] # Extend range to fit labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Ensures the first item in the data list is at the top
        showgrid=False
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=150, r=80, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                family="Arial",
                size=12,
                color="#666666"
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")