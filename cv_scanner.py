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

def get_document_score(key_words: Dict[str, int], path: str) -> float:
    """Counts every accurance of each key word in the document 
    and computes a score for the document located at the specified path.

    Args:
        key_words (Dict[str, int]): The list of key words and the priority each of them has.
        path (str): The path to the document.

    Returns:
        float: Score of the document.
    """
    current_text_words = re.split(r',|;|:| |\n', extract_text_from_doc(path))
    key_words_doc: Dict[str, int] = {}
    for word in key_words:
        key_words_doc[word] = current_text_words.count(word)

    score: float = sum([0.7*key_words[word] + 0.3*key_words_doc[word] for word in key_words])

    return score

def get_top_doc(key_words: Dict[str, int], no_persons: int) -> List[str]:
    """Displays top documents based on the score.

    Args:
        key_words (Dict[str, int]): The list of key words and the priority each of them has.
        no_persons (int): The number of documents that will be displayed.

    Returns:
        List[str]: List of the top documents paths ordered by score.
    """
    doc_paths: List[str] = get_doc_paths('./cv_documents/')

    documents_score: Dict[str, float] = {path: get_document_score(key_words, path) for path in doc_paths}

    return [doc[0] for doc in sorted(documents_score.items(), key=lambda item: item[1], reverse=True)[:no_persons]]
