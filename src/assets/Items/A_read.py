import os

# 指定文件夹路径
folder_path = "D:/Files/学业文档/大三下/人工智能系统/group/Assited-Language-Learning-Role-playing-Game-Based-on-LLM/src/assets/Items"

# 获取文件夹中所有png文件名（不带路径）
png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]

# 写入txt文件
with open('png_filenames.txt', 'w', encoding='utf-8') as f:
    for filename in png_files:
        name_without_ext = os.path.splitext(filename)[0]  # 去掉扩展名
        f.write(name_without_ext + '\n')

print(f'共写入 {len(png_files)} 个PNG文件名到 png_filenames.txt')
