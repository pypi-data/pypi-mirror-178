
# JJTrainer

这个库是基于pytorch的深度学习训练库，你可以通过这个库仅仅通过设定好参数，
定义好模型和数据流过程，便可快速开始训练，
而且模型还支持FP16、梯度累积、lr_shedule、多卡学习、gradient等技巧，帮助你简化训练过程，
快速开始训练。


## Environment


### Requirement.txt
```
  numpy
  torch
  sklearn
  json

```

### Use this method to Install
```
pip install JJTrainer

or git clone it straightly
```
# Quick Start

## CV

参考比赛 Digit-Recognizer
![image]('./readme/competition1.jpg)

来自：https://www.kaggle.com/c/digit-recognizer
```ipynb
#导库
import numpy as np
import pandas as pd
import timm
import torch
import torch.nn as nn
import  albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
from JJTrainer.Trainer import Trainer,Conifg,Metrics,seed_everything
import os
from torch.utils.data import DataLoader,Dataset

#路径定义
root_path = r'your_path'
submission = pd.read_csv(os.path.join(root_path,'sample_submission.csv'))
train_csv = pd.read_csv(os.path.join(root_path,'train.csv'))
test_csv = pd.read_csv(os.path.join(root_path,'test.csv'))

#数据处理
#简单数据划分
from sklearn.model_selection import train_test_split
train_csv,val_csv = train_test_split(train_csv,train_size=0.8,shuffle=True)

#数据增强
data_transforms = {
    'train':A.Compose(
        [
            A.Normalize(
                std = [0.5],
                mean = [0.5]
            ),
            ToTensorV2()
        ]
    ),
    'val':A.Compose(
        [
            A.Normalize(
                std = [0.5],
                mean = [0.5]
            ),
            ToTensorV2()
        ]
    )

}

#dataset 定义
class DigitDataset(Dataset):
    def __init__(self,df,data_transforms):
        self.df = df.reset_index(drop=True)
        self.imgs = self.df.iloc[:,1:]
        self.labels = self.df.iloc[:,0]
        self.data_transforms = data_transforms
    def __len__(self):
        return len(self.imgs)
    def __getitem__(self, item):
        img = np.array(self.imgs.iloc[item,:].values).astype(np.float32).reshape(28,28,1)
        label = self.labels.iloc[item]
        if self.data_transforms is not None:
            img = self.data_transforms(image=img)['image']
        return img,torch.tensor(label,dtype=torch.long)

#模型定义
import timm

class DigitModel(nn.Module):
    def __init__(self):
        super(DigitModel, self).__init__()
        self.model = timm.create_model('resnet18',in_chans=1,num_classes=10,pretrained=True)
    def forward(self,img):
        return self.model(img)


#训练参数定义
class TrainConfig(Config):
    def __init__(self):
        super(TrainConfig, self).__init__()
        self.checkpoint_dict.update({
            'use_checkpoint':True
        })

if __name__ == '__main__':
    #模型声明
    model = DigitModel().cuda()

    #优化器定义和声明
    from torch.optim import Adam
    optimizer = Adam(model.parameters(),lr=2e-4)

    #损失函数定义
    criterion = nn.CrossEntropyLoss()

    #训练参数声明
    train_config = TrainConfig()

    #指标定义
    metrics = Metrics()

    #dataset
    train_dataset = DigitDataset(train_csv,data_transforms['train'])
    val_dataset = DigitDataset(val_csv,data_transforms['val'])

    #开始训练
    trainer = Trainer(train_config)
    trainer.fit(model=model,train_dataset=train_dataset,val_dataset=val_dataset,
                num_epochs=10,
                metric=metrics.acc,optimizer=optimizer,criterion=criterion,
                train_batch_size=32,val_batch_size=16)      
```

模型训练过程：
![image](./readme/train_process1.png)
模型文件结构:
![image](./readme/dir_structure.png)
模型训练参数一览：
```
#模型参数
[
  "一般配置",
  {
    "seed": 0,
    "gpu_nums": 1,
    "use_gpu": true,
    "log_dir": "monitor",
    "experiment_name": "auto",
    "output_train_log": true,
    "output_visual_graphs": true,
    "test_experiment": false
  },
  "训练参数配置",
  {
    "accumulate_num": -1,
    "use_fp16": false
  },
  "模型参数配置",
  {},
  "模型检查点配置",
  {
    "use_checkpoint": true,
    "save_step_interval": false,
    "monitor_by_train_loss": false,
    "monitor_by_val_loss": false,
    "monitor_by_train_metric": false,
    "monitor_by_val_metric": true,
    "use_early_stopping": false,
    "monitor_max": true,
    "save_top_k": -1,
    "save_last": true
  }
]
```
训练日志:
```
Epoch 1 : train_loss 0.2316  | val_loss 0.0335 || train_accuracy 0.9327 | val_accuracy 0.9821 | Time 35.0065s | lr = 0.0002 
val_accuracy由0.0提高到0.9821
Epoch 2 : train_loss 0.0626  | val_loss 0.0249 || train_accuracy 0.9814 | val_accuracy 0.9872 | Time 19.91203s | lr = 0.0002 
val_accuracy由0.9821提高到0.9872
Epoch 3 : train_loss 0.0416  | val_loss 0.0315 || train_accuracy 0.9869 | val_accuracy 0.9842 | Time 21.27667s | lr = 0.0002 
Epoch 4 : train_loss 0.0341  | val_loss 0.0301 || train_accuracy 0.9899 | val_accuracy 0.9849 | Time 24.79746s | lr = 0.0002 
Epoch 5 : train_loss 0.0299  | val_loss 0.0221 || train_accuracy 0.991 | val_accuracy 0.9872 | Time 22.05825s | lr = 0.0002 
Epoch 6 : train_loss 0.0233  | val_loss 0.0294 || train_accuracy 0.9927 | val_accuracy 0.9868 | Time 22.97047s | lr = 0.0002 
Epoch 7 : train_loss 0.0199  | val_loss 0.0342 || train_accuracy 0.9939 | val_accuracy 0.9836 | Time 22.94003s | lr = 0.0002 
Epoch 8 : train_loss 0.0261  | val_loss 0.0222 || train_accuracy 0.9925 | val_accuracy 0.9888 | Time 22.70077s | lr = 0.0002 
val_accuracy由0.9872提高到0.9888
Epoch 9 : train_loss 0.0192  | val_loss 0.03 || train_accuracy 0.9945 | val_accuracy 0.9825 | Time 24.11863s | lr = 0.0002 
Epoch 10 : train_loss 0.0232  | val_loss 0.0226 || train_accuracy 0.9931 | val_accuracy 0.9875 | Time 26.65615s | lr = 0.0002 

```

## NLP （with MultiGPU）

### 新闻分类
```
#导库
import torch
import torch.nn as nn
import transformers
import pandas as pd
import numpy as np
from JJTrainer.Trainer import  Trainer,Metrics,Config,seed_everything
from torch.utils.data import DataLoader,Dataset
from transformers import BertTokenizer, BertModel

#固定种子
seed_everything(0)

#训练参数定义
class TrainConfig(Config):
    def __init__(self):
        super(TrainConfig, self).__init__()
        self.general_dict.update({
            'use_gpu':True,
            'gpu_nums':2
        })
        self.checkpoint_dict.update({
            'use_checkpoint':True,
            'save_step_interval':True
        })
        self.train_dict.update({
            'use_fp16':True
        })


#训练指标定义
class NewsMetrics(Metrics):
    def __init__(self):
        super(NewsMetrics, self).__init__()

class NewsDataset(Dataset):
    def __init__(self,df,tokenizer):
        self.df = df.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.titles = list(self.df['title'])
        self.texts = list(self.df['text'])
        self.labels = list(self.df['label'])
    def __len__(self):
        return len(self.df)
    def get_batch_texts(self,idx):
        #fetch a batch of inputs
        return self.tokenizer(self.texts[idx],
                        padding= 'max_length',max_length=512,truncation=True,
                        return_tensors='pt')
    def __getitem__(self, item):
        title = self.get_batch_texts(item)
        text = self.get_batch_texts(item)
        label = self.labels[item]
        return title,text,torch.tensor(label,dtype=torch.long)
    

    #模型定义
class NewsModel(nn.Module):
    def __init__(self):
        super(NewsModel, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.projection = nn.Linear(self.bert.pooler.dense.out_features*2,2)
    def forward(self,title_dict,text_dict):
        text_embedding = self.bert(input_ids=text_dict['input_ids'].squeeze(1),
                                   token_type_ids=text_dict['token_type_ids'].squeeze(1),
                                   attention_mask = text_dict['attention_mask'].squeeze(1),
                                   )['pooler_output']

        title_embedding = self.bert(input_ids=title_dict['input_ids'].squeeze(1),
                                   token_type_ids=title_dict['token_type_ids'].squeeze(1),
                                   attention_mask = title_dict['attention_mask'].squeeze(1)
                                    )['pooler_output']
        embedding  = torch.concat([text_embedding,title_embedding],dim=-1)
        out = self.projection(embedding)
        return out

    
if __name__ == '__main__':
    metrics = NewsMetrics()

    #读取数据
    all_data = pd.read_csv('./news.csv').iloc[:,1:].fillna('nan')

    #数据处理 (数据划分、数据编码，数据流）
    from sklearn.model_selection import train_test_split
    train_data,val_data = train_test_split(all_data,train_size=0.99,random_state=0)

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    #模型声明
    train_config = TrainConfig()
    model = NewsModel().cuda()

    #数据声明
    train_dataset = NewsDataset(train_data,tokenizer)
    val_dataset = NewsDataset(val_data,tokenizer)

    #优化器定义声明
    from torch.optim import Adam
    optimizer = Adam(model.parameters(),lr=1e-5)
    #损失函数定义
    criterion = nn.CrossEntropyLoss()
    #训练器定义
    trainer = Trainer(train_config)

    #训练过程
    trainer.fit(model=model,train_dataset=train_dataset,val_dataset=val_dataset,optimizer=optimizer,criterion=criterion,metric=metrics.acc,num_epochs=10,feature_dict=True,train_num_workers=28,val_num_workers=2,train_batch_size=40,val_batch_size=128,log_step_interval=5)

```

