import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first and only command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly, preserving the order from the JSON
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [item['text_label'] for item in chart_data]

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',
    hoverinfo='label+percent',
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1)
    ),
    textposition='outside',
    sort=False # This is crucial to preserve the original data order
))

# --- 3. Configure Layout and Styling ---
title_text = texts.get('title', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top',
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    showlegend=True,
    legend=dict(
        x=1,
        y=0.7,
        xanchor='right',
        yanchor='top',
        traceorder='normal',
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        bgcolor='rgba(255,255,255,0)'
    ),
    margin=dict(l=40, r=40, t=80, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Style the text labels outside the pie
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with a higher resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")