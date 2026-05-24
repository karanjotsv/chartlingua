import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
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

# Extract data and texts from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
x_values = [item['category'] for item in chart_data]
y_values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    font_family="Arial",
    font_color="#000000",
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        linecolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        range=[0, 4],
        dtick=0.5,
        linecolor='black'
    ),
    annotations=[
        dict(
            text=texts.get('note'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='top',
            font=dict(
                color="#2A73CF"
            )
        ),
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top'
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12)

# Define output filename from the input JSON filename
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")