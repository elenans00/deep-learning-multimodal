#!/home/elena/deep-learning-multimodal/whisper/venvwhisper/bin/python3
import pandas as pd
import json
import argparse
import os
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings

# Extract data structure from the JSON data
def data_structure(json_data):
    # Initialize an empty list to store the extracted data
    extracted_data = []
    # Initialize variables to store previous timestamps
    prev_start = 0.0
    prev_end = 0.0
    # Iterate through each segment in the JSON data
    for segment in json_data["segments"]:
        # Iterate through each word in the segment
        for word_data in segment["words"]:
            # Extract the word
            word = word_data["word"]
            # Check if "start" and "end" keys exist
            if "start" in word_data and "end" in word_data:
                start = word_data["start"]
                end = word_data["end"]
                # Update previous timestamps
                prev_start = start
                prev_end = end
            else:
                # Use previous timestamps for words without their own timestamps
                start = prev_start
                end = prev_end                
            # Append the data to the list
            extracted_data.append([word, start, end])
    # Create a DataFrame from the list
    df = pd.DataFrame(extracted_data, columns=['word', 'start', 'end'])
    return df

# Extract metadata from the JSON file name
def extract_metadata(json_file):
    # file without extension and path
    filename = json_file.split('/')[-1].split('.')[0]
    # filename example: 2022-2023_ALF_EduardoMartinezGracia_clase1
    school_year = filename.split('_')[0]
    # school_year: 2022-2023
    subject = filename.split('_')[1]
    # subject: ALF
    professor = filename.split('_')[2]
    # professor: EduardoMartinezGracia
    class_title = filename.split('_')[3]
    # class_title: clase1
    return { "filename": filename, 
            "school_year": school_year, 
            "subject": subject, 
            "professor": professor, 
            "class_title": class_title
            }

# Chunk the text from the JSON file
def semantic_chunking(text, data_frame):
    # Create Text Splitter
    hf_embeddings = HuggingFaceEmbeddings()
    text_splitter = SemanticChunker(embeddings=hf_embeddings, number_of_chunks=50)
    # Split Text
    docs = text_splitter.create_documents([text])

    # Initialize an empty list to store the chunks
    chunks = []
    # Initialize the index of the last word processed
    last_word_index = 0

    # Iterate through the documents
    for doc in docs:
        # Get the document text
        doc_text = doc.page_content
        # Split the document text into words
        words = doc_text.split()
        # Get the number of words in the document
        num_words = len(words)
        # Take the words from the DataFrame starting from the index of the last word processed
        selected_words = data_frame.iloc[last_word_index:last_word_index + num_words] #no incluye la ultima fila
        # Calculate start and end times for the chunk
        start_time = selected_words.iloc[0]['start']  # Start time for the chunk is the start time of the first word
        end_time = selected_words.iloc[-1]['end']  # End time for the chunk is the end time of the last word
        # Create a dictionary for the chunk
        chunk_dict = {
            "start": start_time,
            "end": end_time,
            "text": doc_text,
            "words": selected_words.to_dict(orient='records') # Convert the selected words to a dictionary 
        }
        # Append the chunk to the chunks list
        chunks.append(chunk_dict)
        # Update the index of the last word processed for the next iteration
        last_word_index += num_words
    return chunks

# Main function
def main(input_directory, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of JSON files in the input directory
    json_files = [f for f in os.listdir(input_directory) if f.endswith('.json')]

    # Process each JSON file
    for file_name in json_files:
        # Create the input file path
        input_file = os.path.join(input_directory, file_name)

        # Check if the file exists
        if os.path.exists(input_file):
            # Read the JSON file
            with open(input_file, "r") as f:
                json_data = json.load(f) 

        # Create data structure from the JSON data
        df = data_structure(json_data)

        # Extract metadata from the JSON file name 
        metadata = extract_metadata(input_file)

        # Obtain the text from the corresponding TXT file to avoid extracting it from the JSON file
        txt_file_name = file_name.replace('.json', '.txt')
        txt_file_path = os.path.join(input_directory, txt_file_name)
        if os.path.exists(txt_file_path):
            # Read the TXT file
            with open(txt_file_path, 'r') as txt_file:
                text = txt_file.read()
        else:
            # Extract text from JSON if no TXT file exists
            text = []
            for segment in json_data["segments"]:
                text.append(segment["text"])
            text = " ".join(text) # Join all the text segments into a single string
                        # where each segment's text is separated by a space

        # Chunk the text from the JSON data 
        chunks = semantic_chunking(text, df)
        print(f"number of chunks: {len(chunks)}")

        # Create a dictionary to store the extracted data 
        video_data = {
            "metadata": metadata,
            "chunks": chunks
        }

        # Create the output file path
        output_file = os.path.join(output_folder, file_name)
        # Save the result as JSON
        with open(output_file, 'w') as file:
            json.dump(video_data, file, indent=4, ensure_ascii=False)
        print(f"Extraction completed. Output file: {output_file}")

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Extract metadata and chunks from input JSON files.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing JSON files')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    args = parser.parse_args()

    # Run the extraction
    main(args.input_directory, args.output_folder)
