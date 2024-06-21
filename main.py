import pandas as pd
from sqlalchemy import create_engine

file_path = './dataset.xlsx'
xl = pd.ExcelFile(file_path)

workers_df = xl.parse('workers')
multicompanies_df = xl.parse('multicompanies')
evaluations_df = xl.parse('evaluations')

companies = []

posts = []

def export_dataframe_to_excel(dataframes, file_name):
    output_file = f'./{file_name}.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        if isinstance(dataframes, pd.DataFrame):
            dataframes.to_excel(writer, sheet_name=file_name, index=False)
        else:
            for idx, dataframe in enumerate(dataframes):
                sheet_name = dataframe.name if hasattr(dataframe, 'name') and dataframe.name else f'Sheet{idx+1}'
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Archivo exportado a {output_file}")

def get_posts():
    seen_posts = set()
    posts = []

    for index, worker_row in workers_df.iterrows():
        post_entry = {
            'id': index,
            'company_id': worker_row['company_id'],
            'name': worker_row['post_name']
        }
        
        post_identifier = (worker_row['company_id'], worker_row['post_name'])
        
        if post_identifier not in seen_posts:
            seen_posts.add(post_identifier)
            posts.append(post_entry)

    posts_df = pd.DataFrame(posts)

    return posts_df

def get_companies():
    for _, worker_row in workers_df.iterrows():
        company_entry = {
            'id': worker_row['company_id'],
            'name': worker_row['company_name'],
            'worker_manager_id': '',
            'company_manager_id': '',
            'company_manager_name': ''
        }
        existing_company = next((company for company in companies if company['id'] == company_entry['id'] and company['name'] == company_entry['name']), None)
        
        if existing_company:
            existing_company['id'] = company_entry['id']
            existing_company['name'] = company_entry['name']
        else:
            companies.append(company_entry)
    
    for _, multicompanies_row in multicompanies_df.iterrows():
        main_id = multicompanies_row['main_company_id']
        sub_id = multicompanies_row['sub_company_id']
        main_name = multicompanies_row['main_company_name']
        sub_name = multicompanies_row['sub_company_name']
        
        main_company = next((company for company in companies if company['id'] == main_id), None)
        
        if not main_company:
            main_company = {
                'id': main_id,
                'name': main_name,
                'worker_manager_id': '',
                'company_manager_id': '',
                'company_manager_name': ''
            }
            companies.append(main_company)
        
        sub_company_entry = {
            'id': sub_id,
            'name': sub_name,
            'worker_manager_id': '',
            'company_manager_id': main_id,
            'company_manager_name': main_name
        }
        existing_subcompany = next((company for company in companies if company['id'] == sub_id and company['name'] == sub_name), None)
        
        if existing_subcompany:
            existing_subcompany['id'] = sub_id
            existing_subcompany['name'] = sub_name
            existing_subcompany['company_manager_id'] = main_id
            existing_subcompany['company_manager_name'] = main_name
        else:
            companies.append(sub_company_entry)
    
    companies_df = pd.DataFrame(companies)
    companies_df = companies_df.sort_values(by='id', ascending=True).reset_index(drop=True)
    
    return companies_df

def get_areas():
    areas_df = workers_df.copy()
    areas_df['area_name'] = areas_df['area_name'].str.upper()
    areas_df = areas_df[['area_id', 'area_name', 'company_id']].drop_duplicates(['company_id', 'area_name'])
    
    return areas_df

def get_workers():
    posts_df = get_posts()
    
    workers_transformed = workers_df.copy()
    
    workers_transformed['id'] = range(1, len(workers_transformed) + 1)
    
    workers_transformed = workers_transformed.rename(columns={'user_name': 'name'})
    
    workers_transformed['status_id'] = 1
    workers_transformed['evaluation_id'] = 0
    
    workers_transformed = workers_transformed.rename(columns={
        'user_id': 'user_id',
        'area_id': 'area_id',
        'post_id': 'post_id',
        'company_id': 'company_id'
    })
    
    workers_transformed['post_id'] = workers_transformed.apply(
        lambda row: posts_df[posts_df['name'] == row['post_name']]['id'].values[0],
        axis=1
    )
    
    workers_transformed = workers_transformed[['id', 'name', 'user_id', 'area_id', 'post_id', 'status_id', 'company_id', 'evaluation_id']]
    
    return workers_transformed

def get_users():
    users_data = {
        'id': [1, 2, 3],
        'email': ['admin@example.com', 'chief@example.com', 'manager@example.com'],
        'password': ['admin_password', 'chief_password', 'manager_password'],
        'role': ['ADMINISTRATOR', 'AREA_CHIEF', 'MANAGER']
    }
    users_df = pd.DataFrame(users_data)
    
    return users_df

def upload_to_database(dataframe):
    engine = create_engine('sqlite:///hackadisc.db')

    dataframe.to_sql(dataframe.name, con=engine, if_exists='replace', index=False)

    print("DataFrame cargado exitosamente en la base de datos")

# export_dataframe_to_excel(get_posts(), 'posts')
# export_dataframe_to_excel(get_companies(), 'companies')
# export_dataframe_to_excel(get_areas(), 'areas')
# export_dataframe_to_excel(get_workers(), 'workers')
export_dataframe_to_excel(get_users(), 'users')