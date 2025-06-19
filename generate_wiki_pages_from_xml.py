#!/usr/bin/python3
# generate_wiki_pages_from_xml.py
## This Python script is used to generate content from the XML translation files to markdown files located in the /wiki/ page in this repository for better automatization

## Usage: 
### python3 generate_md_from_xml.py --xml-dir=~/SaveDesktop_main/translations/wiki --output-dir=~/SaveDesktop_webpage/wiki/synchronization --strings=individual_strings,_from_xml_file,_separated_with_comma
## Example:
### python3 generate_md_from_xml.py --xml-dir=$HOME/SaveDesktop_main/translations/wiki --output-dir=$HOME/SaveDesktop_webpage/wiki/synchronization --strings=synchronization_between_computers_title,set_up_first_pc,set_up_second_pc,bidirectional_sync,synchronization_files

import os
import glob
import xml.etree.ElementTree as ET
import argparse

def load_xml_strings(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        return {elem.attrib["key"]: (elem.text or "").strip() for elem in root.findall("str")}
    except Exception as e:
        print(f"Failed to parse {xml_path}: {e}")
        return {}

def extract_requested_strings(strings_dict, fallback_dict, requested_keys):
    output_lines = []
    for key in requested_keys:
        value = strings_dict.get(key) or fallback_dict.get(key)
        if value:
            output_lines.append(value)
            output_lines.append("")
        else:
            print(f"Missing string key: '{key}' (not found in translation or fallback)")
    return "\n".join(output_lines)

def main():
    parser = argparse.ArgumentParser(description="Generate Markdown files from XML translations.")
    parser.add_argument("--xml-dir", required=True, help="Path to XML files (e.g. ~/SaveDesktop_main/translations/wiki)")
    parser.add_argument("--output-dir", required=True, help="Where to write output .md files")
    parser.add_argument("--strings", required=True, help="Comma-separated list of XML keys to include (e.g. 'synchronization_between_computers_title,synchronization_files')")
    args = parser.parse_args()

    xml_dir = os.path.expanduser(args.xml_dir)
    output_dir = os.path.expanduser(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    string_keys = [k.strip() for k in args.strings.split(",")]

    # Load fallback English strings
    fallback_path = os.path.join(xml_dir, "en.xml")
    fallback_dict = load_xml_strings(fallback_path)
    if not fallback_dict:
        print("Fallback English XML not found or empty. Aborting.")
        return

    for xml_path in glob.glob(os.path.join(xml_dir, "*.xml")):
        lang_code = os.path.splitext(os.path.basename(xml_path))[0]
        md_path = os.path.join(output_dir, f"{lang_code}.md")

        strings_dict = load_xml_strings(xml_path)
        markdown_content = extract_requested_strings(strings_dict, fallback_dict, string_keys)

        try:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
                f.write("\n{% include footer.html %}")
            print(f"Generated: {md_path}")
        except Exception as e:
            print(f"Failed to write {md_path}: {e}")

if __name__ == "__main__":
    main()

