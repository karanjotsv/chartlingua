import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and settings from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
source_text = texts.get('source')

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,  # Preserve the original order from the JSON file
    direction='clockwise',
    hoverinfo='label+percent',
    automargin=True
))

# Update layout for a clean, accurate appearance
fig.update_layout(
    showlegend=False,
    font=dict(family="Arial", size=12),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=100, r=100, t=40, b=60),  # Adjust margins to prevent label clipping
    annotations=[]
)

# Add source annotation if it exists
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.95,
        y=0,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10, color="#808080")
    )


# Generate the output PNG filename from the input JSON filename
output_filename = json_path.stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")