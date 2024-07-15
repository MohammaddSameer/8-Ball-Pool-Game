import os

def remove_svg_files(directory):
    
    files = os.listdir(directory)

    for file in files:

        if file.endswith('.svg'):
            file_path = os.path.join(directory, file)
            os.remove(file_path)
            # print(f"Removed: {file_path}")

if __name__ == "__main__":
    directory = '.'
    remove_svg_files(directory)
