import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]
json_path_obj = Path(json_file_path)

# Ensure the file exists
if not json_path_obj.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data from the JSON structure
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create a custom text list to show percentages only for larger slices, matching the original
pie_text = [f'{v}%' if v >= 3.3 else '' for v in values]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    text=pie_text,
    textinfo='text',
    textposition='inside',
    insidetextfont=dict(color='white', size=12),
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=100 # Adjust rotation to place the largest slice at the top
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=16, weight='bold')
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.01
    ),
    margin=dict(l=50, r=200, t=80, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True,
    width=800,
    height=550
)

# Define the output image filename from the input JSON filename
output_filename = f"{json_path_obj.stem}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`) for image export.")
    sys.exit(1)