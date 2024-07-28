# HF🤗每日简报机器人

该机器人能自动从 [🤗 Daily Papers](https://huggingface.co/papers) 收集paper信息，然后结合智能体进行解读。

# 🤗每日简报机器人如何工作？

1、获取 [🤗 Daily Papers](https://huggingface.co/papers) 中的所有paper信息

2、将收集到的paper信息使用使用智谱AI模型进行元数据的结构化（先将标题翻译成中文，然后保留ID，最后输出）

3、结合智谱清言智能体API进行解读，生成paper的解读信息。

# 已自动化完成的功能

- [X] 自动从 [🤗 Daily Papers](https://huggingface.co/papers) 获取paper信息
- [X] 自动使用智谱AI模型API进行元数据的结构化
- [X] 自动结合智谱清言智能体API进行解读，生成paper的解读信息
- [X] 解读信息自动推送

# 配套项目

[🐍cow二开版](https://github.com/chatgpt-on-wechat-change/chatgpt-on-wechat-two)

[🤖zhipuai-agent-to-openai](https://github.com/LLM-Red-Team/zhipuai-agent-to-openai)

# 未来预加入的功能

- 语音播报功能

# 大佬贡献

感谢  [**V佬**](https://github.com/Vinlic) 的大力帮助


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=2404589803/hf-daily-paper-newsletter-chinese&type=Date)](https://star-history.com/#2404589803/hf-daily-paper-newsletter-chinese&Date)