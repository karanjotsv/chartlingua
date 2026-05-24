import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read the JSON data
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly, reversing order to match visual (top-to-bottom)
# Plotly's y-axis for horizontal bars starts from the bottom
y_categories = [d['category'] for d in chart_data][::-1]
x_values = [d['value'] for d in chart_data][::-1]

# Format data labels with spaces as thousands separators
text_labels = [f'{v:,}'.replace(',', ' ') for v in x_values]

# Create the bar chart trace
fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='auto', # 'auto' chooses inside/outside placement
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    insidetextanchor='middle'
))

# Combine title and subtitle
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout for a clean and accurate look
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        separatethousands=True,
        range=[0, 30000],
        tick0=0,
        dtick=2500,
        tickformat=" " # Use space as thousands separator on axis
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                family="Arial",
                size=10
            )
        )
    ]
)

# Generate output filename from the input JSON filename base
# e.g., 'path/to/ai-237.json' -> 'ai-237.png'
base_filename = json_path.split('/')[-1].split('.')[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")