import sys
import json
import os
import plotly.graph_objects as go

def get_text_color(hex_color):
    """Determine if text should be black or white based on background color luminance."""
    hex_color = hex_color.lstrip('#')
    try:
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
        return 'black' if luminance > 140 else 'white'
    except (ValueError, IndexError):
        # Default to black for invalid hex codes
        return 'black'

# --- Main script execution ---

# Validate command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_file_path}'.")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
y_categories = chart_data['y_categories']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data['series']):
    text_color = get_text_color(colors[i])
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=y_categories,
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=1) # Creates separation between segments
        ),
        text=series['x'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color=text_color
        )
    ))

# Configure the chart layout
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=12, color='#333333'),
    margin=dict(l=280, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        title_font=dict(size=14),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        autorange=True
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        categoryorder='array', # Enforces the order provided in the JSON
        categoryarray=y_categories
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5,
        traceorder='normal',
        font=dict(size=14)
    )
)

# Add source annotation if it exists
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=12, color='#666666')
    )

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2, width=900, height=600)
    print(f"Chart successfully saved to '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)