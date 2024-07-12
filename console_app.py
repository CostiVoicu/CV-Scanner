from typing import Dict
from cv_scanner import get_top_doc

def get_key_words() -> Dict[str, int]:
    """Displays the available job profiles options that the user can choose from.

    Args:
        None.

    Returns:
        (Dict[str, int]): Key words for the job profile chosed.
    """
    print("""
Pick a job you want to hire for:
1. Django developer
2. .NET developer
3. HR
    """)

    job: int = int(input())
    
    key_words_django_dev: Dict[str, int] = {
        'python': 10, 
        'django': 9, 
        'html': 6, 
        'css': 6,
        'javascript': 6,
        'api': 8,
        'OOP': 8,
        'git': 8
    }
    key_words_dotnet_dev: Dict[str, int] = {
        'c#': 10, 
        '.net': 9, 
        'asp.net': 8, 
        'sql': 6, 
        'wpf': 7,
        'api': 7,
        'OOP': 8,
        'git': 8
    }
    key_words_hr: Dict[str, int] = {
        'communication ': 10, 
        'hr policies': 6, 
        'recruitment ': 9,
        'training': 5
    }

    match job:
        case 1:
            return key_words_django_dev
        case 2:
            return key_words_dotnet_dev
        case 3:
            return key_words_hr
        case _:
            print('There is no such job!')
            return {}

def get_no_persons() -> int:
    """Asks for the number of persons the user will choose from.

    Args:
        None.

    Returns:
        (int): Number of persons.
    """
    return int(input('How many persons you want to choose?: '))

def run_menu() -> None:
    """Display a menu to choose a job profile and the number of persons to choose from and displays top candidates.
    
    Args:
        None.

    Returns:
        (None).
    """

    no_persons = get_no_persons()
    key_words = get_key_words()

    final_counter = get_top_doc(key_words, no_persons)
    print(final_counter)

def main() -> None:
    run_menu()

if __name__ == '__main__':
    main()