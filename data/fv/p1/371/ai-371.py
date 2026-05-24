import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])
legend_labels = texts.get('legend_labels', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add a trace for each data series in the specified order
for i, series_name in enumerate(legend_labels):
    y_values = [item['values'].get(series_name, 0) for item in chart_data]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=y_values,
        name=series_name,
        marker_color=colors[i],
        marker_line=dict(color='black', width=1)
    ))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note
source_text = ""
if texts.get('source'):
    source_text = texts['source']

# Update layout for styling and layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        tickangle=-90,
        showgrid=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        range=[0, 1200],
        dtick=100,
        gridcolor='darkgrey',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.4, # Positioned further down to avoid overlap
        xanchor='center',
        x=0.5,
        borderwidth=1,
        bordercolor='black'
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=150),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.45,  # Positioned below the legend
            xanchor='left', yanchor='bottom',
            align='left'
        )
    ]
)

# Determine output filename from the input JSON path
if '.' in json_file_path:
    base_filename = json_file_path.rsplit('.', 1)[0]
else:
    base_filename = json_file_path

output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")