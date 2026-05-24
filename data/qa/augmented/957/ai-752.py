import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

# Initialize the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=chart_data['x_values'],
    y=chart_data['y_values'],
    text=chart_data['y_values'],
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False  # Prevents text labels from being clipped
))

# Create annotations list for source/note
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#666666')
        )
    )
    
# Create shapes for vertical separator lines
shapes = []
for i in range(len(chart_data['x_values']) - 1):
    shapes.append(
        dict(
            type='line',
            xref='x', yref='paper',
            x0=i + 0.5, y0=0, x1=i + 0.5, y1=1,
            line=dict(color='#EAEAEA', width=1)
        )
    )

# Update the layout of the figure for a clean, professional look
fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=60, b=100, l=80, r=40),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 50],
        tick0=0,
        dtick=10,
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    annotations=annotations,
    shapes=shapes
)

# Derive the output filename from the input JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)