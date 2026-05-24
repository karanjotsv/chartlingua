import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract Data and Texts ---
chart_data = chart_info.get("chart_data", [])
colors = chart_info.get("colors", [])
# texts = chart_info.get("texts", {}) # Not used in this specific chart

# --- 3. Prepare Data for Plotly ---
# Extract labels, values, and text colors from the chart_data list
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_colors = [item['text_color'] for item in chart_data]

# Format the text to be displayed on each slice
# It combines the label and the value, separated by a line break.
texts_formatted = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

# --- 4. Create the Chart Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=texts_formatted,
    textinfo='text',  # Use the custom formatted text
    marker=dict(colors=colors),
    textfont=dict(
        family="Arial",
        size=18,
        color=text_colors  # Apply specific colors to text on each slice
    ),
    hoverinfo='none',  # Disable hover effects as per the original static image
    sort=False,  # Important: This preserves the original data order from the JSON
    direction='clockwise',
    showlegend=False  # The legend is not shown; labels are on the slices
))

# --- 5. Configure Layout and Styling ---
fig.update_layout(
    width=600,
    height=600,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(
        family="Arial"
    ),
    margin=dict(t=30, b=30, l=30, r=30)  # Add margin to prevent text from being cut off
)

# --- 6. Save the Chart as a PNG Image ---
# The output filename is derived from the input JSON filename.
output_path = json_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")