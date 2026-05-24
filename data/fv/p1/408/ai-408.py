import sys
import json
import plotly.graph_objects as go
import pathlib

# This script generates a chart from a JSON file specified as a command-line argument.
# It is designed to be a robust, language-agnostic visualization tool.

# --- 1. Argument Handling and File Loading ---
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# --- 2. Data Extraction ---
# All data, text, and styling are sourced exclusively from the JSON file.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item.get('label') for item in chart_data]
values = [item.get('value') for item in chart_data]

# --- 3. Chart Creation ---
# A 2D pie chart is used as the standard and robust representation for this data type in Plotly.
# The 3D effect from the original image is a stylistic choice not natively supported for this chart type.
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    textinfo='label+percent',
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=18,
        color="black"
    ),
    hole=0,
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise'
))

# --- 4. Layout and Styling ---
# Layout is configured to match the original's aesthetics and prevent text overlap.
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.08,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=22,
            color="black"
        )
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=80, b=120) # Ample margins for labels and title
)

# --- 5. Image Export ---
# The chart is saved as a high-resolution PNG file.
try:
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)