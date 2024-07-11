from typing import Dict
from cv_scanner import key_words_counter

def run_menu() -> None:
    """Display a menu with job profiles option based on what the documents will be scanned."""

    print("""
Pick a job you want to hire for:
1. Django developer
2. .NET developer
3. C++ developer
    """)

    job: int = int(input())
    
    key_words_django_dev: Dict[str, int] = {
        'python': 10, 
        'django': 9, 
        'html': 6, 
        'css': 6,
        'javascript': 6,
        'api': 8,
        'OOP': 8
    }
    key_words_dotnet_dev: Dict[str, int] = {
        'c#': 10, 
        '.net': 9, 
        'entity framework': 8, 
        'sql': 6, 
        'wpf': 7,
        'api': 7,
        'OOP': 8
    }
    key_words_cpp_dev: Dict[str, int] = {
        'c++': 10, 
        'qt': 6, 
        'cmake': 7,
        'OOP': 8
    }
    
    key_words: Dict[str, int] = {}

    match job:
        case 1:
            key_words = key_words_django_dev
        case 2:
            key_words = key_words_dotnet_dev
        case 3:
            key_words = key_words_cpp_dev
        case _:
            print('There is no such job!')

    final_counter = key_words_counter(key_words)
    print(final_counter)

def main() -> None:
    run_menu()

if __name__ == '__main__':
    main()