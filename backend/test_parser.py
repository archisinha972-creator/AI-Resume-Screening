from resume_parser import extract_resume_text

file_path = "data/resumes/sample_resume.pdf"

text = extract_resume_text(file_path)
print("---RESUME TEXT---")
print(text)