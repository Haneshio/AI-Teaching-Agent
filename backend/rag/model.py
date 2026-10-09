"""模型读取"""
from langchain_community.chat_models.tongyi import ChatTongyi
from backend.config import ChatModelConfig,chatmodel_config,dashscope_config
def create_chat_model(config: ChatModelConfig=chatmodel_config):
    model= ChatTongyi(
        model=config.model,
        model_kwargs={
            "temperature":config.temperature,
        },
        api_key=dashscope_config.api_key

    )
    return model
