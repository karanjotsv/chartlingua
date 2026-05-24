import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'")
        sys.exit(1)

    # --- Data Extraction ---
    data_points = chart_data.get('chart_data', [])
    texts = chart_data.get('texts', {})
    colors = chart_data.get('colors', [])

    labels = [item['category'] for item in data_points]
    values = [item['value'] for item in data_points]

    # --- Chart Creation ---
    # Note: Plotly does not support the 3D perspective effect seen in the original image.
    # This script creates a standard 2D pie chart, which is the correct representation of the data.
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#000000', width=1)),
        texttemplate='%{label}<br>%{value}%',
        textposition='inside',
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise'
    ))

    # --- Layout Configuration ---
    title_text = texts.get('title')
    subtitle_text = texts.get('subtitle')
    full_title = ""
    if title_text:
        full_title += f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><i>{subtitle_text}</i>" if full_title else f"<i>{subtitle_text}</i>"
        
    source_text = texts.get('source')

    fig.update_layout(
        title_text=full_title if full_title else None,
        title_x=0.5,
        title_font_size=20,
        font=dict(family="Arial", size=14, color="black"),
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=80, b=80),
        annotations=[
            dict(
                showarrow=False,
                text=source_text if source_text else "",
                x=0,
                y=-0.1,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                align="left"
            )
        ]
    )
    
    fig.update_traces(
        textfont_size=16,
        insidetextorientation='horizontal'
    )

    # --- Output ---
    # Derive output filename from input JSON path without using 'os' module
    last_slash_idx = max(json_file_path.rfind('/'), json_file_path.rfind('\\'))
    filename_with_ext = json_file_path[last_slash_idx+1:]
    last_dot_idx = filename_with_ext.rfind('.')
    base_name = filename_with_ext[:last_dot_idx] if last_dot_idx != -1 else filename_with_ext
    output_image_path = f"{base_name}.png"

    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    # Wrapping the script in a main function for better structure, 
    # but still avoiding defining other functions as requested.
    main()