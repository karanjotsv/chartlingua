import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
# The script requires the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Prepare Data for Plotly ---
# Extract data, texts, and colors from the loaded JSON.
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare lists for the pie chart trace, maintaining original order.
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create custom text for each slice to match the original chart's format.
custom_texts = [
    f"{item['category']}<br>{item['value']:,}<br>{item['percentage']}%"
    for item in chart_data
]

# Define which slices are "pulled" or "exploded" from the center.
# Based on the visual analysis of the original chart.
pull_values = [0.2, 0.1, 0, 0, 0, 0] 

# --- 3. Create the Chart Figure ---
# Initialize a Figure object.
fig = go.Figure()

# Add the Pie trace.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=custom_texts,
    # Use the custom text directly on the chart.
    textinfo='text',
    textposition='outside',
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    pull=pull_values,
    # Ensure the original data order is preserved.
    sort=False,
    direction='clockwise',
    # Customize hover text.
    hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>'
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle from the JSON data.
full_title = f"{texts['title']}<br>{texts['subtitle']}"

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    # Use annotations for source and note text to position them precisely.
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=0,
            xanchor='left', yanchor='bottom',
            align='left'
        ),
        dict(
            text=texts['note'],
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=0,
            xanchor='right', yanchor='bottom',
            align='right'
        )
    ],
    # Set global font to Arial.
    font=dict(family="Arial", size=12, color="black"),
    # Disable the legend as labels are directly on the chart.
    showlegend=False,
    # Set margins to prevent labels or annotations from being clipped.
    margin=dict(l=80, r=80, b=100, t=100, pad=4),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Adjust text font for the pie slices.
fig.update_traces(textfont_size=12)

# --- 5. Output the Image ---
# Generate the output filename from the input JSON filename.
output_filename = json_path.stem + ".png"

# Save the figure as a high-resolution PNG image.
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")