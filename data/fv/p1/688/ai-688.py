import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename base from the input JSON path
last_slash_idx = max(json_path.rfind('/'), json_path.rfind('\\'))
last_dot_idx = json_path.rfind('.')
if last_dot_idx > last_slash_idx:
    filename_base = json_path[last_slash_idx + 1:last_dot_idx]
else:
    filename_base = json_path[last_slash_idx + 1:]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly
# Insert a blank category and null data to create visual separation
categories_with_gap = chart_data['categories'][:1] + [""] + chart_data['categories'][1:]
series_with_gap = []
for s in chart_data['series']:
    new_series = {
        "name": s['name'],
        "values": s['values'][:1] + [None] + s['values'][1:]
    }
    series_with_gap.append(new_series)

# Reverse data for correct top-to-bottom display in Plotly
y_categories = categories_with_gap[::-1]

# Create figure
fig = go.Figure()

# Define text color for each bar series based on visual contrast
text_font_colors = ['white', 'black', 'white']

# Add traces for each data series
for i, series in enumerate(series_with_gap):
    values_reversed = series['values'][::-1]
    fig.add_trace(go.Bar(
        y=y_categories,
        x=values_reversed,
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=[f'{v}%' if v is not None else '' for v in values_reversed],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=14,
            color=text_font_colors[i]
        )
    ))

# Add custom legend-like headers using annotations above the first bar
us_data_values = [s['values'][0] for s in chart_data['series']]
cumulative_sum = 0
for i, series in enumerate(chart_data['series']):
    value = us_data_values[i]
    x_pos = cumulative_sum + value / 2
    cumulative_sum += value
    fig.add_annotation(
        x=x_pos,
        y=len(y_categories) - 1, # Position above the 'U.S.' bar
        yref='y',
        text=f"<b>{series['name']}</b>",
        showarrow=False,
        font=dict(family='Arial', size=12, color='black'),
        yshift=10, # Shift up from the bar
        yanchor='bottom'
    )

# Configure layout
fig.update_layout(
    barmode='stack',
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=12),
    margin=dict(l=90, r=20, t=180, b=80),
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size: 13px;'>{texts['subtitle']}</span>",
        x=0,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[0, 101] # Set range to 0-100%
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=14)
    )
)

# Add source and note annotation at the bottom
fig.add_annotation(
    text=f"{texts['source']}<br><b>{texts['note']}</b>",
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.1, # Adjusted for margins
    xanchor='left',
    yanchor='top'
)

# Output image file
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart generated and saved as {output_filename}")