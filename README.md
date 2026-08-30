# AI Answer Checker

**This project is licensed under CC BY-NC 4.0. No commercial use allowed.**

This is a Django web app I built for my Project Java and Web Development course. 
The idea is simple:

+A teacher creates a subject 

+Uploads the textbook/reference material for it(for example the text book from which the question paper was  created)

+Then uploads photos or PDFs of student answer sheets.

The app sends the sheet to Google's Gemini model along with the reference
material (and an optional tutor answer key), and it comes back with a score, a per-question breakdown,
and written feedback the teacher can review.

## Tech stack

- Django (SQLite for the database, nothing fancy)
- Bootstrap for the front-end
- Google Gemini (via the `google-genai` Python SDK) for reading the handwriting and grading it
- PyPDF2 to pull text out of the uploaded reference textbooks

## Running it locally

1. Clone the repo and set up a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your-key-here
   SECRET_KEY=any-random-string
   ```
   The Gemini key I used for grading is in my submission notes since I didn't want to leave a live key
   sitting in a public repo.
3. Run the migrations and start the server:
   ```
   python manage.py migrate
   python manage.py runserver
   ```
4. Go to `http://127.0.0.1:8000/`, register an account, and you're in.

## Notes

Grading a submission takes a few seconds since it's a real API call to Gemini each time, so don't worry
if the upload page seems to hang a bit after you submit. Just wait patiently! 

Thankyou!
