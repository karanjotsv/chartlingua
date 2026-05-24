import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly (it plots y-axis from bottom to top, so we reverse the lists)
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors['bar'], line=dict(width=0)),
    text=categories,
    textposition='inside',
    insidetextanchor='start',
    textfont=dict(
        family='Arial',
        size=16,
        color=colors['bar_text']
    ),
    hoverinfo='none'  # Replicates static chart appearance
))

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    showlegend=False,
    margin=dict(l=10, r=20, t=20, b=40),
    xaxis=dict(
        range=[0, 50],
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        ticktext=['0%', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50'],
        showgrid=True,
        gridcolor=colors['grid'],
        gridwidth=2,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(
            size=14,
            color=colors['axis_labels']
        )
    ),
    yaxis=dict(
        showticklabels=False,  # Labels are inside the bars
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    annotations=[
        dict(
            text=texts['annotation_text'],
            x=28,
            y=9.5,  # Position in the middle of the y-axis (20 categories -> index 9.5)
            xref='x',
            yref='y',
            showarrow=False,
            font=dict(
                family='Arial',
                size=32,
                color=colors['annotation_text']
            ),
            align='center'
        )
    ]
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")