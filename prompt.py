p_extraction_fv="""You MUST act as an expert Python data visualization assistant. Your primary objective is to meticulously analyze a given chart image, extract its data and text into a structured JSON format suitable for translation, and then generate a robust Python script using Plotly that accurately recreates the chart solely from that JSON data. The generated script must preserve the original data order and handle multilingual text input correctly, in addition to proactively addressing potential layout issues.
Input:
    1. <image_description>: A reference to, or the content of, the input chart image file.
    2. <image_filename_base>: The base filename string for the input image (e.g., "my_chart"). This base name is crucial for naming the JSON file read by the script and the output PNG image.
Your Tasks (Execute Sequentially):
    1. Analyze Image and Generate JSON Data Structure:
        - Identify chart type and store as chart_type if useful.
        - Extract all data series and categories (order must match original visual presentation). Store as chart_data.
        - Extract all visible text elements into a texts dictionary, preserving original English, capitalization, and line breaks (<br>). If an element is missing, set its value to null.
        - Extract primary colors as hex codes in a colors list, aligned with data series order.
        - Final JSON contains chart_data, texts, colors, and optionally chart_type.
    2. Generate Robust Python Plotly Code:
        - The script must accept the JSON path as a required command-line argument (e.g., via sys.argv[1] or argparse). This must be the only way to load the chart data.
        - Read the JSON from the provided path and use it as the only source for data and styling. Absolutely no hardcoded data or text in the script.
        - Use Plotly (plotly.graph_objects) to recreate the chart. Iterate through JSON data in order; apply colors and texts per JSON content.
        - Combine titles/subtitles and source/note using HTML as specified.
        - Multilingual/Unicode support: Code must be language-agnostic, display provided strings as-is, and handle non-Latin scripts without logic changes.
        - Layout: Prevent clipping/overlap with careful margins, anchors, and text placement. Font must be Arial.
        - Output the PNG image as <filename>.png (use the JSON path to derive the base filename), with scale=2.
        - Do not construct any absolute/relative paths or use external dependencies.
        - Clean code: no extra installs, no function definitions, no unnecessary comments, only minimal print.
Output Format:
Return the output in exactly two code blocks:
    - A single JSON code block containing the full JSON object.
    - A single Python code block containing the full script.
        - This script must take the path to the JSON file as its only argument.
Here is the image description: {image_description}, filename: {filename} and the chart image."""


p_extraction="""You MUST act as an expert Python data visualization assistant. Your primary objective is to meticulously analyze a given chart image, extract its data and text into a structured JSON format suitable for translation, and then generate a robust Python script using Plotly that accurately recreates the chart solely from that JSON data. The generated script must preserve the original data order and handle multilingual text input correctly, in addition to proactively addressing potential layout issues.
Input:
    1. <image_filename_base>: The base filename string for the input image (e.g., "my_chart"). This base name is crucial for naming the JSON file read by the script and the output PNG image.
Your Tasks (Execute Sequentially):
    1. Analyze Image and Generate JSON Data Structure:
        - Identify chart type and store as chart_type if useful.
        - Extract all data series and categories (order must match original visual presentation). Store as chart_data.
        - Extract all visible text elements into a texts dictionary, preserving original English, capitalization, and line breaks (<br>). If an element is missing, set its value to null.
        - Extract primary colors as hex codes in a colors list, aligned with data series order.
        - Final JSON contains chart_data, texts, colors, and optionally chart_type.
    2. Generate Robust Python Plotly Code:
        - The script must accept the JSON path as a required command-line argument (e.g., via sys.argv[1] or argparse). This must be the only way to load the chart data.
        - Read the JSON from the provided path and use it as the only source for data and styling. Absolutely no hardcoded data or text in the script.
        - Use Plotly (plotly.graph_objects) to recreate the chart. Iterate through JSON data in order; apply colors and texts per JSON content.
        - Combine titles/subtitles and source/note using HTML as specified.
        - Multilingual/Unicode support: Code must be language-agnostic, display provided strings as-is, and handle non-Latin scripts without logic changes.
        - Layout: Prevent clipping/overlap with careful margins, anchors, and text placement. Font must be Arial.
        - Output the PNG image as <filename>.png (use the JSON path to derive the base filename), with scale=2.
        - Do not construct any absolute/relative paths or use external dependencies.
        - Clean code: no extra installs, no function definitions, no unnecessary comments, only minimal print.
Output Format:
Return the output in exactly two code blocks:
    - A single JSON code block containing the full JSON object.
    - A single Python code block containing the full script.
        - This script must take the path to the JSON file as its only argument.
Here is the filename: {filename} and the chart image."""


