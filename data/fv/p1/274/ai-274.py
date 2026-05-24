import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the file exists before proceeding
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load the chart data and configuration from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Prepare Data for Plotting ---
# Extract data, text, and color information from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Extract categories and values from the chart data
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# The visual order is top-to-bottom, but Plotly plots bottom-to-top.
# Reverse all lists to match the visual representation of the original chart.
categories.reverse()
values.reverse()
colors.reverse()

# Format text labels to match the original chart (e.g., "180,9")
text_labels = [f'{v:.1f}'.replace('.', ',') for v in values]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    marker_color=colors,
    text=text_labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12
    ),
    orientation='h',
    hoverinfo='none',
    cliponaxis=False # Ensures text labels are not clipped by the plot area
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for flexible styling
title_text = texts.get('title') or ''

fig.update_layout(
    # Chart Title
    title=dict(
        text=title_text,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(
            family="Arial",
            size=16,
            color='black'
        )
    ),
    # General Font
    font=dict(
        family="Arial",
        size=12
    ),
    # Axes configuration
    xaxis=dict(
        visible=False,
        range=[0, max(values) * 1.15] # Extend range to fit outside text
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        ticks='',
        tickfont=dict(size=13)
    ),
    # Background and Margins
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=130, r=40, t=70, b=20)
)


# --- 5. Output the Chart ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")