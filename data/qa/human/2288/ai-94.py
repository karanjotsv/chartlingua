import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a command-line argument for the JSON file is provided
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Verify that the JSON file exists
if not json_path.is_file():
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)

# Load the chart data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
text_positions = texts.get('text_positions', ['top center'] * len(texts['legend_items']))

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
num_series = len(texts['legend_items'])
series_data = [[item['values'][i] for item in chart_data] for i in range(num_series)]

# Initialize the Plotly figure
fig = go.Figure()

# Add a trace for each data series
for i in range(num_series):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series_data[i],
        name=texts['legend_items'][i],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=7),
        text=[f'{val:.2f}' for val in series_data[i]], # Format text to two decimal places
        textposition=text_positions[i],
        textfont=dict(
            family="Arial",
            size=12,
            color='#000000'
        )
    ))

# Configure the chart layout
fig.update_layout(
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E7EB',
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#E5E7EB',
        griddash='dash',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[5.2, 6.0],
        dtick=0.1,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, b=120, t=50),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color='grey'
            )
        )
    ]
)

# Define the output PNG filename based on the input JSON filename
output_path = json_path.with_suffix(".png")

# Save the figure to a PNG file
fig.write_image(str(output_path), scale=2)

print(f"Chart successfully generated and saved to '{output_path}'")