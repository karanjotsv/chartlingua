import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    # Read data from the specified JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    # Extract data, texts, and colors
    chart_data = chart_info.get("chart_data", {})
    texts = chart_info.get("texts", {})
    colors = chart_info.get("colors", [])
    
    # Initialize figure
    fig = go.Figure()

    # Add traces for each data series
    for i, series in enumerate(chart_data.get("series", [])):
        fig.add_trace(go.Scatter(
            x=chart_data.get("x"),
            y=series.get("y"),
            mode='lines',
            name=series.get("name", ""),
            line=dict(color=colors[i] if i < len(colors) else None, width=1.5),
            hoverinfo='skip' 
        ))

    # Build title string
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    # Update layout
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title=dict(
            text=title_text,
            x=0.05,
            xanchor='left'
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1930, 2017, 4)),
            ticktext=[f"{year}" for year in range(1930, 2017, 4)],
            showgrid=False,
            showline=True,
            linecolor='lightgrey',
            linewidth=1,
            zeroline=False,
            ticks='outside',
            tickson='boundaries'
        ),
        yaxis=dict(
            autorange='reversed',
            range=[85, -5],
            dtick=10,
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=1,
            showline=False,
            zeroline=False,
            title=texts.get("y_axis_title")
        ),
        showlegend=False,
        margin=dict(l=40, r=20, t=60, b=40)
    )

    # Add source annotation if it exists
    if texts.get("source"):
        fig.add_annotation(
            text=texts.get("source"),
            xref="paper", yref="paper",
            x=0, y=-0.1,
            xanchor="left", yanchor="top",
            showarrow=False,
            font=dict(size=10)
        )

    # Define output filename and save the image
    output_filename = json_path.with_suffix(".png")
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()