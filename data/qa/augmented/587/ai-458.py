import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
json_filepath = pathlib.Path(json_path)

# Ensure the specified JSON file exists
if not json_filepath.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_filepath, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and text from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly; categories on Y-axis, values on X-axis
y_categories = [item['category'] for item in chart_data]
x_values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{val:.2f}' for val in x_values], # Format text to two decimal places
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevent text labels from being clipped
))

# Construct title string from JSON parts, if they exist
title_text = ""
if texts.get("title"):
    title_text = f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

# Prepare annotations for the source text
annotations = []
if texts.get("source"):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

# Update the layout for a clean, professional appearance
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        # Add padding to the right of the x-axis to fit data labels
        range=[0, max(x_values) * 1.15]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Display data from top to bottom as in the JSON
        showgrid=False,
        zeroline=False,
        ticks='',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    # Adjust margins to prevent labels from being cut off
    margin=dict(l=300, r=50, t=50, b=80),
    annotations=annotations
)

# Generate the output filename from the input JSON filename
output_filename = f"{json_filepath.stem}.png"
# Save the figure to a PNG file with high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")