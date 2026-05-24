import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
data_series = chart_config['chart_data']
categories = chart_config['categories']
texts = chart_config['texts']
colors = chart_config['colors']
series_names = [s['name'] for s in data_series]

# Initialize the figure
fig = go.Figure()

# Plotly renders the y-axis from bottom to top, so we reverse the categories
# and the corresponding data values in each series to match the original chart's top-to-bottom order.
reversed_categories = categories[::-1]
for i, series in enumerate(data_series):
    # Determine text color for contrast; the last color is dark, requiring white text.
    text_font_color = 'white' if i == len(colors) - 1 else 'black'
    
    fig.add_trace(go.Bar(
        y=reversed_categories,
        x=series['values'][::-1],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(width=0)
        ),
        text=[f"{v}%" for v in series['values'][::-1]],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=16,
            color=text_font_color
        ),
        hoverinfo='none'
    ))

# Configure the layout
fig.update_layout(
    barmode='stack',
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(l=80, r=20, t=180, b=150),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 101]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        ticklen=0,
        categoryorder='array',
        categoryarray=reversed_categories,
        tickfont=dict(size=16)
    ),
    # Add all text elements as annotations for precise placement
    annotations=[
        # Title and Subtitle Block
        dict(
            text=f"<b>{texts['title']}</b><br>{texts['subtitle']}",
            align='left',
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=1.08,
            xanchor='left', yanchor='bottom',
            font=dict(size=18, color='black')
        ),
        # Column Headers
        dict(
            text=f"<b>{series_names[0]}</b>",
            align='center', showarrow=False, xref='paper', yref='paper',
            x=0.22, y=0.9, xanchor='center', yanchor='bottom',
            font=dict(size=14, color='black')
        ),
        dict(
            text=f"<b>{series_names[1]}</b>",
            align='center', showarrow=False, xref='paper', yref='paper',
            x=0.52, y=0.9, xanchor='center', yanchor='bottom',
            font=dict(size=14, color='black')
        ),
        dict(
            text=f"<b>{series_names[2]}</b>",
            align='center', showarrow=False, xref='paper', yref='paper',
            x=0.84, y=0.9, xanchor='center', yanchor='bottom',
            font=dict(size=14, color='black')
        ),
        # Source and Footer Block
        dict(
            text=f"{texts['source']}<br><b>{texts['footer']}</b>",
            align='left',
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            font=dict(size=12, color='#555555')
        )
    ]
)

# Generate the output PNG file
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")