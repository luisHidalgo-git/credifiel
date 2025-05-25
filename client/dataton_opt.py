import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Constants for bank fees
BBVA_COBRAR_MISMO = 1.6
BANAMEX_INTERBANCARIO = 1.75
SANTANDER_COBRAR_MISMO = 1.97
BANAMEX_COBRAR_MISMO = 1.75
BBVA_INTERBANCARIO = 6

# Bank ID mapping
BANK_MAPPING = {
    12: 'bbvaMexico',
    14: 'santander',
    2: 'banamex'
}

# Emisor ID mapping
EMISOR_MAPPING = {
    'banamex_interbancario': '00496',
    'bbva_cobrar_mismo': '5923',
    'santander_cobrar_mismo': '00623',
    'banamex_cobrar_mismo': '00496',  # Same as banamex_interbancario
    'bbva_interbancario': '4750'
}

def read_and_concatenate_excels(file_paths):
    """Read multiple Excel files and concatenate them into a single DataFrame"""
    dataframes = []
    
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path, parse_dates=['fechaCobroBanco'])
            # Verify columns exist
            required_columns = ['idListaCobro', 'idCredito', 'consecutivoCobro', 
                              'idBanco', 'montoExigible', 'montoCobrar', 
                              'montoCobrado', 'fechaCobroBanco', 'idRespuestaBanco']
            
            if not all(col in df.columns for col in required_columns):
                print(f"Warning: {file_path} missing required columns")
                continue
                
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    if not dataframes:
        raise ValueError("No valid Excel files found")
    
    # Concatenate all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Sort by idCredito and fechaCobroBanco to ensure chronological order
    combined_df['fechaCobroBanco'] = pd.to_datetime(combined_df['fechaCobroBanco'])
    combined_df = combined_df.sort_values(['idCredito', 'fechaCobroBanco'])
    
    return combined_df

def get_emision_elegida(id_banco, points, monto_exigible, monto_cobrado):
    """Determine which emission to use based on bank ID and conditions"""
    # If points < 0 or montoExigible != montoCobrado, always use BBVA
    if points < 0 or ( monto_exigible != monto_cobrado and id_banco != 12):
        return 'bbva_interbancario', BBVA_INTERBANCARIO
    
    # Otherwise, use the bank-specific emission
    elif id_banco == 12:
        return 'bbva_cobrar_mismo', BBVA_COBRAR_MISMO
    elif id_banco == 14:
        return 'santander_cobrar_mismo', SANTANDER_COBRAR_MISMO
    elif id_banco == 2:
        return 'banamex_cobrar_mismo', BANAMEX_COBRAR_MISMO
    else:
        # Default to BBVA if bank ID not recognized
        return 'banamex_interbancario', BANAMEX_INTERBANCARIO

