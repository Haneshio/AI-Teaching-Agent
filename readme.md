# AI 教学助手：基于课程资料的 RAG 问答系统
#### 背景：
学习资料很多，不方便快速查找答案
大模型容易脱离课程资料自由发挥
学生需要更适合初学者的解释
学习后希望能生成练习题或检查理解

#### 项目目标：
构建一个基于课程资料的 AI 教学助手。
教师可以上传课程资料，系统自动建立知识库。
学生可以围绕资料提问，AI 根据资料回答，并展示引用来源。

# 一、需求分析
#### 目标用户：学生和教师
#### （1）文件上传功能
教师可以上传相关课程资料（docx,ppt,pdf,txt等）\
如果课程资料已入知识库，提醒课程资料已入库，不能重复上传\
如果课程资料未入知识库，则将课程资料存入知识库中\
#### （2）学生提问功能
学生提问，根据已上传的课程资料进行回答。
# 二、功能拆分
#### （1）文件上传功能：
   - 教师点击上传按钮，可以上传 txt / md 文件
   - 校验文件类型
   - 检查是否已上传，如果没有，则保存，如果已经上传，则提示
#### （2）文档列表功能：
   - 教师可以查看已上传的资料，展示文件名、大小、上传时间、处理状态等
#### （3）文档解析功能：
   - 读取文本内容
   - 清洗空行
   - 按长度切分 chunk
   - 给 chunk 添加 metadata 
#### （4）向量化与入库
   - 对 chunk 生成 embedding
   - 存入向量数据库
   - 保存 filename、chunk_index、content 等信息
#### （5）问答聊天
   - 用户输入问题
   - 后端检索相关 chunk
   - 拼接 prompt
   - 调用大模型生成回答
   - 返回答案和引用来源
#### （6）前端展示
   - 上传资料区域
   - 文档列表区域
   - 聊天问答区域
   - 引用来源展示
   - loading / error 状态
# 三、系统架构设计
![img_1.png](img_1.png)
course_rag_system/
│
├── backend/                      # 🧠 后端（FastAPI + LangChain）
│   ├── app.py                    # 🚀 启动入口
│   ├── config.py                # ⚙️ 配置
│   ├── requirements.txt         # 📦 依赖
│   ├── .env                     # 🔐 密钥
│
│   ├── rag/                     # 🧠 RAG核心逻辑
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   └── chain.py
│
│   ├── services/                # ⚙️ 业务层
│   │   ├── rag_service.py
│   │   └── upload_service.py
│
│   ├── api/                     # 🌐 API层
│   │   ├── chat.py              # 聊天接口
│   │   ├── upload.py            # 上传接口
│   │   └── health.py            # 健康检查
│
│   └── chroma_db/              # 🗃️ 向量库
│
│
├── frontend/                    # 🖥️ 前端（纯前端项目）
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── config.js               # API地址配置
│
│
└── README.md

# 四、数据流设计
#### (1)文档上传流程
用户选择文件：
  - 前端 FormData 上传
  - FastAPI 接收文件
  - 校验文件类型
  - 保存到 uploads/
  - 读取文本内容
  - 文本切分成 chunks
  - 生成 embeddings
  - 存入向量数据库
  - 返回上传和处理结果
#### (2)问答流程
用户输入问题
  -> 前端发送 POST /api/chat
  -> 后端接收 question
  -> 对 question 生成 embedding
  -> 向量数据库检索 top_k chunks
  -> 把 chunks 拼成 context
  -> 构建 prompt
  -> 调用大模型
  -> 返回 answer + sources
  -> 前端展示答案和引用来源

# 五、接口设计
#### （1）文档上传：
- 1.路径：POST /api/documents/upload
- 2.请求：multipart/form-data\
         file: 课程资料
- 3.返回数据：
>{\
"document_id": "doc_001",\
 "filename": "transformer.md",\
 "status": "processed",\
 "chunk_count": 12\
>}

#### （2）文档列表：
- 1.路径：GET /api/documents
- 2.返回数据： 
>{\
  "documents": [ \
    {\
      "document_id": "doc_001",\
      "filename": "transformer.md",\
      "size": 12031,\
      "status": "processed",\
      "chunk_count": 12,\
      "created_at": "2026-05-14 10:30:00"\
    }\
  ]\
>}

#### （3）聊天问答：
- 1.路径：POST /api/chat
- 2.请求：
>{  \
  "question": "什么是注意力机制？",\
  "mode": "explain",\
  "top_k": 5\
>}
- 3.返回数据：
>{\
 "answer": "注意力机制可以理解为...",\
  "sources": [\
    {\
      "document_id": "doc_001",\
      "filename": "transformer.md",\
      "chunk_index": 2,\
      "content": "注意力机制是一种...",\
      "score": 0.83\
    }
  ]
>}

# 六、数据库设计
- SQLite：保存文档元信息、聊天记录
- Chroma：保存向量和 chunk
- uploads/：保存原始文件
#### （1）documents 表
* id              文档 ID
* filename        原始文件名
* file_path       文件保存路径
* file_type       文件类型
* file_size       文件大小
* status          处理状态
* chunk_count     chunk 数量
* created_at      创建时间
* updated_at      更新时间
#### (2)Chroma向量数据库
>{
  "id": "doc_001_chunk_0", \
  "document": "注意力机制是一种...", \
  "embedding": [0.01, 0.23, ...],\
  "metadata": {\
    "document_id": "doc_001",\
    "filename": "transformer.md",\
    "chunk_index": 0,\
    "file_type": "md"\
  }\
>}
> 
> 
