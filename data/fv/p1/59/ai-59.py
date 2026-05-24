import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the file exists before proceeding
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
    
# Read and parse the JSON file, ensuring UTF-8 encoding for multilingual support
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Prepare Data for Plotting ---
# Create lists for y-axis categories, x-axis values, and data labels
# The y-axis labels are a combination of the category name and its rank
y_labels = [f"{item['category']} {item['rank']}" for item in chart_data]
x_values = [item['value'] for item in chart_data]
text_labels = [f"{item['value']:,}" for item in chart_data]

# Plotly's horizontal bar chart plots the first item at the bottom.
# To match the original chart (rank 1 at the top), we reverse the lists.
y_labels.reverse()
x_values.reverse()
text_labels.reverse()

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=y_labels,
    x=x_values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none'  # Disable tooltips as they are not in the original
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML line breaks for proper display
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,  # Center the title
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='white',
        zeroline=False,
        dtick=500000,
        tickformat='.0s' # Use abbreviated format (e.g., 500k, 1M)
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True
    ),
    plot_bgcolor='#f0f0f0',
    paper_bgcolor='#f0f0f0',
    font=dict(family="Arial", size=12),
    margin=dict(l=250, r=100, t=100, b=50) # Set margins to prevent label clipping
)

# --- 5. Output the Chart ---
# Derive the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")