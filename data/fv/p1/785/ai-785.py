import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Script Execution ---

# 1. Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# 2. Validate and load the JSON file
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# 3. Extract data and texts from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# 4. Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# 5. Create the Plotly figure
fig = go.Figure()

# Create a pull list to "explode" the first slice, matching the original chart
pull_values = [0] * len(values)
if pull_values:
    pull_values[0] = 0.2

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=labels,
    textinfo='text',  # Use the custom text from the 'text' property
    hoverinfo='label+percent',
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    pull=pull_values,
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='clockwise'
))

# 6. Configure the layout
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_y=0.95,
    font=dict(
        family="Arial",
        size=18,
        color="black"
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=120, b=50) # Increased top margin for title
)

# 7. Customize trace appearance for better readability
fig.update_traces(
    textposition='outside',
    textfont_size=20
)

# 8. Write the output image
output_filename = json_path.stem + ".png"
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to '{output_filename}'")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)