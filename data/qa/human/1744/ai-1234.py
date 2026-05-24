import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON object
categories = chart_data['categories']
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create a figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors['bar_colors'][i],
            line=dict(color='white', width=1)
        ),
        text=series['values'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=14,
            color=colors['text_colors'][i]
        ),
        hovertemplate='%{x}%<extra></extra>'
    ))

# Combine title and subtitle
title_text = f"<b style='font-size:20px'>{texts['title']}</b><br><span style='font-size:15px;color:#555555'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    barmode='stack',
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 101] # Sum of percentages is close to 100
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        ticks='',
        autorange='reversed' # To display categories from top to bottom
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.87,
        xanchor="left",
        x=0.3,
        traceorder='normal',
        font=dict(size=12),
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=200, r=20, t=200, b=120),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12)
        )
    ]
)

# Generate the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")