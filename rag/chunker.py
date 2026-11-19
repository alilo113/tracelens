from langchain_text_splitters import RecursiveCharacterTextSplitter

def read_log_file():
    logs = []
    with open("../data/sample_incident.log", "r", encoding="utf-8") as file:
        for log in file:
            logs.append(log)

    return logs

def chunk_logs():
    logs = read_log_file()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=10,
        length_function=len,
    )
    
    chunks = text_splitter.split_text("\n".join(logs))
    return chunks