import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for the pie chart
values = [item['value'] for item in chart_data]
labels = [item['label'] for item in chart_data]
text_on_slice = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=text_on_slice,
    textinfo='text',
    textfont=dict(family="Arial", size=14, color='black'),
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    hole=0,
    sort=False,
    direction='clockwise',
    hoverinfo='none'
))

# Combine title and subtitle
title_text = f'<b>{texts.get("title", "")}</b><br><span style="color:#5D5D5D; font-size:18px;">{texts.get("subtitle", "")}</span>'

# Combine source and footer
source_text = f'{texts.get("source", "")}<br><b>{texts.get("footer", "")}</b>'

# Update layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=24, color='black')
    ),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.01,
            y=0.01,
            xanchor='left',
            yanchor='bottom',
            align='left',
            font=dict(family="Arial", size=12, color='#333333')
        )
    ],
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(l=20, r=20, t=140, b=100)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_directory = os.path.dirname(json_path)
output_filename = os.path.join(output_directory, f"{base_filename}.png")


# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")