import sys
import time

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
import os
from torch.utils import tensorboard
from sklearn.metrics import  accuracy_score,roc_auc_score
import copy
import json
import random
from torch.cuda.amp import autocast,GradScaler
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import torch.distributed as dist
import argparse
import torch.multiprocessing.spawn
class Metrics(object):
    def __init__(self):
        self.acc = self.accuracy
        self.roc_auc = roc_auc_score

    def accuracy(self,y_preds,y_true):
        y_preds = np.argmax(y_preds,axis=-1)
        y_true = y_true
        return accuracy_score(y_pred=y_preds,y_true=y_true)


class Config(object):
    def __init__(self):
        #general_dict | train_dict | checkpoint_dict | model_dict

        self.general_dict = {}
        self.train_dict = {}
        self.checkpoint_dict = {}
        self.model_dict = {}
        self.create_config()
    def general_config(self):
        self.general_dict.update(
            {
            'seed':0,
            'gpu_nums' : 1,
            'use_gpu': True,
            'log_dir' : 'monitor',
            'experiment_name' : "auto",
            'output_train_log':True,
            'output_visual_graphs':True,
            'test_experiment':False
            }
        )

    def train_config(self):

        self.train_dict.update({
            'accumulate_num': -1,
            'use_fp16': False,
        }
        )

    def checkpoint_config(self):

        self.checkpoint_dict.update( {
            'use_checkpoint':False,
            'save_step_interval':False,
            'monitor_by_train_loss':False,
            'monitor_by_val_loss':False,
            'monitor_by_train_metric':False,
            'monitor_by_val_metric':True,
            'use_early_stopping':False,
            'monitor_max':True,
            'save_top_k':-1,
            'save_last':True
        })

    def model_config(self):
        model_dict = {
            'use_gradient_checkpoint': False,
        }
        return model_dict

    def create_config(self):
        self.general_config()
        self.train_config()
        self.model_config()
        self.checkpoint_config()
        print('参数创建完毕')


    def to_json(self,path):
        dicts = ['一般配置',self.general_dict,'训练参数配置',self.train_dict,'模型参数配置',self.model_dict,'模型检查点配置',self.checkpoint_dict]
        with open(os.path.join(path,'total_args.json'), 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(dicts,ensure_ascii=False,indent=2))


