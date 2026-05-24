import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    texttemplate='%{y}',
    cliponaxis=False  # Ensures text for small values (like -1) is not clipped
))

# Update layout for a professional look and feel
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        automargin=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-3000, 16000],
        tickvals=[-2500, 0, 2500, 5000, 7500, 10000, 12500, 15000],
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black'
    ),
    showlegend=False,
    margin=dict(l=90, r=40, t=40, b=120),
    separators='., ',  # Use a space for the thousands separator
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#808080')
        )
    ]
)

# Use the texttemplate with the space separator from the layout
fig.update_traces(texttemplate='%{y: }')

# Determine the output filename from the input JSON path
output_filename = pathlib.Path(json_path).stem + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")