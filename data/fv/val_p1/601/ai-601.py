import sys
import json
import os
import plotly.graph_objects as go

# 1. SCRIPT SETUP AND DATA LOADING
# ==================================
# Check if the path to the JSON file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load the chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# 2. DATA PREPARATION FOR PLOTLY
# ==============================
# Prepare lists for labels and values, preserving the order from the JSON
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# 3. CHART CREATION AND STYLING
# =============================
# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    textinfo='percent',
    texttemplate='%{value}%',
    hoverinfo='label+percent',
    sort=False,  # IMPORTANT: This preserves the original data order
    direction='clockwise',
    textfont=dict(family="Arial", size=14)
)])

# Update the layout of the chart
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_font=dict(size=24, family="Arial"),
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(
        traceorder='normal',  # Ensure legend order matches data order
        font=dict(family="Arial", size=12)
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=350, t=100, b=40)  # Adjust margins to prevent clipping
)

# 4. EXPORTING THE CHART
# ======================
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")