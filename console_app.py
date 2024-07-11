from typing import List
from cv_scanner import key_words_counter

def run_menu() -> None:
    """
    """

    print("""
Pick a job you want to hire for:
1. Django developer
2. .NET developer
3. C++ developer
    """)

    job: int = int(input())
    
    key_words_django_dev: List[str] = ['python', 'django', 'html', 'css', 'javascript', 'api']
    key_words_dotnet_dev: List[str] = ['c#', '.net', 'entity framework', 'sql', 'wpf', 'api']
    key_words_cpp_dev: List[str] = ['c++', 'qt', 'cmake']
    
    key_words: List[str] = []

    match job:
        case 1:
            key_words = key_words_django_dev
        case 2:
            key_words = key_words_dotnet_dev
        case 3:
            key_words = key_words_cpp_dev
        case _:
            print('There is not such job!')

    final_counter = key_words_counter(key_words)
    print(final_counter)

def main() -> None:
    run_menu()

if __name__ == '__main__':
    main()