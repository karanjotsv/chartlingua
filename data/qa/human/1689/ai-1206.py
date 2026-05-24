import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data']
categories = chart_data['categories']
texts = chart_data['texts']
colors = chart_data['colors']

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(width=0)
        ),
        text=series['text'],
        textposition='inside',
        insidetextanchor='middle',
        texttemplate='%{text}',
        insidetextfont=dict(
            family='Arial',
            size=16,
            color=series['textfont_colors']
        )
    ))

# Combine title and subtitle
title_text = f"{texts['title']}<br><span style='font-size:16px; color:#555555;'>{texts['subtitle']}</span>"

# Update layout for a clean, professional look
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=22, family='Arial')
    ),
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        domain=[0.3, 1]  # Leave space for y-axis labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14, family='Arial')
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.01,
        xanchor='left',
        x=0,
        font=dict(size=14),
        bgcolor='rgba(0,0,0,0)',
        traceorder='normal'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=280, r=40, t=140, b=100),
    font=dict(family="Arial", size=12),
    # Add annotation for the source text
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            align='left',
            font=dict(size=12, family='Arial', color='#888888')
        )
    ],
    # Add a separator line above the source
    shapes=[
        go.layout.Shape(
            type="line",
            xref="paper",
            yref="paper",
            x0=0,
            y0=-0.08,
            x1=1,
            y1=-0.08,
            line=dict(color="black", width=0.5)
        )
    ]
)

# Derive output filename from JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")