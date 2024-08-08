import re
import os
import nltk.downloader
import pymupdf
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from typing import Dict, List, Tuple

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

def get_lemmatized_text(path: str) -> str:
    """Lemmatize the text of the document at the specified path.

    Args:
        path (str): The path to the document.

    Returns:
        str: Lemmatized text.
    """
    download_nltk_packages()

    lemmatizer = WordNetLemmatizer()

    doc_text: str = extract_text_from_doc(path)
    tokens: List[str] = word_tokenize(doc_text)

    lemmatized_tokens: List[str] = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(lemmatized_tokens)

def get_document_score(key_words: Dict[str, int], path: str) -> float:
    """Counts every accurance of each key word in the document 
    and computes a score for the document located at the specified path.

    Args:
        key_words (Dict[str, int]): The list of key words and the priority each of them has.
        path (str): The path to the document.

    Returns:
        float: Score of the document.
    """
    normal_text = extract_text_from_doc(path)
    lemmatized_text = get_lemmatized_text(path)
    key_words_doc: Dict[str, Tuple[int, int]] = {}
    for word in key_words:
        normal_text_count = len(re.findall(r'\b' + re.escape(word) + r'\b', normal_text))
        lemmatized_text_count = len(re.findall(r'\b' + re.escape(word) + r'\b', lemmatized_text))
        key_words_doc[word] = (normal_text_count, lemmatized_text_count)

    score: float = sum([0.6*key_words[word] + 0.2*key_words_doc[word][0] + 0.2*key_words_doc[word][1] for word in key_words])

    return score

def download_nltk_packages():
    """Checks if punkt package is installed. If not, it starts downloading punkt and wordnet packages.
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        nltk.download('wordnet')

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
