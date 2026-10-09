<<<<<<< HEAD
#  AI教学助手（V0版本）

## 一、项目概述

#### 项目背景

当前课程资料较分散，学生查阅效率低，教师重复答疑成本较高。

因此开发一个课程知识库问答系统，支持课程资料上传、知识检索与智能问答，提高学习效率。  

#### 项目目标

构建一个基于RAG的 AI 教学助手。

目标用户：教师用户和学生用户。

教师可以上传课程资料，系统自动建立知识库。

学生可以围绕资料提问，AI 根据资料回答，并展示引用来源。

## 二、需求分析（功能需求）

### 1、文件上传功能

教师可以上传相关课程资料。

（1）规定用户只能上传txt文件【后续可扩展】

（2）判断文件是否重复上传【去重操作】：

如果课程资料已入知识库，提醒课程资料已入库，不能重复上传。

如果课程资料未入知识库，则将课程资料存入知识库中。



### 2、智能问答功能

用户（学生/教师）提问，系统根据知识库检索和大模型生成相应答案。

如果知识库为空，提醒无匹配结果。



## 三、用户角色分析

| 用户   | 权限         |
| ------ | ------------ |
| 教师   | 上传课程资料 |
| 学生   | 提问         |
| 管理员 | 管理用户     |



## 四、业务流程分析

用户上传文件
        ↓
文档解析
        ↓
文本切分
        ↓
向量化
        ↓
存入知识库
        ↓
用户提问
        ↓
检索相关知识
        ↓
大模型生成回答



## 五、系统架构设计

表现层（前端）
↓
接口层（API）
↓
业务层（Service）
↓
数据层（DB）



## 六、数据库设计

采用MySQL数据库，chroma数据库，和本地文件系统

### 1、MySQL数据库

存储业务数据信息。包含用户表、文件元信息表、

#### （1）用户表User

设计用户表用来存储用户的相关信息，字段如下：

| 字段      | 类型    | 描述                     |
| --------- | ------- | ------------------------ |
| id        | int     | 用户ID                   |
| username  | varchar | 用户名                   |
| password  | varchar | 密码                     |
| user_type | varchar | 用户类型（teacher/user） |

#### （2）文件元信息表File

设计文件表用来存储文件资料的相关信息，字段如下：

| 字段      | 类型    | 描述                         |
| --------- | ------- | ---------------------------- |
| id        | int     | 文件ID                       |
| filename  | varchar | 文件名                       |
| file_path | varchar | 文件真实路径                 |
| file_type | varchar | 文件类型                     |
| file_size | varchar | 文件大小                     |
| file_hash | varchar | 文件内容的 SHA-256，用于去重 |



### 2、Chroma向量数据库

即知识库，存储向量数据chunk

```
{	
  "id": "chunk_001",				 # chunk的唯一id
  "document": "机器学习是一门...",		 # 文本片段
  "embedding": [0.123,0.567,...],	 # chunk对应的向量 
  "metadata": {						 # 元数据
      "file_id": 1,					 # 文件id
      "filename": "机器学习.pdf",	  # 前端展示文件来源
      "file_type": “txt”			 # 文件类型
      "page": 12,					 # 页码
      "chunk_index": 3				 # 用于知道是第几个文本块。
  }
}

```



### 3、文件系统

上传的原始文件存储在uploads/文件夹下



## 七、模块设计

### 1、文件管理模块

负责课程文件上传、存储、与解析功能。

#### （1）文件上传功能

##### 步骤：

1 - 文件上传：教师可以上传相关课程资料。

2 - 类型检验：规定用户只能上传txt\pdf\doc\doc文件【后续可扩展】

3 - 判断文件是否为空，如果为空给出提示

4 - 去重处理：计算文件的md5值，判断文件是否重复上传，如果重复给出提示

5 - 文件存储：在MySQL存储文件元信息，并将原始文件数据存储至uploads文件夹

##### 依赖关系：

本地文件系统 、MySQL 、Chroma

##### 对应接口：

```
POST /files/upload
```



### 2、知识库模块

针对不重复的文本，负责文档解析、向量化与知识检索。

##### 步骤：

1 - 文档解析：针对不重复的文本，进行读取文本，提取文本内容。

2 - 文本切分：将文本切分为chunk

3 - 向量化处理：文本转为向量

4 - 向量存储：将向量存入Chroma

5 - 相似度检索：TopK检索出与问题最相似的文本内容

##### 依赖关系：

LangChain 、Chroma 、 embedding模型



### 3、问答模块

基于知识检索与 LLM 实现智能问答。

##### 步骤：

1 - 用户提问

2 - 检索相关内容：从知识库中检索相关内容

3 - 构建提示词

4 - 调用大模型

