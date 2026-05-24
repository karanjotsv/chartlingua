import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    sys.exit(1)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [d['label'] if d['label'] is not None else '' for d in data]
values = [d['value'] for d in data]

# Prepare text for display on slices
pie_text = []
for d in data:
    if d['label']:
        # For SiO₂, the subscript '2' is not easily reproducible in standard text.
        # Using the provided label as is.
        if d['label'] == 'SiO₂':
            pie_text.append(f"SiO<sub>2</sub>, {d['value']}")
        else:
            pie_text.append(f"{d['label']}, {d['value']}")
    else:
        pie_text.append('')

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    text=pie_text,
    textinfo='text',
    textposition='inside',
    textfont=dict(size=14, family='Arial', color='#FFFFFF'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
)])

# Update layout
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(family="Arial", color="white"),
    showlegend=False,
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    margin=dict(l=40, r=40, t=100, b=40),
    autosize=False,
    width=800,
    height=600
)

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_directory = os.path.dirname(json_path)
if not output_directory:
    output_directory = "." # handle case where file is in current directory
    
output_filename = os.path.join(output_directory, f"{base_filename}.png")


# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)