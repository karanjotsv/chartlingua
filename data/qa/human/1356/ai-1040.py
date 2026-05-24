import sys
import json
import plotly.graph_objects as go
import os

# Check if the file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = chart_data['categories']
series = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Plotly plots categories from bottom to top, so we reverse the lists
y_categories = categories[::-1]

# Add a trace for each data series
for i, s in enumerate(series):
    # Reverse data to match the reversed categories
    series_data = s['data'][::-1]
    
    fig.add_trace(go.Bar(
        y=y_categories,
        x=series_data,
        name=texts['legend_labels'][i],
        orientation='h',
        marker=dict(
            color=colors[i],
            line_width=0
        ),
        text=[f'{val}%' for val in series_data],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=16,
            color='white'
        ),
        hoverinfo='none'
    ))

# Configure the layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=f"<b>{texts['title']}</b>",
        font=dict(family='Arial', size=20, color='black'),
        x=0.01,
        xanchor='left',
        y=0.96,
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 100.5] # Add a little padding to the right
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        ticks='',
        categoryorder='array',
        categoryarray=y_categories,
        tickfont=dict(family='Arial', size=14)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="right",
        x=1,
        traceorder='normal',
        font=dict(family='Arial', size=14),
        bgcolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=140, r=20, t=140, b=80),
    font=dict(family="Arial", size=12, color="#333333"),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.01, y=1.02,
            text=f"<span style='color:#555555; font-size:16px;'>{texts['subtitle']}</span>",
            showarrow=False,
            xanchor='left',
            yanchor='bottom'
        ),
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.1,
            text=texts['source'],
            showarrow=False,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family='Arial', size=12, color='#666666')
        )
    ]
)

# Add separator lines between categories
# Main line below subtitle/legend
fig.add_shape(type="line", xref="paper", yref="paper",
              x0=0, y0=0.97, x1=1, y1=0.97,
              line=dict(color="darkgrey", width=2))

# Thin lines between bars
for i in range(len(y_categories) - 1):
    fig.add_shape(type="line", xref="paper", yref="y",
                  x0=0, y0=i + 0.5, x1=1, y1=i + 0.5,
                  line=dict(color="lightgrey", width=1))


# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")