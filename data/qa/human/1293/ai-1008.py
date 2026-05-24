import sys
import os
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = chart_config["chart_data"]
texts = chart_config["texts"]
colors = chart_config["colors"]
categories = chart_data["categories"]
series = chart_data["series"]

# --- 2. Create the Chart ---
fig = go.Figure()

# Add the main bar traces for "Disapprove" and "Approve"
for i in range(2):
    fig.add_trace(go.Bar(
        y=categories,
        x=series[i]["values"],
        name=series[i]["name"],
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=[f"{v}" for v in series[i]["values"]],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(family='Arial', size=16, color='black'),
        hoverinfo='none',
        showlegend=False  # Legend will be handled manually
    ))

# --- 3. Configure Layout and Styling ---
# Prepare annotations for the "DK" values
annotations = []
dk_series = series[2]
for i, category in enumerate(categories):
    x_pos = series[0]["values"][i] + series[1]["values"][i]
    annotations.append(dict(
        x=x_pos,
        y=category,
        text=str(dk_series["values"][i]),
        showarrow=False,
        xanchor='left',
        xshift=10, # Add a small gap after the bars
        font=dict(family='Arial', size=16, color='#555555')
    ))

# Add a separate annotation for the source and brand text
source_brand_text = f"{texts['source']}<br><b>{texts['brand']}</b>"
annotations.append(
    go.layout.Annotation(
        showarrow=False,
        text=source_brand_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        align='left',
        font=dict(family="Arial", size=12, color="#555555")
    )
)

# Combine title and subtitle using HTML for rich text formatting
chart_title = (
    f"<span style='font-size:24px; font-weight:bold;'>{texts['title']}</span><br>"
    f"<span style='font-size:15px; color:#555555;'>{texts['subtitle']}</span>"
)

fig.update_layout(
    title=dict(
        text=chart_title,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    barmode='stack',
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[0, 105]  # Extend range to accommodate DK labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=True,
        autorange='reversed',
        tickfont=dict(family='Arial', size=14, weight='bold', color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0.89,
        xanchor="left",
        x=0.35,
        traceorder='normal',
        font=dict(family="Arial", size=13),
        borderwidth=0
    ),
    margin=dict(l=100, r=40, b=100, t=140),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    annotations=annotations,
    showlegend=True
)

# --- 4. Add Custom Legend Entries ---
# Add invisible traces to create a custom legend that matches the original chart's style and placement
fig.add_trace(go.Scatter(
    x=[None], y=[None], mode='markers',
    marker=dict(symbol='square', color=colors[0], size=15),
    name=series[0]["name"]
))
fig.add_trace(go.Scatter(
    x=[None], y=[None], mode='markers',
    marker=dict(symbol='square', color=colors[1], size=15),
    name=series[1]["name"]
))
# For the text-only legend item, use a transparent marker
fig.add_trace(go.Scatter(
    x=[None], y=[None], mode='markers',
    marker=dict(symbol='square', color='rgba(0,0,0,0)', size=0),
    name=f"<span style='color:#555555'>{series[2]['name']}</span>"
))


# --- 5. Output the Image ---
# Derive the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")