p_chart_check="""You are an expert visual comparison and chart quality evaluator. Your task is to assess two chart images (Original, Rendered) based on two criteria: Semantic Consistency and Visual Flaws.
Input:
    1. Original Chart Image
    2. Rendered Chart Image (generated from code based on the original)
Task 1: Evaluate Semantic Consistency 
Assess if the Rendered Image accurately represents the same core data and key information as the Original Image. Focus on:
    - Data Values & Proportions: Are numerical values (bars, points, slices) substantially the same? Do relative proportions match?
    - Categories & Series: Do labels, axes, and legend entries match the original data structure and order?
    - Text Content: Are title, axis titles, legend labels, and other key text elements semantically identical or extremely close to the original?
    - Color Hue Consistency: While exact shades may differ, do the primary colors for data series maintain the same hue category (e.g., reds stay red/orange, blues stay blue/cyan, greens stay green)? A swap from red to blue is a major inconsistency.
    - Overall Message/Trend: Does the rendered chart convey the same main insight or pattern?
IGNORE minor stylistic differences (fonts, gridlines, spacing) UNLESS they hinder interpretation or violate the checks above.
Rating Scale and Criteria:
    - 5: Highly Consistent: Near-perfect semantic match in data, text, color hues, and overall message. Only negligible, non-misleading differences.
    - 4: Mostly Consistent: Core data, text, and message are accurate. Minor data inaccuracies, text variations, or color shade differences (hue preserved), but interpretation unchanged.
    - 3: Moderately Consistent: Some aspects captured, but noticeable discrepancies. Key values may be inaccurate, important text differs, color hues mismatched, or message partially distorted.
    - 2: Poorly Consistent: Significant data errors, trends misrepresented, text is wrong/misleading, or color usage creates confusion. Fundamentally different interpretation.
    - 1: Inconsistent / Unrelated: Completely different data, topic, or structure.
Task 2: Identify Visual Flaws (Yes/No)
Determine if the Rendered Image has significant visual flaws that impede understanding or indicate generation errors. Check for:
    - Severe Text Overlap: Critical labels, titles, or data points overlapping illegibly.
    - Element Clipping: Chart elements (data, labels, legends) cut off by boundaries.
    - Unreadable Text: Text is too small, blurry, or has unsupported characters.
    - Data Obscurity: Data points hidden behind other elements.
    - Empty/Malformed Chart: Blank image, error messages, or not a meaningful chart.
    - Gross Layout Issues: Elements positioned bizarrely, chart is nonsensical.
Answer Yes if any major flaws; No if not. Minor imperfections that do not hinder core interpretation = No.
Output Format:
Respond ONLY with a valid JSON object containing FOUR keys:
    - "similarity_rating": integer (1–5 based on Task 1)
    - "similarity_reason": string (brief explanation for the similarity rating)
    - "has_visual_flaws": boolean (true if significant flaws found, false otherwise)
    - "flaw_reason": string (brief explanation if flaws were found, otherwise “No significant flaws detected.”)
Now, evaluate the Original and Rendered images based on BOTH tasks. Respond ONLY with the JSON object."""


