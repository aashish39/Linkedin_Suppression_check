import pandas as pd
import os
from tqdm import tqdm

df_likedin_links = pd.read_csv("linkedin_link.csv")

lst_of_files_in_supp_folder = [f"Suppression/{i}"for i in os.listdir("Suppression")]

def get_list_of_links(data_table_path):
    lst_domains = []
    data_table = pd.read_csv(data_table_path)
    for i in tqdm(data_table.columns):
        lst_domains.extend(data_table[i].to_list())    
    return lst_domains


if __name__ =="__main__":
    print("Process Started Please Wait.................")
    if os.path.isfile("output.csv"):
        os.remove("output.csv")
    all_files_link = []
    for i in lst_of_files_in_supp_folder:
        all_files_link.extend(get_list_of_links(i))
    all_files_link_set = set(all_files_link)
    set_a = set(df_likedin_links[df_likedin_links.columns[0]].to_list())
    set_b = set_a.intersection(all_files_link_set)
    output = pd.DataFrame(set_b,columns=["list"])
    output.to_csv("output.csv")
    print("Completed Successfully Thank for your Patients,See you next Time !!!")
    
