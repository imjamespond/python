from pathlib import Path
from typing import List

from deepface import DeepFace
import chromadb

import config
import resize
import traverse

# 初始化 ChromaDB 客户端和集合
client = chromadb.PersistentClient(path="./test_db")  # 或使用内存模式
collection = client.get_or_create_collection(name="face_collection")


def batch_save_embeding(img_path: str):
    # for img in os.listdir(img_path):
    #     img = img_path + img
    #     print("正在处理：", img)
    #     # 如果img 不是目录
    #     if os.path.isdir(img):
    #         continue
    #     if not img.lower().endswith((".jpg", ".jpeg")):
    #         continue
    #     try:
    #         save_embeding(img, img)
    #     except Exception as e:
    #         print(e)
    #         continue

    def callback(file: Path):
        if not file.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            return False

        try:
            file_path = str(file)
            save_embeding(file_path, file_path)
        except Exception as e:
            print(e, file_path)
            return False

        return True
    traverse.traverse_files(img_path, callback)


def save_embeding(image_path: str, person_name: str):

    risized_img = resize.resize_to_width(image_path)

    # # DeepFace.represent 返回嵌入向量的列表，每个元素对应图像中检测到的一张人脸
    # embeddings = DeepFace.represent(img_path=image_path, model_name="Facenet", enforce_detection=False)
    embeddings: List[dict] = DeepFace.represent(
        img_path=risized_img, detector_backend=config.detector, align=config.align)
    # print(embeddings)

    for embedding_obj in embeddings:
        embedding = embedding_obj["embedding"]
    
        # 将向量和元数据添加到 ChromaDB
        # embedding 是一个列表，代表向量
        collection.add(
            embeddings=[embedding],           # 向量列表
            ids=[person_name],                # 唯一标识符，通常用姓名或ID
            metadatas=[{"name": person_name}]  # 其他元数据
        )


def search_embeding(image_path):

    risized_img = resize.resize_to_width(image_path)

    embeddings: List[dict] = DeepFace.represent(
        img_path=risized_img,  detector_backend=config.detector, align=config.align)
    # print(embeddings)

    # 假设图像中只有一张人脸，取第一个embedding
    embedding = embeddings[0]["embedding"]

    # 使用向量搜索
    results = collection.query(
        query_embeddings=[embedding],     # 查询向量
        n_results=10                      # 返回最相似的1个结果
    )

    # 获取最相似的元数据
    metadata = results["metadatas"]
    return metadata


if __name__ == '__main__':
    batch_save_embeding("K:\Documents")
