import os
import pandas as pd
import json

from pandas.core.frame import DataFrame


class JsonGenerator:

    def __init__(self):
        self.__metadata = {}
        self.__folder_to_read = f'{os.path.dirname(os.path.realpath(__file__))}\\files'
        self.__folder_to_write = f'{os.path.dirname(os.path.realpath(__file__))}\\jsons'
        self.__run()

    def __read_each_file(self):
        for file in os.listdir(self.__folder_to_read) or []:
            self.__read_file(f'{self.__folder_to_read}\\{file}')

    def __read_file(self, file_path: str):
        df_sheet_multi = pd.read_excel(file_path, sheet_name=['paywalls', 'rg_service_ids', 'applications'])
        paywalls = df_sheet_multi['paywalls']
        rg_service_ids = df_sheet_multi['rg_service_ids']
        applications = df_sheet_multi['applications']
        self.__process_data(paywalls, rg_service_ids, applications)

    def __process_data(self, paywalls: DataFrame, rg_service_ids: DataFrame, applications: DataFrame):
        for i in paywalls.index:
            service_id = int(paywalls['Id'][i])
            self.__metadata[service_id] = {
                'service_name': paywalls['service_name'][i],
                'official_brand_name': paywalls['official_brand_name'][i],
                'rg_service_ids': self.__get_rg_service_ids(service_id, rg_service_ids),
                # ToDo -  check arguments to get paywalls
                'paywalls': self.__get_paywalls(service_id, paywalls),
                'parent_organization': paywalls['parent_organization'][i],
                # ToDo -  check arguments to get content_type
                'content_type': self.__get_content_type(service_id, paywalls),
                'applications': self.__get_applications(service_id, applications)
            }

            # ToDo -  delete
            break

        self.__write_json_file()

    def __get_rg_service_ids(self, service_id, rg_service_ids):
        return {}

    def __get_paywalls(self, service_id, paywalls):
        return {}

    def __get_content_type(self, service_id, paywalls):
        return {}

    def __get_applications(self, service_id, applications):
        return {}

    def __write_json_file(self):
        metadata = json.dumps(self.__metadata, indent=4)
        print(metadata)

        with open(f"{self.__folder_to_write}\\metadata.json", "w") as outfile:
            outfile.write(metadata)

    def __run(self):
        self.__read_each_file()
