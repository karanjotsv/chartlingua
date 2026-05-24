import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
title_text = texts.get('title', '')
source_text = texts.get('source', '')

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add the Pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    texttemplate="<b>%{value:,d}<br>%{percent}</b>",
    textposition='inside',
    textfont=dict(
        family="Arial",
        size=16,
        color=['white', 'black']
    ),
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='counterclockwise',
    rotation=60  # Rotate to match the visual layout of the original image
))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle
full_title = title_text
if texts.get('subtitle'):
    full_title += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for the annotation
caption_text = ""
if source_text:
    caption_text += source_text
if texts.get('note'):
    caption_text += f"<br>{texts['note']}"

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top',
        font=dict(
            family="Arial",
            size=18
        )
    ),
    legend=dict(
        orientation='v',
        x=0.5,
        xanchor='center',
        y=-0.1,
        yanchor='top',
        font=dict(
            family="Arial",
            size=12
        )
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=120, b=180, l=40, r=40),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=caption_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.3, # Positioned below the legend
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(
                family="Arial",
                size=10
            )
        )
    ]
)

# --- 4. Output the Figure ---
# Derive the output filename from the input JSON path
filename_base = os.path.basename(json_path).replace('.json', '')
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")