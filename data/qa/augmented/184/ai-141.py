import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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
values_series_1 = [item['values'][0] for item in chart_data]
values_series_2 = [item['values'][1] for item in chart_data]

fig = go.Figure()

# Add first bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values_series_1,
    name=texts['legend_items'][0],
    orientation='h',
    marker_color=colors[0],
    text=values_series_1,
    textposition='outside',
    textfont=dict(family="Arial", color='black')
))

# Add second bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values_series_2,
    name=texts['legend_items'][1],
    orientation='h',
    marker_color=colors[1],
    text=values_series_2,
    textposition='outside',
    textfont=dict(family="Arial", color='black')
))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure layout
fig.update_layout(
    barmode='group',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts.get('x_axis_label'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=True,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_label'),
        autorange='reversed',  # Ensures the top category in the list is at the top of the chart
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=40, t=50, b=120),
    bargap=0.15,
    bargroupgap=0.1
)

# Add annotations for source and note
annotations = []
if texts.get("source"):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0.99, y=-0.32,
        xanchor='right', yanchor='bottom',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))

fig.update_layout(annotations=annotations)

# Define output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")