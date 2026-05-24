import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Define the input JSON file path
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Derive the base filename for the output image
filename_base = json_file_path.stem

# Load the chart data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data series for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    texttemplate="<b>%{label}</b><br>%{value}%",
    textposition='inside',
    textfont=dict(color='white', size=16),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=75
)

# Create the figure and add the trace
fig = go.Figure(data=[pie_trace])

# Update the layout for title, font, and margins
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top',
        font=dict(size=20)
    ),
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=20, r=20, t=80, b=20),
    paper_bgcolor='rgba(255,255,255,1)' # Explicit white background to match original
)

# Define the output filename and save the chart as a PNG image
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")