from typing import List
from cv_scanner import key_words_counter

def main() -> None:
    key_words: List[str] = ['python', 'c++', 'qt', '.net', 'html', 'c#', 'django']
    final_counter = key_words_counter(key_words)
    print(final_counter)

if __name__ == '__main__':
    main()