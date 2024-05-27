# HF🤗每日简报机器人

该机器人能自动从 [🤗 Daily Papers](https://huggingface.co/papers) 收集paper信息，然后结合智能体进行解读。

# 🤗每日简报机器人如何工作？

1、获取 [🤗 Daily Papers](https://huggingface.co/papers) 中的所有paper信息

    包括：

    ①、论文标题

    ②、arxiv ID

    ③、论文摘要

2、将收集到的paper信息使用GLM-4 API进行元数据的结构化

3、结合智谱清言智能体API进行解读，生成paper的解读信息。

# 已自动化完成的功能

- [x] 自动从 [🤗 Daily Papers](https://huggingface.co/papers) 获取paper信息

- [x] 自动使用GLM-4 API进行元数据的结构化

- [ ] 自动结合智谱清言智能体API进行解读，生成paper的解读信息


