import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filepath}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text}',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Allow text to be drawn outside the axis range
))

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        range=[0, max(values) * 1.25]  # Add padding for outside text
    ),
    yaxis=dict(
        autorange="reversed",
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    margin=dict(l=150, r=40, t=30, b=80),
    showlegend=False,
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color="#808080"
            )
        )
    ]
)

# Determine output filename from JSON path
base_filename = json_filepath.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")