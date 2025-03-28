
# <img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png" width="30"/> Hugging Face 2025-01-15 论文日报

## 📊 今日论文统计
- 总论文数：10
- 热门领域：GPT, Diffusion, LLM, RL

## 📝 论文详情


### 1. MiniMax-01：基于闪电注意力机制扩展基础模型

**原文标题：** MiniMax-01: Scaling Foundation Models with Lightning Attention

**摘要：**
我们推出了MiniMax-01系列，包括MiniMax-Text-01和MiniMax-VL-01，这些模型在性能上可与顶级模型相媲美，同时在处理更长上下文方面展现出卓越能力。其核心在于闪电注意力机制及其高效扩展。为了最大化计算能力，我们将其与专家混合模型（MoE）相结合，创建了一个包含32个专家、总计4560亿参数的模型，其中每个token激活459亿参数。我们为MoE和闪电注意力机制开发了优化的并行策略和高效的计算-通信重叠技术。这种方法使我们能够在跨越数百万token的上下文中，对具有数千亿参数的模型进行高效的训练和推理。MiniMax-Text-01的上下文窗口在训练时可达到100万token，在推理时可外推至400万token，且成本可控。我们的视觉-语言模型MiniMax-VL-01是通过继续训练5120亿视觉-语言token构建的。在标准和内部基准测试中的实验表明，我们的模型在性能上与GPT-4o和Claude-3.5-Sonnet等最先进模型相当，同时提供20-32倍长的上下文窗口。我们在https://github.com/MiniMax-AI上公开发布了MiniMax-01。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08313) | [arXiv](https://arxiv.org/abs/2501.08313)



---

### 2. 基于指令跟随的多模态AI辅助单细胞分析系统

**原文标题：** A Multi-Modal AI Copilot for Single-Cell Analysis with Instruction
  Following

