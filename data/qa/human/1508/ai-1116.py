import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts from the config
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    text=[f"{v}{texts.get('value_suffix', '')}" for v in values],
    textposition='outside',
    textfont=dict(family='Arial', size=14),
    cliponaxis=False,
    hoverinfo='none',
    showlegend=False
))

# Configure the layout
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 14px; color: #555555;'>{texts.get('subtitle', '')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0,
        y=0.98,
        xanchor='left',
        yanchor='top',
        pad=dict(t=10, l=10)
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticksuffix=texts.get('value_suffix', ''),
        tickfont=dict(size=14, family='Arial'),
        range=[0, max(values) * 1.1] # Add padding for text labels
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        showline=False,
        showticklabels=True,
        tickfont=dict(size=16, family='Arial'),
        automargin=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=16, color="#333333"),
    margin=dict(t=120, b=80, l=10, r=40),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.12,
            xanchor='left', yanchor='top',
            font=dict(size=12, color='#888888', family='Arial')
        ),
        dict(
            text=texts.get('note', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.12,
            xanchor='right', yanchor='top',
            font=dict(size=12, color='#888888', family='Arial')
        )
    ]
)

# Generate the output image file path
output_path = json_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_path, scale=2)

print(f"Chart saved successfully to {output_path}")