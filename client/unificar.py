import pandas as pd

# File paths (update with your actual file names)
csv1 = 'ListaCobroDetalle2022.csv'
csv2 = 'ListaCobroDetalle2023.csv'
csv3 = 'ListaCobroDetalle2024.csv'
csv4 = 'ListaCobroDetalle2025.csv'

# Read each CSV file into a DataFrame
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)
df3 = pd.read_csv(csv3)
df4 = pd.read_csv(csv4)

# Concatenate all DataFrames
combined_df = pd.concat([df1], ignore_index=True)

# 3. Merge combined_df with bank_df on 'idBanco'
catbanco_df = pd.read_csv('CatBanco.csv')

# 2. Build the mapping dictionary
banco_map = dict(zip(catbanco_df['IdBanco'], catbanco_df['Nombre']))
print(banco_map)

respuesta_map=dict(zip())

# 3. Replace values in combined_df using a loop
for i in range(len(combined_df)):
    banco_id = combined_df.at[i, 'idBanco']
    if banco_id in banco_map.keys():
        combined_df.at[i, 'idBanco'] = banco_map[banco_id]

# 4. Save the updated DataFrame to a new Excel file
combined_df.to_excel('output.xlsx', index=False)
print("CSV files combined and saved as Excel successfully!")