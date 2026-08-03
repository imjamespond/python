import os
import time
import random
from pathlib import Path
from typing import List

from deepface import DeepFace
import chromadb

import config
import resize
import traverse

# 初始化 ChromaDB 客户端和集合
db_path = os.getenv("DB_PATH", "./test_db")
resize_img = os.getenv("RESIZE_IMG")


from chromadb.config import Settings

settings = Settings(
    chroma_memory_limit_bytes=1 * 1024 * 1024 * 1024,
    chroma_segment_cache_policy="LRU"
)
client = chromadb.PersistentClient(path=db_path, settings=settings)  # 或使用内存模式
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

    img = image_path if resize_img == None else resize.resize_to_width(
        image_path)

    # # DeepFace.represent 返回嵌入向量的列表，每个元素对应图像中检测到的一张人脸
    # embeddings = DeepFace.represent(img_path=image_path, model_name="Facenet", enforce_detection=False)
    embeddings: List[dict] = DeepFace.represent(
        img_path=img, detector_backend=config.detector, align=config.align)
    # print(embeddings)

    for embedding_obj in embeddings:
        embedding = embedding_obj["embedding"]

        # 将向量和元数据添加到 ChromaDB
        # embedding 是一个列表，代表向量
        collection.add(
            embeddings=[embedding],           # 向量列表
            ids=[unique_id()],                # 唯一标识符，通常用姓名或ID
            metadatas=[{"name": person_name}]  # 其他元数据
        )


def unique_id():
    return f"{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

def search_embeding(image_path, top_N=10):

    risized_img = resize.resize_to_width(image_path)

    embeddings: List[dict] = DeepFace.represent(
        img_path=risized_img,  detector_backend=config.backends[3], align=config.align)
    # print(embeddings)

    # 假设图像中只有一张人脸，取第一个embedding
    embedding = embeddings[0]["embedding"]

    # 使用向量搜索
    results = collection.query(
        query_embeddings=[embedding],     # 查询向量
        n_results=top_N                      # 返回最相似的1个结果
        # include: Include = ["metadatas", "documents", "distances"],
    )

    # 获取最相似的元数据
    # metadata = results["metadatas"]
    distances = results["distances"]
    print(distances)

    return results

def search_name_fuzzy_batch(person_name: str, limit: int = 10, batch_size: int = 100):
    """
    分批模糊查找人名（子串匹配，不区分大小写）
    
    Args:
        person_name: 部分人名关键词
        limit: 最多返回条数
        batch_size: 每批拉取的记录数，默认100
    
    Returns:
        匹配的记录，包含 ids, embeddings, metadatas 等
    """
    keyword = person_name.lower()
    matched_ids = []
    
    offset = 0
    while True:
        # 分批获取元数据（不包含向量，减轻传输压力）
        batch = collection.get(
            limit=batch_size,
            offset=offset,
            include=["metadatas"]
        )
        
        # 如果没有更多数据，退出
        if not batch or not batch.get("ids"):
            break

        print('offset', offset, "matched_ids", len(matched_ids))
        
        # 在当前批次中筛选匹配的记录
        for i, meta in enumerate(batch["metadatas"]):
            if meta and "name" in meta and keyword in meta["name"].lower():
                matched_ids.append(batch["ids"][i])
                if len(matched_ids) >= limit:
                    break
        
        # 如果已经找到足够记录，停止分页
        if len(matched_ids) >= limit:
            break
        
        # 如果本批次数量小于 batch_size，说明已是最后一批
        if len(batch["ids"]) < batch_size:
            break
        
        offset += batch_size
    
    # 没有匹配结果
    if not matched_ids:
        return {"ids": [], "embeddings": [], "metadatas": [], "documents": []}
    
    # 根据匹配 ID 获取完整数据（含向量）
    results = collection.get(
        ids=matched_ids,
        include=["embeddings", "metadatas", "documents"]
    )
    return results

if __name__ == '__main__':
    # batch_save_embeding(os.getenv("IMAGE_PATH"))
    print(search_name_fuzzy_batch("林志玲"))