5 - 返回答案

##### 依赖关系：

RAG模块、LLM接口

##### 对应接口：

```
POST /chat
```





## 八、API接口设计

### 1、健康检查

```
GET /health
```

##### （1）功能

检查后端服务是否正常启动。

##### （2）返回数据字段：

```
{
  "status": "ok",			# 状态
  "app": "AI Teaching Assistant"
}
```



### 2、文件上传

```
POST /api/documents/upload
```

##### （1）功能

上传 txt 课程资料，后端保存文件，检测重复，切分文本，并写入向量库。

##### （2）请求类型：multipart/form-data

##### （3）请求：file 上传文件

##### （4）返回数据字段：

```
{
  "document_id": 12,		    # 文档 ID，用于后续查询、删除、展示引用来源。
  "filename": "transformer.md",	# 原始文件名，前端展示用。
  "file_type": "md",			# 文件类型，例如 txt / md / pdf。
  "file_size": 12031,			# 文件大小，单位 bytes。
  "file_hash": "9f86d...",		# 文件内容哈希值，用于去重。
  "status": "processed",		# 处理状态，例如 uploaded / processing / processed / failed。
  "chunk_count": 8,				# 切分出的 chunk 数量。
  "duplicate": false,			# 是否重复上传。
  "message": "上传并处理成功"	    # 给前端展示的提示信息。
}

```

### 3、聊天问答

```
POST /api/chat
```

##### （1）功能

根据用户问题，从 Chroma 检索相关课程资料，并调用大模型生成教学式回答。

##### （2）请求类型：multipart/form-data

##### （3）请求：

```
{
  "user_id": 1,			#当前用户 ID。后面做登录后，可以从 token 中解析，不需要前端传。
  "question": "什么是注意力机制？",	# 用户提问
  "mode": "explain",	#回答模式，例如 qa / explain / quiz
  "top_k": 5	# 检索最相关的几个 chunk。
}
```

##### （4）返回数据字段：

```
{
 "answer": "注意力机制可以理解为...",	  # AI回答
  "sources": [					# 来源
    {
      "document_id": 12,		#文档在 MySQL documents 表中的唯一 ID。后面检索、删除、查看详情时，都可以用它定位这份文档。
      "filename": "transformer.md",	# 用户上传时的原始文件名
      "file_type": "txt",			# 文件类型
      "file_size": 12031,			# 文件大小，单位是bytes
      "status": "processed",		# 文档处理状态，
      "chunk_count": 8,				# 文档被切分成了多少个文本块。
      "duplicate": false			# 是否是重复上传。
    }
  ]
}
```

| status常见值 | 说明                                       |
| ------------ | ------------------------------------------ |
| uploaded     | 已上传，但还没开始处理。                   |
| processing   | 正在解析、切分、向量化。                   |
| processed    | 处理完成，可以用于 RAG 问答。              |
| failed       | 处理失败，比如文件解析失败、向量入库失败。 |



## 九、技术选型

| 技术       | 作用     |
| ---------- | -------- |
| Python     | 后端语言 |
| FastAPI    | 接口框架 |
| MySQL      | 数据存储 |
| chroma     | 向量存储 |
| SQLAlchemy | ORM      |
| Vue        | 前端     |
| LangChain  | AI编排   |

## 十、项目目录结构设计

```
course_rag_system/
│
├── backend/                      # 🧠 后端（FastAPI + LangChain）   
	├── app.py                    # 🚀 启动入口  
	├── config.py                # ⚙️ 配置   
	├── requirements.txt         # 📦 依赖   
	├── .env                     # 🔐 密钥   
	
	├── rag/                     # 🧠 RAG核心逻辑   
	│   ├── loader.py 			 # 读取txt
	│   ├── splitter.py 		 # 文本切分 
	│   ├── embeddings.py		 # 向量模型
	│   ├── vectorstore.py  	 # Chroma存取和检索
	│   ├── retriever.py  		 # retriever
	│   ├── prompt.py 			 # 提示词
	│   └── chain.py  			 # 链
	
	├── services/                # ⚙️ 业务层  
	│   ├── rag_service.py│  	 # 上传、去重、切分、入库流程 
	│   └── upload_service.py│	 # 检索、prompt、AI回答流程
	   
	├── api/                     # 🌐 API层   
	│   ├── chat.py              # 聊天接口  
	│   ├── upload.py            # 上传接口   
	│   └── health.py            # 健康检查
    └── chroma_db/              # 🗃️ 向量库
    
├── frontend/                    # 🖥️ 前端（纯前端项目）  
	├── index.html   
	├── css/   
	│   └── style.css   
	├── js/   
	│   └── app.js   
	└── config.js               # API地址配置
	
└── README.md
```



## 
