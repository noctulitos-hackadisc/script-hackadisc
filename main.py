import pandas as pd
from sqlalchemy import create_engine

file_path = './dataset.xlsx'
xl = pd.ExcelFile(file_path)

multicompanies_df = xl.parse('multicompanies')
workers_df = xl.parse('workers')

companies = []
subCompanies = []

posts = []

def export_dataframe_to_excel(dataframes, file_name):
    output_file = f'./{file_name}.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for dataframe in dataframes:
            dataframe.to_excel(writer, sheet_name=dataframe.name, index=False)

    print(f"Archivo exportado a {output_file}")

def get_companies():
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

    companies_df = pd.DataFrame(companies)
    subCompanies_df = pd.DataFrame(subCompanies)
    
    companies_df.name = 'Companies'
    subCompanies_df.name = 'SubCompanies'
    
    return companies_df, subCompanies_df

def upload_to_database(dataframe):
    engine = create_engine('sqlite:///hackadisc.db')

    dataframe.to_sql(dataframe.name, con=engine, if_exists='replace', index=False)

    print("DataFrame cargado exitosamente en la base de datos")

# export_dataframe_to_pdf(get_companies(), 'companies_and_subcompanies')

# upload_to_database(get_companies()[0])
# upload_to_database(get_companies()[1])

def get_posts():
    seen_posts = set()  # Crear un conjunto para rastrear las combinaciones únicas de company_id y post_name
    posts = []  # Inicializar la lista de posts

    for index, worker_row in workers_df.iterrows():
        post_entry = {
            'post_id': index,
            'company_id': worker_row['company_id'],
            'post_name': worker_row['post_name']
        }
        
        # Crear una tupla (company_id, post_name) para verificar unicidad
        post_identifier = (worker_row['company_id'], worker_row['post_name'])
        
        if post_identifier not in seen_posts:
            seen_posts.add(post_identifier)  # Agregar la tupla al conjunto
            posts.append(post_entry)  # Agregar la entrada a la lista de posts

    posts_df = pd.DataFrame(posts)
    posts_df.name = 'Posts'
    
    print(posts_df)

    return posts_df



get_posts()
export_dataframe_to_excel(get_posts(), 'posts')
# contar cantidad de evaluaciones por cada usuario
# iterar puestos de trabajo por cada empresa