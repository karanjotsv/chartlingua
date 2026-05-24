import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file specified in command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract and prepare data for Plotly ---
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare labels for the legend, combining category name and value
pie_labels = [f"{item['label']} {item['value']}%" for item in chart_data]
pie_values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=pie_labels,
    values=pie_values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    sort=False,  # Preserve the original data order
    direction='clockwise',
    textinfo='none',  # No text on the pie slices
    hoverinfo='label+percent',
    hole=0.0 # Standard pie chart
))

# --- 4. Configure the layout for clarity and accuracy ---
annotations = []
# Add source text if it exists
if texts.get("source"):
    annotations.append(
        dict(
            text=texts["source"],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=0.01,
            xanchor='right',
            yanchor='bottom'
        )
    )

fig.update_layout(
    title=dict(text=""), # No title in the original
    showlegend=True,
    legend=dict(
        traceorder='normal', # Follows data order
        font=dict(family="Arial", size=12),
        bgcolor='rgba(0,0,0,0)', # Transparent background
        borderwidth=0
    ),
    font=dict(family="Arial"),
    margin=dict(l=40, r=40, t=40, b=60), # Margins to prevent clipping
    annotations=annotations,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# --- 5. Save the figure as a PNG image ---
base_filename = json_path.stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")