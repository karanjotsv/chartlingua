import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from JSON
data_points = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Reverse data for correct top-to-bottom display in Plotly
data_points.reverse()

categories = [item['category'] for item in data_points]
values = [item['value'] for item in data_points]
bar_color = colors[0]

# Create text labels for each bar
text_labels = [f"{v}%" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=bar_color),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,  # Allow text to be drawn outside the plot area
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts['x_axis_title'],
        range=[0, 36],
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        title_font=dict(size=14)
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        autorange=True,
        tickfont=dict(size=12)
    ),
    margin=dict(l=380, r=50, t=40, b=80),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.1,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    ]
)

# Set the font for the text on the bars
fig.update_traces(textfont_size=12, textfont_color='black')

# Generate output filename from JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")