**摘要：**
大型语言模型在解释复杂的自然语言指令方面表现出色，使其能够执行广泛的任务。在生命科学领域，单细胞RNA测序（scRNA-seq）数据被视为“细胞生物学的语言”，在单细胞水平上捕捉复杂的基因表达模式。然而，通过传统工具与这种“语言”进行交互通常效率低下且不直观，给研究人员带来了挑战。为了解决这些限制，我们提出了InstructCell，一种多模态AI辅助系统，利用自然语言作为媒介，实现更直接和灵活的单细胞分析。我们构建了一个全面的多模态指令数据集，将基于文本的指令与来自不同组织和物种的scRNA-seq数据配对。在此基础上，我们开发了一种多模态细胞语言架构，能够同时解释和处理这两种模态。InstructCell使研究人员能够使用简单的自然语言命令完成关键任务，如细胞类型注释、条件性伪细胞生成和药物敏感性预测。广泛的评估表明，InstructCell在各种实验条件下始终达到或超越现有单细胞基础模型的性能。更重要的是，InstructCell为探索复杂的单细胞数据提供了一个易于访问且直观的工具，降低了技术门槛，使研究人员能够获得更深入的生物学见解。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08187) | [arXiv](https://arxiv.org/abs/2501.08187)



---

### 3. MangaNinja：基于精确参考跟随的线稿上色

**原文标题：** MangaNinja: Line Art Colorization with Precise Reference Following

**摘要：**
MangaNinja源自扩散模型，专门用于参考引导的线稿上色任务。我们引入了两个深思熟虑的设计，以确保精确的角色细节转录，包括一个用于促进参考彩色图像与目标线稿之间对应学习的补丁混洗模块，以及一个点驱动控制方案，以实现细粒度的颜色匹配。在自收集的基准测试中，实验证明了我们的模型在精确上色方面优于当前解决方案。我们进一步展示了所提出的交互式点控制在处理具有挑战性的案例、跨角色上色、多参考协调等方面的潜力，这些是现有算法无法企及的。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08332) | [arXiv](https://arxiv.org/abs/2501.08332)



---

### 4. 扩散对抗后训练用于一步视频生成

**原文标题：** Diffusion Adversarial Post-Training for One-Step Video Generation

**摘要：**
扩散模型广泛用于图像和视频生成，但其迭代生成过程缓慢且昂贵。虽然现有的蒸馏方法在图像领域展示了一步生成的潜力，但它们仍然存在显著的画质下降问题。在本研究中，我们提出了一种对抗后训练（APT）方法，该方法在扩散预训练之后针对真实数据进行训练，以实现一步视频生成。为了提高训练稳定性和质量，我们引入了对模型架构和训练程序的若干改进，以及一个近似的R1正则化目标。实验表明，我们的对抗后训练模型Seaweed-APT能够实时生成2秒、1280x720分辨率、24帧率的视频，仅需一次前向评估步骤。此外，我们的模型能够一步生成1024像素的图像，其质量可与最先进的方法相媲美。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08316) | [arXiv](https://arxiv.org/abs/2501.08316)



---

### 5. 使用紧凑的文本感知一维标记实现文本到图像掩码生成模型的民主化

**原文标题：** Democratizing Text-to-Image Masked Generative Models with Compact
  Text-Aware One-Dimensional Tokens

**摘要：**
图像标记器构成了现代文本到图像生成模型的基础，但其训练过程众所周知地困难。此外，大多数现有的文本到图像模型依赖于大规模、高质量的私有数据集，这使得它们难以复制。在这项工作中，我们引入了文本感知的基于变压器的一维标记器（TA-TiTok），这是一种高效且强大的图像标记器，可以利用离散或连续的一维标记。TA-TiTok在标记器解码阶段（即去标记化）独特地集成了文本信息，加速了收敛并提高了性能。TA-TiTok还受益于一个简化但有效的一阶段训练过程，消除了之前一维标记器中使用的复杂两阶段蒸馏的需求。这种设计使得能够无缝扩展到大型数据集。在此基础上，我们引入了一系列文本到图像的掩码生成模型（MaskGen），这些模型仅在开放数据上训练，同时实现了与在私有数据上训练的模型相当的性能。我们旨在发布高效的、强大的TA-TiTok标记器以及开放数据、开放权重的MaskGen模型，以促进更广泛的访问并实现文本到图像掩码生成模型领域的民主化。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.07730) | [arXiv](https://arxiv.org/abs/2501.07730)



---

### 6. FramePainter：赋予交互式图像编辑视频扩散先验

**原文标题：** FramePainter: Endowing Interactive Image Editing with Video Diffusion
  Priors

**摘要：**
交互式图像编辑允许用户通过绘制、点击和拖动等视觉交互操作来修改图像。现有方法从视频中构建此类监督信号，因为它们捕捉了物体如何随各种物理交互而变化。然而，这些模型通常基于文本到图像的扩散模型，因此需要（i）大量的训练样本和（ii）额外的参考编码器来学习现实世界的动态和视觉一致性。在本文中，我们将此任务重新表述为图像到视频生成问题，从而继承强大的视频扩散先验，以减少训练成本并确保时间一致性。具体来说，我们引入了FramePainter作为这一表述的高效实例化。通过Stable Video Diffusion初始化，它仅使用轻量级的稀疏控制编码器来注入编辑信号。考虑到时间注意力在处理两帧之间大运动时的局限性，我们进一步提出了匹配注意力，以扩大感受野，同时鼓励编辑图像和源图像标记之间的密集对应。我们强调了FramePainter在各种编辑信号中的有效性和效率：它在训练数据远远少于之前最先进方法的情况下，显著优于这些方法，实现了高度无缝和连贯的图像编辑，例如自动调整杯子的反射。此外，FramePainter在现实世界视频中不存在的场景中也表现出卓越的泛化能力，例如将小丑鱼转变为鲨鱼形状。我们的代码将可在https://github.com/YBYBZhang/FramePainter获取。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08225) | [arXiv](https://arxiv.org/abs/2501.08225)



---

### 7. PokerBench：训练大型语言模型成为专业扑克玩家

**原文标题：** PokerBench: Training Large Language Models to become Professional Poker
  Players

**摘要：**
我们介绍了PokerBench——一个用于评估大型语言模型（LLMs）扑克游戏能力的基准。随着LLMs在传统自然语言处理任务中的卓越表现，它们在复杂、策略性游戏如扑克中的应用提出了新的挑战。扑克作为一种不完全信息游戏，需要多种技能，如数学、推理、规划、策略以及对博弈论和人类心理学的深刻理解。这使得扑克成为大型语言模型的理想前沿领域。PokerBench包含11,000个最重要的场景，分为翻牌前和翻牌后游戏，这些场景是与训练有素的扑克玩家合作开发的。我们评估了包括GPT-4、ChatGPT 3.5以及各种Llama和Gemma系列模型在内的知名模型，发现所有最先进的LLMs在玩最优扑克时表现不佳。然而，经过微调后，这些模型显示出显著的改进。我们通过让不同得分的模型相互竞争来验证PokerBench，证明在PokerBench上得分更高的模型在实际扑克游戏中具有更高的胜率。通过我们微调后的模型与GPT-4之间的游戏，我们还发现了简单监督微调在学习最优游戏策略方面的局限性，表明需要更先进的方法来有效训练语言模型在游戏中表现出色。因此，PokerBench提供了一个独特的基准，用于快速可靠地评估LLMs的扑克游戏能力，并作为一个全面的基准来研究LLMs在复杂游戏场景中的进展。数据集和代码将在以下网址提供：https://github.com/pokerllm/pokerbench。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08328) | [arXiv](https://arxiv.org/abs/2501.08328)



---

### 8. 大型语言模型作为非结构化文本数据评判者的潜力与风险

**原文标题：** Potential and Perils of Large Language Models as Judges of Unstructured
  Textual Data

**摘要：**
大型语言模型（LLMs）的快速发展在处理和总结非结构化文本数据方面展现了显著的能力。这对分析丰富的开放式数据集（如调查反馈）具有重要意义，LLMs有望高效提炼关键主题和情感。然而，随着组织越来越多地依赖这些强大的AI系统来理解文本反馈，一个关键问题随之而来：我们能否信任LLMs准确反映这些基于文本的数据集中的观点？尽管LLMs在生成类似人类的总结方面表现出色，但其输出可能无意中偏离原始反馈的真实内容。LLM生成的输出与数据中实际主题之间的差异可能导致决策失误，对组织产生深远影响。本研究探讨了LLMs作为评判模型评估其他LLMs生成总结的主题一致性的有效性。我们使用Anthropic Claude模型从开放式调查反馈中生成主题总结，并以亚马逊的Titan Express、Nova Pro和Meta的Llama作为LLM评判者。通过Cohen's kappa、Spearman's rho和Krippendorff's alpha等方法，将LLM作为评判者的方法与人类评估进行比较，验证了其作为传统以人为中心评估方法的可扩展替代方案。我们的研究结果表明，尽管LLMs作为评判者提供了与人类评估者相当的可扩展解决方案，但人类在检测细微、特定于上下文的细微差别方面可能仍具有优势。本研究为AI辅助文本分析领域的知识体系做出了贡献。我们讨论了局限性，并为未来研究提供了建议，强调在跨不同上下文和用例推广LLM评判模型时需要谨慎考虑。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08167) | [arXiv](https://arxiv.org/abs/2501.08167)



---

### 9. HALoGEN：大型语言模型的幻觉及其发现之处

**原文标题：** HALoGEN: Fantastic LLM Hallucinations and Where to Find Them

**摘要：**
尽管生成式大型语言模型（LLMs）在生成高质量和流畅文本方面表现出色，但它们也会产生幻觉：即与既定世界知识或提供的输入上下文不符的陈述。然而，测量幻觉可能具有挑战性，因为让人类即时验证模型生成既昂贵又耗时。在本研究中，我们发布了HALoGEN，一个全面的幻觉基准，包括：（1）10,923个涵盖九个领域的生成模型提示，包括编程、科学归因和摘要等；（2）每个用例的自动高精度验证器，将LLM生成分解为原子单元，并根据高质量知识源验证每个单元。我们使用此框架评估了来自14个语言模型的约150,000次生成，发现即使表现最佳的模型也充满了幻觉（有时高达86%的生成原子事实，具体取决于领域）。我们进一步定义了一种新的LLM幻觉错误分类，基于它们是否可能源于训练数据的错误回忆（A类错误）、训练数据中的错误知识（B类错误）或虚构（C类错误）。我们希望我们的框架为系统研究生成模型为何产生幻觉提供基础，并推动可信赖的大型语言模型的发展。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.08292) | [arXiv](https://arxiv.org/abs/2501.08292)



---

### 10. Tarsier2：从详细视频描述到全面视频理解的大型视觉语言模型进展

**原文标题：** Tarsier2: Advancing Large Vision-Language Models from Detailed Video
  Description to Comprehensive Video Understanding

**摘要：**
我们介绍了Tarsier2，这是一种最先进的大型视觉语言模型（LVLM），旨在生成详细且准确的视频描述，同时展现出卓越的通用视频理解能力。Tarsier2通过三个关键升级实现了显著进展：（1）将预训练数据从1100万扩展到4000万视频-文本对，丰富了数据量和多样性；（2）在监督微调期间进行细粒度的时间对齐；（3）使用基于模型的采样自动构建偏好数据，并应用DPO训练进行优化。大量实验表明，Tarsier2-7B在详细视频描述任务中始终优于领先的专有模型，包括GPT-4o和Gemini 1.5 Pro。在DREAM-1K基准测试中，Tarsier2-7B的F1分数比GPT-4o提高了2.8%，比Gemini-1.5-Pro提高了5.8%。在人类并行评估中，Tarsier2-7B的表现优势比GPT-4o高出8.6%，比Gemini-1.5-Pro高出24.9%。Tarsier2-7B还在15个公共基准测试中创下了新的最先进结果，涵盖了视频问答、视频定位、幻觉测试和具身问答等任务，展示了其作为强大通用视觉语言模型的多功能性。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.07888) | [arXiv](https://arxiv.org/abs/2501.07888)



---


## 🔍 关键词云图
![关键词云图](images/keywords_wordcloud.png)

## 📈 近期论文趋势
![论文趋势](images/daily_papers.png)

## 🎙️ 语音播报
- [收听今日论文解读](audio/2025-01-15_daily_papers.mp3)

## 📱 订阅渠道
- GitHub: [hf-daily-paper-newsletter-chinese](https://github.com/2404589803/hf-daily-paper-newsletter-chinese)