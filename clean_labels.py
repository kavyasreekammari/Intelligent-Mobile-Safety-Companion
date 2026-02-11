import os

# CHANGE THIS PATH IF NEEDED
LABEL_DIRS = [
    "mine_ppe_dataset/labels/train",
    "mine_ppe_dataset/labels/val"
]

VALID_CLASSES = {"0", "1", "2", "3"}  # helmet, gloves, shoes, goggles

for label_dir in LABEL_DIRS:
    if not os.path.exists(label_dir):
        print(f"❌ Folder not found: {label_dir}")
        continue

    print(f"\n🔍 Cleaning folder: {label_dir}")

    for file_name in os.listdir(label_dir):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(label_dir, file_name)

        with open(file_path, "r") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts and parts[0] in VALID_CLASSES:
                cleaned_lines.append(line)

        with open(file_path, "w") as f:
            f.writelines(cleaned_lines)

    print(f"✅ Cleaned: {label_dir}")

print("\n🎉 DONE! Invalid class labels removed safely.")
