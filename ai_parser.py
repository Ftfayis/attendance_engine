# ai_parser.py
from google import genai
import json
import time

def extract_timetable_data(image_path: str, api_key: str) -> dict:
    """
    Analyzes an image of a timetable and extracts unique subjects and weekly hours.
    Automatically retries up to 3 times if Google's servers are busy.
    """
    client = genai.Client(api_key=api_key)
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            
            image_file = client.files.upload(file=image_path)
            prompt = """
            Analyze this university timetable image. 
            Extract a list of all unique academic subjects and calculate the total number of hours scheduled per week for each subject.
            Return ONLY a raw JSON dictionary where the keys are the subject names (strings) and the values are the total weekly hours (integers). 
            Do not include any explanation or markdown formatting like ```json.
            """
            
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=[prompt, image_file])
            
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            return json.loads(raw_text.strip())
            
        except Exception as e:
            error_message = str(e)
            
    
            if "503" in error_message or "UNAVAILABLE" in error_message:
                if attempt < max_retries - 1:
                    time.sleep(5)  
                    continue
            return {"Error": f"Extraction failed after {attempt + 1} attempt(s). Details: {error_message}"}