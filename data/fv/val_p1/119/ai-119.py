import sys
import json
import plotly.graph_objects as go
import os

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Ensure the file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    slice_colors = chart_config.get('colors', [])

    # Prepare data for Plotly trace
    labels = [d['category'] for d in chart_data]
    values = [d['value'] for d in chart_data]
    display_texts = [d['display_text'] for d in chart_data]
    pull_values = [d.get('pull', 0) for d in chart_data]
    text_colors = [d['text_color'] for d in chart_data]
    font_sizes = [d['font_size'] for d in chart_data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        text=display_texts,
        textinfo='text',
        marker=dict(colors=slice_colors),
        pull=pull_values,
        sort=False,
        direction='clockwise',
        showlegend=False,
        textfont=dict(
            family="Arial",
            color=text_colors,
            size=font_sizes
        )
    )

    # Create the figure
    fig = go.Figure(data=[pie_trace])

    # Combine title and subtitle
    title_text = texts.get('title')
    subtitle_text = texts.get('subtitle')
    full_title = ""
    if title_text:
        full_title += f"<b>{title_text}</b>"
    if subtitle_text:
        if full_title:
            full_title += "<br>"
        full_title += f"<i>{subtitle_text}</i>"

    # Update layout
    fig.update_layout(
        title_text=full_title if full_title else None,
        title_x=0.5,
        title_font_family="Arial",
        font_family="Arial",
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        margin=dict(t=60, b=60, l=40, r=40)
    )

    # Determine output filename
    filename_base = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{filename_base}.png"

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()