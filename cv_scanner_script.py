import re
import os
import pymupdf
from typing import Dict, List
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile

def extract_text_from_doc(file: UploadedFile) -> str:
    """Extract text from a document.

    Args:
        file (UploadedFile): The document that will be read.

    Returns:
        str: The whole text of the document.
    """
    doc: pymupdf.Document = pymupdf.open(stream=file.read(), filetype='pdf')

    if not doc.is_pdf:
        pdfbytes = doc.convert_to_pdf()
        doc = pymupdf.open('pdf', pdfbytes)
    
    text: str = chr(32).join([page.get_text() for page in doc])
    
    doc.close()

    return text.lower()

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

def get_top_doc(files:List[InMemoryUploadedFile], no_persons: int, key_words: Dict[str, int]) -> List[InMemoryUploadedFile]:
    """Gives top documents based on the score.

    Args:
        files (List[InMemoryUploadedFile]): The input documents.
        key_words (Dict[str, int]): The list of key words and the priority each of them has.
        no_persons (int): The number of documents that will be displayed.

    Returns:
        List[InMemoryUploadedFile]: List of the top documents ordered by score.
    """

    documents_score: Dict[str, float] = {path: get_document_score(key_words, path) for path in files}

    return [doc[0] for doc in sorted(documents_score.items(), key=lambda item: item[1], reverse=True)[:no_persons]]
