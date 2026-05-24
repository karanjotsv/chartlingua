import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data'][0]
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add the area trace
fig.add_trace(go.Scatter(
    x=data['x'],
    y=data['y'],
    mode='lines',
    fill='tozeroy',
    fillcolor=colors[0],
    line=dict(color=colors[1], width=1.5),
    showlegend=False
))

# Update layout and styling
fig.update_layout(
    title=dict(
        text=f'<span style="font-size:24px;">{texts["title"]}</span>',
        font=dict(family="Arial", color="#F5E87D"),
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        zeroline=False,
        tickvals=[1870, 1890, 1910, 1930, 1950, 1970, 1990, 2010],
        range=[1868, 2008]
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        type='log',
        showgrid=True,
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        tickvals=[10000, 100000, 1000000],
        ticktext=['10,000', '100,000', '1,000,000'],
        range=[4, 6] # log10(10000) to log10(1000000)
    ),
    plot_bgcolor='#D6D4C0',
    paper_bgcolor='#333333',
    font=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    margin=dict(l=90, r=50, t=120, b=80),
    annotations=[
        dict(
            text=texts['subtitle'],
            x=1940,
            y=800000,
            showarrow=False,
            font=dict(family="Arial", size=14, color="black"),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            borderpad=5,
            opacity=0.9
        ),
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.88,
            y=1.0,
            xanchor='center',
            yanchor='bottom',
            align='center',
            font=dict(family="Arial", size=10, color="white")
        )
    ]
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")