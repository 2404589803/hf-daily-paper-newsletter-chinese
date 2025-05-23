
# <img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png" width="30"/> Hugging Face 2025-01-14 论文日报

## 📊 今日论文统计
- 总论文数：9
- 热门领域：LLM, Transformer, Audio, GPT

## 📝 论文详情


### 1. 数学推理中过程奖励模型开发的启示

**原文标题：** The Lessons of Developing Process Reward Models in Mathematical
  Reasoning

**摘要：**
过程奖励模型（PRMs）作为一种有前景的方法，用于大型语言模型（LLMs）数学推理中的过程监督，旨在识别和缓解推理过程中的中间错误。然而，开发有效的PRMs面临重大挑战，特别是在数据注释和评估方法方面。本文通过大量实验证明，与LLM作为评判者和人工注释方法相比，常用的基于蒙特卡罗（MC）估计的PRMs数据合成通常表现较差且泛化能力不足。MC估计依赖于完成模型来评估当前步骤的正确性，导致步骤验证不准确。此外，我们发现了传统Best-of-N（BoN）评估策略在PRMs中的潜在偏差：（1）不可靠的策略模型生成的响应虽然答案正确但过程有缺陷，导致BoN评估标准与PRMs的过程验证目标不一致。（2）PRMs对此类响应的容忍导致BoN评分虚高。（3）现有PRMs在最终答案步骤上集中了大量最低分，揭示了BoN优化PRMs从过程评估向结果评估的转变。为解决这些挑战，我们开发了一种共识过滤机制，有效整合了MC估计与LLM作为评判者，并提倡结合响应级和步骤级指标的更全面评估框架。基于这些机制，我们在BoN评估和逐步错误识别任务中显著提高了模型性能和数据效率。最后，我们发布了一种新的最先进的PRM，其性能优于现有的开源替代方案，并为未来构建过程监督模型的研究提供了实用指南。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.07301) | [arXiv](https://arxiv.org/abs/2501.07301)



---

### 2. 张量积注意力机制：一切你所需要的

**原文标题：** Tensor Product Attention Is All You Need

**摘要：**
扩展语言模型以处理更长的输入序列通常需要大量的键值（KV）缓存，导致推理过程中内存开销显著增加。本文提出了一种新颖的注意力机制——张量积注意力（Tensor Product Attention, TPA），该机制利用张量分解来紧凑地表示查询、键和值，从而在推理时显著缩小KV缓存的大小。通过将这些表示分解为上下文低秩分量（上下文分解）并与RoPE无缝集成，TPA在提高模型质量的同时实现了内存效率的提升。基于TPA，我们引入了一种新的序列建模模型架构——张量积注意力变换器（Tensor ProducT ATTenTion Transformer, T6）。通过对语言建模任务进行广泛的实证评估，我们证明T6在包括困惑度和一系列著名评估基准在内的各种指标上均优于标准Transformer基线模型，包括MHA、MQA、GQA和MLA。值得注意的是，TPA的内存效率使得在固定资源约束下能够处理显著更长的序列，解决了现代语言模型中的一个关键可扩展性挑战。代码可在https://github.com/tensorgi/T6获取。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.06425) | [arXiv](https://arxiv.org/abs/2501.06425)



---

### 3. VideoAuteur：迈向长篇叙事视频生成

**原文标题：** VideoAuteur: Towards Long Narrative Video Generation

**摘要：**
最近的视频生成模型在生成持续数秒的高质量视频片段方面显示出令人瞩目的成果。然而，这些模型在生成长序列以传达清晰且信息丰富的事件方面面临挑战，限制了其支持连贯叙事的能力。本文提出了一个大规模烹饪视频数据集，旨在推动烹饪领域的长篇叙事生成。我们分别使用最先进的视觉-语言模型（VLMs）和视频生成模型验证了所提出数据集在视觉保真度和文本字幕准确性方面的质量。我们进一步引入了一个长篇叙事视频导演，以增强生成视频的视觉和语义连贯性，并强调对齐视觉嵌入在提高整体视频质量中的作用。我们的方法在生成视觉细节丰富且语义对齐的关键帧方面展示了显著改进，这得益于在视频生成过程中整合文本和图像嵌入的微调技术。项目页面：https://videoauteur.github.io/

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.06173) | [arXiv](https://arxiv.org/abs/2501.06173)



---

### 4. Transformer^2：自适应大语言模型

**原文标题：** Transformer^2: Self-adaptive LLMs

**摘要：**
自适应大语言模型（LLMs）旨在解决传统微调方法所面临的挑战，这些方法通常计算密集且在处理多样化任务时能力较为静态。我们引入了\implname，这是一种新颖的自适应框架，通过选择性地仅调整权重矩阵的单一组件，实时适应LLMs以应对未见过的任务。在推理过程中，\implname采用两阶段机制：首先，调度系统识别任务属性，然后使用强化学习训练的任务特定“专家”向量动态混合，以获得针对输入提示的目标行为。我们的方法在参数更少、效率更高的情况下，优于诸如LoRA等普遍采用的方法。\implname展示了在不同LLM架构和模态（包括视觉语言任务）中的多功能性。\implname代表了一个重大飞跃，为增强LLMs的适应性和任务特定性能提供了一个可扩展、高效的解决方案，为真正动态、自组织的AI系统铺平了道路。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.06252) | [arXiv](https://arxiv.org/abs/2501.06252)



---

### 5. WebWalker：大语言模型在网页遍历中的基准测试

**原文标题：** WebWalker: Benchmarking LLMs in Web Traversal

**摘要：**
检索增强生成（RAG）在开放领域问答任务中表现出色。然而，传统搜索引擎可能检索到浅层内容，限制了大语言模型（LLMs）处理复杂、多层次信息的能力。为解决这一问题，我们引入了WebWalkerQA，这是一个旨在评估LLMs执行网页遍历能力的基准测试。它评估LLMs遍历网站子页面以系统提取高质量数据的能力。我们提出了WebWalker，这是一个多代理框架，通过探索-批评范式模拟人类网页导航。大量实验结果表明，WebWalkerQA具有挑战性，并通过现实场景中的横向和纵向整合展示了RAG与WebWalker结合的有效性。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.07572) | [arXiv](https://arxiv.org/abs/2501.07572)



---

### 6. O1复制之旅——第三部分：医学推理中的推理时间扩展

**原文标题：** O1 Replication Journey -- Part 3: Inference-time Scaling for Medical
  Reasoning

**摘要：**
基于我们之前对O1复制的研究（第一部分：旅程学习[Qin等，2024]和第二部分：蒸馏[Huang等，2024]），本研究探讨了在大型语言模型（LLMs）中推理时间扩展在医学推理任务中的潜力，范围从诊断决策到治疗计划。通过对不同复杂度的医学基准（MedQA、Medbullets和JAMA临床挑战）进行广泛实验，我们的研究揭示了几个关键发现：（1）增加推理时间确实能提高性能。在仅有500个样本的训练集下，我们的模型实现了6%-11%的显著性能提升。（2）任务复杂度与所需推理链的长度直接相关，证实了对于具有挑战性的问题，扩展思维过程的必要性。（3）我们的模型生成的鉴别诊断遵循假设-演绎法的原则，生成一系列可能解释患者症状的潜在条件，并通过评估证据系统地缩小这些可能性。这些发现展示了推理时间扩展与旅程学习在提升LLMs现实世界临床推理能力方面的有希望的协同作用。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.06458) | [arXiv](https://arxiv.org/abs/2501.06458)



---

### 7. MinMo：用于无缝语音交互的多模态大语言模型

**原文标题：** MinMo: A Multimodal Large Language Model for Seamless Voice Interaction

**摘要：**
近年来，大语言模型（LLMs）和多模态语音-文本模型的进展为无缝语音交互奠定了基础，使得实时、自然且类人的对话成为可能。以往的语音交互模型可分为原生模型和对齐模型。原生模型在一个框架内集成语音和文本处理，但面临序列长度不一致和预训练不足等问题。对齐模型则保持文本LLM的能力，但通常受限于小数据集和狭窄的语音任务范围。在本研究中，我们提出了MinMo，一个拥有约80亿参数的多模态大语言模型，旨在实现无缝语音交互。我们解决了以往对齐多模态模型的主要局限。通过在140万小时的多样化语音数据和广泛的语音任务上进行多阶段训练，包括语音到文本对齐、文本到语音对齐、语音到语音对齐以及双工交互对齐，MinMo在语音理解和生成的多个基准测试中达到了最先进的性能，同时保持了文本LLM的能力，并支持全双工对话，即用户与系统之间的双向同时通信。此外，我们提出了一种新颖且简单的语音解码器，在语音生成方面优于之前的模型。MinMo增强的指令跟随能力支持基于用户指令控制语音生成，包括情感、方言和语速等多种细微差别，并能模仿特定声音。对于MinMo，语音到文本的延迟约为100毫秒，全双工延迟理论约为600毫秒，实际约为800毫秒。MinMo项目网页为https://funaudiollm.github.io/minmo，代码和模型将很快发布。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.06282) | [arXiv](https://arxiv.org/abs/2501.06282)



---

### 8. ChemAgent：大语言模型中的自更新库提升化学推理能力

**原文标题：** ChemAgent: Self-updating Library in Large Language Models Improves
  Chemical Reasoning

**摘要：**
化学推理通常涉及复杂、多步骤的过程，需要精确的计算，其中即使微小的错误也可能导致级联失败。此外，大语言模型（LLMs）在处理特定领域的公式、准确执行推理步骤以及有效整合代码时，面临诸多困难。为了解决这些挑战，我们提出了ChemAgent，这是一个通过动态自更新库来提升LLMs性能的新框架。该库通过将化学任务分解为子任务，并将这些子任务编译成一个结构化集合来开发，以便在未来的查询中参考。然后，当遇到新问题时，ChemAgent从库中检索并精炼相关信息，我们称之为记忆，从而促进有效的任务分解和解决方案的生成。我们的方法设计了三种类型的记忆和一个库增强的推理组件，使LLMs能够通过经验不断改进。在SciBench的四个化学推理数据集上的实验结果表明，ChemAgent实现了高达46%（GPT-4）的性能提升，显著优于现有方法。我们的研究结果表明，未来在药物发现和材料科学等任务中具有巨大的应用潜力。我们的代码可以在https://github.com/gersteinlab/chemagent找到。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.06590) | [arXiv](https://arxiv.org/abs/2501.06590)



---

### 9. 三维中的非常见物体

**原文标题：** UnCommon Objects in 3D

**摘要：**
我们介绍了三维中的非常见物体（Uncommon Objects in 3D，简称uCO3D），这是一个新的以物体为中心的数据集，专为三维深度学习和三维生成人工智能设计。uCO3D是目前公开可用的最大规模的高分辨率视频集合，这些视频带有三维注释，确保了360度全方位覆盖。与MVImgNet和CO3Dv2相比，uCO3D在多样性上显著提升，涵盖了超过1,000个物体类别。由于对收集的视频和三维注释进行了广泛的质量检查，uCO3D的质量也更高。与类似的数据集一样，uCO3D包含三维相机姿态、深度图和稀疏点云的注释。此外，每个物体都配备了一个描述和一个三维高斯溅射重建。我们在MVImgNet、CO3Dv2和uCO3D上训练了几个大型三维模型，并使用后者获得了更优的结果，这表明uCO3D更适合学习应用。

**论文链接：** [HuggingFace](https://huggingface.co/papers/2501.07574) | [arXiv](https://arxiv.org/abs/2501.07574)



---


## 🔍 关键词云图
![关键词云图](images/keywords_wordcloud.png)

## 📈 近期论文趋势
![论文趋势](images/daily_papers.png)

## 🎙️ 语音播报
- [收听今日论文解读](audio/2025-01-14_daily_papers.mp3)

## 📱 订阅渠道
- GitHub: [hf-daily-paper-newsletter-chinese](https://github.com/2404589803/hf-daily-paper-newsletter-chinese)