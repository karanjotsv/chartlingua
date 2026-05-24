import sys
import json
import plotly.graph_objects as go

# Load chart data from the JSON file provided as a command-line argument
json_file_path = sys.argv[1]
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_details = json.load(f)

# Extract data and text from the loaded JSON
chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

# Prepare data for the plot
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create a Figure object
fig = go.Figure()

# Add the bar trace with data and styling from the JSON
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update the layout of the chart to match the original image
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        showline=False,
        range=[0, 70],
        dtick=10,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    ]
)

# Derive the base filename from the input JSON file path to name the output image
filename_part = json_file_path.split('/')[-1]
base_name = filename_part.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")