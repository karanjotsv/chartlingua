import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize figure
fig = go.Figure()

# Add a separate bar trace for each data point to control individual colors
for i, item in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=[item['category']],
        y=[item['value']],
        name=item['category'],
        marker_color=colors[i],
        text=[f"{item['value']:.1f}"],
        textposition='outside',
        textfont=dict(color=colors[i], size=14, family="Arial"),
        hoverinfo='none'
    ))

# Build combined title string
title_text = f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='#EFF6F9',
    paper_bgcolor='#EFF6F9',
    showlegend=False,
    bargap=0.5,
    margin=dict(t=100, b=100, l=50, r=50),
    xaxis=dict(
        showticklabels=False,
        showline=False,
        zeroline=False,
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 16],
        tickmode='linear',
        tick0=0,
        dtick=2,
        gridcolor='#FFFFFF',
        zerolinecolor='#FFFFFF',
        showline=False,
        title=None
    )
)

# Add custom annotations
annotations = []

# Source text
annotations.append(dict(
    xref='paper', yref='paper',
    x=0.99, y=1.05,
    xanchor='right', yanchor='bottom',
    text=texts['source'],
    showarrow=False,
    font=dict(size=12, color='#555555')
))

# Custom colored x-axis labels
for i, item in enumerate(chart_data):
    annotations.append(dict(
        xref='x', yref='paper',
        x=item['category'], y=0,
        xanchor='center', yanchor='top',
        text=item['category'],
        showarrow=False,
        yshift=-15,
        font=dict(color=colors[i], size=12),
        textangle=-45
    ))

# Info box annotation
if 'info_box' in texts and texts['info_box']:
    info_box = texts['info_box']
    annotations.append(dict(
        x=info_box['x_anchor_category'],
        y=info_box['y_anchor_value'],
        text=info_box['text'],
        showarrow=True,
        arrowhead=0,
        arrowside='start',
        ax=50,
        ay=0,
        align='left',
        bgcolor='rgba(255, 255, 255, 0.95)',
        bordercolor='#c7c7c7',
        borderwidth=1,
        font=dict(family="Arial", size=12)
    ))

fig.update_layout(annotations=annotations)

# Output the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")