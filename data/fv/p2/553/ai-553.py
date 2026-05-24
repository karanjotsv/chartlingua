import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly, maintaining original order
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='label',
    textposition='outside',
    sort=False,  # This is crucial to preserve the order from the JSON
    direction='counterclockwise',
    pull=[0, 0.1] # Slightly separate the 'Atrophy' slice
))

# Update trace properties
fig.update_traces(
    hoverinfo='label+percent',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
)

# Combine title and subtitle using HTML for multi-line formatting
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Construct source annotation
annotations = []
source_text = texts.get('source')
if source_text:
    annotations.append(
        dict(
            showarrow=False,
            text=source_text,
            x=1,
            y=-0.1,
            xref="paper",
            yref="paper",
            xanchor="right",
            yanchor="top",
            font=dict(family="Arial", size=12)
        )
    )

# Update layout for a clean and accurate presentation
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    showlegend=False,
    font=dict(
        family="Arial",
        size=14
    ),
    margin=dict(t=100, b=80, l=40, r=40),
    annotations=annotations,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
if '.' in json_path:
    output_filename_base = json_path.rsplit('.', 1)[0]
else:
    output_filename_base = json_path
output_png_path = f"{output_filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")