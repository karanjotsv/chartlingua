import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_filepath = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format text labels for display on the chart (with space as thousand separator)
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False,  # Prevent text from being clipped by the plot area
    hoverinfo='none' # Mimic static chart
))

# Update layout for a clean, professional look
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        showline=False,
        tickformat=' ', # Use space as thousands separator
        range=[0, max(values) * 1.15] # Add padding for text labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Ensure the order from JSON is top-to-bottom
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    margin=dict(l=100, r=80, t=50, b=80) # Adjust margins for labels and source
)

# Add source text as an annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=0,
        xanchor='right',
        yanchor='top',
        yshift=-25, # Position below the chart area
        font=dict(size=10)
    )

# Define output filename based on the input JSON file's name
base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")