p_claim_check="""You are an expert evaluator for chart-claim pairs. Your task is to assess whether the provided 'Claim' is supported or refuted - based solely on the information presented in the accompanying chart image.
Do not use any external knowledge or make assumptions beyond what is visually represented or directly calculable from the chart.
Decision Criteria:
    - **support**:
        - The claim is explicitly and clearly validated by chart data.
        - All key facts in the claim are accurately represented in the chart.
        - Relationships (e.g., trends, comparisons, magnitudes) stated in the claim are directly visible or inferable from the chart without speculation.
        - There are no contradictions, missing references, or need for external assumptions.
    - **refute**:
        - The claim is directly contradicted by the chart's data or structure.
        - The chart disproves the key point(s) of the claim.
        - The claim misrepresents values, trends, or comparisons (e.g., states "X is highest" when Y is actually highest).
        - The claim fails to align with visible chart information and leads to false conclusions if taken as true.
Input Context:
    1. Chart Image
    2. Claim
Output Format:
You MUST respond ONLY with a valid JSON object containing two keys:
    - "class": one of "support" or "refute"
    - "reason": string (a brief explanation for your decision, referencing chart elements or data points where possible)
Example Output (support):
{
    "class": "support",
    "reason": "The claim correctly states that 'Product A' had the highest sales in Q4, which is clearly shown in the bar chart."
}
Example Output (refute):
{
    "class": "refute",
    "reason": "The claim says that 'Revenue increased in 2023 compared to 2022', but the chart shows a decrease in revenue."
}
Now, evaluate the specific image and claim provided in the user prompt. Respond only with the JSON object."""


p_query_check = """You are an expert evaluator for chart question-answering pairs. Your task is to assess the quality and correctness of the provided ’Answer’ in response to the ’Question’, based solely on the information presented in the accompanying chart image. Assign a rating from 1 to 5 based on the criteria below.
Do not use any external knowledge or make assumptions beyond what is visually represented or directly calculable from the chart.
Rating Scale and Criteria:
    - 5: Excellent (Fully Correct): The answer is completely accurate according to the chart data; directly and fully addresses the question; all information is visible or directly calculable from the chart; no ambiguities or unsupported inferences.
    - 4: Good (Mostly Correct): Substantially correct; addresses main point; may contain very minor inaccuracies or omissions that do not significantly mislead.
    - 3: Fair (Partially Correct): Mix of correct and incorrect information; may extract data but fail to answer the question; may make unsupported inferences; partially or inaccurately addresses the question.
    - 2: Poor (Mostly Incorrect): Contains significant factual errors; fundamentally misunderstands chart or question; core claim is wrong based on chart evidence.
    - 1: Very Poor (Completely Incorrect or Irrelevant): Completely false or irrelevant; no connection between answer and the chart content
Input Context:
    1. Chart Image
    2. Chart Question
    3. Proposed Answer
Output Format:
You MUST respond ONLY with a valid JSON object containing two keys:
    - "rating": integer (1 to 5)
    - "reason": string (brief explanation for your assigned rating, referencing chart elements or data points where possible)
Example Output (rating 5):
{
    "rating": 5,
    "reason": "The answer accurately states the value for 'Q3 Revenue' is $1.2M, which matches the value ..."
}
Example Output (rating 3):
{
    "rating": 3,
    "reason": "The answer correctly identifies 'Product A' as having the highest value, but incorrectly states ..."
}
Example Output (rating 1):
{
    "rating": 1,
    "reason": "The answer discusses stock market trends, which are completely absent from the provided ..."
}
Now, evaluate the specific image, question, and answer provided in the user prompt based on the 1-5 scale. Respond ONLY with the JSON object."""


p_translation="""You are an expert linguist and JSON data localization specialist simulating a translation process. Your task is to translate a given JSON object representing chart data & the associated {task_type} from {source_language_name}({source_language_code}) to {target_language_name}({target_language_code}). You must intelligently identify and translate only the user-facing text while preserving the JSON structure and non-textual data precisely.
Input Data:
You will receive a JSON object containing two keys:
    1. chart_json_data: The JSON object extracted from a chart (variable structure).
    2. {task_type}_to_translate: The "{task_type}" string in {source_language_code}.
CRITICAL Instructions for Translation:
    1. Goal: Produce a translated version of the input suitable for displaying the chart and {task_type} in {target_language_name}.
    2. Translate chart_json_data recursively:
        - Traverse the entire structure (nested dicts/lists).
        - ONLY translate string values meant for user display in {source_language_name} (titles, axis labels, legend entries, annotations, etc.).
        - DO NOT translate/modify:
            - JSON keys
            - Numerical values (int/float)
            - Strings only of numbers (e.g., "2023", "1.5")
            - Strings only of numbers with "%" (e.g., "55.5%", "-10%")
            - Hex color codes (e.g., "#1f77b4")
            - URLs, file paths, system identifiers
            - Boolean strings ("true", "false")
            - Type keywords (e.g., "stacked_bar", "Arial", "auto"). If unsure, do NOT translate.
            - null values and empty strings.
        - Preserve units and symbols unless a direct, standard equivalent is always used in {target_language_name}.
        - Output JSON MUST be identical in structure and data types to input. ONLY translatable string values change.
    3. Translate {task_type}_to_translate:
        - Translate "{task_type}".
        - Consistency: Use the exact same translation for terms that appear in both the chart JSON and {task_type}.
    4. Translation Quality Requirements:
        - Accuracy & Fidelity: Preserve factual meaning.
        - Naturalness & Fluency: Use grammatically correct, natural phrasing.
        - Consistency: Identical source terms = identical translation.
        - Cultural Appropriateness: Target-audience appropriate.
        - Linguistic Integrity: Correct grammar, syntax, style.
        - Vocabulary Usage: Accurate and context-appropriate.
        - Non-Latin/BiDi Support: Generate correct unicode. Standard rendering will handle text direction.
        - HTML tags: Preserve tags like <br> in correct position.
Output Format:
You MUST respond ONLY with a single, valid JSON object containing:
    - translated_chart_json: The processed chart JSON, structure identical to input, translations ONLY on user-facing text.
    - translated_{task_type}: The translated "{task_type}" string.
Input Data to Process:"""


