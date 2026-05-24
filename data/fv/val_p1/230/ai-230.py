import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Prepare data for Plotly
chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

x_values = [item['year'] for item in chart_data]
y_values = [item['movements'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='inside',
    textangle=-90,
    insidetextanchor='middle',
    textfont=dict(
        family="Arial",
        size=12,
        color='white'
    ),
    hoverinfo='none'
))

# Build title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=24,
            color='black'
        )
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        tickfont=dict(family="Arial", size=12, color='black')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='#E5E5E5',
    paper_bgcolor='#E5E5E5',
    showlegend=False,
    margin=dict(t=100, b=80, l=40, r=40)
)

# Determine output filename and save the image
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")