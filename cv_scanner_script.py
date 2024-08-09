import re
import pymupdf
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from typing import Dict, List, Tuple
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

def download_nltk_packages():
    """Checks if punkt package is installed. If not, it starts downloading punkt and wordnet packages.
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        nltk.download('wordnet')

def get_lemmatized_text(document: InMemoryUploadedFile) -> str:
    """Lemmatize the text of the document at the specified path.

    Args:
        document (InMemoryUploadedFile): The document.

    Returns:
        str: Lemmatized text.
    """
    document.seek(0)
    download_nltk_packages()

    lemmatizer = WordNetLemmatizer()

    doc_text = extract_text_from_doc(document)
    
    tokens: List[str] = word_tokenize(doc_text)
    lemmatized_tokens: List[str] = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(lemmatized_tokens)

def get_document_score(key_words: Dict[str, int], document: InMemoryUploadedFile) -> float:
    """Counts every accurance of each key word in the document 
    and computes a score for the document.

    Args:
        key_words (Dict[str, int]): The list of key words and the priority each of them has.
        document (InMemoryUploadedFile): The document analyzed.

    Returns:
        float: Score of the document.
    """
    normal_text: str = extract_text_from_doc(document)
    lemmatized_text: str = get_lemmatized_text(document)

    key_words_doc: Dict[str, Tuple[int, int]] = {}
    for word in key_words:
        normal_text_count = len(re.findall(r'(?<!\w)' + re.escape(word) + r'(?!\w)', normal_text))
        lemmatized_text_count = len(re.findall(r'(?<!\w)' + re.escape(word) + r'(?!\w)', lemmatized_text))
        key_words_doc[word] = (normal_text_count, lemmatized_text_count)

    score: float = sum(
        (
            0.6*key_words[word] + 
            0.25*key_words_doc[word][0] + 
            0.15*key_words_doc[word][1]
        ) * (key_words_doc[word][0] > 0 or key_words_doc[word][1] > 0) 
        for word in key_words
    )

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

    documents_score: Dict[InMemoryUploadedFile, float] = {path: get_document_score(key_words, path) for path in files}

    return [doc[0] for doc in sorted(documents_score.items(), key=lambda item: item[1], reverse=True)[:no_persons]]
