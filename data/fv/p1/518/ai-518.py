import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load the chart data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly by extracting labels and values, preserving order
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Plotly Figure ---
# Initialize the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='counterclockwise'
))

# --- 3. Configure Layout and Styling ---
# Build annotations for source/note
annotations = []
source_text = []
if texts.get("source"):
    source_text.append(texts["source"])
if texts.get("note"):
    source_text.append(texts["note"])

if source_text:
    annotations.append(
        dict(
            text="<br>".join(source_text),
            showarrow=False,
            xref='paper', yref='paper',
            x=0.98, y=-0.15,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(family="Arial", size=10, color="#cccccc")
        )
    )

# Update the layout of the figure
fig.update_layout(
    title=None, # No title in the original image
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(family="Arial", color='white'),
    margin=dict(l=40, r=40, t=40, b=100),
    annotations=annotations
)

# --- 4. Output the Figure ---
# Define the output image file name based on the input JSON file name
output_filename = json_file_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")