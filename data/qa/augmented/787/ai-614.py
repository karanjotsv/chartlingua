import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly by extracting categories and values
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False # Allows text to be drawn outside the plot area
))

# Combine source and note for the annotation
source_text = ""
if texts.get("source") and texts.get("note"):
    source_text = f'{texts["source"]}<br>{texts["note"]}'
elif texts.get("source"):
    source_text = texts["source"]
elif texts.get("note"):
    source_text = texts["note"]

# Update layout for a clean and accurate representation
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black',
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5000],
        gridcolor='#EAEAEA',
        linecolor='black',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color="#555555")
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12, textfont_family="Arial")

# Derive output filename from the input JSON file path
base_filename = os.path.splitext(json_file_path)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")