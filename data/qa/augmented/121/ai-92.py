import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_file_path}'.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# --- 2. Create the Chart ---
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=chart_data['categories'],
        y=series['values'],
        marker_color=colors[i],
        text=[f'{v:.1f}' for v in series['values']],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False  # Prevent text labels from being clipped
    ))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle if they exist
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for the footer
source_text = texts.get('source') or ''
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 20],
        tickmode='linear',
        tick0=0,
        dtick=5,
        showline=False,
        gridcolor='#E5E5E5'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=90, r=40, b=120, t=40),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")