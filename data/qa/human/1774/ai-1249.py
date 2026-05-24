import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data ---
# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [item['text'] for item in chart_data]

# --- 2. Create Chart ---
# Initialize figure
fig = go.Figure()

# Add the bar trace with data-driven styling
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors,
    textfont=dict(
        color=colors,
        size=12,
        family="Arial"
    ),
    cliponaxis=False  # Ensures text for zero/small values is not clipped
))

# --- 3. Configure Layout ---
# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px; color:#555555;'>{texts['subtitle']}</span>"

# Update layout properties
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    yaxis=dict(
        # Set a dynamic range to ensure the highest bar's label fits
        range=[0, max(values) * 1.15 if max(values) > 0 else 0.1],
        tickvals=[i / 10 for i in range(0, 20, 2)],
        ticktext=[f"{i / 10:.1f}M" for i in range(0, 20, 2)],
        showgrid=True,
        gridcolor='white',
        zeroline=False,
        title_text=texts.get('y_axis_title')
    ),
    xaxis=dict(
        tickangle=-45,
        showgrid=False,
        title_text=texts.get('x_axis_title')
    ),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=1.06,
            text=texts['source'],
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                size=12,
                family="Arial"
            )
        )
    ],
    plot_bgcolor='#e6f0f2',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=60, r=40, t=100, b=80)
)

# --- 4. Output Image ---
# Derive output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")