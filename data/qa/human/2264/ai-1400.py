import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data_series = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Create a list of all categories to enforce the correct order
all_categories = []
for series in chart_data_series:
    all_categories.extend(series['categories'])

# Add a bar trace for each series defined in the JSON
for i, series in enumerate(chart_data_series):
    fig.add_trace(go.Bar(
        x=series['categories'],
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        texttemplate='%{y}%',
        textposition='inside',
        textfont=dict(color='white', size=14, family="Arial", weight="bold"),
        insidetextanchor='middle'
    ))

# Construct the title block using HTML for flexible formatting
title_text = ""
if texts.get('title'):
    title_text += f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 16px;'>{texts['subtitle']}</span>"

# Apply layout settings to match the original chart's appearance
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        categoryorder='array',
        categoryarray=all_categories,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 60],
        ticksuffix='%',
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5,
        font=dict(size=14)
    ),
    margin=dict(l=80, r=40, t=60, b=180),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.4,
            xanchor='right', yanchor='bottom',
            text=texts.get('source'),
            showarrow=False,
            font=dict(size=12, color='#555555')
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")