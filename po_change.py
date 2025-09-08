#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import re
import argparse
from pathlib import Path

def process_po_file_simple(file_path, dry_run=False):
    """
    Zpracuje PO soubor a nahradí msgstr prázdným řetězcem tam, kde je identický s msgid.
    Podporuje víceřádkové řetězce.
    """
    changes_made = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"Varování: Nelze číst soubor {file_path} jako UTF-8, přeskakuji...")
        return 0

    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Hledáme řádky začínající msgid
        if line.strip().startswith('msgid'):
            # Shromáždíme celý msgid blok (včetně víceřádkových)
            msgid_lines, msgid_content, next_i = collect_message_block(lines, i, 'msgid')

            # Přeskočíme prázdné msgid (obvykle pro metadata)
            if not msgid_content.strip():
                new_lines.extend(msgid_lines)
                i = next_i
                continue

            # Najdeme odpovídající msgstr
            j = next_i
            # Přeskočíme komentáře a prázdné řádky mezi msgid a msgstr
            while j < len(lines) and not lines[j].strip().startswith('msgstr'):
                if lines[j].strip() and not lines[j].strip().startswith('#'):
                    break
                new_lines.append(lines[j])
                j += 1

            if j < len(lines) and lines[j].strip().startswith('msgstr'):
                # Shromáždíme celý msgstr blok
                msgstr_lines, msgstr_content, final_i = collect_message_block(lines, j, 'msgstr')

                # Pokud jsou msgid a msgstr identické, nahradíme msgstr prázdným řetězcem
                if msgid_content == msgstr_content and msgid_content.strip() != "":
                    new_lines.extend(msgid_lines)
                    new_lines.append('msgstr ""\n')
                    changes_made += 1
                    # Zkrátíme dlouhé texty pro výpis
                    display_text = msgid_content[:50] + "..." if len(msgid_content) > 50 else msgid_content
                    print(f"  Změněno: '{display_text}' -> prázdný řetězec")
                else:
                    new_lines.extend(msgid_lines)
                    new_lines.extend(msgstr_lines)

                i = final_i
            else:
                new_lines.extend(msgid_lines)
                i = next_i
        else:
            new_lines.append(line)
            i += 1

    # Zapíšeme změny zpět do souboru (pokud to není dry run)
    if changes_made > 0 and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    return changes_made

def collect_message_block(lines, start_index, msg_type):
    """
    Shromáždí celý blok msgid nebo msgstr včetně víceřádkových řetězců.
    Vrací tuple: (seznam řádků, spojený obsah, index dalšího řádku)
    """
    block_lines = []
    content_parts = []
    i = start_index

    # První řádek (msgid "..." nebo msgstr "...")
    first_line = lines[i].strip()
    block_lines.append(lines[i])

    # Extrahujeme obsah z prvního řádku
    if '"' in first_line:
        start_quote = first_line.find('"')
        end_quote = first_line.rfind('"')
        if start_quote != end_quote:
            first_content = first_line[start_quote + 1:end_quote]
            content_parts.append(decode_po_string(first_content))

    i += 1

    # Pokračujeme čtením dalších řádků, dokud najdeme řádky začínající uvozovkami
    while i < len(lines):
        line = lines[i].strip()

        # Pokud řádek začíná uvozovkou, je to pokračování
        if line.startswith('"') and line.endswith('"'):
            block_lines.append(lines[i])
            # Extrahujeme obsah mezi uvozovkami
            content = line[1:-1]  # Odstraníme uvozovky
            content_parts.append(decode_po_string(content))
            i += 1
        else:
            break

    # Spojíme všechny části obsahu
    full_content = ''.join(content_parts)

    return block_lines, full_content, i

def decode_po_string(content):
    """
    Dekóduje escape sekvence v PO řetězci.
    """
    content = content.replace('\\n', '\n')
    content = content.replace('\\t', '\t')
    content = content.replace('\\r', '\r')
    content = content.replace('\\"', '"')
    content = content.replace('\\\\', '\\')
    return content

def find_po_files(directory="."):
    """
    Najde všechny *.po soubory v zadaném adresáři a podadresářích.
    """
    po_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.po'):
                po_files.append(os.path.join(root, file))

    return po_files

def main():
    parser = argparse.ArgumentParser(description="Nahradí msgstr prázdným řetězcem tam, kde je msgid identické s msgstr v PO souborech")
    parser.add_argument("-d", "--directory", default=".", help="Adresář pro vyhledávání PO souborů (výchozí: aktuální adresář)")
    parser.add_argument("--dry-run", action="store_true", help="Pouze zobrazí změny bez jejich provedení")
    parser.add_argument("-v", "--verbose", action="store_true", help="Podrobný výstup")

    args = parser.parse_args()

    # Najdeme všechny PO soubory
    po_files = find_po_files(args.directory)

    if not po_files:
        print(f"V adresáři '{args.directory}' nebyly nalezeny žádné *.po soubory.")
        return

    print(f"Nalezeno {len(po_files)} PO souborů:")

    total_changes = 0

    for po_file in po_files:
        if args.verbose:
            print(f"\nZpracovávám: {po_file}")
        else:
            print(f"Zpracovávám: {os.path.basename(po_file)}")

        changes = process_po_file_simple(po_file, args.dry_run)
        total_changes += changes

        if changes > 0:
            status = "(DRY RUN)" if args.dry_run else "(ULOŽENO)"
            print(f"  Provedeno změn: {changes} {status}")
        elif args.verbose:
            print(f"  Žádné změny")

    print(f"\n" + "="*50)
    print(f"Celkem změn: {total_changes}")
    if args.dry_run:
        print("Poznámka: Spusťte bez --dry-run pro provedení změn.")
    else:
        print("Všechny změny byly uloženy.")

if __name__ == "__main__":
    main()
