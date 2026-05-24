import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
categories = [item['category'] for item in data]
num_series = len(texts['legend_labels'])
series_data = [[item['values'][i] for item in data] for i in range(num_series)]

# Create the figure
fig = go.Figure()

# Add a trace for each series
for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=texts['legend_labels'][i],
        marker_color=colors[i],
        text=series_data[i],
        texttemplate='%{y}%',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black')
    ))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a professional look
fig.update_layout(
    barmode='group',
    title_text=title_text,
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        tickvals=[0, 25, 50, 75, 100, 125],
        ticktext=['0%', '25%', '50%', '75%', '100%', '125%'],
        range=[0, 130]
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=180, t=50),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.55,
            xanchor='right',
            yanchor='bottom',
            align="right",
            font=dict(size=10)
        )
    ]
)

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")