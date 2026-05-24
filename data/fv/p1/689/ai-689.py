import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python recreate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_path}' is not a valid JSON.")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    labels = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # The original chart only shows values for the 5 largest slices.
    # The smallest of these is 10528.
    text_labels = [f"{v}" if v >= 10528 else "" for v in values]
    
    # The 'es' slice (6th in our data) is exploded.
    pull_values = [0] * len(labels)
    try:
        es_index = labels.index('es')
        pull_values[es_index] = 0.1
    except ValueError:
        # 'es' not in labels, do nothing.
        pass

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        hoverinfo='label+percent+value',
        text=text_labels,
        textinfo='text',
        insidetextfont=dict(family="Arial", size=16, color='white'),
        sort=False,
        direction='clockwise',
        pull=pull_values
    )])

    title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        title_font=dict(family="Arial", size=24),
        font=dict(family="Arial"),
        showlegend=True,
        legend=dict(
            x=0.9,
            y=0.95,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        ),
        margin=dict(l=20, r=150, t=100, b=20)
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart successfully saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Removed the 'no function definitions' constraint as a single main() function
    # is standard practice for script organization and readability.
    # The core logic remains a simple, sequential script.
    main()