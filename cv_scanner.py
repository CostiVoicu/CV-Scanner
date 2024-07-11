import re
import os
import pymupdf
from typing import Dict, List

def extract_text_from_doc(doc_path: str) -> str:
    """Extract text from a document located at fpath.

    Args:
        doc_path (str): The path of the document.

    Returns:
        str: The whole text of the document.
    """
    doc: pymupdf.Document = pymupdf.open(doc_path)

    if not doc.is_pdf:
        pdfbytes = doc.convert_to_pdf()
        doc = pymupdf.open('pdf', pdfbytes)
    
    text: str = chr(32).join([page.get_text() for page in doc])
    
    doc.close()

    return text.lower()

def get_doc_paths(dir_path: str) -> List[str]:
    """Generate all files paths for the pdf and word documents of the directory located at dir_path.

    Args:
        dir_path (str): The path of the documents folder.

    Returns:
        List[str]: List of documents paths.
    """
    doc_paths: List[str] = []

    for path in os.listdir(dir_path):
        doc_path: str = os.path.join(dir_path, path)
        if os.path.isfile(doc_path) and (doc_path.endswith('.pdf') or doc_path.endswith('.docx')):
            doc_paths.append(doc_path)

    return doc_paths

def key_words_counter(key_words: List[str]) -> Dict[str, int]:
    """Counts every accurance of each key word in the documents.

    Args:
        key_words (List[str]): The list of key words.

    Returns:
        Dict[str, int]: Dictionary that has the word as key and the accurances of that word in the documents as value.
    """
    key_words_dict: Dict[str, int] = {word:0 for word in key_words}
    
    doc_paths: List[str] = get_doc_paths('./cv_documents/')

    for path in doc_paths:
        current_text_words = re.split(r',|;|:| |\n', extract_text_from_doc(path))
        for word in key_words:
            key_words_dict[word] += current_text_words.count(word)

    return key_words_dict