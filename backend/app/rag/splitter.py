from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_pages(pages: list[dict], chunk_size: int = 800, chunk_overlap: int = 120) -> list[dict]:
    if pages and "chunks" in pages[0]:
        return [chunk for page in pages for chunk in page.get("chunks", [])]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    )
    chunks: list[dict] = []
    for page in pages:
        clean = " ".join(page["text"].split())
        for text in splitter.split_text(clean):
            if len(text.strip()) >= 20:
                chunks.append({"content": text.strip(), "page_no": page["page_no"]})
    return chunks
