import os
import pandas as pd
import csv

def remove_newlines(text):
    if text is None:
        return ""
    text = str(text)
    text = text.replace('\n', ' ')
    text = text.replace('\\n', ' ')
    return ' '.join(text.split())

def process_text_files(domain):
    os.makedirs(f"text/{domain}", exist_ok=True)
    os.makedirs("processed", exist_ok=True)
    
    texts = []
    text_dir = f"text/{domain}/"
    
    for file in os.listdir(text_dir):
        file_path = os.path.join(text_dir, file)
        if os.path.isfile(file_path) and not file.startswith('.'):
            try:
                with open(file_path, "r", encoding='utf-8') as f:
                    text = f.read()
                    processed_name = os.path.splitext(file)[0]
                    texts.append((processed_name, text))
            except Exception as e:
                print(f"Error processing file {file}: {str(e)}")
    
    df = pd.DataFrame(texts, columns=['fname', 'text'])
    df['text'] = df['text'].apply(remove_newlines)
    
    output_path = 'processed/scraped.csv'
    try:
        df.to_csv(output_path, 
                 index=False,
                 escapechar='\\',
                 doublequote=True,
                 encoding='utf-8',
                 quoting=csv.QUOTE_ALL)
        print(f"Processed {len(texts)} files and saved to {output_path}")
    except Exception as e:
        print(f"Error saving CSV: {str(e)}")
        df['text'] = df['text'].replace(r'[\x00-\x1F\x7F-\x9F]', '', regex=True)
        df.to_csv(output_path,
                 index=False,
                 encoding='utf-8',
                 escapechar='\\')
    
    return df