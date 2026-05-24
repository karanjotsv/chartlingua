import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
y_labels = texts.get('y_axis_labels', {})

categories = [item['category'] for item in data]
values = [item['value'] for item in data]
bar_colors = [item['color'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=bar_colors,
    width=0.8,
    showlegend=False
))

# Update layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='#E5E5E5',
    margin=dict(l=80, r=20, t=40, b=150),
    xaxis=dict(
        tickangle=-60,
        tickfont=dict(size=10),
        showgrid=False,
        zeroline=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_standoff=25,
        tickmode='array',
        tickvals=y_labels.get('values', []),
        ticktext=y_labels.get('texts', []),
        range=[-0.5, 3.5],
        showgrid=False,
        zeroline=False,
        linecolor='black',
        ticks='outside'
    ),
    bargap=0.2
)

# Derive output filename from JSON path
base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")