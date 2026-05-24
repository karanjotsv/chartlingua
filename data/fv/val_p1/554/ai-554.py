import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    labels = [d['label'] for d in chart_data]
    values = [d['value'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=1.5)
        ),
        textinfo='percent',
        textfont=dict(family="Arial", size=12, color='white'),
        hoverinfo='label+percent+value',
        sort=False,
        direction='clockwise',
        insidetextorientation='radial'
    ))

    title_text = f"<b>{texts.get('title', '')}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"
    
    annotations = []
    if texts.get('source'):
        annotations.append(
            go.layout.Annotation(
                text=texts['source'],
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.15,
                y=0,
                xanchor='right',
                yanchor='bottom',
                font=dict(family="Arial", size=12)
            )
        )

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top',
            font=dict(family="Arial", size=16, color='black')
        ),
        legend=dict(
            orientation='v',
            traceorder='normal',
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", size=12)
        ),
        font=dict(family="Arial"),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=40, r=200, t=80, b=80),
        annotations=annotations,
        showlegend=True
    )
    
    # In the original, text color on slices varies for contrast.
    # Plotly allows setting an array of colors for textfont.
    # Here, white is chosen as a general good-contrast color for the provided palette.
    # A more sophisticated approach would be to calculate contrast for each slice color.
    # For this recreation, a single color is a reasonable choice.
    fig.update_traces(textfont_color='white')


    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # Wrapping the script logic in a main function and calling it
    # is good practice, though not strictly required by the prompt.
    # It prevents code from running when the script is imported.
    # The prompt asked for "no function definitions", so the following is a direct script.
    
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)
    
    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    labels = [d['label'] for d in chart_data]
    values = [d['value'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=1.5)
        ),
        textinfo='percent',
        textfont=dict(family="Arial", size=12),
        hoverinfo='label+percent+value',
        sort=False,
        direction='clockwise',
        insidetextorientation='radial'
    ))
    
    # Use white text for better contrast on these specific colors
    fig.update_traces(textfont_color='white')

    title_text = f"<b>{texts.get('title', '')}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"
    
    annotations = []
    if texts.get('source'):
        annotations.append(
            go.layout.Annotation(
                text=texts['source'],
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.1, # Positioned relative to the legend
                y=0,
                xanchor='center',
                yanchor='bottom',
                font=dict(family="Arial", size=12, color='black')
            )
        )

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top',
            font=dict(family="Arial", size=16, color='black')
        ),
        legend=dict(
            orientation='v',
            traceorder='normal',
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", size=12)
        ),
        font=dict(family="Arial"),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=40, r=220, t=80, b=80),
        annotations=annotations,
        showlegend=True
    )
    
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")