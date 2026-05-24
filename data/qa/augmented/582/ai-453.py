import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly by separating categories and values
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse the order of data to display from top to bottom, matching the original image
categories.reverse()
values.reverse()

# Create the figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    hoverinfo='none'
))

# Combine source and note for the caption, handling null values
source_text = texts.get('source')
note_text = texts.get('note')
caption_parts = [part for part in [source_text, note_text] if part]
caption = "<br>".join(caption_parts)

# Update layout for a clean, accurate, and professional appearance
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dash',
        zeroline=False,
        range=[0, 85]  # Set range to match original and provide space for bar labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False
    ),
    margin=dict(l=150, r=60, t=40, b=80),  # Adjust margins to prevent labels from being cut off
    annotations=[
        dict(
            text=caption,
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top'
        )
    ] if caption else []
)

# Generate the output filename from the input JSON path
output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_png_path, scale=2)

print(f"Chart successfully generated and saved to '{output_png_path}'")