class Trainer(object):
    def __init__(self,
                 config,
                 **kwargs
                 ):
        self.metric = None
        self.config = config


    def log(self,tag, scalar_value, global_step=None):
        self.writer.add_scalar(tag,scalar_value,global_step)

    def fit(self,model,criterion,train_dataset: Dataset,val_dataset: Dataset=None,metric=None,
            optimizer=None,schedule=None,feature_dict=False,train_batch_size=16,val_batch_size=16,
            num_epochs=None,num_steps=None,train_num_workers=0,val_num_workers=0,log_step_interval=-1,resume=""):
        arg_dict = {
            'local_rank':None,
            'model':model,
            'criterion':criterion,'train_dataset':train_dataset,'val_dataset':val_dataset,'metric':metric,
            'optimizer':optimizer,'schedule':schedule,'feature_dict':feature_dict,'train_batch_size':train_batch_size,
            'val_batch_size':val_batch_size,'num_epochs':num_epochs,'num_steps':num_steps,'train_num_workers':train_num_workers,
            'val_num_workers':val_num_workers,'log_step_interval':log_step_interval,'resume':resume
        }

        if self.config.general_dict['gpu_nums']>1:
            torch.multiprocessing.spawn(self.fit_,args=(
            model,criterion,train_dataset,val_dataset,metric,
            optimizer,schedule,feature_dict,train_batch_size,val_batch_size,
            num_epochs,num_steps,train_num_workers,val_num_workers,log_step_interval,resume),
            nprocs=self.config.general_dict['gpu_nums'])
        else:
            self.fit_(**arg_dict)

    def fit_(self,local_rank, model,criterion,train_dataset: Dataset,val_dataset: Dataset=None,metric=None,
            optimizer=None,schedule=None,feature_dict=False,train_batch_size=16,val_batch_size=16,
            num_epochs=None,num_steps=None,train_num_workers=0,val_num_workers=0,log_step_interval=-1,resume=""
            ):
        assert num_epochs is not  None or num_steps is not None
        assert optimizer is not None and train_dataset is not None
        self.local_rank = local_rank if self.config.general_dict['gpu_nums']>1 else -1
        print(self.local_rank)
        if self.config.general_dict['gpu_nums']>1:
            self.distributed_learning_init(self.local_rank)
            if self.local_rank == 0:
                print('检测到你正在进行多卡学习,初始化完毕。')


        self.train_num_workers = train_num_workers
        self.val_num_workers = val_num_workers
        #init
        if self.config.general_dict['test_experiment']:
            pass
        else:
            self.fit_init()

        self.train_batch_size = train_batch_size
        self.val_batch_size = val_batch_size
        self.train_loader,self.val_loader = self.prepare_loader(train_dataset,val_dataset)
        self.log_step_interval = len(self.train_loader) if log_step_interval == -1 else log_step_interval
        self.feature_dict = feature_dict
        self.num_epochs = num_epochs
        self.num_steps = num_steps
        self.actual_accumulate_num = 0 if self.config.train_dict['accumulate_num'] > 0 else -1
        self.actual_epoch = 0
        self.actual_step = len(self.train_loader) * (self.actual_epoch) + 1
        self.start_epoch = 0
        self.start_step = 0
        self.last_train_loss = np.inf
        self.last_val_loss = np.inf
        self.resume = resume
        # if self.config.general_dict['output_visual_graphs']:
        #     self.train_loss_history = []
        #     self.val_loss_history = []
        #     self.train_metric_history = []
        #     self.val_metric_history = []

        if self.config.checkpoint_dict['monitor_max']:
            self.last_train_metric = 0.
            self.last_val_metric = 0.
        else:
            self.last_train_metric = np.inf
            self.last_val_metric = np.inf

        self.metric = metric

        self.model = model
        if self.resume != "":
            if self.local_rank <=0:
                print(f"loading from {resume}")
            checkpoint = torch.load(resume, map_location=torch.device("cpu"))  # 可以是cpu,cuda,cuda:index
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.start_epoch = checkpoint['epoch']
            self.actual_epoch = checkpoint['epoch']
            self.actual_step = checkpoint['step']
            if self.local_rank <=0:
                print(f"\nloadding successfully! Start from {self.start_epoch} Epoch and {self.actual_step} Step")

        if self.config.general_dict['gpu_nums'] > 1:
            if self.local_rank == 0:
                print('model has turn to parallel model')
            self.model = nn.parallel.distributed.DistributedDataParallel(self.model.cuda(self.local_rank),device_ids=[self.local_rank])

        self.optimizer = optimizer
        self.criterion = criterion
        self.schedule = schedule

        if self.config.train_dict['use_fp16']:
            if self.config.general_dict['gpu_nums'] == 1 or (self.config.general_dict['gpu_nums'] > 1 and self.local_rank == 0):
                print('Use FP16!!!')
            self.scaler = GradScaler()


        for i in range(self.start_epoch,num_epochs):
            one_time = time.time()

            if self.config.general_dict['gpu_nums'] > 1:
                self.train_sampler.set_epoch(i)

            self.train_avg_loss,self.train_metric_value = self.train_per_epoch()
            if self.local_rank <0 or self.local_rank == 0:
                self.log('Train_AvgLoss_Epoch',self.train_avg_loss,self.actual_epoch)

            if self.train_metric_value is not None:
                if self.local_rank < 0 or self.local_rank == 0:
                    self.log(f'Train_{self.metric.__name__}', self.train_metric_value, self.actual_epoch)

            torch.cuda.synchronize()
            two_time = time.time()

            self.val_avg_loss, self.val_metric_value = self.val_per_epoch()

            self.epoch_information = f'Epoch_{self.actual_epoch}'
            self.train_loss_infor = f'train_loss_{round(self.train_avg_loss,4)}'
            self.val_loss_infor = f'val_loss_{round(self.val_avg_loss,4)}'
            self.train_metric_infor = f'train_{self.metric.__name__}_{round(self.train_metric_value,4)}'
            self.val_metric_infor = f'val_{self.metric.__name__}_{round(self.val_metric_value,4)}'

            self.monitor_information = f'Epoch {self.actual_epoch} : train_loss {round(self.train_avg_loss,4)}  | val_loss {round(self.val_avg_loss,4)} || train_{self.metric.__name__} {round(self.train_metric_value,4)} | val_{self.metric.__name__} {round(self.val_metric_value,4)} | Time {round(two_time-one_time,5)}s | lr = {self.optimizer.state_dict()["param_groups"][0]["lr"]} '
            #print
            if self.local_rank <= 0:
                print()
                print(self.monitor_information)
            if self.config.general_dict['output_train_log'] and self.local_rank <=0:
                self.train_log.write(self.monitor_information+'\n')
            #checkpoint
            if self.config.checkpoint_dict['use_checkpoint'] :
                self.save_checkpoint(self.train_avg_loss,self.val_avg_loss,self.train_metric_value,self.val_metric_value)

        # #output_visual_graphs
        # if self.config.general_dict['output_visual_graphs'] and self.local_rank <=0:
        #     index = list(range(1,self.num_epochs+1))
        #     data = self.train_loss_history
        #     wide_df = pd.DataFrame(data, index, [str('best_'+self.train_loss_infor)])
        #     fig = sns.lineplot(data=wide_df)
        #     plt.xlabel("Epoch");plt.ylabel("Train_loss");plt.title("Visual Graph")
        #     fig.get_figure()
        #     plt.savefig(os.path.join(self.experiment_path,'train_loss.png'), dpi=400)
        #     plt.clf()
        #
        #     data = self.val_loss_history
        #     wide_df = pd.DataFrame(data, index, [str('best_'+self.val_loss_infor)])
        #     fig = sns.lineplot(data=wide_df)
        #     plt.xlabel("Epoch");plt.ylabel("Val_loss");plt.title("Visual Graph")
        #     fig.get_figure()
        #     plt.savefig(os.path.join(self.experiment_path,'val_loss.png'), dpi=400)
        #     plt.clf()
        #
        #     data = self.train_metric_history
        #     wide_df = pd.DataFrame(data, index, [str('best_'+self.train_metric_infor)])
        #     fig = sns.lineplot(data=wide_df)
        #     plt.xlabel("Epoch");plt.ylabel("train_"+self.metric.__name__);plt.title("Visual Graph")
        #     fig.get_figure()
        #     plt.savefig(os.path.join(self.experiment_path,str(f"train_{self.metric.__name__}.png")), dpi=400)
        #     plt.clf()
        #
        #     data = self.val_metric_history
        #     wide_df = pd.DataFrame(data, index, [str('best_'+self.val_metric_infor)])
        #     fig = sns.lineplot(data=wide_df)
        #     plt.xlabel("Epoch");plt.ylabel("val_"+self.metric.__name__);plt.title("Visual Graph")
        #     fig.get_figure()
        #     plt.savefig(os.path.join(self.experiment_path,str(f"val_{self.metric.__name__}.png")), dpi=400)
        #     plt.clf()

        if self.config.checkpoint_dict['use_checkpoint'] and self.config.checkpoint_dict['save_last'] and self.local_rank <=0:
            self.save_last()
        self.train_log.close()
        if self.local_rank >= 0:
            dist.destroy_process_group()

    def train_per_step(self,batch):

        if self.config.general_dict['use_gpu']:
            if self.config.general_dict['gpu_nums'] > 1:

                if self.feature_dict:
                    for b in batch[:-1]:
                        for key,value in b.items():
                            b[key] = value.cuda(self.local_rank)
                    batch[-1] = batch[-1].cuda(self.local_rank)
                else:
                    for i,b in enumerate(batch):
                        batch[i] = b.cuda(self.local_rank)
            else:
                if self.feature_dict:
                    for b in batch[:-1]:
                        for key,value in b.items():
                            b[key] = value.cuda()
                    batch[-1] = batch[-1].cuda()
                                
                else:
                    for i,b in enumerate(batch):
                        batch[i] = b.cuda()                
        else:
            for i, b in enumerate(batch):
                batch[i] = b

        features,label = batch[:-1],batch[-1]

        if self.config.train_dict['use_fp16']:
            with autocast():
                y_pred = self.model(*features)
                loss = self.criterion(y_pred,label)
            if self.config.train_dict['accumulate_num'] > 0:
                loss = loss / self.config.train_dict['accumulate_num']
            self.scaler.scale(loss).backward()
        else:
            y_pred = self.model(*features)
            loss = self.criterion(y_pred, label)
            if self.config.train_dict['accumulate_num'] > 0:
                loss = loss / self.config.train_dict['accumulate_num']
            loss.backward()

        ##累积梯度
        self.accumulate_gradient()

        return loss.item(), y_pred, label

    def val_per_step(self,batch):

        if self.config.general_dict['use_gpu']:
            if self.config.general_dict['gpu_nums'] > 1:

                if self.feature_dict:
                    for b in batch[:-1]:
                        for key,value in b.items():
                            b[key] = value.cuda(self.local_rank)
                    batch[-1] = batch[-1].cuda(self.local_rank)
                else:
                    for i,b in enumerate(batch):
                        batch[i] = b.cuda(self.local_rank)
            else:
                if self.feature_dict:
                    for b in batch[:-1]:
                        for key,value in b.items():
                            b[key] = value.cuda()
                    batch[-1] = batch[-1].cuda()
                else:
                    for i,b in enumerate(batch):
                        batch[i] = b.cuda()   
        else:
            for i, b in enumerate(batch):
                batch[i] = b

        features,label = batch[:-1],batch[-1]

        y_pred = self.model(*features)

        loss = self.criterion(y_pred,label)

        return loss.item(), y_pred, label

    def train_per_epoch(self,
                        use_tqdm=True):

        train_losses  = 0.
        y_preds = []
        labels = []
        if use_tqdm:
            loader_bar = tqdm(self.train_loader)
        else:
            loader_bar = self.train_loader

        self.model.train()
        if self.local_rank<=0:
            print(f'\n***** Running training at epoch {self.actual_epoch} *****')

        for i,batch in enumerate(loader_bar):
            train_loss, y_pred, label = self.train_per_step(batch)
            labels.append(label.detach().cpu().numpy())
            y_preds.append(y_pred.detach().cpu().numpy())

            if self.local_rank <= 0:
                loader_bar.set_postfix({'train_loss_step':train_loss})
                self.log('train_loss_step',train_loss,self.actual_step)

            if self.actual_step % self.log_step_interval == 0 and (self.log_step_interval != len(self.train_loader)) and (self.local_rank <= 0):
                print(f'\n***** Running valid at step {self.actual_step} *****')
                self.val_avg_loss, self.val_metric_value = self.val_per_epoch(use_tqdm=True,use_posfix=True)
                self.log('Val_AvgLoss_step', self.val_avg_loss, self.actual_step)

                if self.val_metric_value is not None:
                    self.log(f'val_{self.metric.__name__}_step', self.val_metric_value, self.actual_step)

                self.step_information = f'Step_{self.actual_step}'
                self.val_loss_infor = f'Val_loss_{round(self.val_avg_loss, 4)}'
                self.val_metric_infor = f'Val_{self.metric.__name__}_{round(self.val_metric_value, 4)}'
                self.monitor_information = f'\nStep {self.actual_step} : Val_loss {round(self.val_avg_loss, 4)} || Val_{self.metric.__name__} {round(self.val_metric_value, 4)} | lr = {self.optimizer.state_dict()["param_groups"][0]["lr"]} '

                print(self.monitor_information)
                # checkpoint
                if self.config.checkpoint_dict['save_step_interval']:
                    self.save_checkpoint_interval(self.val_avg_loss ,self.val_metric_value)
            train_losses += train_loss
            if self.local_rank <=0:
                self.actual_step += 1

            if self.actual_step == self.num_steps:
                if self.local_rank <= 0:
                    print(f"The number of steps has reached {self.actual_step}, terminate the training, save the final weight.")
                    self.val_avg_loss, self.val_metric_value = self.val_per_epoch(use_tqdm=True, use_posfix=True)
                    self.savemodel(f'Final_Step{self.actual_step}_val_{self.metric.__name__}_{round(self.val_metric_value,4)}_'+
                                   f'val_loss_{round(self.val_avg_loss,4)}')
                    if self.local_rank >= 0:
                        dist.destroy_process_group()
                    sys.exit()

        y_preds = np.concatenate(y_preds, axis=0)
        labels = np.concatenate(labels, axis=None)

        if self.local_rank <= 0:

            if self.metric is not None:
                metric_value = self.metric(y_preds,labels)
            else:
                metric_value = None


        if self.local_rank < 0:
            train_losses = train_losses / len(self.train_loader)
            self.actual_epoch += 1
        elif self.local_rank == 0:
            train_losses / dist.get_world_size() / len(self.train_loader)
            self.actual_epoch += 1

        return train_losses,metric_value



    def val_per_epoch(self,use_tqdm=True,use_posfix=True):

        val_losses = 0.
        y_preds = []
        labels = []
        if self.val_loader is None:
            return None,None
        if use_tqdm:
            loader_bar = tqdm(self.val_loader)
        else:
            loader_bar = self.val_loader

        self.model.eval()
        for i, batch in enumerate(loader_bar):
            with torch.no_grad():
                val_loss, y_pred, label= self.val_per_step(batch)
                if self.local_rank <=0:
                    if use_posfix:
                        loader_bar.set_postfix({'val_loss':val_loss})

            labels.append(label.detach().cpu().numpy())
            y_preds.append(y_pred.detach().cpu().numpy())

            val_losses += val_loss

        y_preds = np.concatenate(y_preds,axis=0)
        labels = np.concatenate(labels,axis=None)
        if self.local_rank <= 0:

            if self.metric is not None:
                metric_value = self.metric(y_preds,labels)
            else:
                metric_value = None


        if self.local_rank < 0:
            val_losses = val_losses / len(self.train_loader)
        elif self.local_rank == 0:
            val_losses / dist.get_world_size() / len(self.train_loader)

        return val_losses, metric_value

    def savemodel(self,model_name):
        save_path = os.path.join(self.experiment_path,'checkpoint')
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        model_path = str(os.path.join(save_path, f'{model_name}.pth'))
        if self.config.general_dict['gpu_nums'] <=1:
            torch.save({
                'epoch': self.actual_epoch,
                'step': self.actual_step,
                'model_state_dict': copy.deepcopy(self.model.state_dict()),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'loss': self.criterion,
            },model_path)
        else:
            torch.save({
                'epoch': self.actual_epoch,
                'step': self.actual_step,
                'model_state_dict': copy.deepcopy(self.model.module.state_dict()),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'loss': self.criterion,
            },model_path)
        print(f'Save Model at {model_path}')

    def save_checkpoint(self,train_avg_loss,val_avg_loss,train_metric_value,val_metric_value):
        if self.local_rank <=0:
            if self.config.checkpoint_dict['monitor_by_train_loss']:
                if train_avg_loss < self.last_train_loss:
                    print(f'train_loss由{round(self.last_train_loss, 4)}降到{train_avg_loss}')
                    if self.config.general_dict['output_train_log']:
                        self.train_log.write(f'train_loss由{round(self.last_train_loss, 4)}降到{train_avg_loss}' + '\n')
                    self.last_train_metric = train_avg_loss
                    self.savemodel(self.epoch_information + '_' + self.train_loss_infor)
            elif self.config.checkpoint_dict['monitor_by_val_loss']:
                if val_avg_loss < self.last_val_loss:
                    print(f'val_loss由{round(self.last_val_loss, 4)}降到{val_avg_loss}')
                    if self.config.general_dict['output_train_log']:
                        self.train_log.write(f'val_loss由{round(self.last_val_loss, 4)}降到{val_avg_loss}' + '\n')
                    self.last_val_metric = val_avg_loss
                    self.savemodel(self.epoch_information + '_' + self.val_loss_infor)
            elif self.config.checkpoint_dict['monitor_by_train_metric']:
                if self.config.checkpoint_dict['monitor_max']:

                    if train_metric_value > self.last_train_metric:
                        print(
                            f'train_{self.metric.__name__}由{round(self.last_train_metric, 4)}提高到{round(train_metric_value, 4)}')
                        if self.config.general_dict['output_train_log']:
                            self.train_log.write(f'train_{self.metric.__name__}由{round(self.last_train_metric, 4)}提高到{round(train_metric_value, 4)}' + '\n')
                        self.last_train_metric = train_metric_value
                        self.savemodel(self.epoch_information + '_' + self.train_metric_infor)
                else:
                    if train_metric_value < self.last_train_metric:
                        print(
                            f'train_{self.metric.__name__}由{round(self.last_train_metric, 4)}降低到{round(train_metric_value, 4)}')
                        if self.config.general_dict['output_train_log']:
                            self.train_log.write(f'train_{self.metric.__name__}由{round(self.last_train_metric, 4)}降低到{round(train_metric_value, 4)}' + '\n')
                        self.last_train_metric = train_metric_value
                        self.savemodel(self.epoch_information + '_' + self.train_metric_infor)
            elif self.config.checkpoint_dict['monitor_by_val_metric']:
                if self.config.checkpoint_dict['monitor_max']:

                    if val_metric_value > self.last_val_metric:
                        print(
                            f'val_{self.metric.__name__}由{round(self.last_val_metric, 4)}提高到{round(val_metric_value, 4)}')
                        if self.config.general_dict['output_train_log']:
                            self.train_log.write(f'val_{self.metric.__name__}由{round(self.last_val_metric, 4)}提高到{round(val_metric_value, 4)}' + '\n')
                        self.last_val_metric = val_metric_value
                        self.savemodel(self.epoch_information + '_' + self.val_metric_infor)
                else:
                    if val_metric_value < self.last_val_metric:
                        print(
                            f'train_{self.metric.__name__}由{round(self.last_val_metric, 4)}降低到{round(val_metric_value, 4)}')

                        if self.config.general_dict['output_train_log']:
                            self.train_log.write(f'val_{self.metric.__name__}由{round(self.last_val_metric, 4)}降低到{round(val_metric_value, 4)}' + '\n')
                        self.last_val_metric = val_metric_value
                        self.savemodel(self.epoch_information + '_' + self.val_metric_infor)

    def accumulate_gradient(self):
        if self.config.train_dict['accumulate_num'] < 0 or self.actual_accumulate_num == self.config.train_dict['accumulate_num'] -1:
            if self.config.train_dict['use_fp16']:
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad()
                if self.schedule is not None:
                    self.schedule.step()
            else:
                self.optimizer.step()
                self.optimizer.zero_grad()
                if self.schedule is not None:
                    self.schedule.step()
            if self.config.train_dict['accumulate_num'] > 0:
                self.actual_accumulate_num = 0
        else:
            if self.config.train_dict['accumulate_num']> 0:
                self.actual_accumulate_num += 1

    def save_last(self):
        if self.config.checkpoint_dict['monitor_by_train_loss']:
            self.savemodel('last_model_'+ self.epoch_information + '_' + self.train_loss_infor)
        elif self.config.checkpoint_dict['monitor_by_val_loss']:
            self.savemodel('last_model_'+ self.epoch_information + '_' + self.val_loss_infor)
        elif self.config.checkpoint_dict['monitor_by_train_metric']:
            self.savemodel('last_model_'+ self.epoch_information + '_' + self.train_metric_infor)
        elif self.config.checkpoint_dict['monitor_by_val_metric']:
            self.savemodel('last_model_'+ self.epoch_information + '_' + self.val_metric_infor)

    def fit_init(self):
        if self.config.general_dict['gpu_nums'] > 1:
            assert self.local_rank != None

        if self.config.general_dict['log_dir'] is not None:
            if not os.path.exists(self.config.general_dict['log_dir']):
                os.mkdir(self.config.general_dict['log_dir'])
        self.experiment_id = 0
        if self.config.general_dict['experiment_name'] == 'auto':
            while os.path.exists(os.path.join(self.config.general_dict['log_dir'],"exp"+str(self.experiment_id))):
                self.experiment_id +=1

            self.experiment_path = os.path.join(self.config.general_dict['log_dir'], "exp"+str(self.experiment_id))
            os.mkdir(self.experiment_path)
        else:
            self.experiment_path = os.path.join(self.config.general_dict['log_dir'], self.config.general_dict['experiment_name'])
            if not os.path.exists(self.experiment_path):
                os.mkdir(self.experiment_path)

        self.writer  = tensorboard.SummaryWriter(log_dir=self.experiment_path,comment='trainer')
        self.config.to_json(self.experiment_path)
        if self.config.general_dict['output_train_log']:
            self.train_log = open(os.path.join(self.experiment_path,'train_log.txt'),'w',encoding='utf-8')


    def prepare_loader(self, train_dataset, val_dataset):
        if self.config.general_dict['gpu_nums'] > 1:
            self.train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
            train_loader = DataLoader(train_dataset,batch_size=self.train_batch_size,shuffle=False,sampler=self.train_sampler)
        else:
            train_loader = DataLoader(train_dataset,batch_size=self.train_batch_size,shuffle=False,
                                      num_workers=self.train_num_workers)
        if val_dataset is not None:
            val_loader = DataLoader(val_dataset, batch_size=self.val_batch_size, shuffle=False,
                                num_workers=self.val_num_workers)
        else:
            val_loader =None
        return train_loader,val_loader

    def save_checkpoint_interval(self,val_avg_loss ,val_metric_value):
        if self.config.checkpoint_dict['monitor_by_val_loss']:
            if val_avg_loss < self.last_val_loss:
                print(f'val_loss由{round(self.last_val_loss, 4)}降到{val_avg_loss}')
                if self.config.general_dict['output_train_log']:
                    self.train_log.write(f'val_loss由{round(self.last_val_loss, 4)}降到{val_avg_loss}' + '\n')
                self.last_val_metric = val_avg_loss
                self.savemodel(self.step_information + '_' + self.val_loss_infor)

        elif self.config.checkpoint_dict['monitor_by_val_metric']:
            if self.config.checkpoint_dict['monitor_max']:

                if val_metric_value > self.last_val_metric:
                    print(
                        f'val_{self.metric.__name__}由{round(self.last_val_metric, 4)}提高到{round(val_metric_value, 4)}')
                    if self.config.general_dict['output_train_log']:
                        self.train_log.write(
                            f'val_{self.metric.__name__}由{round(self.last_val_metric, 4)}提高到{round(val_metric_value, 4)}' + '\n')
                    self.last_val_metric = val_metric_value
                    self.savemodel(self.step_information + '_' + self.val_metric_infor)
            else:
                if val_metric_value < self.last_val_metric:
                    print(
                        f'train_{self.metric.__name__}由{round(self.last_val_metric, 4)}降低到{round(val_metric_value, 4)}')

                    if self.config.general_dict['output_train_log']:
                        self.train_log.write(
                            f'val_{self.metric.__name__}由{round(self.last_val_metric, 4)}降低到{round(val_metric_value, 4)}' + '\n')
                    self.last_val_metric = val_metric_value
                    self.savemodel(self.step_information + '_' + self.val_metric_infor)

    def distributed_learning_init(self,local_rank):
        os.environ['MASTER_ADDR'] = 'localhost'
        os.environ['MASTER_PORT'] = '5678'
        dist.init_process_group(backend='nccl',world_size=self.config.general_dict['gpu_nums'],rank=local_rank)
        torch.cuda.set_device(local_rank)



def seed_everything(seed,deterministic=False):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False



