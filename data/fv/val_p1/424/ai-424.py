import sys
import json
import plotly.graph_objects as go

# The script must accept the JSON path as a required command-line argument.
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON from the provided path and use it as the only source.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Prepare data for Plotly from the JSON structure
labels = [d['label'] for d in chart_info['chart_data']]
values = [d['value'] for d in chart_info['chart_data']]

# Use Plotly to recreate the chart.
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=chart_info['colors']),
    sort=False,  # Preserve original data order
    direction='clockwise',
    rotation=180,
    textinfo='percent',
    textposition='auto',
    hoverinfo='label+percent',
    insidetextfont=dict(family="Arial", size=16, color='black'),
    outsidetextfont=dict(family="Arial", size=14, color='black')
)])

# Handle layout, titles, fonts, and colors.
fig.update_layout(
    title=dict(
        text=chart_info['texts']['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(family="Times New Roman, serif", size=24, color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=14)
    ),
    font=dict(family="Arial", size=12, color="black"), # Global font
    paper_bgcolor=chart_info.get('background_color', 'white'),
    plot_bgcolor=chart_info.get('background_color', 'white'),
    margin=dict(t=120, b=100, l=40, r=40) # Prevent clipping
)

# Derive the base filename from the input JSON path to name the output PNG.
base_filename = json_path.rsplit('/', 1)[-1].rsplit('\\', 1)[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Output the PNG image with a scale of 2 for higher resolution.
fig.write_image(output_filename, scale=2)

# Minimal print output confirming the file has been saved.
print(f"Chart saved to {output_filename}")