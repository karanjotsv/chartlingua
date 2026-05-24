import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)


# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly (Plotly plots y-axis from bottom to top)
# To match the visual top-to-bottom order, we reverse the lists.
categories = [d['category'] for d in data]
values = [d['value'] for d in data]

categories.reverse()
values.reverse()
colors.reverse()

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker_color=colors,
    text=[f"{v:.2f}{texts['data_label_suffix']}" for v in values],
    textposition='outside',
    hoverinfo='none',
    cliponaxis=False
))

# Combine title and subtitle using HTML
title_text = f"<span style='font-size: 28px;'><b>{texts['title']}</b></span><br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=[0, 0.5, 1, 1.5, 2],
        ticktext=['0 t', '0.5 t', '1 t', '1.5 t', '2 t'],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        showline=False,
        showticklabels=True,
        range=[0, max(values) * 1.15] # Add padding for text labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticks='',
        tickfont=dict(size=14)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='#f9f9f9',
    margin=dict(l=100, r=60, t=100, b=80),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.12,
            xanchor='left', yanchor='top',
            text=texts['source_left'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        ),
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.12,
            xanchor='right', yanchor='top',
            text=texts['source_right'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    ]
)

# Derive output filename from input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")