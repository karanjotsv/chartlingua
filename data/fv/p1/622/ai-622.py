import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
value_suffix = texts.get("value_suffix", "")

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=[f"{v}{value_suffix}" for v in values],
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        size=16,
        color='white',
    ),
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    template='plotly_white',
    font=dict(family="Arial"),
    showlegend=False,
    plot_bgcolor='white',
    xaxis=dict(
        range=[400, 700],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        showline=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        autorange='reversed',  # To display categories from top to bottom
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='',
        title_text=texts.get('y_axis_title')
    ),
    margin=dict(l=80, r=20, t=20, b=40),
    annotations=[
        dict(
            x=630,
            y=0.5,
            xref='x',
            yref='y',
            text=texts.get('title'),
            showarrow=False,
            font=dict(family='Arial', size=14, weight='bold'),
            align='center'
        ),
        dict(
            x=630,
            y=1.5,
            xref='x',
            yref='y',
            text=texts.get('subtitle'),
            showarrow=False,
            font=dict(family='Arial', size=12),
            align='center'
        ),
        dict(
            x=650,
            y=2.4, # Positioned below the last bar
            xref='x',
            yref='y',
            text=texts.get('source'),
            showarrow=False,
            font=dict(family='Arial', size=12, style='italic'),
            align='left'
        )
    ]
)

# Generate output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")