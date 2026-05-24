import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)


# Extract data and texts
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format text labels to match original (e.g., "52" instead of "52.0")
text_labels = [str(v) if v == int(v) else f'{v:.1f}' for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    hoverinfo='none'  # Mimic a static chart
))

# Build title and source strings safely from JSON
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get("source", "")

# Update layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='lightgrey',
        range=[0, max(values) * 1.25] # Ensure space for text labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        autorange='reversed'  # This preserves the order from the JSON data (top-to-bottom)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=50, t=40, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Derive output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")