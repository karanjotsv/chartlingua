import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

# Prepare data for Plotly
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
labels = [d['label'] for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='dimgray'
    )
))

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

# Update layout for a clean, professional appearance
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'] if texts['x_axis_title'] else "",
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        zeroline=False,
        ticksuffix='%',
        range=[0, max(values) * 1.1] # Set range dynamically
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'] if texts['y_axis_title'] else "",
        autorange='reversed',
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=80, t=140, b=80), # Adjust margins to prevent clipping
    font=dict(
        family="Arial",
        size=12,
        color='dimgray'
    )
)

# Add source annotation at the bottom left
fig.add_annotation(
    text=texts['source'],
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.12,
    xanchor='left',
    yanchor='top',
    font=dict(
        family="Arial",
        size=12,
        color='dimgray'
    )
)

# Add CC BY annotation at the bottom right
fig.add_annotation(
    text="CC BY",
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1.0,
    y=-0.12,
    xanchor='right',
    yanchor='top',
    font=dict(
        family="Arial",
        size=12,
        color='dimgray'
    )
)

# Derive output filename from the input JSON filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")