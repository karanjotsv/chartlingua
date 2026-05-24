import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and load the JSON data file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1)
    ),
    textposition='outside',
    texttemplate='%{label} %{value}%',
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    rotation=80
))

# Update the layout for a clean and accurate appearance
fig.update_layout(
    showlegend=False,
    font=dict(
        family="Arial",
        size=12
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=50, b=50),
    autosize=False,
    width=800,
    height=600,
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=10, color='grey')
        )
    ]
)

# Customize the font for the outside labels
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")