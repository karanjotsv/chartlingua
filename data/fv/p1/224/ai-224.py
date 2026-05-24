import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Use pathlib for robust path handling
json_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load all data and text from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly by extracting categories and values
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize a Plotly graph objects Figure
fig = go.Figure()

# Add the bar trace using data from the JSON file
# Note: The original chart has a gradient which is not a standard feature for go.Bar.
# A solid color is used as a standard representation.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    textfont=dict(color='black', size=12),
    cliponaxis=False  # Prevents text labels from being clipped by the plotting area
))

# Dynamically construct the title string using HTML for styling
title_text = f"<b style='font-size: 24px; color: #D35400;'>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 18px; color: #D35400;'>{texts['subtitle']}</span>"

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False,
        range=[0, max(values) * 1.20]  # Add padding for the highest text label
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=50, l=30, r=30) # Adjust margins for title and labels
)

# Determine the output filename from the input JSON path
output_filename = json_path.stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

# Provide minimal feedback to the user
print(f"Chart saved to {output_filename}")