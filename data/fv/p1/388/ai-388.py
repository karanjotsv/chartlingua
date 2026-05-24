import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly pie chart
labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create custom text labels to show '%' and hide for zero-value slices
# This ensures the output matches the visual representation of the original chart
custom_text = [f"{v}%" if v > 0 else "" for v in values]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    text=custom_text,
    textinfo='text',
    textposition='auto',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=100
))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note
source_text = []
if texts.get('source'):
    source_text.append(texts.get('source'))
if texts.get('note'):
    source_text.append(texts.get('note'))
source_note_text = "<br>".join(source_text)

# Update layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(t=120, b=80, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True
)

# Add source/note as an annotation if it exists
if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        xanchor='left',
        yanchor='top'
    )

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")