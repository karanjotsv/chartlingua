import sys
import json
import plotly.graph_objects as go

def format_number(n):
    return f"{n:,}".replace(",", " ")

# Check if a file path is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for plotting
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Format text for display on bars
bar_texts = [format_number(y) for y in y_values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=50, b=100, l=90, r=40),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 50000],
        tickvals=[0, 10000, 20000, 30000, 40000, 50000],
        ticktext=[format_number(v) for v in [0, 10000, 20000, 30000, 40000, 50000]],
        gridcolor='#e0e0e0',
        showline=False,
        zeroline=False
    )
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12)
    )

# Determine output filename and save the image
if '.' in json_path:
    base_filename = json_path[:json_path.rfind('.')]
else:
    base_filename = json_path

output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")