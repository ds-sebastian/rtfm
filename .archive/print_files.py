import os

from langchain_community.document_loaders import TextLoader


def extract_all_files(allowed_extensions=[".py"]):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs = []
    # os walk but skip '.archive' directories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            file_extension = os.path.splitext(file)[1]
            if file_extension in allowed_extensions and ".archive" not in dirpath:
                try:
                    loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                    docs.extend(loader.load_and_split())
                except Exception as e:
                    pass
    return docs


def main():
    docs = extract_all_files()
    for doc in docs:
        print("----------------")
        print(f'File: {doc.metadata["source"]}\n')
        print(f"Code:\n {doc.page_content}\n")


if __name__ == "__main__":
    main()
