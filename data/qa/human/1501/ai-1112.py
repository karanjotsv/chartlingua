import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Reverse data for top-to-bottom display in Plotly
chart_data.reverse()
colors.reverse()

# Prepare data for plotting
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
text_labels = [f"{v} t" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none',
    textfont=dict(family="Arial", size=12)
))

# Create combined title string with HTML for styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size:0.9em; color:#555555;'>{texts['subtitle']}</span>"

# Define annotations for source and note
annotations = [
    dict(
        xref='paper', yref='paper',
        x=0, y=-0.12,
        xanchor='left', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=11, color="#666666")
    ),
    dict(
        xref='paper', yref='paper',
        x=1.0, y=-0.12,
        xanchor='right', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=11, color="#666666")
    )
]

# Configure layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12, color="#333333"),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        showline=False,
        showticklabels=True,
        range=[0, max(values) * 1.1],
        tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4],
        ticktext=[f"{v:.1f}".replace('.0', '') + " t" for v in [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4]]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        ticks='',
        tickfont=dict(size=14)
    ),
    margin=dict(l=240, r=40, t=100, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    annotations=annotations
)

# Determine output filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")