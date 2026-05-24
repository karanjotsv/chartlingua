import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure based on the series data
# This structure supports multiple series, but the example has one
for i, series in enumerate(series_list):
    series_data = series.get('data', [])
    
    # Create text labels for the bars (e.g., "32%")
    text_labels = [f'{val}%' for val in series_data]

    fig.add_trace(go.Bar(
        x=series_data,
        y=categories,
        orientation='h',
        marker_color=colors[i % len(colors)],
        text=text_labels,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        # Increase the gap between the bar and the text label
        texttemplate='%{x}%',
        insidetextanchor='end'
    ))

# Update the layout of the figure for a clean, professional look
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts.get('title') if texts.get('title') else '',
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        ticksuffix='%',
        range=[0, 45], # Set range to provide space for labels
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40] # Explicitly set tick values
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showline=False,
        ticks='',
        autorange="reversed" # This is not strictly needed if data is pre-sorted, but ensures top-to-bottom display
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Use cliponaxis=False to prevent text labels from being cut off by the plot area
fig.update_traces(cliponaxis=False)


# Determine the output filename from the input JSON path
base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")