import sys
import json
import plotly.graph_objects as go

# Check if a command-line argument is provided
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
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})
categories = chart_data.get("categories", [])
series_list = chart_data.get("series", [])
series_colors = colors.get("series_colors", [])
text_font_colors = colors.get("text_font_colors", [])

# Create a new figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get("data", []),
        name=series.get("name", ""),
        marker_color=series_colors[i % len(series_colors)],
        text=series.get("data", []),
        texttemplate='%{text:.2f}%',
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color=text_font_colors[i % len(text_font_colors)],
            size=12
        )
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='stack',
    barnorm='percent',
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 100],
        ticksuffix='%',
        gridcolor='#e0e0e0'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        type='category',
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, b=120, t=40),
    annotations=[
        dict(
            text=texts.get("source", ""),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                family="Arial",
                size=10,
                color="#666666"
            )
        )
    ]
)

# Define the output filename based on the input JSON filename
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")