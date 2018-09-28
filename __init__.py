from binaryninja import *
import re

def create_tmp(base, depth):
    """
    Split the base file into several smaller ones based on depth.
    For some reason Binary Ninja does not want to process the base
    file correctly if it is too big.
    """
    pass

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
        for current_line in f_map.readlines():
            match = re.match(r"^(?P<address>[a-fA-F0-9]{5,16})\s+(function)\s+(?P<library>[\w]+)\.(?P<procedure>[\w]+):(?P<return>[\w]+);\s+[\w]+;$", current_line.strip())
            if match:
                address = int(match.group("address"), 16)
                if not bv.get_function_at(address):
                    bv.add_function(address)
                if not bv.get_symbol_at(address):
                    bv.define_user_symbol(Symbol(SymbolType.FunctionSymbol, address, match.group("procedure")))


PluginCommand.register_for_address("Import MAP from IDR...", "Import MAP", import_map)
