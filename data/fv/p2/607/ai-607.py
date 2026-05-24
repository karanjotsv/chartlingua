import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})

# Prepare data for plotting
# Plotly's horizontal bar chart displays categories from bottom to top,
# so we reverse the lists to match the visual order of the original image.
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

categories.reverse()
values.reverse()

# Format data labels to be bold using HTML tags
bold_text_values = [f'<b>{v}</b>' for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors.get("bars"),
    text=bold_text_values,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        size=18,
        color=colors.get("data_labels")
    ),
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    title_text=texts.get("title"),
    title_x=0.05,
    title_font=dict(
        family='Arial',
        size=24,
        color='black'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    font=dict(
        family='Arial',
        size=16,
        color='black'
    ),
    xaxis=dict(
        visible=False
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(
            family='Arial',
            size=18
        )
    ),
    margin=dict(l=150, r=30, t=100, b=30)
)

# Determine output filename from JSON path
output_path = pathlib.Path(json_path)
output_filename = f"{output_path.stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")