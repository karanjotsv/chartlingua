import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
data_series = chart_info['chart_data']
x_categories = chart_info['x_categories']
texts = chart_info['texts']
bar_colors = chart_info['colors']['bar_colors']
text_font_colors = chart_info['colors']['text_font_colors']

# Initialize the figure
fig = go.Figure()

# Iterate through the data series from JSON to create a bar trace for each
for i, series in enumerate(data_series):
    # Format text to use a space for the thousands separator, matching the original image
    formatted_text = [f'{val:,.2f}'.replace(',', ' ') for val in series['y']]
    
    fig.add_trace(go.Bar(
        name=series['name'],
        x=x_categories,
        y=series['y'],
        marker_color=bar_colors[i],
        text=formatted_text,
        textposition='inside',
        textfont=dict(
            family="Arial",
            size=14,  # Increased for better visibility
            color=text_font_colors[i]
        ),
        insidetextanchor='middle'
    ))

# Configure the chart layout
fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, 3000],
        dtick=500,
        tickformat=" " # Use space as thousands separator on axis
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='array',
        tickvals=list(range(len(x_categories))),
        ticktext=x_categories,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=90, r=40, t=40, b=120),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.28,
            font=dict(size=10, color='#666666')
        )
    ]
)

# Determine the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")