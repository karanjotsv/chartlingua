import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data for easier access
chart_data = config['chart_data']
categories = chart_data['categories']
series_data = chart_data['series']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=1)
        ),
        text=[f'<b>{v}</b>' for v in series['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=14,
            color='white'
        )
    ))

# Adjust text color for better readability on lighter backgrounds
fig.update_traces(
    textfont_color='black', 
    selector=dict(marker_color=colors[2])
)
fig.update_traces(
    textfont_color='black', 
    selector=dict(marker_color=colors[3])
)

# Combine title and subtitle using HTML for rich text formatting
full_title = f"{texts['title']}<br><span style='font-size:14px;color:#505050'>{texts['subtitle']}</span>"

# Combine source and footer for the annotation
full_source_footer = f"{texts['source']}<br>{texts['footer']}"

# Update the layout of the figure for a clean, professional look
fig.update_layout(
    barmode='stack',
    title=dict(
        text=full_title,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family='Arial', size=18, color='black')
    ),
    xaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        autorange='reversed',
        tickfont=dict(family='Arial', size=12, color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="left",
        x=0.25,
        traceorder="normal",
        font=dict(family='Arial', size=12),
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(255,255,255,0)'
    ),
    margin=dict(l=220, r=20, t=150, b=120),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Arial'),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.22,
            xanchor='left', yanchor='top',
            text=full_source_footer,
            showarrow=False,
            align='left',
            font=dict(family='Arial', size=11, color='#666666')
        )
    ]
)

# Derive the output PNG filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")