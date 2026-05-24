import sys
import json
import plotly.graph_objects as go

# The script expects the path to the JSON file as the only command-line argument.
json_path = sys.argv[1]

# Load all chart data and text from the specified JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded dictionary.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly by extracting labels and values into separate lists.
# The order from the JSON is preserved.
labels = [d.get('label', '') for d in chart_data]
values = [d.get('value', 0) for d in chart_data]

# Create the figure and add the pie chart trace.
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1.5)),
    sort=False,  # This is crucial to maintain the order from the JSON file.
    direction='counterclockwise',
    textposition='outside',
    textinfo='label'
))

# Combine title and subtitle using HTML tags for formatting.
title_str = ""
if texts.get("title"):
    title_str += texts["title"]
if texts.get("subtitle"):
    title_str = f"{title_str}<br><sup>{texts['subtitle']}</sup>" if title_str else f"<sup>{texts['subtitle']}</sup>"

# Update the figure's layout.
fig.update_layout(
    showlegend=False,
    title_text=title_str if title_str else None,
    title_x=0.5,
    font_family="Arial",
    paper_bgcolor='white',
    plot_bgcolor='white',
    # Margins are set to prevent outside labels from being cut off.
    margin=dict(l=120, r=120, t=60, b=80)
)

# Add source text as an annotation at the bottom of the chart if it exists.
if texts.get("source"):
    fig.add_annotation(
        showarrow=False,
        text=texts["source"],
        xref="paper",
        yref="paper",
        x=0,
        y=0,
        xanchor="left",
        yanchor="top",
        yshift=-15 # Fine-tune vertical position below the chart area
    )

# Derive the output filename from the input JSON path without external libraries.
# This ensures the output PNG is named after the input JSON (e.g., 'my_chart.json' -> 'my_chart.png').
base_name_with_ext = json_path.split('/')[-1].split('\\')[-1]
base_name = base_name_with_ext.rsplit('.', 1)[0]
output_path = f"{base_name}.png"

# Save the figure to a PNG file with a higher resolution.
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")