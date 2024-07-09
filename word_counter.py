import os
import pymupdf

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
        doc = pymupdf.open("pdf", pdfbytes)
    
    text: str = chr(32).join([page.get_text() for page in doc])
    
    return text

def get_doc_paths(dir_path: str) -> list[str]:
    """Generate all files paths for the pdf and word documents of the directory located at dir_path.

    Args:
        dir_path (str): The path of the documents folder.

    Returns:
        list[str]: List of documents paths.
    """
    doc_paths: list[str] = []

    for path in os.listdir(dir_path):
        doc_path: str = os.path.join(dir_path, path)
        if os.path.isfile(doc_path) and (doc_path.endswith(".pdf") or doc_path.endswith(".docx")):
            doc_paths.append(doc_path)

    return doc_paths

def main():
    docs_paths: list[str] = get_doc_paths("./cv_documents/")

    first_doc_text: str = extract_text_from_doc(docs_paths[0])
    print(first_doc_text)


if __name__ == '__main__':
    main()