import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#A72727',
    showlegend=False
))

# Configure the layout of the chart
fig.update_layout(
    title_text=f"<b>{texts.get('title', '')}</b>" if texts.get('title') else None,
    title_x=0.5,
    title_font_size=28,
    yaxis_title_text=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    bargap=0.2,
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickmode='array',
        tickvals=categories,
        tickangle=0
    ),
    yaxis=dict(
        range=[0, 25000000],
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#DCDCDC',
        tickformat=',.0f'
    ),
    margin=dict(l=90, r=40, t=100, b=80)
)

# Determine the output filename from the input JSON path
output_filename_base = json_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")