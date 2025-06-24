import os

folder = r

def should_delete(filename: str) -> bool:
    # 文件名（不包含扩展名）含有空格、下划线、连字符就返回True
    name, _ = os.path.splitext(filename)
    return any(c in name for c in [' ', '_', '-'])

def main():
    for fname in os.listdir(folder):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            if should_delete(fname):
                file_path = os.path.join(folder, fname)
                print(f"Deleting file: {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    main()
