import sys
import json
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument.
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data structures from the loaded JSON.
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly trace.
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]
text_labels = [item['text'] for item in chart_data]

# Create a Figure object.
fig = go.Figure()

# Add the bar trace to the figure.
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(size=11, family="Arial")
))

# Combine title and subtitle for the main chart title.
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

# Update the layout for a clean, professional appearance.
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis_title=texts['xaxis_title'],
    yaxis_title=texts['yaxis_title'],
    yaxis=dict(
        range=[0, 25000000],
        tickvals=[0, 5000000, 10000000, 15000000, 20000000],
        ticktext=["0", "5M", "10M", "15M", "20M"]
    ),
    font=dict(family="Arial"),
    template='plotly_white',
    plot_bgcolor='white',
    margin=dict(t=100, b=80, l=80, r=40),
    showlegend=False
)

# Derive the output filename from the input JSON path.
base_filename = json_path.replace('\\', '/').split('/')[-1].split('.')[0]
output_filename = f"{base_filename}.png"

# Write the figure to a high-resolution PNG file.
fig.write_image(output_filename, scale=2)

# Print a confirmation message to standard output.
print(f"Image saved to {output_filename}")