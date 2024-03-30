import json

# 读取JSON文件
with open("D:\\python project\\hf-daily-paper-newsletter-chinese\\daily_papers\\daily_papers_2024-03-29.json", "r") as file:
    data = json.load(file)

# 提取论文信息并按指定顺序排列
papers_clean = [{"title": paper["paper"]["title"],
                "id": paper["paper"]["id"],
                "summary": paper["paper"]["summary"]} for paper in data]

# 生成新文件名
original_filename = "D:\\python project\\hf-daily-paper-newsletter-chinese\\daily_papers_clean\\daily_papers_2024-03-29.json"
filename_parts = original_filename.split(".")
new_filename = f"{filename_parts[0]}_clean.{filename_parts[1]}"

# 保存到新文件
with open(new_filename, "w") as file:
    json.dump(papers_clean, file, indent=4)
