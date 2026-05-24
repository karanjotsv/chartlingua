import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from JSON
data = chart_data['chart_data']
texts = chart_data['texts']
bar_color = chart_data['colors'][0]

# Prepare data for Plotly
y_categories_raw = [item['category'] for item in data]
x_values = [item['value'] for item in data]
label_colors = [item['color'] for item in data]

# Create HTML-formatted y-axis tick labels to apply specific colors
y_categories_html = [f"<span style='color: {color};'>{text}</span>" for text, color in zip(y_categories_raw, label_colors)]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_categories_raw,
    orientation='h',
    marker=dict(color=bar_color),
    text=[f'{val:,}' for val in x_values],
    textposition='outside',
    textfont=dict(
        family='Arial',
        color=label_colors
    ),
    hoverinfo='none',
    cliponaxis=False
))

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, max(x_values) * 1.1] # Proactive range adjustment
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        tickmode='array',
        tickvals=y_categories_raw,
        ticktext=y_categories_html
    ),
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#F0F0F0',
    showlegend=False,
    margin=dict(
        l=350,  # Increased left margin for long labels
        r=80,   # Increased right margin for outside text
        t=100,  # Increased top margin for title
        b=60    # Bottom margin for axis title
    )
)

# Derive output filename from JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")