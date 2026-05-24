import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the chart data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the loaded JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create a Plotly figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    textinfo='value',
    insidetextfont=dict(
        family="Arial",
        size=14,
        # Define text color for each slice for better contrast
        color=['white', 'black', 'black', 'white', 'white', 'white']
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

# Construct the title string with HTML for multi-line and styling
# The title is bolded to give it more emphasis, similar to the original.
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 16px;'>{texts['subtitle']}</span>"

# Update the figure layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20) # Main title font size
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    # Adjust margins to prevent title and source text from being clipped
    margin=dict(l=40, r=40, t=150, b=80),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15, # Position below the chart
            font=dict(size=10, family="Arial")
        )
    ]
)

# Derive the output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")