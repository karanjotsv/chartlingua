import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    name=''
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 125],
        tick0=0,
        dtick=20,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False
    ),
    annotations=[
        dict(
            text=texts.get('additional_info', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top'
        ),
        dict(
            text=f"{texts.get('source', '')}<br>{texts.get('note', '')}",
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='top'
        )
    ]
)

# Derive the output filename from the input JSON path
# This handles paths like './path/to/file.json' or 'file.json' on both Windows and Linux
base_name_with_ext = json_path.replace('\\', '/').split('/')[-1]
base_name = base_name_with_ext.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")