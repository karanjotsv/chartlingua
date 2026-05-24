import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0], line=dict(width=0)),
    text=[f"<b>{v}</b>" for v in values],  # Make text bold
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(family="Arial", size=16, color='white')
))

# Construct the title string
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout for a clean, professional appearance
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        visible=False,  # Hide the entire x-axis
    ),
    yaxis=dict(
        autorange='reversed',  # Ensure order matches the input data (top to bottom)
        showline=False,
        showgrid=False,
        tickfont=dict(size=18, color='black')
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=200, r=40, t=100, b=40),
    font=dict(family="Arial") # Set global font
)

# Determine the output filename from the input JSON path
base_name = json_path.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")