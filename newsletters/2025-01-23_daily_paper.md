
# <img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png" width="30"/> Hugging Face 2025-01-23 论文日报

## 📊 今日论文统计
- 总论文数：5
- 热门领域：LLM, GPT, RL

## 📝 论文详情


### 1. FilmAgent：虚拟3D空间中端到端电影自动化的多智能体框架

**原文标题：** FilmAgent: A Multi-Agent Framework for End-to-End Film Automation in
  Virtual 3D Spaces

**摘要：**
虚拟电影制作需要复杂的决策过程，包括剧本创作、虚拟摄影以及精确的演员定位和动作。受近期基于语言智能体的自动化决策进展的启发，本文提出了FilmAgent，一个基于大语言模型（LLM）的多智能体协作框架，用于在我们构建的3D虚拟空间中进行端到端的电影自动化制作。FilmAgent模拟了各种剧组角色，包括导演、编剧、演员和摄影师，并涵盖了电影制作工作流程的关键阶段：（1）创意开发将头脑风暴的想法转化为结构化的故事大纲；（2）剧本创作详细阐述每个场景的对话和角色动作；（3）摄影确定每个镜头的摄像机设置。一组智能体通过迭代反馈和修订进行协作，从而验证中间剧本并减少幻觉。我们评估了基于15个创意和4个关键方面生成的视频。人类评估显示，FilmAgent在所有方面均优于所有基线模型，平均得分为3.98（满分5分），展示了多智能体协作在电影制作中的可行性。进一步分析表明，尽管FilmAgent使用了较不先进的GPT-4o模型，但其表现优于单智能体o1，显示了协调良好的多智能体系统的优势。最后，我们讨论了OpenAI的文本到视频模型Sora与我们的FilmAgent在电影制作中的互补优势和劣势。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.12909) | [arXiv](https://arxiv.org/abs/2501.12909)



---

### 2. DeepSeek-R1：通过强化学习激励大语言模型的推理能力

**原文标题：** DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via
  Reinforcement Learning

**摘要：**
我们介绍了第一代推理模型DeepSeek-R1-Zero和DeepSeek-R1。DeepSeek-R1-Zero是一个通过大规模强化学习（RL）训练的模型，无需监督微调（SFT）作为初步步骤，展示了显著的推理能力。通过RL，DeepSeek-R1-Zero自然涌现出许多强大且有趣的推理行为。然而，它也面临诸如可读性差和语言混合等挑战。为了解决这些问题并进一步提升推理性能，我们引入了DeepSeek-R1，它在RL之前结合了多阶段训练和冷启动数据。DeepSeek-R1在推理任务上的表现与OpenAI-o1-1217相当。为了支持研究社区，我们开源了DeepSeek-R1-Zero、DeepSeek-R1以及基于Qwen和Llama从DeepSeek-R1蒸馏出的六个密集模型（1.5B、7B、8B、14B、32B、70B）。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.12948) | [arXiv](https://arxiv.org/abs/2501.12948)



---

### 3. 专家自主模型

**原文标题：** Autonomy-of-Experts Models

**摘要：**
专家混合模型（Mixture-of-Experts, MoE）通常使用路由器将令牌分配给特定的专家模块，仅激活部分参数，并且往往优于密集模型。我们认为，路由器的决策与专家的执行之间的分离是一个关键但被忽视的问题，导致专家选择次优和学习效果不佳。为了解决这一问题，我们提出了专家自主模型（Autonomy-of-Experts, AoE），这是一种新颖的MoE范式，其中专家自主选择自己来处理输入。AoE基于一个洞察，即专家了解自己有效处理令牌的能力，这种意识反映在其内部激活的规模上。在AoE中，路由器被移除；相反，专家预先计算输入的内部激活，并根据其激活范数进行排名。只有排名最高的专家继续进行前向传播，而其他专家则中止。通过低秩权重分解，减少了预先计算激活的开销。这种先自我评估再伙伴比较的方法确保了改进的专家选择和有效的学习。我们预训练了参数从700M到4B的语言模型，证明AoE在效率相当的情况下优于传统的MoE模型。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.13074) | [arXiv](https://arxiv.org/abs/2501.13074)



---

### 4. Kimi k1.5：利用大语言模型扩展强化学习

**原文标题：** Kimi k1.5: Scaling Reinforcement Learning with LLMs

**摘要：**
通过下一个词预测进行语言模型预训练已被证明在计算扩展方面是有效的，但其受限于可用训练数据的数量。扩展强化学习（RL）为人工智能的持续改进开辟了新的方向，其前景在于大语言模型（LLMs）能够通过奖励驱动的探索来扩展其训练数据。然而，先前发表的工作尚未产生具有竞争力的结果。鉴于此，我们报告了Kimi k1.5的训练实践，这是我们最新通过RL训练的多模态LLM，包括其RL训练技术、多模态数据配方和基础设施优化。长上下文扩展和改进的策略优化方法是我们方法的关键要素，该方法建立了一个简单而有效的RL框架，而不依赖于更复杂的技术，如蒙特卡罗树搜索、价值函数和过程奖励模型。值得注意的是，我们的系统在多个基准测试和模态上实现了最先进的推理性能——例如，AIME上77.5分，MATH 500上96.2分，Codeforces上94百分位，MathVista上74.9分——与OpenAI的o1相当。此外，我们提出了有效的长到短方法，利用长链思维（long-CoT）技术改进短链思维（short-CoT）模型，产生了最先进的短链思维推理结果——例如，AIME上60.8分，MATH500上94.6分，LiveCodeBench上47.3分——大幅超越了现有的短链思维模型，如GPT-4o和Claude Sonnet 3.5（高达+550%）。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.12599) | [arXiv](https://arxiv.org/abs/2501.12599)



---

### 5. O1-Pruner：用于O1类推理剪枝的长度协调微调

**原文标题：** O1-Pruner: Length-Harmonizing Fine-Tuning for O1-Like Reasoning Pruning

**摘要：**
最近，像OpenAI的O1这样的长思维推理大语言模型（LLMs）采用了类似于人类思考复杂问题的扩展推理过程。这种推理范式显著增强了模型的问题解决能力，并取得了令人瞩目的成果。然而，长思维推理过程导致推理时间大幅增加。一个紧迫的挑战是在确保准确性的同时减少长思维LLMs的推理开销。在本文中，我们通过实验证明，长思维推理模型难以根据问题难度和推理冗余有效分配token预算。为了解决这一问题，我们提出了长度协调微调（O1-Pruner），旨在最小化推理开销的同时保持准确性。这种有效的微调方法首先通过预采样估计LLM的基线性能，然后使用强化学习风格的微调来鼓励模型在准确性约束下生成更短的推理过程。这使得模型能够在保持准确性的同时以较低的冗余实现高效推理。在各种数学推理基准上的实验表明，O1-Pruner不仅显著减少了推理开销，还实现了更高的准确性，为这一挑战提供了一个新颖且有前景的解决方案。我们的代码即将发布在https://github.com/StarDewXXX/O1-Pruner。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.12570) | [arXiv](https://arxiv.org/abs/2501.12570)



---


## 🔍 关键词云图
![关键词云图](../images/keywords_wordcloud.png)

## 📈 近期论文趋势
![论文趋势](../images/daily_papers.png)

## 🎙️ 语音播报
- [收听今日论文解读](../audio/2025-01-23_daily_papers.mp3)

## 📱 订阅渠道
- GitHub: [hf-daily-paper-newsletter-chinese](https://github.com/2404589803/hf-daily-paper-newsletter-chinese)