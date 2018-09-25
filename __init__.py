from binaryninja import *
import re

def import_map(bv,function):
    
    map_path = get_open_filename_input("MAP file...")
    
    if not map_path:
        log_error("No MAP file selected")
        return

    with open(map_path, "r") as f_map:
        # First line is empty
        if f_map.readline().strip():
            log_error("Invalid MAP file format")
            return
        
        # Second line is field values
        if not re.match(r"^Start\s+Length\s+Name\s+Class$", f_map.readline().strip()):
            log_error("Invalid MAP file format")
            return

        # Read lines until the end and create symbols for valid functions
        for current_line in f_map:
            m = re.match(r"^(?P<address>[a-fA-F0-9]{5,16})\s+(function|procedure)\s+(?P<library>[\w]+)\.(?P<procedure>[\w]+)(:|\(|;)", current_line.strip())
            if m:
                bv.define_user_symbol(Symbol(SymbolType.DataSymbol, int(m.group("address"), 16), m.group("procedure")))


PluginCommand.register_for_address("Import MAP from IDR...", "Import MAP", import_map)
