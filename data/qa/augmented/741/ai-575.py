import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and load the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file at {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file at {json_path} is not a valid JSON.")
    sys.exit(1)

# Extract data and text elements from the loaded JSON
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly trace
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else '#CCCCCC',
    cliponaxis=False,
    texttemplate='%{text:.1f}',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
))

# Construct the source and note string with HTML for proper line breaks
source_note_text = []
if texts.get('note'):
    source_note_text.append(texts['note'])
if texts.get('source'):
    source_note_text.append(texts['source'])
source_note_html = "<br>".join(source_note_text)

# Update the layout of the chart to match the original image
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 15],
        showgrid=True,
        gridcolor='#E5E5E5',
        linecolor='black'
    ),
    margin=dict(l=100, r=20, t=40, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=source_note_html,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the chart to a PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    print("Please ensure you have the 'kaleido' package installed (`pip install kaleido`)")