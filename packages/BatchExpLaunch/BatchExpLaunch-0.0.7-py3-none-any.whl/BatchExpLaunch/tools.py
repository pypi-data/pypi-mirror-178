import os
import json
import logging
def configure_logging(logging):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
def iterate_settings(all_settings,cur_setting={},path=".",ind=0,settingName="setting.json"):
    setting_name_list=list(all_settings.keys())
    # print(setting_name_list)
    if ind==len(setting_name_list):
        cur_setting["log_dir"]=path
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path+"/"+settingName, 'w+') as f:
                json.dump(cur_setting, f)            
        return
    cur_setting=dict(cur_setting)
    cur_setting_name=setting_name_list[ind]
    # print(cur_setting)
    for i in all_settings[cur_setting_name]:
        cur_path=os.path.join(path, cur_setting_name+"_"+str(i))
        cur_setting[cur_setting_name]=i
        iterate_settings( all_settings,cur_setting,cur_path,ind+1,settingName=settingName)