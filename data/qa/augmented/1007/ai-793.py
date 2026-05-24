import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and text elements from the configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data directly from the JSON structure
categories = [d.get('category') for d in chart_data]
values = [d.get('value') for d in chart_data]

# Format text labels to match the original chart's style (e.g., "11 773")
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

# Initialize the figure object
fig = go.Figure()

# Add the horizontal bar trace using data from the JSON
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Allow text labels to be drawn outside the plot area
))

# Update the layout for a clean, professional, and accurate presentation
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        range=[0, 15000]  # Set a fixed range to provide space for text labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Ensures the y-axis order matches the JSON order (top to bottom)
        showgrid=False
    ),
    margin=dict(l=150, r=60, t=30, b=80),
    # Add source text as a positioned annotation
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    ]
)

# Derive the output filename from the input JSON path's base name
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")