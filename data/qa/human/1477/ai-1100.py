import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly's horizontal bar chart (requires reversing order for top-down display)
categories = [d['category'] for d in chart_data][::-1]
values = [d['value'] for d in chart_data][::-1]
reversed_colors = colors[::-1]

# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=reversed_colors, line_width=0),
    hoverinfo='none',
    cliponaxis=False
))

# Create a list for all annotations
annotations = []

# Add data labels at the end of each bar
for i in range(len(values)):
    annotations.append(dict(
        xref='x', yref='y',
        x=values[i], y=categories[i],
        text=f"{values[i]}%",
        font=dict(family='Arial', size=12, color='black'),
        showarrow=False,
        xanchor='left',
        xshift=5
    ))

# Construct and add the title
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations.append(dict(
    xref='paper', yref='paper',
    x=0, y=1.06,
    xanchor='left', yanchor='bottom',
    text=title_text,
    font=dict(family='Arial', size=18, color='black'),
    showarrow=False,
    align='left'
))

# Add the source text
annotations.append(dict(
    xref='paper', yref='paper',
    x=0, y=-0.14,
    xanchor='left', yanchor='top',
    text=texts.get('source', ''),
    font=dict(family='Arial', size=10, color='grey'),
    showarrow=False,
    align='left'
))

# Update layout for a clean and accurate appearance
fig.update_layout(
    annotations=annotations,
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=100, r=60, t=80, b=100),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticksuffix='%',
        range=[0, max(values) * 1.12]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        categoryorder='array',
        categoryarray=categories,
        tickfont=dict(size=12)
    )
)

# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")