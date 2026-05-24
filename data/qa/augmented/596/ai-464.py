import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive the base filename from the input JSON path for the output image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Load chart data and configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:.1f}' for v in values],
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False  # Prevent data labels from being clipped
))

# Update the layout of the chart for a clean, professional look
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 17.5],
        dtick=2.5
    ),
    margin=dict(l=80, r=40, t=40, b=120),  # Adjust margins to fit all elements
    annotations=[
        dict(
            text=f'<span style="color:#1F77B4;">{texts["note"]}</span>',
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.25,
            xanchor='left', yanchor='bottom',
            align='left'
        ),
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor='right', yanchor='bottom',
            align='right'
        )
    ]
)

# Customize the text font on the bars
fig.update_traces(
    textfont=dict(family='Arial', size=12, color='black')
)

# Write the output image file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)