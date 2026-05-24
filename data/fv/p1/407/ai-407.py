import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
# Note: Plotly does not support 3D pie charts like the original Excel chart.
# A 2D pie chart is created as the standard and most accurate representation.
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='none', # Use texttemplate for more control
    texttemplate='%{label}<br>%{value}%',
    textposition='outside',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Update layout for a clean and professional look
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font=dict(
        family="Arial",
        size=16,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=40, r=40, t=100, b=40), # Adjust margins to prevent label/title clipping
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
if '.' in json_path:
    base_name = json_path.rsplit('.', 1)[0]
else:
    base_name = json_path
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")