p_translation_check="""You are an expert linguistic evaluator comparing two versions of content in {source_language_name}({source_language_code}). One is the 'Original Content', and the other is the 'Back-Translated Content'(which was translated to another language and then back to {source_language_name}). Your task is to evaluate the semantic equivalence between the Original and Back-Translated content based on the provided context, assigning ratings on a 1-5 scale. The required output format depends on the provided context.
Input Format (Provided in User Prompt):
You will receive a JSON object with three keys:
    1. context: A string indicating the type of content: either 'Chart JSON' or '{task_type_cap}'.
    2. original_content: The original content (either a JSON object for chart texts or a string of {task_type} in {source_language_name}).
    3. back_translated_content: The back-translated content (matching the structure of original_content) in {source_language_name}.
Evaluation Criteria and Rating Scale (1-5):
    - Focus: Semantic meaning and preservation of key information. Does the back-translation mean the same thing as the original?
    - Ignore: Minor grammatical variations, stylistic choices, or synonymous phrasing common in translation unless they significantly alter the meaning, introduce ambiguity, or omit/distort critical information.
    - 5: Excellent Equivalence— Perfect semantic match; only stylistic or trivial differences.
    - 4: Good Equivalence— Main meaning and most key info conveyed accurately; minor acceptable differences.
    - 3: Fair Equivalence— General topic captured, but some important details, nuance, or accuracy lost.
    - 2: Poor Equivalence— Significant errors; key info lost, distorted, or contradicted.
    - 1: No Equivalence/Unrelated— Meaning is completely different, nonsensical, or unrelated.
CRITICAL: Output Format Based on Context:
A. If context is 'Chart JSON':
    - Evaluate the overall semantic equivalence of the translatable text content in back_translated_content JSON vs. original_content JSON.
    - Respond ONLY with a single, valid JSON object with TWO keys:
        - rating: integer (1-5, overall JSON equivalence)
        - reason: string (brief justification)
Example:
{{
    "rating": 4,
    "reason": "Overall JSON text equivalence is good. Most titles and labels match semantically, though..."
}}
B. If context is '{task_type_cap}':
    - Evaluate the semantic equivalence between the original_content and back_translated_content.
    - Respond ONLY with a valid JSON object containing TWO keys:
        - {task_type}_rating: integer (1-5, {task_type} equivalence)
        - {task_type}_reason: string (brief justification)
Example:
{{
    "{task_type}_rating": 5,
    "{task_type}_reason": "Back-translated {task_type} perfectly matches original meaning.",
}}
Final Instruction: Analyze the original_content and back_translated_content based on context. Respond ONLY with the valid JSON object matching the required output format for that context."""


p_label_translation="""You are an expert linguist. Your task is to return a translated chart label in {target_language_name}({target_language_code}), using the given translated_query as context. 
Input:  
    - translated_query: A query string already translated into {target_language_code}.  
    - label_to_translate: The query label string to be translated into {target_language_code}.
Output:  
    - translated_label: The query label translated consistently with the terminology in translated_query.  
Return only the translated_label as plain text.
Input data to process:"""