def process_credits_optimized(df, current_date=None):
    """Process all credits in a single pass, calculating points and generating output"""
    if current_date is None:
        current_date = datetime.now()
    
    output_data = []
    points_map = {}

    # Group by idCredito and process everything in one pass
    for id_credito, credit_group in df.groupby('idCredito'):
        points = 0
        
        monto = credit_group['montoExigible'].sum()

        # Get the first bank ID for this credit - KEEPING ORIGINAL LOGIC
        id_banco = credit_group.iloc[0]['idBanco']
        print(id_banco)
        
        # Process each record for points calculation
        for idx, row in credit_group.iterrows():
            # Calculate months from current date
            record_date = row['fechaCobroBanco']
            if pd.isna(record_date):
                months_diff = float('inf')
            else:
                # Ensure record_date is datetime
                if not isinstance(record_date, datetime):
                    record_date = pd.to_datetime(record_date)
                months_diff = (current_date - record_date).days / 30.44  # Average days per month
            
            # Determine point multiplier based on recency from current date
            if months_diff <= 1:  # Within last month from now
                multiplier = 6
            elif months_diff <= 2:  # Within 2nd last month from now
                multiplier = 5
            elif months_diff <= 3:  # Within 3rd last month from now
                multiplier = 4
            elif months_diff <= 4:  # Within 4th last month from now
                multiplier = 3
            elif months_diff <= 5:  # Within 5th last month from now
                multiplier = 2
            else:  # Older than 5 months
                multiplier = 1
            
            # Apply point rules
            if row['montoCobrar'] != row['montoCobrado']:
                points -= 1 * multiplier
            selected_date='no pago'
            if pd.notna(row['montoExigible']) and pd.notna(row['montoCobrado']) and row['montoCobrar'] == row['montoCobrado']:
                points += 1 * multiplier
                fecha_cobro = row['fechaCobroBanco']
                if pd.notna(fecha_cobro):
                    if not isinstance(fecha_cobro, datetime):
                        fecha_cobro = pd.to_datetime(fecha_cobro)
                    
                    # Find nearest fortnight (1st or 15th)
                    day = fecha_cobro.day
                    if day <= 8:  # Closer to 1st
                        fortnight_date = fecha_cobro.replace(day=1)
                    elif day >= 23:  # Closer to next month's 1st
                        # Move to next month's 1st
                        if fecha_cobro.month == 12:
                            fortnight_date = fecha_cobro.replace(year=fecha_cobro.year + 1, month=1, day=1)
                        else:
                            fortnight_date = fecha_cobro.replace(month=fecha_cobro.month + 1, day=1)
                    else:  # Closer to 15th
                        fortnight_date = fecha_cobro.replace(day=15)
                    
                    # Adjust if fortnight falls on weekend (0=Monday, 6=Sunday)
                    while fortnight_date.weekday() >= 5:  # Saturday or Sunday
                        fortnight_date = fortnight_date - timedelta(days=1)
                    
                    selected_date = fortnight_date
            
            if pd.notna(row['montoExigible']) and pd.notna(row['montoCobrado']) and row['montoExigible'] == row['montoCobrado']:
                points += 1 * multiplier
        

        # Store points in map
        points_map[id_credito] = points
        
        # FIXING THE LOGIC ERRORS FROM ORIGINAL CODE:
        # Get last row's montoExigible for total amount check
        last_row = credit_group.iloc[-1]
        monto_tot = last_row['montoExigible']
        monto_cobrado = last_row['montoCobrado']
        
        # Get emission choice and fee - FIXED: using id_banco instead of credit_group[1]
        emision_name, emision_fee = get_emision_elegida(id_banco, points, monto_tot, monto_cobrado)
        
        # Determine if we should collect
        cobrar = True
        if monto_tot <= emision_fee:
            cobrar = False
        
        # Determine if partial - FIXED: checking id_banco == 12, not id_credito
        parcial = True
        if points > 0:
            parcial = False
        # Only add to output if cobrar is True and monto is positive
        
        if cobrar and monto > 0:

            #ELIMINA SI NO SE HA COBRADO
            if selected_date == 'no pago':
                continue
            else:
                output_data.append({
                    'idCredito': id_credito,
                    'idEmisor': EMISOR_MAPPING[emision_name],
                    'montoExigible': monto,
                    'montoACobrar': monto,
                    'emisionUsada': emision_name,
                    'points': points,
                    'Parcial': parcial,
                    'Date': selected_date
                })
    
    return pd.DataFrame(output_data), points_map

def main():
    # Example usage - replace with your actual file paths
    excel_files = [
        'ListaCobroDetalle2022.csv',
        #'ListaCobroDetalle2023.csv', 
        #'ListaCobroDetalle2024.csv',
        #'ListaCobroDetalle2025.csv'
    ]
    
    # Read and concatenate Excel files
    print("Reading and concatenating Excel files...")
    df = read_and_concatenate_excels(excel_files)
    print(f"Total records: {len(df)}")
    
    # Process credits with optimized single-pass function
    print("Processing credits...")
    output_df, points_map = process_credits_optimized(df)
    print(f"Credits processed. Output records: {len(output_df)}")
    
    # Save output
    output_filename = 'processed_credits.xlsx'
    output_df.to_excel(output_filename, index=False)    
    
    return output_df, points_map

if _name_ == "_main_":
    main()