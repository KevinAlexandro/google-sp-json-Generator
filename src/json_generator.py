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
                'paywalls': self.__get_paywalls(service_id, paywalls),
                'parent_organization': paywalls['parent_organization'][i],
                'content_type': self.__get_content_type(service_id, paywalls),
                'applications': self.__get_applications(service_id, applications)
            }

        self.__write_json_file()

    @staticmethod
    def __get_rg_service_ids(service_id: int, rg_service_ids: DataFrame):
        service_ids = []
        for i in rg_service_ids.index:
            if service_id == rg_service_ids['Id'][i]:
                if not pd.isna(rg_service_ids['rg_service_ids'][i]):
                    service_ids.append(rg_service_ids['rg_service_ids'][i])
                else:
                    service_ids.append('')

        return service_ids

    @staticmethod
    def __get_paywalls(service_id: int, paywalls_data: DataFrame):
        paywalls = {}
        for i in paywalls_data.index:

            if service_id == paywalls_data['Id'][i]:

                paywalls['no_login_required'] = paywalls_data['no_login_required'][i]
                paywalls['free'] = paywalls_data['free'][i]
                paywalls['subscription'] = paywalls_data['subscription'][i]
                paywalls['rental'] = paywalls_data['rental'][i]
                paywalls['purchase'] = paywalls_data['purchase'][i]
                paywalls['tve'] = paywalls_data['tve'][i]

        print(type(paywalls['subscription']))
        return paywalls

    @staticmethod
    def __get_content_type(service_id: int, paywalls_data: DataFrame):
        content_type = {}
        for i in paywalls_data.index:

            if service_id == paywalls_data['Id'][i]:

                content_type['vod'] = paywalls_data['vod'][i]
                content_type['live_tv'] = paywalls_data['live_tv'][i]

        return content_type

    @staticmethod
    def __get_applications(service_id, applications):
        apps = {}

        for i in applications.index:
            if service_id == applications['Id'][i]:
                apps[applications['OS'][i]] = {
                    applications['Region'][i]:
                        {
                            'id': applications['id'][i],
                            'download_url': applications['download_url'][i],
                            'download_deeplink': applications['download_deeplink'][i]
                        }
                }

        return apps

    def __write_json_file(self):
        metadata = json.dumps(self.__metadata, indent=4)

        with open(f"{self.__folder_to_write}\\metadata.json", "w") as outfile:
            outfile.write(metadata)

    def __run(self):
        self.__read_each_file()
