import os
import shutil
import yaml
from pathlib import Path

def get_last_exp_dir(proj_path, name='exp'):
    # имя каталогу с экспериментами дается так # Method 1
    """
    for n in range(2, 9999):
        p = f'{path}{sep}{n}{suffix}'  # increment path
        if not os.path.exists(p):  #
            break
    path = Path(p)
    """

    last_exp_dir = None
    if os.path.isdir(proj_path):
        last_exp_dir = proj_path + os.sep + name
        if os.path.isdir(last_exp_dir):
            # был как минимум один эксперимент
            exp_dir_list = sorted([
                exp_dir for exp_dir in os.listdir(proj_path) if
                (os.path.isdir(proj_path + os.sep + exp_dir)) &
                (exp_dir.find(name) == 0)
            ])
            exp_dir_list = exp_dir_list[1:]  # удалили каталог '/exp/'
            if len(exp_dir_list) > 1:
                exp_dir_num = max(
                    [int(exp_dir[len(name):]) for exp_dir in exp_dir_list])
                # print('exp_dir_num', exp_dir_num)
                last_exp_dir = last_exp_dir + str(exp_dir_num)


    return last_exp_dir


def get_model_last_exp_dir(model, sub='train'):
    exp_dict = model.exp_dict[sub]
    # print(exp_dict)
    try:
        # в приоритете текущая история модели
        last_best_weights_path = exp_dict['project'] + os.sep + exp_dict['name']
    except:
        # last_best_weights_path = get_model_last_exp_dir(model, sub)
        proj_path = model.model_dir + os.sep + exp_dict.get('def_dir')
        last_best_weights_path = get_last_exp_dir(proj_path=proj_path, name='exp')
    return last_best_weights_path


def save_data_yaml(yaml_dict, dest_yaml_path):
    yaml_content = f'''
        train: {yaml_dict['train']}
        val: {yaml_dict['val']}
        test: {yaml_dict['test']}

        # number of classes
        nc: {yaml_dict['nc']}

        # class names
        names: {yaml_dict['names']}
        '''
    with open(dest_yaml_path, 'w') as f:
        f.write(yaml_content)
    return dest_yaml_path


def get_data_dict(yaml_file_path):
    with open(yaml_file_path, 'r') as f:
        return yaml.safe_load(f)


class TerraYoloV5:

    def __init__(self,
                 # data_path: str, #путь к файлу описания датасета.yaml
                 work_dir='.',
                 model_ref='https://github.com/ultralytics/yolov5',
                 log_f_name='model.log',
                 reload=False,
                 # data_dict = dict(),
                 ):

        if os.path.exists(work_dir) == False:
            os.makedirs(work_dir, exist_ok=True)
        self.work_dir = os.path.abspath(work_dir + os.sep)

        self.log_f_name = work_dir + '/' + log_f_name
        self.model_ref = model_ref
        # self.model_name = model_name
        self.reload = reload
        self.model_dir = self.work_dir + os.sep + 'yolov5/'
        self.download()
        self.model_dict = self.get_model_dict()

        # self.data = data_path #dataset.base_data_dir+dataset.data_yaml
        '''        
        with open(self.data, 'r') as f:
            self.data_dict = yaml.safe_load(f)
        print(self.data)
        print(self.data_dict)
        '''
        self.exp_dict = dict()
        for sub in ['train', 'val', 'test']:
            self.exp_dict[sub] = dict()

        self.exp_dict['train']['def_dir'] = '/runs/train/'
        self.exp_dict['val']['def_dir'] = '/runs/val/'
        self.exp_dict['test']['def_dir'] = '/runs/detect/'

        self.exp_dict['train']['script'] = 'train.py'
        self.exp_dict['val']['script'] = 'val.py'
        self.exp_dict['test']['script'] = 'detect.py'
        self.exp_dict['detect'] = self.exp_dict['test']

    def os_com(self, command, log_f=True):
        if log_f == True:
            os.system(command + '>>' + self.log_f_name)
        #else:
            #!{command}
        return

    def download(self):
        # если reload = True полностью удаляем каталог с моделью и загружаем снова
        # если reload = False перезагружаем только в случае отсутствия каталога с моделью

        if os.path.isdir(self.model_dir) == True:
            if self.reload == True:
                shutil.rmtree(self.model_dir)
            else:
                return

        wd = os.getcwd()
        os.chdir(self.work_dir)

        self.os_com(f'git clone {self.model_ref}')
        os.chdir(self.model_dir)
        self.os_com('pip install -r requirements.txt')
        os.chdir(wd)
        return

    def get_model_dict(self):
        # в первом приближении пропустил модели .py
        model_path = Path(self.model_dir + '/models/')
        model_full_path = sorted(list(model_path.rglob('*.yaml')))
        model_names = [str(path)[len(str(model_path)) + 1:].split('.')[0]
                       for path in model_full_path]
        # return model_short_path
        return dict(zip(model_names, model_full_path))

    def get_annotation(self, model_name):
        # пока yaml, словарь если что сделаем
        with open(self.model_dict[model_name], 'r') as f:
            print(f.read())

    def do_experiment(self, command, param_dict):
        # чуть позже написал доп функцию
        project_dir = param_dict['project']
        if os.path.isdir(project_dir):
            exp_dir_set = set(os.listdir(project_dir))
        else:
            exp_dir_set = set()

        self.os_com(command, log_f=False)

        if os.path.isdir(project_dir) == True:
            # теоретически должен быть один новый каталог
            # или если что-то пойдет не так - не будет ни одного
            last_train_dir = sorted(list(set(os.listdir(project_dir)) -
                                         exp_dir_set))[-1]
        else:
            last_train_dir = None

        return last_train_dir

    def run(self, param_dict, exp_type='val'):

        arg_str = ''.join(
            [' --' + str(k) + ' ' + str(v) for k, v in param_dict.items()]).strip()
        exp_dict = self.exp_dict[exp_type]
        exp_dict['history'] = exp_dict.get('history', []) + [param_dict]

        command = 'python ' + self.model_dir + exp_dict['script'] + ' ' + arg_str
        print('command', command)
        # print(exp_dict)
        exp_dict['project'] = param_dict.get('project',
                                             self.model_dir + exp_dict['def_dir'])
        exp_dict['name'] = self.do_experiment(command, exp_dict)

        return
