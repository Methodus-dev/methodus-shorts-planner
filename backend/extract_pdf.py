import PyPDF2
import json
from pathlib import Path
import re

def extract_pdf_content(pdf_path: str, max_pages: int = 50):
    """Extract content from PDF files"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            print(f"📄 Processing: {pdf_path}")
            print(f"   Total pages: {total_pages}")
            
            content = {
                "source": pdf_path,
                "total_pages": total_pages,
                "sections": []
            }
            
            full_text = ""
            pages_to_extract = min(max_pages, total_pages)
            
            for i in range(pages_to_extract):
                try:
                    text = reader.pages[i].extract_text()
                    full_text += text + "\n\n"
                except Exception as e:
                    print(f"   ⚠️ Error on page {i+1}: {e}")
            
            # Extract key sections and patterns
            sections = extract_sections(full_text)
            content["sections"] = sections
            content["full_text_preview"] = full_text[:5000]  # First 5000 chars as preview
            
            return content
            
    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")
        return None

def extract_sections(text: str):
    """Extract structured sections from text"""
    sections = []
    
    # Common section patterns in content creation guides
    section_patterns = [
        r"(Step \d+:.*?)(?=Step \d+:|$)",
        r"(Chapter \d+.*?)(?=Chapter \d+:|$)",
        r"(Module \d+.*?)(?=Module \d+:|$)",
        r"(\d+\.\s+[A-Z].*?)(?=\d+\.\s+[A-Z]|$)",
    ]
    
    for pattern in section_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)
        for match in matches:
            section_text = match.group(1).strip()
            if len(section_text) > 50:  # Only meaningful sections
                sections.append({
                    "type": "section",
                    "content": section_text[:1000]  # Limit to 1000 chars
                })
    
    # Extract bullet points and lists
    bullet_pattern = r"[•\-\*]\s+(.+?)(?=\n|$)"
    bullets = re.findall(bullet_pattern, text)
    if bullets:
        sections.append({
            "type": "bullets",
            "items": bullets[:50]  # First 50 bullets
        })
    
    # Extract questions (useful for prompts)
    question_pattern = r"([A-Z][^.!?]*\?)"
    questions = re.findall(question_pattern, text)
    if questions:
        sections.append({
            "type": "questions",
            "items": questions[:30]  # First 30 questions
        })
    
    return sections

def create_knowledge_base():
    """Create knowledge base from all PDFs"""
    pdf_files = [
        "../Copy_of_The_Content_Operating_System_By_Justin_Welsh.pdf",
        "../The_Content_Operating_System.pdf",
        "../The_Operating_System_2_.pdf"
    ]
    
    knowledge_base = {
        "sources": [],
        "content_creation_principles": [],
        "writing_frameworks": [],
        "examples": []
    }
    
    for pdf_path in pdf_files:
        if Path(pdf_path).exists():
            content = extract_pdf_content(pdf_path, max_pages=30)  # Limit pages for speed
            if content:
                knowledge_base["sources"].append(content)
    
    # Add hardcoded content creation principles from the templates we already know
    knowledge_base["content_creation_principles"] = [
        "Use the trailer-meat-summary-CTC structure for LinkedIn posts",
        "Start with a hook that creates curiosity or tension",
        "Provide actionable value in the meat section",
        "End with a clear call-to-action or question",
        "Mix content structures: actionable, motivational, analytical, contrarian, etc.",
        "Focus on helping your specific sub-niche",
        "Be polarizing - have a clear point of view",
        "Use storytelling to connect emotionally",
        "Keep posts concise and scannable",
        "Use line breaks for readability"
    ]
    
    knowledge_base["writing_frameworks"] = [
        {
            "name": "Trailer-Meat-Summary-CTC",
            "description": "Hook, deliver value, summarize, call-to-action",
            "example": "The trailer: Hook with curiosity\nThe meat: 3-5 key points\nThe summary: Recap the value\nThe CTC: Ask a question or give next step"
        },
        {
            "name": "Actionable",
            "description": "Step-by-step guide on how to do something",
            "example": "Here's how to [achieve X]:\n1. First step\n2. Second step\n3. Third step"
        },
        {
            "name": "Motivational",
            "description": "Inspire through story or anecdote",
            "example": "I was [problem]. Then [change event]. Now [result]. You can too."
        },
        {
            "name": "Contrarian",
            "description": "Challenge status quo with different perspective",
            "example": "Everyone says [common belief]. But here's why that's wrong..."
        },
        {
            "name": "Analytical",
            "description": "Break down and analyze a concept, company, or trend",
            "example": "Let's break down why [company/person] is successful..."
        }
    ]
    
    return knowledge_base

if __name__ == "__main__":
    print("🚀 Extracting PDF content...\n")
    
    knowledge_base = create_knowledge_base()
    
    # Save to JSON
    output_path = "../data/knowledge_base.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Knowledge base created successfully at {output_path}")
    print(f"📚 Sources processed: {len(knowledge_base['sources'])}")
    print(f"📝 Principles: {len(knowledge_base['content_creation_principles'])}")
    print(f"🎯 Frameworks: {len(knowledge_base['writing_frameworks'])}")

