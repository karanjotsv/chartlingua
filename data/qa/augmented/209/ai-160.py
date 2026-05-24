import sys
import json
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Extract data and texts from the loaded JSON ---
categories = chart_data['categories']
series_data = chart_data['series']
texts = chart_data['texts']
colors = chart_data['colors']

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Plotly plots categories from bottom to top, so we reverse the lists to match the image's top-to-bottom order.
y_categories_reversed = categories[::-1]

for i, series in enumerate(series_data):
    # Reverse values to align with reversed categories
    values_reversed = series['values'][::-1]
    
    # Format text labels to show '.0' as integer
    text_labels = [f"{v:.1f}%".replace(".0%", "%") for v in values_reversed]
    
    fig.add_trace(go.Bar(
        y=y_categories_reversed,
        x=values_reversed,
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i]),
        text=text_labels,
        textposition='outside',
        cliponaxis=False,  # Prevents text labels from being clipped at the chart edge
        hoverinfo='none'
    ))

# --- 4. Configure the layout for accuracy and appearance ---
# Construct title string
title_text = ""
if texts.get("title") and texts.get("subtitle"):
    title_text = f"<b>{texts['title']}</b><br><sub>{texts['subtitle']}</sub>"
elif texts.get("title"):
    title_text = f"<b>{texts['title']}</b>"

fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        range=[0, 42]  # Set range to provide space for text labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    margin=dict(l=220, r=50, t=50, b=120),  # Adjust margins for labels and source text
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=10)
        )
    ]
)

fig.update_traces(textfont=dict(family="Arial"))

# --- 5. Save the chart as a high-resolution PNG file ---
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")