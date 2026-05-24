import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

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
    marker=dict(color=colors),
    hoverinfo='none'
))

# Add annotations for data labels
annotations = []
for i in range(len(categories)):
    annotations.append(dict(
        xref='x',
        yref='y',
        x=values[i],
        y=categories[i],
        text=f"{values[i]}%",
        font=dict(family='Arial', size=14, color='rgb(50,50,50)'),
        showarrow=False,
        xanchor='left',
        xshift=5
    ))

# Add source and note annotations
annotations.append(dict(
    xref='paper', yref='paper',
    x=0, y=-0.12,
    xanchor='left', yanchor='top',
    text=texts['source'],
    showarrow=False,
    align='left',
    font=dict(family='Arial', size=12, color='rgb(100,100,100)')
))

annotations.append(dict(
    xref='paper', yref='paper',
    x=1.0, y=-0.12,
    xanchor='right', yanchor='top',
    text=texts['note'],
    showarrow=False,
    align='right',
    font=dict(family='Arial', size=12, color='rgb(100,100,100)')
))

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size: 16px; color:#555555;'>{texts['subtitle']}</span>",
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family='Arial', size=22)
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticksuffix='%',
        range=[0, max(values) * 1.1]
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    annotations=annotations,
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=60, t=120, b=80),
    bargap=0.35
)

# Generate output filename from JSON path
base_name = os.path.basename(json_path)
name_without_ext = os.path.splitext(base_name)[0]
output_filename = f"{name_without_ext}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")