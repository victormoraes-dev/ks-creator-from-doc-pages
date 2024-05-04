import os


def remove_repeated_lines_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # Temporarily remove leading and trailing whitespaces from non-empty lines,
        # but keep empty lines and new lines as they are for formatting
        temp_lines = [line.rstrip() if line.strip() else '\n' for line in lines]

        unique_lines = []
        seen = set()

        for line in temp_lines:
            # Check if the line is not just a new line and not seen before
            if line.strip() and line not in seen:
                unique_lines.append(line + '\n')  # Add back the new line for non-empty lines
                seen.add(line)
            # If the line is just a new line, add it to maintain format
            elif line == '\n':
                unique_lines.append(line)

    # Write the cleaned content back to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)


def clean_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.md'):
            filepath = os.path.join(directory_path, filename)
            remove_repeated_lines_from_file(filepath)
            print(f"Cleaned {filename}")


# Specify the directory containing the markdown files
knowledge_sources_dir = 'knowledge_sources'
clean_directory(knowledge_sources_dir)
