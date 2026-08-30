'''
This is the main service for the whole application, where gemini api is being used to evaluate answer sheets
'''
import os
import json
import re
from google import genai
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def evaluate_exam_submission(
    student_image_path: str,
    subject_book_context: str,
    tutor_solution_text: str = None
):
    is_pdf = student_image_path.lower().endswith('.pdf')
    if is_pdf:
        student_file = client.files.upload(file=student_image_path)
    else:
        student_file = Image.open(student_image_path)
    #this is the prompt which i am using for evaluating answer sheets with two contexts , one optional and the other compulsory
    prompt = f"""
    You are an academic evaluator grading a student's handwritten answer sheet.

    === CONTEXT 1: OFFICIAL SUBJECT REFERENCE MATERIAL (PRIMARY SOURCE OF TRUTH) ===
    {subject_book_context}

    === CONTEXT 2: TUTOR ANSWER KEY (OPTIONAL REFERENCE) ===
    {tutor_solution_text if tutor_solution_text else "No extra tutor answer key provided. Rely strictly on Context 1."}

    === GRADING RULES ===
    1. Read the student's submission and identify each distinct question they answered.
    2. Grade EACH question individually against the Reference Material (Context 1).
    3. For each question, assign a status:
       - "Correct": Fully accurate based on the textbook.
       - "Wrong": Factually incorrect or contradicts the textbook.
       - "Doubt": Partial credit, ambiguous handwriting, or concepts not found in the textbook requiring human teacher review.
    4. For each question, name the specific part of the Reference Material (e.g. unit, section, or chapter
       title/number) that you used to judge that answer. If nothing in the Reference Material covers that
       question, say so plainly instead of guessing.
    5. Calculate the overall total_score out of 100 based on the individual question points.

    Return ONLY a JSON object formatted as:
    {{
      "total_score": 85,
      "confidence": "High",
      "transcription_summary": "Extracted student answer text...",
      "book_citations": "Relevant textbook chapters/concepts matched...",
      "questions": [
        {{
            "question_number": "Q1",
            "student_answer_snippet": "Short snippet of what they wrote...",
            "status": "Correct",
            "awarded_points": 10,
            "max_points": 10,
            "reasoning": "Explanation of why it is correct, wrong, or why the AI has doubt.",
            "citation": "The specific unit/section/chapter of the Reference Material this question was graded against."
        }}
      ],
      "pedagogical_feedback": "Overall summary of the student's performance."
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[prompt, student_file],
    )
    
    
    if is_pdf:
        client.files.delete(name=student_file.name) #cleaning pdf for data privacy 

    raw_text = response.text

    match = re.search(r'\{.*\}', raw_text, re.DOTALL) #{...} for pulling this out incase it comes in gemini response
    if match:
        return json.loads(match.group(0))
    return {
        "total_score": 0,
        "confidence": "Low",
        "transcription_summary": "N/A",
        "book_citations": "N/A",
        "rubric_breakdown": [],
        "pedagogical_feedback": "Failed to parse structured JSON from AI."
    }