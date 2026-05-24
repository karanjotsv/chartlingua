import sys
import json
import plotly.graph_objects as go
import os

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
    
# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)


# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels_from_data = [f"{item['label']},<br>{item['value']:,}" for item in chart_data]
values_from_data = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels_from_data,
    values=values_from_data,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    textposition='outside',
    textinfo='none', # Using labels for text outside the chart
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    pull=[0.02] * len(values_from_data) # Explode all slices slightly
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout for a professional look, matching the original
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_font=dict(size=20),
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    margin=dict(l=100, r=100, t=100, b=50), # Adjust margins to prevent label clipping
    paper_bgcolor='white',
    plot_bgcolor='white',
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")