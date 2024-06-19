import pandas as pd

file_path = './dataset.xlsx'
xl = pd.ExcelFile(file_path)

multicompanies_df = xl.parse('multicompanies')
workers_df = xl.parse('workers')

companies = []
subCompanies = []

for index, company_row in multicompanies_df.iterrows():
    company_entry = {
        'company_id': company_row['main_company_id'],
        'company_name': company_row['main_company_name']
    }
    if company_entry not in companies:
        companies.append(company_entry)

for index, worker_row in workers_df.iterrows():
    company_id = worker_row['company_id']
    company_name = worker_row['company_name']
    
    main_match = multicompanies_df[multicompanies_df['main_company_id'] == company_id]
    sub_match = multicompanies_df[multicompanies_df['sub_company_id'] == company_id]
    
    if not main_match.empty:
        continue
    elif not sub_match.empty:
        for sub_index, sub_row in sub_match.iterrows():
            sub_company_entry = {
                'company_id': sub_row['main_company_id'],
                'sub_company_id': company_id,
                'company_name': sub_row['main_company_name'],
                'sub_company_name': sub_row['sub_company_name']
            }
            if sub_company_entry not in subCompanies:
                subCompanies.append(sub_company_entry)
    else:
        company_entry = {
            'company_id': company_id,
            'company_name': company_name
        }
        if company_entry not in companies:
            companies.append(company_entry)

print("Companies without match in 'multicompanies':")
for comp in companies:
    print(comp)

print("\nSub Companies with matches in 'sub_company_id':")
for sub_comp in subCompanies:
    print(sub_comp)

companies_df = pd.DataFrame(companies)
subCompanies_df = pd.DataFrame(subCompanies)

output_file = './companies_and_subcompanies.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    companies_df.to_excel(writer, sheet_name='Companies', index=False)
    subCompanies_df.to_excel(writer, sheet_name='SubCompanies', index=False)

print(f"Archivo exportado a {output_file}")


# contar cantidad de evaluaciones por cada usuario
# iterar puestos de trabajo por cada empresa