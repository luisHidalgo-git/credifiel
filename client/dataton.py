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
            df = pd.read_csv(file_path)
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
    if points < 0 or (pd.notna(monto_exigible) and pd.notna(monto_cobrado) and monto_exigible != monto_cobrado and id_banco != 12):
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

def calculate_points_for_credit(credit_df, current_date=None):
    """Calculate points for a specific credit based on rules"""
    points = 0
    
    # Use provided date or current date
    if current_date is None:
        current_date = datetime.now()
    
    for idx, row in credit_df.iterrows():
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
        if pd.isna(row['montoCobrar']):
            points -= 1 * multiplier
        
        if pd.notna(row['montoExigible']) and pd.notna(row['montoCobrado']) and row['montoExigible'] == row['montoCobrado']:
            points += 1 * multiplier
    
    return points

def calculate_all_credit_points(df, current_date=None):
    """Calculate points for all credits and return a mapping"""
    print("entered calculate all credit points")
    if current_date is None:
        current_date = datetime.now()
    
    # Initialize points map
    points_map = {}
    
    # Group by idCredito and calculate points for each
    for id_credito, credit_group in df.groupby('idCredito'):
        points = calculate_points_for_credit(credit_group, current_date)
        points_map[id_credito] = points
    
    print("Exited for loop calculate all credit points")
    return points_map

def process_credits(df, points_map=None):
    """Process all credits and generate output data"""
    output_data = []
    

    
    # Group by idCredito
    for id_credito, credit_group in df.groupby('idCredito'):
        # Calculate monto (sum of montoExigible where montoCobrar is null)
        monto_mask = credit_group['montoExigible'].isna()
        monto = 0
        monto = credit_group.loc[not monto_mask, 'montoExigible'].sum()
        monto_cobrado = credit_group.loc['montoCobrado']
        
        # Get points from map
        points = points_map.get(id_credito, 0)

        # Get emission choice and fee
        emision_name, emision_fee = get_emision_elegida(credit_group[1], points,monto, monto_cobrado)
        
        monto_tot=0
        monto_tot = credit_group.iloc[-1]       
        cobrar = True
        if  monto_tot <= emision_fee:
            cobrar = False
        
        parcial = True
        if(points>0 or id_credito ==12):
            parcial=False
        # Only add to output if cobrar is True
        if cobrar and monto > 0:  # Also check that monto is positive
            output_data.append({
                'idCredito': id_credito,
                'idEmisor': EMISOR_MAPPING[emision_name],
                'montoExigible': monto,
                'montoACobrar': monto,
                'emisionUsada': emision_name,
                'points': points,
                'Parcial': parcial
            })
    
    return pd.DataFrame(output_data), points_map

def main():
    # Example usage - replace with your actual file paths
    excel_files = [
        'ListaCobroDetalle2022.csv',
        'ListaCobroDetalle2023.csv', 
        'ListaCobroDetalle2024.csv',
        'ListaCobroDetalle2025.csv'
    ]
    
    # Read and concatenate Excel files
    print("Reading and concatenating Excel files...")
    df = read_and_concatenate_excels(excel_files)
    print(f"Total records: {len(df)}")
    
    # Calculate points for all credits first
    current_date = datetime.now()
    points_map = calculate_all_credit_points(df, current_date)
    print("Points calculated for all credits.")
    
    # Process credits
    output_df, _ = process_credits(df, points_map)
    print("Credits processed.")
    
    # Save output
    output_filename = 'processed_credits.xlsx'
    output_df.to_excel(output_filename, index=False)    
    
    return output_df, points_map

if _name_ == "_main_":
    main()