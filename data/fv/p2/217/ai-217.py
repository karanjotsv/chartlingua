import sys
import json
import plotly.graph_objects as go
import os

def main():
    """
    Generates a pie chart from a JSON data file.
    Usage: python <script_name>.py <path_to_json_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python {} <json_file_path>".format(sys.argv[0]))
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'")
        sys.exit(1)

    # Extract data and texts from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    labels = [item.get('label', '') for item in chart_data]
    values = [item.get('value', 0) for item in chart_data]

    # Create the pie chart trace
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        textinfo='percent',
        texttemplate='%{value:.1f}%',
        insidetextfont=dict(color='white', size=14, family="Arial"),
        hoverinfo='label+percent',
        sort=False,  # Preserve the order from the JSON file
        direction='clockwise'
    ))

    # Update layout
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        showlegend=True,
        legend=dict(
            x=1,
            y=0.9,
            xanchor='left',
            yanchor='top',
            font=dict(size=12)
        ),
        margin=dict(t=100, b=50, l=50, r=250), # Increased right margin for legend
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)'
    )
    
    # Although Plotly's default pie is 2D, the prompt asks to recreate the chart.
    # The 3D effect in the source image is non-standard and not directly supported.
    # This script generates a clean 2D representation which is the standard Plotly equivalent.

    # Generate output filename from JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure to a PNG file
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Wrapping the script in a main function for better structure,
    # but keeping it simple and direct as requested.
    main()