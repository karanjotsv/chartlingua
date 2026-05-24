import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare subplot titles, wrapping them in bold tags for styling
subplot_titles = [f"<b>{item['title']}</b>" for item in chart_data]

# Create a figure with subplots, one for each pie chart
fig = make_subplots(
    rows=len(chart_data),
    cols=1,
    specs=[[{'type': 'domain'}] for _ in chart_data],
    subplot_titles=subplot_titles,
    vertical_spacing=0.08  # Adjust spacing between charts
)

# Iterate through the chart data to create and add each pie chart trace
for i, item in enumerate(chart_data):
    # Map labels to their corresponding colors from the colors dictionary
    marker_colors = [colors[label] for label in item['labels']]
    
    fig.add_trace(go.Pie(
        labels=item['labels'],
        values=item['values'],
        marker=dict(colors=marker_colors, line=dict(color='#000000', width=1)),
        hoverinfo='label+percent',
        textinfo='value',
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        sort=False,  # Preserve the original data order
        showlegend=True,
        name=item['title'] # Use title for hover differentiation
    ), row=i + 1, col=1)

# Combine main title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the overall layout of the figure
fig.update_layout(
    title_text=title_text,
    font=dict(family="Arial", size=12, color="black"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=1400,
    width=700,
    margin=dict(l=50, r=200, t=80, b=50),
    showlegend=True,
    legend=dict(
        title='Ancestry',
        traceorder='normal' # Use the order traces were added
    )
)

# Update subplot title font
fig.update_annotations(font=dict(family="Arial", size=14, color="black"))


# Define the output filename based on the input JSON filename
output_filename = json_file_path.stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")