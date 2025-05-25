import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt
import seaborn as sns

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

# Morning collection methods
MORNING_EMISORS = ['5923', '00496']  # BBVA and Banamex morning collection IDs

# Collection opening hours (24-hour format)
COLLECTION_HOURS = {
    'bbva_cobrar_mismo': {'hour': 9, 'minute': 0},
    'banamex_interbancario': {'hour': 8, 'minute': 30},
    'santander_cobrar_mismo': {'hour': 9, 'minute': 30},
    'banamex_cobrar_mismo': {'hour': 8, 'minute': 30},
    'bbva_interbancario': {'hour': 9, 'minute': 0}
}

# Emisor ID mapping
EMISOR_MAPPING = {
    'banamex_interbancario': '00496',
    'bbva_cobrar_mismo': '5923',
    'santander_cobrar_mismo': '00623',
    'banamex_cobrar_mismo': '00496',  # Same as banamex_interbancario
    'bbva_interbancario': '4750'
}

def create_visualizations(df, output_df, points_map):
    """Create and save visualizations"""
    # Set the style for all plots
    plt.style.use('ggplot')  # Using ggplot style instead of seaborn
    
    # 1. Monthly Collection Trends
    plt.figure(figsize=(12, 6))
    monthly_data = df.groupby(df['fechaCobroBanco'].dt.to_period('M')).agg({
        'montoCobrado': 'sum',
        'montoCobrar': 'sum'
    }).reset_index()
    monthly_data['fechaCobroBanco'] = monthly_data['fechaCobroBanco'].astype(str)
    
    plt.plot(monthly_data['fechaCobroBanco'], monthly_data['montoCobrado'], marker='o', label='Collected')
    plt.plot(monthly_data['fechaCobroBanco'], monthly_data['montoCobrar'], marker='o', label='Expected')
    plt.title('Monthly Collection Trends')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('monthly_trends.png')
    plt.close()

    # 2. Collection Efficiency by Bank
    plt.figure(figsize=(10, 6))
    bank_efficiency = df.groupby('idBanco').agg({
        'montoCobrado': 'sum',
        'montoCobrar': 'sum'
    })
    bank_efficiency['efficiency'] = (bank_efficiency['montoCobrado'] / bank_efficiency['montoCobrar']) * 100
    bank_efficiency.index = bank_efficiency.index.map(lambda x: BANK_MAPPING.get(x, str(x)))
    
    sns.barplot(x=bank_efficiency.index, y=bank_efficiency['efficiency'])
    plt.title('Collection Efficiency by Bank')
    plt.xlabel('Bank')
    plt.ylabel('Efficiency (%)')
    plt.tight_layout()
    plt.savefig('bank_efficiency.png')
    plt.close()

    # 3. Points Distribution
    plt.figure(figsize=(10, 6))
    points_series = pd.Series(points_map)
    sns.histplot(points_series, bins=20)
    plt.title('Distribution of Credit Points')
    plt.xlabel('Points')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('points_distribution.png')
    plt.close()

    # 4. Monthly Collection Success Rate
    plt.figure(figsize=(12, 6))
    monthly_success = df.groupby(df['fechaCobroBanco'].dt.to_period('M')).agg({
        'idCredito': 'count',
        'montoCobrado': lambda x: (x > 0).sum()
    })
    monthly_success['success_rate'] = (monthly_success['montoCobrado'] / monthly_success['idCredito']) * 100
    monthly_success.index = monthly_success.index.astype(str)
    
    plt.plot(monthly_success.index, monthly_success['success_rate'], marker='o')
    plt.title('Monthly Collection Success Rate')
    plt.xlabel('Month')
    plt.ylabel('Success Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('success_rate.png')
    plt.close()

def fetch_data_from_api():
    """Fetch data from Django API and convert to DataFrame"""
    try:
        response = requests.get('http://localhost:8000/api/collection-stats/')
        if response.status_code != 200:
            raise ValueError(f"API request failed with status code {response.status_code}")
        
        data = response.json()
        
        # Convert the API data into a format similar to our original CSV structure
        all_records = []
        for year, year_data in data.items():
            for month_data in year_data:
                # Skip records with None month
                if month_data['month'] is None:
                    continue
                    
                record = {
                    'idListaCobro': int(year),
                    'idCredito': month_data['month'],
                    'consecutivoCobro': f"{year}-{month_data['month']}",
                    'idBanco': 12,  # Default to BBVA
                    'montoExigible': float(month_data['total_por_cobrar']),
                    'montoCobrar': float(month_data['total_por_cobrar']),
                    'montoCobrado': float(month_data['total_cobrado']),
                    'fechaCobroBanco': f"{year}-{month_data['month']:02d}-01",
                    'idRespuestaBanco': None
                }
                all_records.append(record)
        
        df = pd.DataFrame(all_records)
        df['fechaCobroBanco'] = pd.to_datetime(df['fechaCobroBanco'])
        return df.sort_values(['idCredito', 'fechaCobroBanco'])
    
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        raise

def get_emision_elegida(id_banco, points, monto_exigible, monto_cobrado, last_emisor_id=None):
    """Determine which emission to use based on bank ID and conditions"""
    # If last payment was with a morning collection method, force morning collection
    if last_emisor_id in MORNING_EMISORS:
        if id_banco == 12:
            return 'bbva_cobrar_mismo', BBVA_COBRAR_MISMO
        elif id_banco == 2:
            return 'banamex_cobrar_mismo', BANAMEX_COBRAR_MISMO
    
    if id_banco == 12:
        return 'bbva_cobrar_mismo', BBVA_COBRAR_MISMO
    
    elif points < 0 or (monto_exigible != monto_cobrado and id_banco != 12):
        return 'bbva_interbancario', BBVA_INTERBANCARIO
    
    elif id_banco == 14:
        return 'santander_cobrar_mismo', SANTANDER_COBRAR_MISMO
    elif id_banco == 2:
        return 'banamex_cobrar_mismo', BANAMEX_COBRAR_MISMO
    else:
        return 'banamex_interbancario', BANAMEX_INTERBANCARIO

def process_credits_optimized(df, current_date=None):
    """Process all credits in a single pass, calculating points and generating output"""
    if current_date is None:
        current_date = datetime.now()
    
    output_data = []
    points_map = {}

    for id_credito, credit_group in df.groupby('idCredito'):
        points = 0
        monto = float(credit_group['montoExigible'].sum())
        id_banco = credit_group.iloc[0]['idBanco']
        last_emisor_id = None
        
        # Get the last successful payment's emisor ID
        last_payment = credit_group[credit_group['montoCobrado'] > 0].iloc[-1] if len(credit_group[credit_group['montoCobrado'] > 0]) > 0 else None
        if last_payment is not None and not pd.isna(last_payment['idRespuestaBanco']):
            last_emisor_id = last_payment['idRespuestaBanco']
        
        for idx, row in credit_group.iterrows():
            record_date = row['fechaCobroBanco']
            if pd.isna(record_date):
                months_diff = float('inf')
            else:
                if not isinstance(record_date, datetime):
                    record_date = pd.to_datetime(record_date)
                months_diff = (current_date - record_date).days / 27
            
            multiplier = 6 if months_diff <= 1 else (
                5 if months_diff <= 2 else (
                4 if months_diff <= 3 else (
                3 if months_diff <= 4 else (
                2 if months_diff <= 5 else 1))))
            
            if row['montoCobrar'] != row['montoCobrado']:
                points -= 1 * multiplier
            
            selected_date = 'no pago'
            if pd.notna(row['montoExigible']) and pd.notna(row['montoCobrado']):
                if row['montoCobrar'] == row['montoCobrado']:
                    points += 1 * multiplier
                    fecha_cobro = row['fechaCobroBanco']
                    if pd.notna(fecha_cobro):
                        if not isinstance(fecha_cobro, datetime):
                            fecha_cobro = pd.to_datetime(fecha_cobro)
                        
                        day = fecha_cobro.day
                        if day <= 8:
                            fortnight_date = fecha_cobro.replace(day=1)
                        elif day >= 23:
                            if fecha_cobro.month == 12:
                                fortnight_date = fecha_cobro.replace(year=fecha_cobro.year + 1, month=1, day=1)
                            else:
                                fortnight_date = fecha_cobro.replace(month=fecha_cobro.month + 1, day=1)
                        else:
                            fortnight_date = fecha_cobro.replace(day=15)
                        
                        while fortnight_date.weekday() >= 5:
                            fortnight_date = fortnight_date - timedelta(days=1)
                        
                        selected_date = fortnight_date
                
                if row['montoExigible'] == row['montoCobrado']:
                    points += 1 * multiplier

        points_map[id_credito] = points
        
        last_row = credit_group.iloc[-1]
        monto_tot = float(last_row['montoExigible'])
        monto_cobrado = float(last_row['montoCobrado'])
        
        emision_name, emision_fee = get_emision_elegida(id_banco, points, monto_tot, monto_cobrado, last_emisor_id)
        
        cobrar = monto_tot > emision_fee
        parcial = points <= 0
        
        if cobrar and monto > 0 and selected_date != 'no pago':
            # Adjust the collection time based on the emission method
            collection_time = COLLECTION_HOURS[emision_name]
            selected_date = selected_date.replace(
                hour=collection_time['hour'],
                minute=collection_time['minute']
            )
            
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
    print("Fetching data from Django API...")
    df = fetch_data_from_api()
    print(f"Total records: {len(df)}")
    
    print("Processing credits...")
    output_df, points_map = process_credits_optimized(df)
    print(f"Credits processed. Output records: {len(output_df)}")
    
    print("Generating visualizations...")
    create_visualizations(df, output_df, points_map)
    print("Visualizations saved as PNG files")
    
    output_filename = 'processed_credits.xlsx'
    output_df.to_excel(output_filename, index=False)
    print(f"Results saved to {output_filename}")
    
    return output_df, points_map

if __name__ == "__main__":
    main()