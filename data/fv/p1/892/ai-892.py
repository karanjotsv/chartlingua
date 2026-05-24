import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Generates a pie chart from a JSON data file.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    # Ensure the file exists
    if not os.path.isfile(json_file_path):
        print(f"Error: File not found at '{json_file_path}'")
        sys.exit(1)

    # Load data from JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_spec = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file_path}'")
        sys.exit(1)

    # Extract data for the chart
    chart_data = chart_spec.get('chart_data', [])
    texts = chart_spec.get('texts', {})
    colors = chart_spec.get('colors', [])
    text_colors = chart_spec.get('text_colors', [])

    labels = [item.get('label', '') for item in chart_data]
    values = [item.get('value', 0) for item in chart_data]

    # Create the pie chart
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
        texttemplate='%{label}<br>%{value}%',
        textposition='inside',
        textfont=dict(color=text_colors, size=12),
        sort=False,
        direction='clockwise',
        hoverinfo='skip'
    ))
    
    # Format the title
    title_text = f"<b>{texts.get('title', '')}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    # Update layout
    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        title_font_size=16,
        font=dict(family="Arial", size=12),
        showlegend=False,
        margin=dict(t=90, b=90, l=40, r=40),
        annotations=[
            dict(
                text=texts.get('source', ''),
                showarrow=False,
                xref="paper", yref="paper",
                x=1, y=0,
                xanchor='right', yanchor='bottom',
                align='right',
                font=dict(size=10)
            )
        ]
    )

    # Determine output filename and save the chart
    base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()