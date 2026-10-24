from pathlib import Path

from pypdf import PdfReader

folder = Path("data/raw/avalon")
total_pages = 0
total_pdfs = 0

if not folder.exists():
    print(f"Folder not found: {folder.resolve()}")
else:
    for pdf in folder.glob("*.pdf"):
        try:
            reader = PdfReader(str(pdf))
            pages = len(reader.pages)

            print(f"{pdf.name}: {pages} pages")
            total_pages += pages
            total_pdfs += 1

        except Exception as e:
            print(f"Could not read {pdf.name}: {e}")

    print("-----------------------")
    print(f"TOTAL PDF FILES: {total_pdfs}")
    print(f"TOTAL PAGES: {total_pages}")