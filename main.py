import sys
import chroma 


img_path = "e:/temp/covers/"
img1 = "e:/temp/covers/6 (1).jpg"
img2 = "e:/temp/covers/IMG_380-gigapixel-hq-scale-8_00x-cropped.jpg"
db_path = "e:/temp/covers"


if __name__ == '__main__':

    # config.config_gpu()


    # chroma.batch_save_embeding(img_path)

    # 检测两张图片的人脸相似度
    # result: dict = DeepFace.verify(img1_path=img1, img2_path=img2, detector_backend=config.detector, align=config.align)
    # print(result)

    # 搜索图片
    # dfs: List[pd.DataFrame] = DeepFace.find(
    #     img_path=img_path, db_path=db_path)
    # print(dfs)

    # 连数据库
    # DeepFace.register(database_type = "postgres")



    if len(sys.argv) < 2:
        print("请提一个参数")
        sys.exit(1)
    file_path = sys.argv[1]
    
    person_name = chroma.search_embeding(file_path)
    print(person_name)