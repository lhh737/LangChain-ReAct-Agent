# Per-Question Chunk Recall 诊断报告

**生成时间**: 2026-06-21 13:46  
**数据集**: `rag_eval_20.jsonl` (16 answerable questions)  
**检索策略**: `hybrid_score` (BM25 45% + Reranker 25% + Keyword 20% + Metadata 10%)  
**k 值**: [1, 3, 5, 10, 20]

---

# 1. 逐题详情

## 1. [cross_001_en] Compare the core decompilation approaches of DnD, BTD, and NeuroDeX. What shared technique do all three use, and how do 

**Type**: `comparison` | **Lang**: `EN` | **Expected chunks**: 9

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.0000 |
| 20 | 0.0000 | 0.2222 |

**Expected sources**: DnD, all-Decompiling+x86, NeuroDeX

### Expected Chunks (9)

### 8d4c6565f46d91f8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 8 |
| chunk_index | 11 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
As such, we can represent the output of a DNN opera-
tor as symbolic expressions of the operator’s input and the
2140    31st USENIX Security Symposium USENIX Association
operator’s parameters.

These expressions contain the math-
ematical semanticsDND needs to recover.

To extract such
symbolic expressions,DND performs customized selective
symbolic execution with the IVs (identiﬁed in Section 5.2.1)
as symbolic variables.

This is because making IVs as sym-
bolicvariablesbringsthetwofollowingbeneﬁts:(1)itenables
DND to symbolize the mathematical expressions of the DNN
operator’s output as symbolic expressions. (2) it allowsDND
to eﬃciently extract the symbolic expressions of a DNN op-
erator’s output by only executing one iteration of each loop,
as discussed inSolution 2of Section 4.

We will explain those
beneﬁts using Figure 3b.
```

### 0fe413d265df53df

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 7 |
| chunk_index | 5 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We will explain how we handle
common compiler optimizations and advanced attributes in
USENIX Association 31st USENIX Security Symposium    2139
I00 I01 I02
I10 I11 I12
I20 I21 I22
F00 F01
F10 F11
O00 O01
O10 O11
Input 1x3x3 Filter 1x2x2 Output 1x2x2
(a) Conv operator
1 void Conv(PTR ∗ input, PTR ∗ filter, PTR ∗ output){
2 for(i=0;i<2;i++) // output width index
3 for(j=0;j<2;j++) // output length index
4 for(u=0;u<2;u++) // filter width index
5 for(v=0;v<2;v++) // filter length index
6 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
7 }
(b) Simplifed decompiled code ofConv
1 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
(c) Extracted symbolic expression ofConv
1 addr: output[i][j]
2 expr: Sum( element =Mul(input[i+u][j+v],
3 filter[u][v]),
4 index =(u, v))
5 IVs: (u, init=0,inc=1,count=2)
6 (v, init=0,inc=1,count=2)
7 (i, init=0,inc=1,count=2)
8 (j, init=0,inc=1,count=2)
(d) Generated operator summary
Figure 3: Operator summary generation ofConv
Sections 5.2.4 and 5.4.3, respectively.
5.2.1 Loop Analysis
The main goal of loop analysis is to identify the information
on the basic induction variable (IV), or informally loop index
variable of each loop in a DNN operator.
```

### 16dc5ceb2dad79e0

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how to identify IVs using the
aforementioned three properties by symbolically executing
each DNN operator from its entry point to its exit point (Line
2,16-17).

Leveragingtheproperty(i), DND symbolizesevery
general register initialized by a constant in the loop’s entry
block (Line 10-12).
```

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### be1c6ddebe8e6fc5

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 3 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Some operators are too costly for symbolic exe-
cution to analyze.

We use taint analysis to keep only tainted
sub-traces for more expensive symbolic execution to ana-
lyze (R3), as noted in Sec. 4.3.1.

BTD is an end-to-end, fully
automated DNN decompiler (R4).

BTD produces model spec-
iﬁcations that behave identically to original models, whose
focus and addressed challenges are distinct from C/C++ de-
compilation.

BTD does not guarantee 100% correct outputs.

In Sec. 5, we discuss procedures users can follow to ﬁx errors.

Dimensions and parameters conﬁgure DNN operators.

We
show representative cases in Fig. 3(b).

Type I operators, in-
cluding activation functions like ReLU and element-wise
arithmetic operators, do not ship with parameters; recovering
their dimensions is trivial, as clariﬁed in the caption of Fig. 3.

Type II and III operators require dimensions or parameters,
such as Pooling’s stride S and kernel size K.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### 2f2cb9ddcb1914fa

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute recovery, where it leverages dynamic anal-
ysis and code semantic understanding from LLMs to support
compatibility with various types of models.

Dynamic analysis
aims to monitor the runtime information of operator functions.

Dynamic analysis in NeuroDeX requires only trivial input that
satisfies the expected input format.

This is due to the fact
that any input can guarantee full coverage of the whole DNN
model, and the mathematical dependencies of intermediate
features are fixed.
```

### 03e5ee11ed5284cb

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from DNN exe-
cutables using ghidra.

Inspired by previous works [6], [9], NeuroDeX can identify
the dimensions of operator parameters from disassembled
code in TVM compiler.

NeuroDeX further expands on their
methods, NeuroDeX also extracts the types of operator param-
eters and recover the optimized parameters’ dimensions.
```

### dd6347b07eaca9c2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 11 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The threat model used in our study is consistent with previ-
ous works [7]–[10] and is generally common and practical
in real-world scenarios.

The design of NeuroDeX aims to
highlight security risks of DNN executables and promote the
safe use of DL compilers.

Operator Recovery
DNN 
Executable
Operator Function 
Extraction
Dynamic 
Analysis 
LLM
Operator Type 
Recognition
Operator Attribute 
Recovery
Computational 
Graph Recovery
Model Weights 
Recovery
Model Reconstruction
High-level 
Model
Fig. 3: Workflow of NeuroDeX
```

### Retrieved Top-20

**#1** — 2eda3aacde4e38c8 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.2-2 | sec=related_work | ci=4

```
However, each of these methods has its limitations.

We summarize the previous works and compare them with
NeuroDeX in Table I.

Libsteal cannot decompile standalone
DNN executables and is unable to handle compilation opti-
mizations.

The accuracy of the models recovered by Libsteal
is relatively low.

The work by Shi et al. only supports x86
architecture and cannot recover models with high accuracy.

DND and Neuroscope do not effectively handle compila-
tion optimizations.

Although BTD consid
```

**#2** — 74238bd6bc7e40c9 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=3

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of Neuro
```

**#3** — 5f882e74e4b278f2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=3

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive 
```

**#4** — cdce554512cc3586 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=0

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implement
```

**#5** — 09693a185e42519d | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-3 | sec=related_work | ci=6

```
Libsteal and Shi et al.’s work
do not guarantee sufficient accuracy; DND relies on symbolic
execution, which incurs significant overhead and limits the size
of supported models; Neuroscope only supports 12 DNN oper-
ators.

More importantly, these methods fail to provide adequate
support for fused operators from compilation optimizations.

Observation2:BTD considers the impact of compilation
optimizations and supports a wider range of operator types.

However, BTD trains machine learning model f
```

**#6** — 6647adfcb117af59 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-3 | sec=related_work | ci=9

```
The decompiler should also have cross-architecture
support capabilities.

C3:Quantized compiled models exhibit
new characteristics different from standard models, involving
quantization scaling factors between integer and float domains.

The decompiler needs to be compatible with these differences.

To address these challenges, we design NeuroDeX to imple-
ment a more comprehensive decompiler for DNN executables.

For C1:We systematically analyze the characteristics of oper-
ators in DL compiler
```

**#7** — e8d85764315c72e4 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-1 | sec=introduction | ci=2

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

N
```

**#8** — 71c795d9bc036eb2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=0

```
In this section, we show the experimental results to answer
the research questions.

A.

RQ1: Correctness
To answer RQ1, we compare NeuroDeX with the SOTA
method BTD, using the models involved in BTD experiments
to demonstrate the performance of NeuroDeX.

TABLE V: TRA and THA of BTD (consistent with Table IV)
on Different Compiler Versions (all value in %)
Metric
TVM O0 TVM O3 GLOW
v0.7 v0.8 v0.9dev v0.7 v0.8 v0.9dev 2020 2021 2022
TRA Avg 80.4 64.43 61.31 70.33 57.67 54.86 72.57 79.36 78.99
TH
```

**#9** — 8b2f1dfb72bfacf4 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.2-2 | sec=related_work | ci=2

```
The general workflow of a
DL compiler involves three steps:frontend processing, which
converts general model representations, such as ONNX [11],
into computational graphs supported by the compiler’s fron-
tend;compilation optimization, applying various optimization
techniques, including high-level optimizations like operator
fusion and constant folding, and low-level optimizations such
TABLE I: Comparison with Existing DNN Decompilers
Works Optimization Cross Arch Quantization
Libsteal [6]# # #

```

**#10** — c88a1a6168cbec88 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.10-10 | sec=results | ci=5

```
The overhead of BTD and
NeuroDeX is shown in Table VI.

For TVM O0, TVM O3 and GLOW, the average time spent
by BTD is about6.79times,2.77times, and12.76times
that of NeuroDeX respectively.

The main time overhead for
NeuroDeX comes from network request to LLM and dynamic
memory monitor.

The time of LLM requests can fluctuate
due to network conditions.

However, in our implementation,
requests to LLM are executed through a single thread.

Using
a multi-threaded approach could easily optimize the
```

**#11** — 6f0f7d6275f908ad | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-10 | sec=results | ci=4

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O
```

**#12** — 735eeb19e5a0fa60 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=1

```
We conduct
experiments on both x86 and aarch64 architectures, we use
Intel Pin [23] for dynamic analysis in the x86 architecture, and
GDB [24] in the aarch64 architecture.

Both Pin and GDB are
automated through Pintool scripts and GDB scripts to finish
tasks like memory dump.

NeuroDeX employs Ghidra [19], a
well-known decompiler in reverse engineering, and the version
is 11.1.2.

NeuroDeX reconstructs DNN executables into high-
level models using PyTorch.

We statistics and compare the
overhea
```

**#13** — cba88a60112f4554 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=1

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the
```

**#14** — de129f4e590e236e | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.13-14 | sec=experiment | ci=28

```
We man-
ually reviewed all “substantial” commits, i.e., commits with
more than 100 LOC changes, and conﬁrmed that they do
not change optimization strategies or binary code generation
that may affect BTD .

Besides, DL compilers heavily use
parallel instruction extensions (e.g., SSE) to speed up model
inference on CPUs.

These extensions have been stable and
unchanged over the long term.

To answer RQ2, we again
underline that BTD ’s essential assumption is that symbolic
constraints extracted fro
```

**#15** — 20ac523f29224b53 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.7-7 | sec=method | ci=6

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the brea
```

**#16** — a1922c6875e023e8 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=14

```
We can use this output to reveal the DNN
model’s details and conduct security analysis, such as model
extraction, adversarial examples discovery, and model hard-
ening.

DND does not recover the algorithm hyper-parameters
(deﬁned in Section 2.1) because they neither aﬀect the infer-
ence process nor are recoverable from the binary.

Assumptions.

DND relies on the following assumptions:
1.

We have access to a DNN binary (e.g., dumping DNN
binaries running on an embedded system).
2.

The control
```

**#17** — fda9347922c4147c | Codellm-Devkit: A Framework for Contextualizing.pdf | p.4-4 | sec=method | ci=7

```
MCQ
B3.

What programming language(s) do you use to build CodeLLM applications?

Open-ended
B4.

What is the target programming language(s) you use CodeLLMs for?

Open-ended
B5.

Does your CodeLLM usecase require additional program analysis?

MCQ
B6.

Do you use any program analysis tools?

MCQ
B7.

On average, how much time do you spend on prototyping and building your Code
LLM use cases?

MCQ
Background of
LLM use cases
B8.

What fraction of the time do you typically spend obtaining program an
```

**#18** — c72c8f73fb291b99 | Codellm-Devkit: A Framework for Contextualizing.pdf | p.3-4 | sec=method | ci=6

```
The overall
distribution is shown in Fig. 5.
0% 5% 10%15%20%JavaPythonGoTypescriptJavascriptCOBOLC#AnsiblePL1ZRNodeJSBashC++.

NetYAMLC
Fig. 5: Target programming languages for LLM-assisted tasks
at IBM.
• Use of program analysis (B5).

All but two participants (R1
and E2) agreed that that they use program analysis in their
code LLM pipeline.

Of the two exceptions, R1 answered that
their use case is surrounding taking LLM output off-the-shelf
whereas E1 works on building an evaluation pipeline 
```

**#19** — 166f2a148d788590 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.14-14 | sec=discussion | ci=0

```
Existing General-Purpose Decompiler Existing general-
purpose decompilers (e.g., Hex-Rays) have the following lim-
itations when dealing with DNN binaries: (1) they do not
recognize vectorized mathematical computations, leading to
decompilation representations containing long loop bodies
and excessive bitwise operations; (2) their decompilation rep-
resentations diﬀer signiﬁcantly depending on the compilers
or ISAs; (3) even with the same compiler and ISAs, DNN
operators of the same type but wit
```

**#20** — 7c20d122b7ceac18 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.9-9 | sec=experiment | ci=0

```
In this section, we evaluate BTD by exploring the following
four research questions (RQs) below:
RQ1 (Comprehensiveness and Correctness): Is BTD com-
prehensive and correct to process all operators used in com-
mon DL models compiled with different compilers and opti-
mization options?

RQ2 (Robustness): Is BTD robust to survive frequent DL
compiler implementation changes?

RQ3 (Extensibility): Can BTD be easily extended to support
new operators and models?

What efforts are needed?

RQ4 (Error 
```

### Missed Chunks (9 — expected but NOT in top-20)

### 8d4c6565f46d91f8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 8 |
| chunk_index | 11 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
As such, we can represent the output of a DNN opera-
tor as symbolic expressions of the operator’s input and the
2140    31st USENIX Security Symposium USENIX Association
operator’s parameters.

These expressions contain the math-
ematical semanticsDND needs to recover.

To extract such
symbolic expressions,DND performs customized selective
symbolic execution with the IVs (identiﬁed in Section 5.2.1)
as symbolic variables.

This is because making IVs as sym-
bolicvariablesbringsthetwofollowingbeneﬁts:(1)itenables
DND to symbolize the mathematical expressions of the DNN
operator’s output as symbolic expressions. (2) it allowsDND
to eﬃciently extract the symbolic expressions of a DNN op-
erator’s output by only executing one iteration of each loop,
as discussed inSolution 2of Section 4.

We will explain those
beneﬁts using Figure 3b.
```

### 0fe413d265df53df

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 7 |
| chunk_index | 5 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We will explain how we handle
common compiler optimizations and advanced attributes in
USENIX Association 31st USENIX Security Symposium    2139
I00 I01 I02
I10 I11 I12
I20 I21 I22
F00 F01
F10 F11
O00 O01
O10 O11
Input 1x3x3 Filter 1x2x2 Output 1x2x2
(a) Conv operator
1 void Conv(PTR ∗ input, PTR ∗ filter, PTR ∗ output){
2 for(i=0;i<2;i++) // output width index
3 for(j=0;j<2;j++) // output length index
4 for(u=0;u<2;u++) // filter width index
5 for(v=0;v<2;v++) // filter length index
6 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
7 }
(b) Simplifed decompiled code ofConv
1 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
(c) Extracted symbolic expression ofConv
1 addr: output[i][j]
2 expr: Sum( element =Mul(input[i+u][j+v],
3 filter[u][v]),
4 index =(u, v))
5 IVs: (u, init=0,inc=1,count=2)
6 (v, init=0,inc=1,count=2)
7 (i, init=0,inc=1,count=2)
8 (j, init=0,inc=1,count=2)
(d) Generated operator summary
Figure 3: Operator summary generation ofConv
Sections 5.2.4 and 5.4.3, respectively.
5.2.1 Loop Analysis
The main goal of loop analysis is to identify the information
on the basic induction variable (IV), or informally loop index
variable of each loop in a DNN operator.
```

### 16dc5ceb2dad79e0

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how to identify IVs using the
aforementioned three properties by symbolically executing
each DNN operator from its entry point to its exit point (Line
2,16-17).

Leveragingtheproperty(i), DND symbolizesevery
general register initialized by a constant in the loop’s entry
block (Line 10-12).
```

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### be1c6ddebe8e6fc5

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 3 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Some operators are too costly for symbolic exe-
cution to analyze.

We use taint analysis to keep only tainted
sub-traces for more expensive symbolic execution to ana-
lyze (R3), as noted in Sec. 4.3.1.

BTD is an end-to-end, fully
automated DNN decompiler (R4).

BTD produces model spec-
iﬁcations that behave identically to original models, whose
focus and addressed challenges are distinct from C/C++ de-
compilation.

BTD does not guarantee 100% correct outputs.

In Sec. 5, we discuss procedures users can follow to ﬁx errors.

Dimensions and parameters conﬁgure DNN operators.

We
show representative cases in Fig. 3(b).

Type I operators, in-
cluding activation functions like ReLU and element-wise
arithmetic operators, do not ship with parameters; recovering
their dimensions is trivial, as clariﬁed in the caption of Fig. 3.

Type II and III operators require dimensions or parameters,
such as Pooling’s stride S and kernel size K.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### 2f2cb9ddcb1914fa

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute recovery, where it leverages dynamic anal-
ysis and code semantic understanding from LLMs to support
compatibility with various types of models.

Dynamic analysis
aims to monitor the runtime information of operator functions.

Dynamic analysis in NeuroDeX requires only trivial input that
satisfies the expected input format.

This is due to the fact
that any input can guarantee full coverage of the whole DNN
model, and the mathematical dependencies of intermediate
features are fixed.
```

### 03e5ee11ed5284cb

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from DNN exe-
cutables using ghidra.

Inspired by previous works [6], [9], NeuroDeX can identify
the dimensions of operator parameters from disassembled
code in TVM compiler.

NeuroDeX further expands on their
methods, NeuroDeX also extracts the types of operator param-
eters and recover the optimized parameters’ dimensions.
```

### dd6347b07eaca9c2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 11 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The threat model used in our study is consistent with previ-
ous works [7]–[10] and is generally common and practical
in real-world scenarios.

The design of NeuroDeX aims to
highlight security risks of DNN executables and promote the
safe use of DL compilers.

Operator Recovery
DNN 
Executable
Operator Function 
Extraction
Dynamic 
Analysis 
LLM
Operator Type 
Recognition
Operator Attribute 
Recovery
Computational 
Graph Recovery
Model Weights 
Recovery
Model Reconstruction
High-level 
Model
Fig. 3: Workflow of NeuroDeX
```

### False Positives (20 — in top-20 but NOT expected)

### 2eda3aacde4e38c8

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
However, each of these methods has its limitations.

We summarize the previous works and compare them with
NeuroDeX in Table I.

Libsteal cannot decompile standalone
DNN executables and is unable to handle compilation opti-
mizations.

The accuracy of the models recovered by Libsteal
is relatively low.

The work by Shi et al. only supports x86
architecture and cannot recover models with high accuracy.

DND and Neuroscope do not effectively handle compila-
tion optimizations.

Although BTD considers the impact of
compilation optimizations, it only supports x86 architecture.

Moreover, all previous works overlook models compiled with
quantization, which limits the applicability of these methods
in practical scenarios.

Previous DNN executables decompilers
have their own limitations and existing decompilers struggle
tosimultaneously address compilation optimizations, sup-
port different architectures, and accommodate quantized
compiled models.

Beyond the aforementioned discussion, we conduct a sys-
tematic analysis of operator type recognition, the critical
step in decompilation pipeline.
```

### 74238bd6bc7e40c9

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of NeuroDeX
with BTD and analyze the underlying reasons.

We choose four models: EfficientNet, ResNet18, Incep-
tionv1 and ShuffleNetv2.

These models cover a range of
weights size and topological complexities, enabling a compre-
hensive evaluation of the overhead associated with BTD and
NeuroDeX.

The model reconstruction strategies for NeuroDeX
and BTD are identical.

Therefore, we only compare the time
associated with operator type recognition and operator attribute
recovery processes.
```

### 5f882e74e4b278f2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive experiments across different optimization
levels and different compiler versions, which demonstrates its
effectiveness.

Overall, BTD is currently the SOTA method
available.

As shown in Table III, to ease of comparison, we evaluate
NeuroDeX on six different DL models, comprising a total of
54 DNN executables (varying in compiler, optimization level,
and compiler version) that are analyzed in BTD.
```

### cdce554512cc3586

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implementation & Environment
We implement NeuroDeX with about 8K LOC Python code
and about 1K LOC C++ code.

In our experiments, we select
GPT-4o [20] for its superior performance in code understand-
ing [21], [22] and the large size (128K) of context window,
which is sufficient to cover the operator functions.
```

### 09693a185e42519d

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Libsteal and Shi et al.’s work
do not guarantee sufficient accuracy; DND relies on symbolic
execution, which incurs significant overhead and limits the size
of supported models; Neuroscope only supports 12 DNN oper-
ators.

More importantly, these methods fail to provide adequate
support for fused operators from compilation optimizations.

Observation2:BTD considers the impact of compilation
optimizations and supports a wider range of operator types.

However, BTD trains machine learning model for each com-
piler version to make predictions.

This approach relies heavily
on training data and treats the compiler version as prior
knowledge, which limits its scalability in real world scenario.

Moreover, we find that about 57.9% of the training data in
TVM and 18.3% in GLOW appear in the test dataset, further
undermining the effectiveness of the method.
```

### 6647adfcb117af59

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 9 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The decompiler should also have cross-architecture
support capabilities.

C3:Quantized compiled models exhibit
new characteristics different from standard models, involving
quantization scaling factors between integer and float domains.

The decompiler needs to be compatible with these differences.

To address these challenges, we design NeuroDeX to imple-
ment a more comprehensive decompiler for DNN executables.

For C1:We systematically analyze the characteristics of oper-
ators in DL compilers and design a progressive operator type
recognition strategy.

NeuroDeX leverages dynamic analysis
and code semantic understanding from LLMs to support com-
patibility with various types of operators and fused operators.

For C2:Based on the operator type recognition method, we
subsequently implement operator attribute recovery and model
reconstruction, forming a complete decompilation pipeline
compatibility with various types of different models.

The
core technology of NeuroDeX is hardware-platform indepen-
dent, ensuring its cross-architecture support capabilities.
```

### e8d85764315c72e4

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

NeuroDeX features an accurate operator
type recognition and operator attribute recovery mechanism
that does not rely on prior knowledge such as compiler ver-
sions or training data.

NeuroDeX can accurately recover fused
operators and its core components do not depend on resource-
intensive analysis techniques like symbolic execution, allowing
for rapid and efficient analysis.

Furthermore, NeuroDeX is
extendable to different architectures, different DL compilers,
and quantized models.
```

### 71c795d9bc036eb2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In this section, we show the experimental results to answer
the research questions.

A.

RQ1: Correctness
To answer RQ1, we compare NeuroDeX with the SOTA
method BTD, using the models involved in BTD experiments
to demonstrate the performance of NeuroDeX.

TABLE V: TRA and THA of BTD (consistent with Table IV)
on Different Compiler Versions (all value in %)
Metric
TVM O0 TVM O3 GLOW
v0.7 v0.8 v0.9dev v0.7 v0.8 v0.9dev 2020 2021 2022
TRA Avg 80.4 64.43 61.31 70.33 57.67 54.86 72.57 79.36 78.99
THA Avg 96.42 94.57 98.50 98.04 97.05 97.10 97.33 98.48 96.91
We remove the training data that is also on test dataset (op-
erators of the six models in Table IV) and retrain the BTD op-
erator type recognition models following the default settings.

The comparison results of TRA are shown in Table IV.
```

### 8b2f1dfb72bfacf4

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The general workflow of a
DL compiler involves three steps:frontend processing, which
converts general model representations, such as ONNX [11],
into computational graphs supported by the compiler’s fron-
tend;compilation optimization, applying various optimization
techniques, including high-level optimizations like operator
fusion and constant folding, and low-level optimizations such
TABLE I: Comparison with Existing DNN Decompilers
Works Optimization Cross Arch Quantization
Libsteal [6]# # #
Shi et al [9]# # #
DND [7]#  #
Neuroscope [10]#  #
BTD [8] # #
NeuroDeX   
as layout rearrangement;code generation, which generates
executables adapted for the target device’s hardware.

B.

DNN Executables Decompiler
The goal of DNN decompiler is to reverse DNN executables
into identical high-level models.
```

### c88a1a6168cbec88

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 5 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The overhead of BTD and
NeuroDeX is shown in Table VI.

For TVM O0, TVM O3 and GLOW, the average time spent
by BTD is about6.79times,2.77times, and12.76times
that of NeuroDeX respectively.

The main time overhead for
NeuroDeX comes from network request to LLM and dynamic
memory monitor.

The time of LLM requests can fluctuate
due to network conditions.

However, in our implementation,
requests to LLM are executed through a single thread.

Using
a multi-threaded approach could easily optimize the time
overhead.

EfficientNet represents high-capacity and compu-
tationally intensive models, while ShuffleNetv2 serves as an
example of lightweight model.

ResNet18 and InceptionV1 are
further included to encompass a broader range of distinct
architectural designs.

According to our evaluation results, Neu-
roDeX performs better than BTD in time overhead obviously
across all these various models.
```

### 6f0f7d6275f908ad

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW
BTD 676.3 265.0 2904.7 468.7 681.2 2416.3 982.8 705.6 4328.8 152.7 92.8 296.2
NeuroDeX 76.9 122.2 204.5 41.4 127.9 129.2 208.3 288.8 304.7 66.0 80.9 75.4
for fair comparison.

The compiler version for our experiment
is TVM v0.9dev and GLOW 2022.
```

### 735eeb19e5a0fa60

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
We conduct
experiments on both x86 and aarch64 architectures, we use
Intel Pin [23] for dynamic analysis in the x86 architecture, and
GDB [24] in the aarch64 architecture.

Both Pin and GDB are
automated through Pintool scripts and GDB scripts to finish
tasks like memory dump.

NeuroDeX employs Ghidra [19], a
well-known decompiler in reverse engineering, and the version
is 11.1.2.

NeuroDeX reconstructs DNN executables into high-
level models using PyTorch.

We statistics and compare the
overhead of different methods on AMD EPYC 9654 CPU with
60GB RAM.
```

### cba88a60112f4554

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the number
of operator classes, and it’s also the length of the prediction
vector for a single sample.

The average result of TRA and
THA for different compiler versions are shown in Table V.

Although THA may achieve higher results, TRA undoubtedly
provides a more scientific measure of the true effectiveness of
operator recognition.

For instance, prediction-label pair like
[1,0,0,0,0. . .]20 and[0,1,0,0,0. . .] 20 will yield THA with
18/20 = 0.9, but from the operator functional perspective, it is
entirely incorrect.
```

### de129f4e590e236e

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 13 |
| page_end | 14 |
| chunk_index | 28 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We man-
ually reviewed all “substantial” commits, i.e., commits with
more than 100 LOC changes, and conﬁrmed that they do
not change optimization strategies or binary code generation
that may affect BTD .

Besides, DL compilers heavily use
parallel instruction extensions (e.g., SSE) to speed up model
inference on CPUs.

These extensions have been stable and
unchanged over the long term.

To answer RQ2, we again
underline that BTD ’s essential assumption is that symbolic
constraints extracted from each DNN operator’s assembly
function should be invariant across compilers and optimiza-
tions.

Other features, such as function signatures, operator
fusion, and optimization strategies, are independent ofBTD’s
core techniques and are also unlikely to be largely changed in
the near future.

Answer to RQ2: BTD is robust enough against changes
in current and prior versions of DL compilers.
```

### 20ac523f29224b53

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 6 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the break edges (denoting the edges in CFG that
jump out of the current loop).
```

### a1922c6875e023e8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 14 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We can use this output to reveal the DNN
model’s details and conduct security analysis, such as model
extraction, adversarial examples discovery, and model hard-
ening.

DND does not recover the algorithm hyper-parameters
(deﬁned in Section 2.1) because they neither aﬀect the infer-
ence process nor are recoverable from the binary.

Assumptions.

DND relies on the following assumptions:
1.

We have access to a DNN binary (e.g., dumping DNN
binaries running on an embedded system).
2.

The control-ﬂow graph (CFG) recovery is reliable.

Our
evaluation shows that the recovered CFGs, though impre-
cise, are suﬃcient enough for our decompilation purpose.
3.

DNN compilers do not use obfuscation technique.
```

### fda9347922c4147c

| Field | Value |
|-------|-------|
| source_file | Codellm-Devkit: A Framework for Contextualizing.pdf |
| section | method |
| section_title | II. MOTIVATION |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 7 |
| paper_id | Codellm-Devkit: A Framework for Contextualizing |

```
MCQ
B3.

What programming language(s) do you use to build CodeLLM applications?

Open-ended
B4.

What is the target programming language(s) you use CodeLLMs for?

Open-ended
B5.

Does your CodeLLM usecase require additional program analysis?

MCQ
B6.

Do you use any program analysis tools?

MCQ
B7.

On average, how much time do you spend on prototyping and building your Code
LLM use cases?

MCQ
Background of
LLM use cases
B8.

What fraction of the time do you typically spend obtaining program analysis insights
for your projects?

MCQ
C1.

What are the pros/cons of the tool(s) used?

Please explain.

Open-ended
C2.

What features or capabilities do you find missing in current program analysis tools?

Open-ended
Need for Better/Easier
Program Analysis Tools
C3.

How effective are your current tools when working with new programming languages
or applications?

Likert Scale
C4.

How would you rate the learning curve of your program analysis tools when applied
to new languages or applications?
```

### c72c8f73fb291b99

| Field | Value |
|-------|-------|
| source_file | Codellm-Devkit: A Framework for Contextualizing.pdf |
| section | method |
| section_title | II. MOTIVATION |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 6 |
| paper_id | Codellm-Devkit: A Framework for Contextualizing |

```
The overall
distribution is shown in Fig. 5.
0% 5% 10%15%20%JavaPythonGoTypescriptJavascriptCOBOLC#AnsiblePL1ZRNodeJSBashC++.

NetYAMLC
Fig. 5: Target programming languages for LLM-assisted tasks
at IBM.
• Use of program analysis (B5).

All but two participants (R1
and E2) agreed that that they use program analysis in their
code LLM pipeline.

Of the two exceptions, R1 answered that
their use case is surrounding taking LLM output off-the-shelf
whereas E1 works on building an evaluation pipeline for code
LLM (which does not warrant additional program analysis).
• Program analysis tool use (B6).

Of the participants that
answered affirmatively to the above, more than 60% of them
TABLE II: Developer survey questions.

Category Question Format
A1.

What is your job title?

Open-ended
Role and Experience
A2.

How many years of software engineering experience do you have?

Numeric
B1.

How would you rate your experience with Code LLMs ?

MCQ
B2.

What are your primary use cases for Code LLMs?
```

### 166f2a148d788590

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | discussion |
| section_title | 9 Discussion and Limitations |
| page_start | 14 |
| page_end | 14 |
| chunk_index | 0 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Existing General-Purpose Decompiler Existing general-
purpose decompilers (e.g., Hex-Rays) have the following lim-
itations when dealing with DNN binaries: (1) they do not
recognize vectorized mathematical computations, leading to
decompilation representations containing long loop bodies
and excessive bitwise operations; (2) their decompilation rep-
resentations diﬀer signiﬁcantly depending on the compilers
or ISAs; (3) even with the same compiler and ISAs, DNN
operators of the same type but with diﬀerent attributes have
diﬀerent decompilation representations, because they arespe-
cialized.

We demonstrate these limitations in Appendix C.

These limitations hinder using simple pattern matching to
recover the DNN high-level representation.

Correctness of the Recovered CFG and Binary Code.

As
other decompilation works [19,56,57],DND assumes that
the recovered CFG provided by the disassembler is reliable.
```

### 7c20d122b7ceac18

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 0 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In this section, we evaluate BTD by exploring the following
four research questions (RQs) below:
RQ1 (Comprehensiveness and Correctness): Is BTD com-
prehensive and correct to process all operators used in com-
mon DL models compiled with different compilers and opti-
mization options?

RQ2 (Robustness): Is BTD robust to survive frequent DL
compiler implementation changes?

RQ3 (Extensibility): Can BTD be easily extended to support
new operators and models?

What efforts are needed?

RQ4 (Error Fixing): How does BTD handle decompilation
errors?

We evaluated BTD with seven real-world CV models and
an NLP model compiled with eight versions of compilers
to provide a comprehensive evaluation.

BTD can produce
correct model speciﬁcations on 59 of 65 DNN executables,
and experienced users can quickly ﬁx 3 of 6 remaining errors.

Nevertheless, we recognize that some errors cannot be easily
ﬁxed by normal users.
```

---

## 2. [single_002_en] What is BTD's three-step recovery method, and how does it classify DNN operators?

**Type**: `method` | **Lang**: `EN` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.0000 |
| 20 | 0.2000 | 0.4000 |

**Expected sources**: all-Decompiling+x86

### Expected Chunks (5)

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### be1c6ddebe8e6fc5

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 3 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Some operators are too costly for symbolic exe-
cution to analyze.

We use taint analysis to keep only tainted
sub-traces for more expensive symbolic execution to ana-
lyze (R3), as noted in Sec. 4.3.1.

BTD is an end-to-end, fully
automated DNN decompiler (R4).

BTD produces model spec-
iﬁcations that behave identically to original models, whose
focus and addressed challenges are distinct from C/C++ de-
compilation.

BTD does not guarantee 100% correct outputs.

In Sec. 5, we discuss procedures users can follow to ﬁx errors.

Dimensions and parameters conﬁgure DNN operators.

We
show representative cases in Fig. 3(b).

Type I operators, in-
cluding activation functions like ReLU and element-wise
arithmetic operators, do not ship with parameters; recovering
their dimensions is trivial, as clariﬁed in the caption of Fig. 3.

Type II and III operators require dimensions or parameters,
such as Pooling’s stride S and kernel size K.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### c54826ab77483b01

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 4 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In addition to
simple arithmetic operators, BiasAdd involves biasB, as extra
parameters.

Type IV operators require both parameters and di-
mensions.

These operators form most DNN models.

Sec. 7.1
empirically demonstrates “comprehensivness” of our study.

BTD recovers dimensions/parameters of all DNN opera-
tors used by CV models in ONNX Zoo (see Sec. 7.1).

Due to
limited space, Sec. 4.3 only discusses decompiling the most
challenging operator, Conv.

The core techniques explained in
Sec. 4.3 are utilized to decompile other DNN operators.

How-
ever, other operators may use different (but simpler) patterns.

Appendix C lists other operator patterns.

We further discuss
the extensibility of BTD in Sec. 7.3.

Disassembling and Function Recovery.

BTD targets 64-bit
x86 executables.

Cross-platform support is discussed in Sec. 8.

BTD supports stripped executables without symbol or debug
information.
```

### cd0df6f97d9e32fe

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 6 |
| chunk_index | 7 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We discuss decompiling
NNFusion-emitted executables in Sec. 4.4.
4.1 DNN Operator Recovery
As introduced in Sec. 2, one or a few fused DNN operators are
compiled into an assembly function.

We train a neural model
to map assembly functions to DNN operators.

Recent works
perform representation learning by treating x86 opcodes as
natural language tokens [28,29,59,81,108].

These works help
comprehend x86 assembly code and assist downstream tasks
like matching similar code.

Instead of deﬁning explicit pat-
terns over x86 opcodes to infer DNN operators (which could
be tedious and need manual efforts), we use representation
learning and treat x86 opcodes as language tokens.

Atomic OPs.

Launching representation learning directly over
x86 opcodes syntax can result in poor learning quality.
```

### Retrieved Top-20

**#1** — 5f882e74e4b278f2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=3

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive 
```

**#2** — cdce554512cc3586 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=0

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implement
```

**#3** — 7c20d122b7ceac18 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.9-9 | sec=experiment | ci=0

```
In this section, we evaluate BTD by exploring the following
four research questions (RQs) below:
RQ1 (Comprehensiveness and Correctness): Is BTD com-
prehensive and correct to process all operators used in com-
mon DL models compiled with different compilers and opti-
mization options?

RQ2 (Robustness): Is BTD robust to survive frequent DL
compiler implementation changes?

RQ3 (Extensibility): Can BTD be easily extended to support
new operators and models?

What efforts are needed?

RQ4 (Error 
```

**#4** — 62cf5a5130e8a5fd | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.4-4 | sec=method | ci=3

```
The recovery of optimized parameters’
dimensions can help analyze optimized operators.

Figure 4
is a specific example ofTransformoperator.

The parameters’
dimensions and types can be extracted by scanning the disas-
sembled code.

The dimension of the first parameter is optimized into
[N, C, H, W, c]layout.

NCHWc [1] is a commonly used
inference optimization method, which adapts to hardware
and accelerates inference.

NeuroDeX can recover it into
standard[N, C∗c, H, W]format.

Similarly, the 
```

**#5** — da2e9320264c822e | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.4-5 | sec=method | ci=4

```
The parameters of the function correspond sequentially to the
inputs and outputs of the operator.

Each type operator has
a fixed number of inputs and outputs, and NeuroDeX can
accurately recover parameters’ dimensions.

We validate this
characteristic across both historical and recent TVM versions,
ensuring the generality and robustness of our approach.

B.

Operator Type Recognition
The purpose of operator type recognition is to determine
the specific type of the operator function.

We manuall
```

**#6** — bf1dca8f8840f813 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.7-7 | sec=method | ci=20

```
Quantized compiled methods involves global scale mode and
kl divergence mode.

Scale refers to the scaling factor between
the float domain and int domain during quantized compi-
lation.

The global scale method uses the same scale across
different operators, and does not rely on data calibration.

The
kl divergence method needs data for calibration, resulting in
higher precision.

The weights of quantized compiled models
are in the integer domain, and model inference is in inte-
ger domain as we
```

**#7** — bd30f4fcfe778733 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.1-2 | sec=introduction | ci=3

```
Given a (stripped) executable compiled from a DNN model,
w1w2…mergeable nodes
operator optimizationModelSpecificationComputationGraph Creation
Graph IR &Optimization
Low-Level IR
Hardware-specificOptimization
(Auto) Scheduling& (Auto) TuningCode Gen &OptimizationDNNExecutable(a) DNN compilation pipeline.(b) Sample DNN computation graph.

DNN compiler frontend looks for holisticopt. chances likemergeable nodes, whereas backend explores efficient machinecode foreach operator.

ConvReLU ConvPool
Fi
```

**#8** — 784da26bfe4a09ce | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.11-11 | sec=method | ci=32

```
Forexample,forthe Mul
functioninthe FC operator’ssummary(Line2-3inFigure5b),
DNDidentiﬁesthatthe input[i] istheoutputoftheprevious
DNN operator (i.e., its address range overlaps with previous
DNN operator’s output range), and that theweight[j][i]
is the parameter (i.e., its address range does not overlap with
any previous DNN operator’s output range).
5.4.3 Attributes and Parameters Recovery
In the last step,DND recovers the attributes and parameters
of each DNN operator by leveraging the genera
```

**#9** — 6afe0195be94b982 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.11-11 | sec=results | ci=14

```
Nonetheless, our evaluation indicates that the
operator type recognition accuracy on all TVM operators
reach 99.22%, and it is 97.62% for GLOW, maintaining high
accuracy.

In operator attribute recovery, the errors are very
rare and they are obvious in the decompiled code, such
as kernel size “*0.00591716 (1/169)” should be 13 but is
incorrectly identified as 17.

Therefore, it does not require a
systematic error fix mechanism.

We analyze the causes of
errors in operator type recognition and th
```

**#10** — b2d5ec795a6e003a | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=4

```
Moreover,
we have supplemented our evaluation with six more different
models, aiming to cover more model structures and varying
hyperparameters for same model structure.

Furthermore, we
conduct an additional analysis on 42 BTD unexplored DNN
executables, covering a wider range of compiler versions,
architectures, and quantized models.

All the executables in
our evaluation are stripped.

C.

Evaluation Metrics
We evaluate the effectiveness of NeuroDeX from three
perspectives: operator type reco
```

**#11** **[HIT]** — c54826ab77483b01 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.5-5 | sec=method | ci=4

```
In addition to
simple arithmetic operators, BiasAdd involves biasB, as extra
parameters.

Type IV operators require both parameters and di-
mensions.

These operators form most DNN models.

Sec. 7.1
empirically demonstrates “comprehensivness” of our study.

BTD recovers dimensions/parameters of all DNN opera-
tors used by CV models in ONNX Zoo (see Sec. 7.1).

Due to
limited space, Sec. 4.3 only discusses decompiling the most
challenging operator, Conv.

The core techniques explained in
Sec. 4.3
```

**#12** — 547a3b0f9080d220 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.9-9 | sec=method | ci=1

```
Given a DNN executable, a user ﬁrst disassembles
it (e.g., using IDA-Pro) and recovers all assembly functions.

The user also need to provide a format-valid input of this
executable for use.

Next, as an end-to-end procedure, BTD
predicts compilation provenance and each disassembly func-
tion’s operator type.

BTD then launches the network topology
recovery before conducting symbolic execution and recov-
ering dimensions and parameters for each operator, as ex-
plained in Sec. 4.

Note that at t
```

**#13** — c6bac3be25d235ea | Hardening Deep Neural Network Binaries against ReverseEngine | p.12-12 | sec=experiment | ci=23

```
Fake Operator Insertion ( fi) further lowers the recovery rates
to 47.18% and 3.03% respectively, by inserting fake operators and
causing the random input from BTD to trigger wrong execution
paths.

When all NeuroShield’s obfuscation primitives are applied,
the operator recovery rate is the same as fi, but the attack time
increases by around 3x because cr causes BTD to log and analyze
more instructions.
6.4 Strength of Inserted Control Flow
To demonstrate the resilience of the input-dependent co
```

**#14** — e8d85764315c72e4 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-1 | sec=introduction | ci=2

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

N
```

**#15** — cba88a60112f4554 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=1

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the
```

**#16** — 74238bd6bc7e40c9 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=3

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of Neuro
```

**#17** — 69052d09957be415 | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=9

```
Diff (%) VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 27.90 27.57 34.71 28.59 28.44 28.88 34.24 36.73 35.53 35.72
FlatD 17.43 17.48 18.76 12.91 12.91 12.90 17.04 22/45 21.93 21.94
of Operator functions, which is only related to the Operator
Type recovery, we only evaluate our defense mechanism on
how it can affect the inference of Operator Type of each
reversing-based model extraction attack.

Moreover, Operator-
type recovery is the most essential and fundam
```

**#18** — a56d6a08d27f78a8 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.2-2 | sec=introduction | ci=7

```
In summary, we
contribute the following:
• This paper, for the ﬁrst time1, advocates for reverse engi-
neering DNN executables.

BTD accepts as input (stripped)
executables generated by production DL compilers and out-
puts complete model speciﬁcations.

BTD can be used to aid
in the comprehension, migration, hardening, and exploita-
tion of DNN executables.
• BTD features a three-step approach to recovering high-
level DNN models.

It incorporates various design principles
and techniques to del
```

**#19** — 6f0f7d6275f908ad | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-10 | sec=results | ci=4

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O
```

**#20** — 1abbd1f5f8db7fc2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-3 | sec=related_work | ci=7

```
To avoid the
influence of data leak, we randomly split all the data with
an 8:2 ratio for train dataset and test dataset, and retrain the
model for each compiler version, strictly following the default
settings of BTD.

As illustrated in Figure 1, we have analyzed
BTD’s type recognition accuracy across different compiler
versions.

It is evident that BTD’s method exhibits poor cross-
version support for compilers after avoiding data leak.

Even
within the same version, errors of operator type oc
```

### Missed Chunks (4 — expected but NOT in top-20)

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### be1c6ddebe8e6fc5

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 3 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Some operators are too costly for symbolic exe-
cution to analyze.

We use taint analysis to keep only tainted
sub-traces for more expensive symbolic execution to ana-
lyze (R3), as noted in Sec. 4.3.1.

BTD is an end-to-end, fully
automated DNN decompiler (R4).

BTD produces model spec-
iﬁcations that behave identically to original models, whose
focus and addressed challenges are distinct from C/C++ de-
compilation.

BTD does not guarantee 100% correct outputs.

In Sec. 5, we discuss procedures users can follow to ﬁx errors.

Dimensions and parameters conﬁgure DNN operators.

We
show representative cases in Fig. 3(b).

Type I operators, in-
cluding activation functions like ReLU and element-wise
arithmetic operators, do not ship with parameters; recovering
their dimensions is trivial, as clariﬁed in the caption of Fig. 3.

Type II and III operators require dimensions or parameters,
such as Pooling’s stride S and kernel size K.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### cd0df6f97d9e32fe

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 6 |
| chunk_index | 7 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We discuss decompiling
NNFusion-emitted executables in Sec. 4.4.
4.1 DNN Operator Recovery
As introduced in Sec. 2, one or a few fused DNN operators are
compiled into an assembly function.

We train a neural model
to map assembly functions to DNN operators.

Recent works
perform representation learning by treating x86 opcodes as
natural language tokens [28,29,59,81,108].

These works help
comprehend x86 assembly code and assist downstream tasks
like matching similar code.

Instead of deﬁning explicit pat-
terns over x86 opcodes to infer DNN operators (which could
be tedious and need manual efforts), we use representation
learning and treat x86 opcodes as language tokens.

Atomic OPs.

Launching representation learning directly over
x86 opcodes syntax can result in poor learning quality.
```

### False Positives (19 — in top-20 but NOT expected)

### 5f882e74e4b278f2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive experiments across different optimization
levels and different compiler versions, which demonstrates its
effectiveness.

Overall, BTD is currently the SOTA method
available.

As shown in Table III, to ease of comparison, we evaluate
NeuroDeX on six different DL models, comprising a total of
54 DNN executables (varying in compiler, optimization level,
and compiler version) that are analyzed in BTD.
```

### cdce554512cc3586

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implementation & Environment
We implement NeuroDeX with about 8K LOC Python code
and about 1K LOC C++ code.

In our experiments, we select
GPT-4o [20] for its superior performance in code understand-
ing [21], [22] and the large size (128K) of context window,
which is sufficient to cover the operator functions.
```

### 7c20d122b7ceac18

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 0 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In this section, we evaluate BTD by exploring the following
four research questions (RQs) below:
RQ1 (Comprehensiveness and Correctness): Is BTD com-
prehensive and correct to process all operators used in com-
mon DL models compiled with different compilers and opti-
mization options?

RQ2 (Robustness): Is BTD robust to survive frequent DL
compiler implementation changes?

RQ3 (Extensibility): Can BTD be easily extended to support
new operators and models?

What efforts are needed?

RQ4 (Error Fixing): How does BTD handle decompilation
errors?

We evaluated BTD with seven real-world CV models and
an NLP model compiled with eight versions of compilers
to provide a comprehensive evaluation.

BTD can produce
correct model speciﬁcations on 59 of 65 DNN executables,
and experienced users can quickly ﬁx 3 of 6 remaining errors.

Nevertheless, we recognize that some errors cannot be easily
ﬁxed by normal users.
```

### 62cf5a5130e8a5fd

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The recovery of optimized parameters’
dimensions can help analyze optimized operators.

Figure 4
is a specific example ofTransformoperator.

The parameters’
dimensions and types can be extracted by scanning the disas-
sembled code.

The dimension of the first parameter is optimized into
[N, C, H, W, c]layout.

NCHWc [1] is a commonly used
inference optimization method, which adapts to hardware
and accelerates inference.

NeuroDeX can recover it into
standard[N, C∗c, H, W]format.

Similarly, the dimension
[Oc, Ic, K, K]of aConvkernel parameter may be optimized
into[O c/A, Ic/B, K, K, B, A][1].

The optimized layout de-
cides the storage order of model weights in memory.

Neu-
roDeX extracts this optimized dimension layout and converts
it to standard format.

This method is layout agnostic, it is
compatible with other optimized layout, such as[N, H, W, C].
```

### da2e9320264c822e

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The parameters of the function correspond sequentially to the
inputs and outputs of the operator.

Each type operator has
a fixed number of inputs and outputs, and NeuroDeX can
accurately recover parameters’ dimensions.

We validate this
characteristic across both historical and recent TVM versions,
ensuring the generality and robustness of our approach.

B.

Operator Type Recognition
The purpose of operator type recognition is to determine
the specific type of the operator function.

We manually analyze DL compiler’s support for DNN
operators [1], [2] and align it with the practice of general
DL frameworks like ONNX [11] to classify operators.

The
operators can be divided into four types as shown in Table II.

Type 1 isLayout Transformation.

This type of operator adjusts
TABLE II: Operator Classification
Type Operators Description
1.

Layout
Transformation
1.1 concat,split...
1.2 flatten,reshape,
transpose...

Inter-tensor layout transforma-
tion
Intra-tensor layout transforma-
tion
2.
```

### bf1dca8f8840f813

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 20 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Quantized compiled methods involves global scale mode and
kl divergence mode.

Scale refers to the scaling factor between
the float domain and int domain during quantized compi-
lation.

The global scale method uses the same scale across
different operators, and does not rely on data calibration.

The
kl divergence method needs data for calibration, resulting in
higher precision.

The weights of quantized compiled models
are in the integer domain, and model inference is in inte-
ger domain as well.

NeuroDeX makes certain adaption to
model weights recovery, NeuroDeX also records the parameter
types and transforms dumped bytes into corresponding type.

Our goal is to recover a reusable, general model with float
weights.

During model inference, we observe that weights in
the integer domain are updated through shift multiplication
(e.g.,weight∗(0x6f65c500>>0x28)) to prevent integer
overflow.
```

### bd30f4fcfe778733

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 1 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Given a (stripped) executable compiled from a DNN model,
w1w2…mergeable nodes
operator optimizationModelSpecificationComputationGraph Creation
Graph IR &Optimization
Low-Level IR
Hardware-specificOptimization
(Auto) Scheduling& (Auto) TuningCode Gen &OptimizationDNNExecutable(a) DNN compilation pipeline.(b) Sample DNN computation graph.

DNN compiler frontend looks for holisticopt. chances likemergeable nodes, whereas backend explores efficient machinecode foreach operator.

ConvReLU ConvPool
Figure 1: The high-level workﬂow of DL compilation.
we propose a three-step approach for full recovery of DNN op-
erators, network topology, dimensions, and parameters.

BTD
conducts representation learning over disassembler-emitted
assembly code to classify assembly functions as DNN oper-
ators, such as convolution layers (Conv).
```

### 784da26bfe4a09ce

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 32 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Forexample,forthe Mul
functioninthe FC operator’ssummary(Line2-3inFigure5b),
DNDidentiﬁesthatthe input[i] istheoutputoftheprevious
DNN operator (i.e., its address range overlaps with previous
DNN operator’s output range), and that theweight[j][i]
is the parameter (i.e., its address range does not overlap with
any previous DNN operator’s output range).
5.4.3 Attributes and Parameters Recovery
In the last step,DND recovers the attributes and parameters
of each DNN operator by leveraging the generated operator
summary and recovered DNN topology, and it then generates
a high-level DNN representation in the ONNX format.

Attribute Recovery.

For DNN operators with only shape-
related attributes (e.g., ﬁlter length ofAveragePool),DND
recovers their attributes by checking the nesting structure of
their loops and the loops’ counts (e.g., the ﬁlter length is the
loop count of the loop that iterates over the inputs).
```

### 6afe0195be94b982

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 14 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Nonetheless, our evaluation indicates that the
operator type recognition accuracy on all TVM operators
reach 99.22%, and it is 97.62% for GLOW, maintaining high
accuracy.

In operator attribute recovery, the errors are very
rare and they are obvious in the decompiled code, such
as kernel size “*0.00591716 (1/169)” should be 13 but is
incorrectly identified as 17.

Therefore, it does not require a
systematic error fix mechanism.

We analyze the causes of
errors in operator type recognition and the errors can be
classified into three categories.

Type1:a single operator is
split into multiple functions;Type2:incorrect recognition of
activation functions;Type3:other random operator recognition
errors.

The proportions of these three wrong types are 36.2%,
13.8% and 50% respectively.

NeuroDeX has corresponding
error fix strategies for different types of errors:
Type 1:Error operators exhibit fixed patterns.

These er-
rors accur inSoftmax,AvgpoolandDense add.

These errors
can be detected immediately after operator type recognition.
```

### b2d5ec795a6e003a

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Moreover,
we have supplemented our evaluation with six more different
models, aiming to cover more model structures and varying
hyperparameters for same model structure.

Furthermore, we
conduct an additional analysis on 42 BTD unexplored DNN
executables, covering a wider range of compiler versions,
architectures, and quantized models.

All the executables in
our evaluation are stripped.

C.

Evaluation Metrics
We evaluate the effectiveness of NeuroDeX from three
perspectives: operator type recognition, operator attribute re-
covery and recovered model inference.

For operator type recognition, we measure Type Recog-
nition Accuracy (TRA).

Meanwhile, for operator attribute
recovery, we measure Attribute Recovery Accuracy (ARA).

Regarding model inference, we adopt the same method from
previous studies [7], [8], which compares the inference results
and confidence scores of the recovered model with those of the
executables.

We regard the inference results as consistent only
if the labels and confidence scores are exactly identical or dif-
fer solely by negligible precision loss.
```

### 547a3b0f9080d220

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 5 Implementation |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Given a DNN executable, a user ﬁrst disassembles
it (e.g., using IDA-Pro) and recovers all assembly functions.

The user also need to provide a format-valid input of this
executable for use.

Next, as an end-to-end procedure, BTD
predicts compilation provenance and each disassembly func-
tion’s operator type.

BTD then launches the network topology
recovery before conducting symbolic execution and recov-
ering dimensions and parameters for each operator, as ex-
plained in Sec. 4.

Note that at this step, BTD uses a set of
error detection rules (see below) to detect and ﬁx potential
errors.

Decompilation process is then re-invoked if errors are
ﬁxed.

If the error cannot be resolved, human intervention is
required.

The user needs to read and understand the symbolic
constraints to ﬁx the error.

Human comprehension at this step
is the only uncertain but necessary step of the decompilation if
complex errors occur.
```

### c6bac3be25d235ea

| Field | Value |
|-------|-------|
| source_file | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks.pdf |
| section | experiment |
| section_title | 6 Experiments |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 23 |
| paper_id | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks |

```
Fake Operator Insertion ( fi) further lowers the recovery rates
to 47.18% and 3.03% respectively, by inserting fake operators and
causing the random input from BTD to trigger wrong execution
paths.

When all NeuroShield’s obfuscation primitives are applied,
the operator recovery rate is the same as fi, but the attack time
increases by around 3x because cr causes BTD to log and analyze
more instructions.
6.4 Strength of Inserted Control Flow
To demonstrate the resilience of the input-dependent control flow
introduced by NeuroShield, we measure how long symbolic execu-
tion takes to resolve the constraints added by Fusor and Fake Oper-
ator Insertion (fi).

We firstly use a random input to identify the
input and output buffer of a function dynamically (similar to BTD),
mark the elements in the input buffer as symbolic, and run symbolic
execution using angr [ 3] for 5 days.
```

### e8d85764315c72e4

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

NeuroDeX features an accurate operator
type recognition and operator attribute recovery mechanism
that does not rely on prior knowledge such as compiler ver-
sions or training data.

NeuroDeX can accurately recover fused
operators and its core components do not depend on resource-
intensive analysis techniques like symbolic execution, allowing
for rapid and efficient analysis.

Furthermore, NeuroDeX is
extendable to different architectures, different DL compilers,
and quantized models.
```

### cba88a60112f4554

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the number
of operator classes, and it’s also the length of the prediction
vector for a single sample.

The average result of TRA and
THA for different compiler versions are shown in Table V.

Although THA may achieve higher results, TRA undoubtedly
provides a more scientific measure of the true effectiveness of
operator recognition.

For instance, prediction-label pair like
[1,0,0,0,0. . .]20 and[0,1,0,0,0. . .] 20 will yield THA with
18/20 = 0.9, but from the operator functional perspective, it is
entirely incorrect.
```

### 74238bd6bc7e40c9

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of NeuroDeX
with BTD and analyze the underlying reasons.

We choose four models: EfficientNet, ResNet18, Incep-
tionv1 and ShuffleNetv2.

These models cover a range of
weights size and topological complexities, enabling a compre-
hensive evaluation of the overhead associated with BTD and
NeuroDeX.

The model reconstruction strategies for NeuroDeX
and BTD are identical.

Therefore, we only compare the time
associated with operator type recognition and operator attribute
recovery processes.
```

### 69052d09957be415

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 9 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Diff (%) VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 27.90 27.57 34.71 28.59 28.44 28.88 34.24 36.73 35.53 35.72
FlatD 17.43 17.48 18.76 12.91 12.91 12.90 17.04 22/45 21.93 21.94
of Operator functions, which is only related to the Operator
Type recovery, we only evaluate our defense mechanism on
how it can affect the inference of Operator Type of each
reversing-based model extraction attack.

Moreover, Operator-
type recovery is the most essential and fundamental step in
reconstructing the final models because, in some attacks [32],
[34], [35], the recovery of other parts highly depends on the
recovery of Operator-type.

We report the difference in the accuracy of DNN operator
inference between the original version and the transformed
version generated from O-LLVM and FlatD in Table V.
```

### a56d6a08d27f78a8

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 7 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In summary, we
contribute the following:
• This paper, for the ﬁrst time1, advocates for reverse engi-
neering DNN executables.

BTD accepts as input (stripped)
executables generated by production DL compilers and out-
puts complete model speciﬁcations.

BTD can be used to aid
in the comprehension, migration, hardening, and exploita-
tion of DNN executables.
• BTD features a three-step approach to recovering high-
level DNN models.

It incorporates various design principles
and techniques to deliver an effective pipeline.
• We evaluate BTD against executables compiled from large-
scale DNN models using production DL compilers.

BTD
achieves high accuracy in recovering (nearly) full speciﬁca-
tions of complex DNN models.

We also demonstrate how
common attacks are boosted by BTD.
2 Preliminary
Fig. 1(a) depicts DNN model compilation.

DNN compila-
tion can be divided into two phases [58], with each phase
manipulates one or several intermediate representations (IR).
```

### 6f0f7d6275f908ad

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW
BTD 676.3 265.0 2904.7 468.7 681.2 2416.3 982.8 705.6 4328.8 152.7 92.8 296.2
NeuroDeX 76.9 122.2 204.5 41.4 127.9 129.2 208.3 288.8 304.7 66.0 80.9 75.4
for fair comparison.

The compiler version for our experiment
is TVM v0.9dev and GLOW 2022.
```

### 1abbd1f5f8db7fc2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 7 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
To avoid the
influence of data leak, we randomly split all the data with
an 8:2 ratio for train dataset and test dataset, and retrain the
model for each compiler version, strictly following the default
settings of BTD.

As illustrated in Figure 1, we have analyzed
BTD’s type recognition accuracy across different compiler
versions.

It is evident that BTD’s method exhibits poor cross-
version support for compilers after avoiding data leak.

Even
within the same version, errors of operator type occur to an
unacceptable degree, make it difficult to apply directly.

Observation3:To overcome the reliance on prior knowl-
edge and improve recognition accuracy, we attempt to use a
mathematical feature-based approach for operator type recog-
nition.

We specifically calculate the proportion of arithmetic
operators (e.g., +, -, *, /) within the decompiled code of
operator functions, and apply TSNE dimensionality reduc-
tion.
```

---

## 3. [single_003_en] What role does the LLM play in NeuroDeX's decompilation pipeline, and what accuracy does it achieve?

**Type**: `method` | **Lang**: `EN` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.0000 |
| 20 | 0.4000 | 0.8000 |

**Expected sources**: NeuroDeX

### Expected Chunks (5)

### 03e5ee11ed5284cb

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from DNN exe-
cutables using ghidra.

Inspired by previous works [6], [9], NeuroDeX can identify
the dimensions of operator parameters from disassembled
code in TVM compiler.

NeuroDeX further expands on their
methods, NeuroDeX also extracts the types of operator param-
eters and recover the optimized parameters’ dimensions.
```

### 2f2cb9ddcb1914fa

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute recovery, where it leverages dynamic anal-
ysis and code semantic understanding from LLMs to support
compatibility with various types of models.

Dynamic analysis
aims to monitor the runtime information of operator functions.

Dynamic analysis in NeuroDeX requires only trivial input that
satisfies the expected input format.

This is due to the fact
that any input can guarantee full coverage of the whole DNN
model, and the mathematical dependencies of intermediate
features are fixed.
```

### 6647adfcb117af59

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 9 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The decompiler should also have cross-architecture
support capabilities.

C3:Quantized compiled models exhibit
new characteristics different from standard models, involving
quantization scaling factors between integer and float domains.

The decompiler needs to be compatible with these differences.

To address these challenges, we design NeuroDeX to imple-
ment a more comprehensive decompiler for DNN executables.

For C1:We systematically analyze the characteristics of oper-
ators in DL compilers and design a progressive operator type
recognition strategy.

NeuroDeX leverages dynamic analysis
and code semantic understanding from LLMs to support com-
patibility with various types of operators and fused operators.

For C2:Based on the operator type recognition method, we
subsequently implement operator attribute recovery and model
reconstruction, forming a complete decompilation pipeline
compatibility with various types of different models.

The
core technology of NeuroDeX is hardware-platform indepen-
dent, ensuring its cross-architecture support capabilities.
```

### 07d58c1a191e9499

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 8 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The result is shown in Figure 2, the distributions of
different types significantly overlap, indicating that classifying
operators solely based on their mathematical characteristics
is evidently challenging.

Successfully performing operator
type recognition requires a thorough capture of the semantic
features of operator functions.

The operator type recognition
mechanism should have a good grasp of code semantic rather
than strict mathematical feature matching.

Reflecting on these observations,existing works struggle
with operator type recognition.

They exhibit limitations in
the scope of covered operators and recognition accuracy.

We summarize the challenges faced as follows.

C1:A
method for accurate operator type recognition needs to be
designed.

It should be able to cover a wide variety of opera-
tors and fused operators under compilation optimization.

The
method should not rely on prior knowledge such as compiler
version or training data.

C2:A decompiler needs to integrate
Fig. 2: TSNE Dimensionality Reduction of Different Operators
the new method for operator type recognition, forming an end-
to-end pipeline that recover DNN executables into high-level
models.
```

### 62cf5a5130e8a5fd

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The recovery of optimized parameters’
dimensions can help analyze optimized operators.

Figure 4
is a specific example ofTransformoperator.

The parameters’
dimensions and types can be extracted by scanning the disas-
sembled code.

The dimension of the first parameter is optimized into
[N, C, H, W, c]layout.

NCHWc [1] is a commonly used
inference optimization method, which adapts to hardware
and accelerates inference.

NeuroDeX can recover it into
standard[N, C∗c, H, W]format.

Similarly, the dimension
[Oc, Ic, K, K]of aConvkernel parameter may be optimized
into[O c/A, Ic/B, K, K, B, A][1].

The optimized layout de-
cides the storage order of model weights in memory.

Neu-
roDeX extracts this optimized dimension layout and converts
it to standard format.

This method is layout agnostic, it is
compatible with other optimized layout, such as[N, H, W, C].
```

### Retrieved Top-20

**#1** — cdce554512cc3586 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=0

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implement
```

**#2** — 2eda3aacde4e38c8 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.2-2 | sec=related_work | ci=4

```
However, each of these methods has its limitations.

We summarize the previous works and compare them with
NeuroDeX in Table I.

Libsteal cannot decompile standalone
DNN executables and is unable to handle compilation opti-
mizations.

The accuracy of the models recovered by Libsteal
is relatively low.

The work by Shi et al. only supports x86
architecture and cannot recover models with high accuracy.

DND and Neuroscope do not effectively handle compila-
tion optimizations.

Although BTD consid
```

**#3** — 6afe0195be94b982 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.11-11 | sec=results | ci=14

```
Nonetheless, our evaluation indicates that the
operator type recognition accuracy on all TVM operators
reach 99.22%, and it is 97.62% for GLOW, maintaining high
accuracy.

In operator attribute recovery, the errors are very
rare and they are obvious in the decompiled code, such
as kernel size “*0.00591716 (1/169)” should be 13 but is
incorrectly identified as 17.

Therefore, it does not require a
systematic error fix mechanism.

We analyze the causes of
errors in operator type recognition and th
```

**#4** — e0b75a7c3a534224 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.10-10 | sec=results | ci=6

```
Moreover, it is noteworthy that NeuroDeX’s approach does
not involve heavy analysis constrained by hardware resources.

In contrast, the methods utilized by BTD demand considerable
memory and CPU resources, which can lead to performance
degradation on consumer-grade devices.

Answer to RQ2:NeuroDeX can decompile DNN executa-
bles with a shorter time overhead than SOTA methods and
NeuroDeX does not rely heavily on hardware resources.

C.

RQ3: Comprehensiveness
To answer RQ3, we aim to evaluate N
```

**#5** — 49c598a0d4c59151 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.11-12 | sec=results | ci=16

```
To demonstrate the effectiveness of NeuroDeX on different
LLMs, we also compare the performance of different LLMs
including GPT-4.1 [38], Deepseekv3 [39], GPT-4o mini [40],
Gemini2.5 flash [41].

The selection of LLMs will affect TRA
directly.

Results are shown in Table IX.

Deepseekv3 and
GPT-4.1 perform well in all models across different compiler
settings.

Gemini2.5 flash struggles to identify operators of
GLOW, GPT-4o mini fails to identify TVM optimization
operators and GLOW operators.

I
```

**#6** — cba88a60112f4554 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=1

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the
```

**#7** — 74238bd6bc7e40c9 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=3

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of Neuro
```

**#8** — 5f882e74e4b278f2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=3

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive 
```

**#9** — cd7444c98cc84207 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.12-12 | sec=conclusion | ci=0

```
In this work, we design NeuroDeX to provide diverse
support in decompiling DNN executables. NeuroDeX recovers
DNN executables back into high-level models through oper-
ator type recognition, operator attribute recovery and model
reconstruction. NeuroDeX leverages the semantic understand-
ing capabilities of LLMs along with dynamic analysis to
construct a comprehensive and robust decompilation pipeline.
Our evaluations demonstrate that NeuroDeX can successfully
decompile DNN executables across di
```

**#10** — f797fdd22fb510af | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=2

```
As for operator attribute recovery and model reconstruc-
tion, NeuroDeX reaches 100% ARA and MIA on all mod-
els in TVM; NeuroDeX reaches 100% ARA besides Incep-
tionv1 2020, ShuffleNetv2 2021, EfficientNet 2020 and Effi-
cientNet 2021 in GLOW.

The very few errors in operator at-
tribute recovery are due to occasional wrongs ofLrn,Avgpool
andClip.

The attributes of these wrong operators are directly
evident in the decompiled code, making it easy to correct
them through manual verification.

As
```

**#11** **[HIT]** — 6647adfcb117af59 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-3 | sec=related_work | ci=9

```
The decompiler should also have cross-architecture
support capabilities.

C3:Quantized compiled models exhibit
new characteristics different from standard models, involving
quantization scaling factors between integer and float domains.

The decompiler needs to be compatible with these differences.

To address these challenges, we design NeuroDeX to imple-
ment a more comprehensive decompiler for DNN executables.

For C1:We systematically analyze the characteristics of oper-
ators in DL compiler
```

**#12** — c72c8f73fb291b99 | Codellm-Devkit: A Framework for Contextualizing.pdf | p.3-4 | sec=method | ci=6

```
The overall
distribution is shown in Fig. 5.
0% 5% 10%15%20%JavaPythonGoTypescriptJavascriptCOBOLC#AnsiblePL1ZRNodeJSBashC++.

NetYAMLC
Fig. 5: Target programming languages for LLM-assisted tasks
at IBM.
• Use of program analysis (B5).

All but two participants (R1
and E2) agreed that that they use program analysis in their
code LLM pipeline.

Of the two exceptions, R1 answered that
their use case is surrounding taking LLM output off-the-shelf
whereas E1 works on building an evaluation pipeline 
```

**#13** — bedca5e784a8ba90 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.5-5 | sec=method | ci=7

```
For example,
an operator with two parameters’ dimensions:[1,1000,1,1]
and[1,1000]can be directly identified asFlatten.

ForConv, in-
put channel and output channel of kernel parameter correspond
respectively to the channel of the first and last parameters.

For
Element-wiseandReductiontype, operators can be determined
candidate list among 2.1, 2.2, 3.1 in Table II according to the
number and dimension of parameters.

Further, leveraging the
code semantic understanding capabilities of LLMs, Neuro
```

**#14** — 3fa7b9f026009fe2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.7-7 | sec=method | ci=16

```
The input height
Ih, paddingP, kernel sizeK, strideS, and output heightO h
satisfy the following constraint:
Oh =
(Ih + 2P−K)
S

+ 1(3)
Except for stride and padding, all other variables forConv
are known, and both stride and padding must be integers.

To
determine the values of them, NeuroDeX employs a constraint
enumeration method.

Starting with stride= 1and padding=
0, NeuroDeX enumerates different combinations in ascending
order to find solution that satisfies the constraint.

ForAvgpoola
```

**#15** — ab34bb9750cf1e98 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.5-5 | sec=method | ci=9

```
Oth-
erwise, NeuroDeX starts recording the memory access during
the operator function execution, identifying the instruction that
initially accesses the parameter address.

From this instruction,
NeuroDeX performs taint analysis, tracking relevant registers
until first encounter a multiply or add instruction.

Activation
functions likeReluandClipare often attached to the tail of
the fused operator with repeated patterns in decompiled code.

NeuroDeX extracts the tail part of the decompiled code 
```

**#16** — 75400e9cae287630 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-2 | sec=introduction | ci=3

```
NeuroDeX is evaluated on 88 non-quantized DNN exe-
cutables and NeuroDeX can accurately recover them into
nearly identical high-level models.

NeuroDeX adapts for the
different compiler versions, accommodates a wider range of
models, and supports different architectures.

The operator type
recognition accuracy for all TVM executables and GLOW
executables reaches 99.22% and 97.62% respectively.

The
operator attribute recovery accuracy is nearly 100%.

Neu-
roDeX incorporates robust error fix str
```

**#17** — fe80626d0b613db0 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.7-7 | sec=method | ci=17

```
NeuroDeX then enumerates different combinations
of kernel size, stride and padding, simulates the forward of
theMaxpooluntil the computed tensor exactly matches the
actual output tensor.

It is worth noting that any trivial input
can achieve full coverage, so NeuroDeX only needs one trivial
input to simulate forward.

In the case ofAvgpool, kernel size
is evidently reflected in the decompiled code.

For example,
patterns like “∗0.020408(1/49)” repeatedly appear, indicating
that kernel size is 7.
```

**#18** — 017ece968e194724 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.6-6 | sec=method | ci=12

```
TVM fused:conv2d·(mul|add)*·(activation)?, dense
·(mul|add)*·(activation)?, add·(activation)?, concat·
(reshape·transpose·reshape)?·(activation)?, concat·
(reshape·transpose·reshape)?·split, reshape·transpose
·reshape.

GLOW:maxpool, avgpool, softmax, relu, lrn, add, sub,
mul, dense, conv2d, convdkkc8, conv2d relu, conv2d clip,
tensor transformation (insert tensor, extract tensor...).

We compile and decompile validated computer vision mod-
els from the ONNX Model Zoo, and NeuroDeX can cover all
```

**#19** **[HIT]** — 2f2cb9ddcb1914fa | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.4-4 | sec=method | ci=0

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute r
```

**#20** — e8d85764315c72e4 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-1 | sec=introduction | ci=2

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

N
```

### Missed Chunks (3 — expected but NOT in top-20)

### 03e5ee11ed5284cb

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from DNN exe-
cutables using ghidra.

Inspired by previous works [6], [9], NeuroDeX can identify
the dimensions of operator parameters from disassembled
code in TVM compiler.

NeuroDeX further expands on their
methods, NeuroDeX also extracts the types of operator param-
eters and recover the optimized parameters’ dimensions.
```

### 07d58c1a191e9499

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 8 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The result is shown in Figure 2, the distributions of
different types significantly overlap, indicating that classifying
operators solely based on their mathematical characteristics
is evidently challenging.

Successfully performing operator
type recognition requires a thorough capture of the semantic
features of operator functions.

The operator type recognition
mechanism should have a good grasp of code semantic rather
than strict mathematical feature matching.

Reflecting on these observations,existing works struggle
with operator type recognition.

They exhibit limitations in
the scope of covered operators and recognition accuracy.

We summarize the challenges faced as follows.

C1:A
method for accurate operator type recognition needs to be
designed.

It should be able to cover a wide variety of opera-
tors and fused operators under compilation optimization.

The
method should not rely on prior knowledge such as compiler
version or training data.

C2:A decompiler needs to integrate
Fig. 2: TSNE Dimensionality Reduction of Different Operators
the new method for operator type recognition, forming an end-
to-end pipeline that recover DNN executables into high-level
models.
```

### 62cf5a5130e8a5fd

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The recovery of optimized parameters’
dimensions can help analyze optimized operators.

Figure 4
is a specific example ofTransformoperator.

The parameters’
dimensions and types can be extracted by scanning the disas-
sembled code.

The dimension of the first parameter is optimized into
[N, C, H, W, c]layout.

NCHWc [1] is a commonly used
inference optimization method, which adapts to hardware
and accelerates inference.

NeuroDeX can recover it into
standard[N, C∗c, H, W]format.

Similarly, the dimension
[Oc, Ic, K, K]of aConvkernel parameter may be optimized
into[O c/A, Ic/B, K, K, B, A][1].

The optimized layout de-
cides the storage order of model weights in memory.

Neu-
roDeX extracts this optimized dimension layout and converts
it to standard format.

This method is layout agnostic, it is
compatible with other optimized layout, such as[N, H, W, C].
```

### False Positives (18 — in top-20 but NOT expected)

### cdce554512cc3586

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implementation & Environment
We implement NeuroDeX with about 8K LOC Python code
and about 1K LOC C++ code.

In our experiments, we select
GPT-4o [20] for its superior performance in code understand-
ing [21], [22] and the large size (128K) of context window,
which is sufficient to cover the operator functions.
```

### 2eda3aacde4e38c8

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
However, each of these methods has its limitations.

We summarize the previous works and compare them with
NeuroDeX in Table I.

Libsteal cannot decompile standalone
DNN executables and is unable to handle compilation opti-
mizations.

The accuracy of the models recovered by Libsteal
is relatively low.

The work by Shi et al. only supports x86
architecture and cannot recover models with high accuracy.

DND and Neuroscope do not effectively handle compila-
tion optimizations.

Although BTD considers the impact of
compilation optimizations, it only supports x86 architecture.

Moreover, all previous works overlook models compiled with
quantization, which limits the applicability of these methods
in practical scenarios.

Previous DNN executables decompilers
have their own limitations and existing decompilers struggle
tosimultaneously address compilation optimizations, sup-
port different architectures, and accommodate quantized
compiled models.

Beyond the aforementioned discussion, we conduct a sys-
tematic analysis of operator type recognition, the critical
step in decompilation pipeline.
```

### 6afe0195be94b982

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 14 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Nonetheless, our evaluation indicates that the
operator type recognition accuracy on all TVM operators
reach 99.22%, and it is 97.62% for GLOW, maintaining high
accuracy.

In operator attribute recovery, the errors are very
rare and they are obvious in the decompiled code, such
as kernel size “*0.00591716 (1/169)” should be 13 but is
incorrectly identified as 17.

Therefore, it does not require a
systematic error fix mechanism.

We analyze the causes of
errors in operator type recognition and the errors can be
classified into three categories.

Type1:a single operator is
split into multiple functions;Type2:incorrect recognition of
activation functions;Type3:other random operator recognition
errors.

The proportions of these three wrong types are 36.2%,
13.8% and 50% respectively.

NeuroDeX has corresponding
error fix strategies for different types of errors:
Type 1:Error operators exhibit fixed patterns.

These er-
rors accur inSoftmax,AvgpoolandDense add.

These errors
can be detected immediately after operator type recognition.
```

### e0b75a7c3a534224

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 6 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Moreover, it is noteworthy that NeuroDeX’s approach does
not involve heavy analysis constrained by hardware resources.

In contrast, the methods utilized by BTD demand considerable
memory and CPU resources, which can lead to performance
degradation on consumer-grade devices.

Answer to RQ2:NeuroDeX can decompile DNN executa-
bles with a shorter time overhead than SOTA methods and
NeuroDeX does not rely heavily on hardware resources.

C.

RQ3: Comprehensiveness
To answer RQ3, we aim to evaluate NeuroDeX on a wider
range of models and on aarch64 architecture to demonstrate
its versatility.

We also discuss the compatibility with quantized
compiled models of NeuroDeX.

We first evaluate NeuroDeX on the latest compiler verison
to verify its scalability.

According to our observations, TVM
is a project that is frequently maintained; GLOW is a stable
project, we have counted the commits since 2023, which
total only about 100, and the majority are related to feature
maintenance and bug fixes.
```

### 49c598a0d4c59151

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 11 |
| page_end | 12 |
| chunk_index | 16 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
To demonstrate the effectiveness of NeuroDeX on different
LLMs, we also compare the performance of different LLMs
including GPT-4.1 [38], Deepseekv3 [39], GPT-4o mini [40],
Gemini2.5 flash [41].

The selection of LLMs will affect TRA
directly.

Results are shown in Table IX.

Deepseekv3 and
GPT-4.1 perform well in all models across different compiler
settings.

Gemini2.5 flash struggles to identify operators of
GLOW, GPT-4o mini fails to identify TVM optimization
operators and GLOW operators.

In summary, NeuroDeX does
not rely on a specific LLM.

LLMs that perform well in general
domains are equally suitable for completing the operator type
recognition task.

Answer to RQ4:NeuroDeX has a stable error-fix mech-
anism that effectively addresses different types of errors.

NeuroDeX is not sensitive to the selection of LLMs, and
various different LLMs are suitable for NeuroDeX.
```

### cba88a60112f4554

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the number
of operator classes, and it’s also the length of the prediction
vector for a single sample.

The average result of TRA and
THA for different compiler versions are shown in Table V.

Although THA may achieve higher results, TRA undoubtedly
provides a more scientific measure of the true effectiveness of
operator recognition.

For instance, prediction-label pair like
[1,0,0,0,0. . .]20 and[0,1,0,0,0. . .] 20 will yield THA with
18/20 = 0.9, but from the operator functional perspective, it is
entirely incorrect.
```

### 74238bd6bc7e40c9

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of NeuroDeX
with BTD and analyze the underlying reasons.

We choose four models: EfficientNet, ResNet18, Incep-
tionv1 and ShuffleNetv2.

These models cover a range of
weights size and topological complexities, enabling a compre-
hensive evaluation of the overhead associated with BTD and
NeuroDeX.

The model reconstruction strategies for NeuroDeX
and BTD are identical.

Therefore, we only compare the time
associated with operator type recognition and operator attribute
recovery processes.
```

### 5f882e74e4b278f2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive experiments across different optimization
levels and different compiler versions, which demonstrates its
effectiveness.

Overall, BTD is currently the SOTA method
available.

As shown in Table III, to ease of comparison, we evaluate
NeuroDeX on six different DL models, comprising a total of
54 DNN executables (varying in compiler, optimization level,
and compiler version) that are analyzed in BTD.
```

### cd7444c98cc84207

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | conclusion |
| section_title | VIII. CONCLUSION |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In this work, we design NeuroDeX to provide diverse
support in decompiling DNN executables. NeuroDeX recovers
DNN executables back into high-level models through oper-
ator type recognition, operator attribute recovery and model
reconstruction. NeuroDeX leverages the semantic understand-
ing capabilities of LLMs along with dynamic analysis to
construct a comprehensive and robust decompilation pipeline.
Our evaluations demonstrate that NeuroDeX can successfully
decompile DNN executables across different DL compiler set-
tings, different architectures and quantized compiled models.
```

### f797fdd22fb510af

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
As for operator attribute recovery and model reconstruc-
tion, NeuroDeX reaches 100% ARA and MIA on all mod-
els in TVM; NeuroDeX reaches 100% ARA besides Incep-
tionv1 2020, ShuffleNetv2 2021, EfficientNet 2020 and Effi-
cientNet 2021 in GLOW.

The very few errors in operator at-
tribute recovery are due to occasional wrongs ofLrn,Avgpool
andClip.

The attributes of these wrong operators are directly
evident in the decompiled code, making it easy to correct
them through manual verification.

As for MIA in GLOW,
one specific situation needs to be addressed: the inference
confidence scores of recovered Inceptionv1 by NeuroDeX
differ from the executables.

When ignoring these confidence
score differences, the class prediction accuracy is 96.4%.

The
differences in confidence are primarily attributed to precision
loss during compilation.

Compared to inference results of
source high-level ONNX models, the MIA reaches 100%.
```

### c72c8f73fb291b99

| Field | Value |
|-------|-------|
| source_file | Codellm-Devkit: A Framework for Contextualizing.pdf |
| section | method |
| section_title | II. MOTIVATION |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 6 |
| paper_id | Codellm-Devkit: A Framework for Contextualizing |

```
The overall
distribution is shown in Fig. 5.
0% 5% 10%15%20%JavaPythonGoTypescriptJavascriptCOBOLC#AnsiblePL1ZRNodeJSBashC++.

NetYAMLC
Fig. 5: Target programming languages for LLM-assisted tasks
at IBM.
• Use of program analysis (B5).

All but two participants (R1
and E2) agreed that that they use program analysis in their
code LLM pipeline.

Of the two exceptions, R1 answered that
their use case is surrounding taking LLM output off-the-shelf
whereas E1 works on building an evaluation pipeline for code
LLM (which does not warrant additional program analysis).
• Program analysis tool use (B6).

Of the participants that
answered affirmatively to the above, more than 60% of them
TABLE II: Developer survey questions.

Category Question Format
A1.

What is your job title?

Open-ended
Role and Experience
A2.

How many years of software engineering experience do you have?

Numeric
B1.

How would you rate your experience with Code LLMs ?

MCQ
B2.

What are your primary use cases for Code LLMs?
```

### bedca5e784a8ba90

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 7 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
For example,
an operator with two parameters’ dimensions:[1,1000,1,1]
and[1,1000]can be directly identified asFlatten.

ForConv, in-
put channel and output channel of kernel parameter correspond
respectively to the channel of the first and last parameters.

For
Element-wiseandReductiontype, operators can be determined
candidate list among 2.1, 2.2, 3.1 in Table II according to the
number and dimension of parameters.

Further, leveraging the
code semantic understanding capabilities of LLMs, NeuroDeX
determines the specific operator types within the candidate list
based on the mathematical features of the decompiled code.

Operator type recognition needs code semantic understanding
rather than strict mathematical feature matching, LLMs are
more suitable for it.

This approach overcomes the limitations
of previous methods, which rely heavily on training data
and struggle with the cross-version support for compilers.

NeuroDeX does not rely on complex prompt design, a simple
and clear prompt can effectively accomplish the task, ensuring
the stability of LLM participation in NeuroDeX.
```

### 3fa7b9f026009fe2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 16 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The input height
Ih, paddingP, kernel sizeK, strideS, and output heightO h
satisfy the following constraint:
Oh =
(Ih + 2P−K)
S

+ 1(3)
Except for stride and padding, all other variables forConv
are known, and both stride and padding must be integers.

To
determine the values of them, NeuroDeX employs a constraint
enumeration method.

Starting with stride= 1and padding=
0, NeuroDeX enumerates different combinations in ascending
order to find solution that satisfies the constraint.

ForAvgpoolandMaxpool, kernel size does not explictly
appear in the dimension information.

In the case ofMax-
pool, kernel size is reflected in the number of max-related
instructions.

However, due to compilation optimizations, it is
hard to accurately infer the kernel size directly.

To precisely
recover the attributes ofMaxpool, NeuroDeX instruments
the executable to record the input and output tensors of
Maxpool.
```

### ab34bb9750cf1e98

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 9 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Oth-
erwise, NeuroDeX starts recording the memory access during
the operator function execution, identifying the instruction that
initially accesses the parameter address.

From this instruction,
NeuroDeX performs taint analysis, tracking relevant registers
until first encounter a multiply or add instruction.

Activation
functions likeReluandClipare often attached to the tail of
the fused operator with repeated patterns in decompiled code.

NeuroDeX extracts the tail part of the decompiled code and
uses LLM to verify if activation is accompanied by the fused
operator.

NeuroDeX employs the same processing method for
other fused operators like the operator consisting ofConcat
and activation.

NeuroDeX provides more comprehensive anal-
ysis and support for fused operators than previous works.

For GLOW, the disassembled code does not contain dimen-
sion information, but the optimization strategy in GLOW is
relatively simple.

Operator fusion almost only occurs after
Convwith activation.
```

### 75400e9cae287630

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 1 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX is evaluated on 88 non-quantized DNN exe-
cutables and NeuroDeX can accurately recover them into
nearly identical high-level models.

NeuroDeX adapts for the
different compiler versions, accommodates a wider range of
models, and supports different architectures.

The operator type
recognition accuracy for all TVM executables and GLOW
executables reaches 99.22% and 97.62% respectively.

The
operator attribute recovery accuracy is nearly 100%.

Neu-
roDeX incorporates robust error fix strategies, andallthe
recovered model’s inference accuracy reaches 100% after the
errors are fixed.

Additionally, we evaluate NeuroDeX on 8
quantized compiled DNN executables, the results indicate that
NeuroDeX can successfully recover functionally similar high-
level models.

For model inference, the average top 1 accuracy
is 72%, and the average top 5 accuracy is 86%.

Our contributions are summarized as follows:
•We propose NeuroDeX to provide diverse support in
decompiling DNN executables.
```

### fe80626d0b613db0

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 17 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX then enumerates different combinations
of kernel size, stride and padding, simulates the forward of
theMaxpooluntil the computed tensor exactly matches the
actual output tensor.

It is worth noting that any trivial input
can achieve full coverage, so NeuroDeX only needs one trivial
input to simulate forward.

In the case ofAvgpool, kernel size
is evidently reflected in the decompiled code.

For example,
patterns like “∗0.020408(1/49)” repeatedly appear, indicating
that kernel size is 7.

LLM can extract kernel size from
decompiled code to reduce the overhead of dynamic analysis.

NeuroDeX infers stride and padding ofAvgpoolthrough the
constraint enumeration method same withConv.

Local response normalization (lrn) has attributes:size,β,α,
biasandCliphas attributes:min,max.

The attributes of lrn
and clip generally have a large search space, making them
unsuitable for simulation execution using dynamic analysis
enumeration.
```

### 017ece968e194724

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 12 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
TVM fused:conv2d·(mul|add)*·(activation)?, dense
·(mul|add)*·(activation)?, add·(activation)?, concat·
(reshape·transpose·reshape)?·(activation)?, concat·
(reshape·transpose·reshape)?·split, reshape·transpose
·reshape.

GLOW:maxpool, avgpool, softmax, relu, lrn, add, sub,
mul, dense, conv2d, convdkkc8, conv2d relu, conv2d clip,
tensor transformation (insert tensor, extract tensor...).

We compile and decompile validated computer vision mod-
els from the ONNX Model Zoo, and NeuroDeX can cover all
the operators of them.

The operator type recognition method
of NeuroDeX has good scalability.

For more operators, it
only requires defining their types in Table II.

The pipeline
of operator type recognition in NeuroDeX is universal and
scalable.

C.
```

### e8d85764315c72e4

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

NeuroDeX features an accurate operator
type recognition and operator attribute recovery mechanism
that does not rely on prior knowledge such as compiler ver-
sions or training data.

NeuroDeX can accurately recover fused
operators and its core components do not depend on resource-
intensive analysis techniques like symbolic execution, allowing
for rapid and efficient analysis.

Furthermore, NeuroDeX is
extendable to different architectures, different DL compilers,
and quantized models.
```

---

## 4. [single_006_en] What are the main categories of pitfalls when using LLMs for code intelligence, according to the Pitfalls survey?

**Type**: `fact` | **Lang**: `EN` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.0000 |
| 20 | 0.0000 | 0.2000 |

**Expected sources**: Pitfalls

### Expected Chunks (5)

### e22e391ecb25e743

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 10 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
During the review process, the first two authors independently examined and extracted information from
each paper, developing an initial classification scheme for pitfalls based on thematic analysis.

Guided by prior
literatureonmachinelearningsystemworkflows[ 7,54],westructuredourtaxonomyaroundfourkeystages:data
collection and labeling, system design and learning, performance evaluation, and deployment and maintenance,
as illustrated in Figure 3.

Categorization disagreements were resolved through structured discussions among
all authors until consensus was reached.

A similar process guided the development of implication categories
in Section 7.

Additionally, we also conducted snowballing backward and forward [71] to complement database
searchesandavoidexcludingimportantworks.

Throughthissystematiccombinationofsearchstrategies,selection
criteria, and quality checks, we identified 121 high-quality studies investigating the pitfalls and challenges of
LM4Code.
```

### 5e3a10550389184d

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 11 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The complete review protocol, including detailed search strategies, selection criteria, and quality
assessment procedures, is available in the Appendix A.
2.3 Statistics of Collected Publications
Figure 1 displays the distribution of the collected research studies across the published year and published venues.

From Figure 1a, we have noted that there is a significant increase in the number of relevant research studies
published annually from 2021.

Prior studies, such as Watsonet al. [172] and Yanget al. [183], have acknowledged
the prevalence of language models in code-related tasks between 2014 and 2020.

However, our results indicate
that limited attention has been paid to the identification and analysis of pitfalls in LM4Code.

Nevertheless,
Figure 1a shows a rising trend over the last three years, indicating an increasing interest in research within the
research community about the potential pitfalls in LM4Code.

Figure 1b shows the distribution of publications
across Software Engineering (SE), Security (SEC), and Artificial Intelligence (AI) domains.
```

### 58a91a46accb3900

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 4 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Through a rigorous systematic literature review (SLR) protocol as
outlined by [70, 72] and after an in-depth analysis of the primary studies, we collected 121 primary papers
(spanning 2018 to 2024) closely related to evaluating or addressing LM4Code pitfalls.

Comprehensive
details on our review process and the collected papers are available online1.
• Comprehensive Taxonomy.

We conducted a qualitative and quantitative synthesis of the collected studies.

We present a taxonomy of the collected studies according to the LM4Code lifecycle, including data
collectionandlabeling,systemdesignandlearning,performanceevaluation,deployment,andmaintenance.

Our synthesis investigates the pitfalls present in LM4Code, summarizes the implications of these pitfalls,
investigates how these issues are addressed, and outlines future challenges in this field.
1https://github.com/yueyueL/ReliableLM4Code
ACM Trans.

Softw.

Eng.

Methodol.
```

### 8940d9ce37888e6f

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Their superior
performance stems from the fact that many LMs are trained on vast and diverse code repositories, enabling LMs
to discern complex syntax, comprehend semantic context, and effectively predict code sequences [162].

However, the lack of transparency, often termed “black-box”, poses significant challenges and concerns [151,
153].

In other words, while language models for code intelligence (LM4Code) approaches offer powerful capabili-
ties,theyoftenlacktransparencyintheirunderlyingreasoninganddecision-makingprocess.

Tantithamthavorn et
al. [65, 153] also raised concerns that such a lack of transparency often leads to a lack of adoption of LM4Code
in practice.

Consequently, hidden or neglected pitfalls in data or algorithms may persist, leading to unrealistic
performance evaluation and unreliable code recommendations [55, 152].
```

### 316a1c2233137437

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 13 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The temporal analysis in Figure 2
reveals LSTM’s dominance before 2020, followed by a significant shift toward transformer-based language
models in the past four years, particularly pre-trained models like CodeBERT and Codex.

Recent years have seen
increased investigation into large language models such as GPT-4 and CodeLlama, aligning with observations
from previous surveys in learning-based software engineering [54, 165, 172].

Table 1 summarizes the distribution
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 5
0 5 10 15 20 25 30OthersGPT-4CodeLlamaGPT-3.5CodeBERTCodeT5CodeXBERTGPT-2General TransformerLSTMRNN
N of Papers
2018201920202021202220232024
Figure 2.
```

### Retrieved Top-20

**#1** — ea2a2e488a871826 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.10-11 | sec=method | ci=5

```
Meanwhile, spurious correlations have become more prominent
with the advent of explainable artificial intelligence (XAI) techniques for elucidating model reasoning [22,
151, 153].

Discussions around inappropriate model design remain ongoing as new frameworks and learning
strategies continue to emerge.

Similar to our observations regarding the data collection and labeling process,
Figure 7 reveals a greater emphasis on modern Transformer-based language models and GPT series compared to
conventi
```

**#2** — b6092ceb2394c280 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.9-10 | sec=method | ci=0

```
This section examines pitfalls in the system design and learning process for LM4Code.

The training of these
LM4Code models directly impacts their quality and efficacy for empowering code intelligence.

However, several
challenges arise in crafting optimal model architectures, formulating strategic training-testing approaches,
refining data preprocessing techniques, and selecting suitable learning algorithms.

Each design decision risks
introducing pitfalls that can undermine model robustness an
```

**#3** — 0d9684287a79f05b | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.6-6 | sec=method | ci=1

```
The implications of these pitfalls (RQ3) are discussed in
Section 7, and in Section 8, we further discuss open challenges and promising research directions.

This organized
structure enables a comprehensive analysis of pitfalls and considerations across the entire LM4Code pipeline.

Our taxonomy aims to provide crucial insights for developing more robust, reliable, and practical LM systems for
code intelligence tasks.
3 DATA COLLECTION AND LABELING
The data-hungry language models require large-s
```

**#4** — 247013ec6baa4e33 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.10-10 | sec=method | ci=3

```
Actually, introducing advanced pre-trained models like CodeBERT has
not eliminated these pitfalls.

Specifically, if not fine-tuned appropriately for downstream tasks, these models
might still overemphasize basic elements like keywords over richer code semantics [198].

Inappropriate Model Design:Inappropriate model design in LM4Code arises when the underlying architecture
fails to capture critical characteristics of code, such as hierarchy and composition.

The inability to construct robust
sem
```

**#5** — 91a40a4af6d5eccf | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.11-11 | sec=method | ci=9

```
Secondly, model nnsembling is gaining
traction, where the strengths of multiple models are leveraged to offset individual biases, as seen in the work by
Zhanget al. [198]whichemploysmultipleviewsofthesamedataformorerobustpredictions.

Lastly,regularization
and fine-tuning techniques play a pivotal role.

Regularization, such as dropout or L2 regularization, helps in
preventing overfitting, while fine-tuning allows pre-trained models, like CodeBERT, to adapt to specific dataset
nuances, as demons
```

**#6** — 63b73457012267c6 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.6-6 | sec=method | ci=2

```
In this section, we provide a brief description of related studies and discuss
the implications and potential solutions during the data collection and labeling stages.
3.1 RQ1-Pitfalls
From the collected papers, we identified 22 research studies focusing on pitfalls during the data collection and
labeling process.

Table 2 presents the statistics of literature on this topic, where the pitfalls can be grouped into
three main categories.

Unbalanced Distribution:Unbalanced distribution arises when
```

**#7** — 6d72b38d82a9cec3 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.22-23 | sec=results | ci=48

```
Liet al. [83] demonstrate that imitation models
can even exceed the performance of the victim model.

Additionally, when models are deployed on user clients,
they face the potential threat of reverse engineering.

Zhouet al. [200] highlight that the on-device models may
leak their confidential information, such as hyper-parameters and weights.

The risk of copyright infringement
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 23
and
```

**#8** — f15adeaa0d343f2e | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.21-21 | sec=results | ci=40

```
Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 21
Data Collection Phase:High-quality training data serves as the foundation for trustworthy model training, yet
inherent noise and errors can severely compromise model efficacy by causing models to learn irrelevant patterns
or establish spurious correlations.

Sunet al. [148] demonstrated that when code search models are trained
on carefully cleaned datasets, their performance improves significantly, with MRR rising from
```

**#9** — d044b1089f599fe6 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.10-10 | sec=method | ci=2

```
Liuet al. [95] and Shiet al. [139] emphasize that pitfalls can emerge from the data
processing processes such as test prefix generation or concurrent use of same-class data.

Spurious Correlations:Spurious correlations arise when language models mistakenly depend on irrelevant
artifacts rather than the intrinsic logic or intent of code for decision-making, leading to misleading associations.

The artifacts vary across SE tasks.

For instance, in vulnerability detection, artifacts may manifest as
```

**#10** — 7f16a532b9759a15 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.11-11 | sec=method | ci=8

```
While Shiet al. [140]
unravels how transformer-based models allocate attention for code summarization, Wanet al. [160] probes into
the nuances of attention during code-to-code translation.

These XAI approaches can serve to identify and rectify
model pitfalls, ensuring the reliability of LM4Code applications.

Model Optimization Strategies:In light of the pitfalls introduced by inappropriate model design, researchers
have turned to model optimization strategies to address and minimize their effe
```

**#11** — 187fbd5de9fc878c | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.3-3 | sec=introduction | ci=7

```
While related research evaluating LM4Code [16, 93, 108, 178] identifies some issues, our
work distinguishes itself in two key ways: (1) we employ a rigorous SLR methodology that systematically
identifies and categorizes pitfalls, and (2) we present a comprehensive taxonomy structured around the entire
LLM lifecycle, from dataset construction to deployment.

This approach enables us to systematically analyze not
only the identified issues but also their corresponding solutions and practical impac
```

**#12** — e21d4c9a69b6a80d | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.24-25 | sec=discussion | ci=7

```
Ensuring that these models are robust and trustworthy is essential.

This does not just relate to their
prediction accuracy but extends to the reliability, interpretability, and generalization capacity of the model,
especially in diverse and evolving coding environments [111, 167].

Building Interpretable LM4Code.

The black-box nature of language models has been a long-term concern,
especially when LM4Code applications directly influence software development outcomes [22, 151, 167, 172].

Trans
```

**#13** — 734a7fcf2cbba4e9 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.8-9 | sec=method | ci=12

```
Compared with the code snippets in open-source repositories, which can be
difficult to classify by task and slice accurately, such human-written code tasks are closer to the real user requests
in practice, which better reflects the performance of the model.

For instance, Linet al. [85] use a real-world
dataset composed of human-written programming exercises with multiple solutions.

Similarly, Mozannaret
al. [105, 106] uses user behavior data to demonstrate the effectiveness of their proposed m
```

**#14** — c55d4bbedea5c375 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.18-19 | sec=results | ci=30

```
This model boasts a lean
memory footprint, consuming just 6 MB of RAM — a significant 19x reduction compared to previous models.

It
can generate a single piece of code completion in a mere 8 ms and delivers an impressive 90% accuracy rate for
its top five suggestions.
6.2.3 Privacy and Copyright Protection.

The ability of large language models to memorize and reproduce training
dataraisescriticalprivacyandcopyrightconcerns.

Thus,developingeffectiveprotectionforprivacyandcopyright
has been wid
```

**#15** — a26ce090645b26fd | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.3-3 | sec=introduction | ci=5

```
Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 3
2 1 2 10
05101520253035404550
2018201920202021202220232024
N of Papers
Published Year
(a) Distribution of papers over years
ICSE, 29
ASE, 15ISSTA, 12TSE, 14
FSE/ESEC, 11
TOSEM, 12
S&P, 4USENIX Security, 3ACL, 6SANER, 2 ISSRE, 2 Others, 10 (b) Distribution of papers across venues
Figure 1.

Overview of papers
• Insightful Findings and Recommendations.

In addition to identifying and analyzing pitfalls, we distilled
pract
```

**#16** — e556a06e05abdc0b | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.12-13 | sec=results | ci=3

```
However, they argue that this assumption overlooks the continuous evolution
of software vulnerabilities and projects, leading to the Cross-Domain issue, where test sets should contain novel
vulnerabilities or projects.

Furthermore, Nonget al. [113] further reveal that vulnerability datasets like SARD [12]
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 13
comprise unrealistic synthetic examples, which exhibit smaller vocabulary, sm
```

**#17** — f70e48b81eb48682 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.3-4 | sec=introduction | ci=8

```
This research
question aims to identify the prevalent pitfalls in LM4Code systems, exploring how they could affect
various stages of the learning-based system lifecycle.
• RQ2: What solutions have been proposed to address these pitfalls?

This research question reviews
the existing body of literature to identify proposed approaches for solving the identified pitfalls.

ACM Trans.

Softw.

Eng.

Methodol.
4 • Xinyu She, Yue Liu, Yanjie Zhao, Yiling He, Li Li, Chakkrit Tantithamthavorn, Zhan Qin, 
```

**#18** — 1e7857e3861e9475 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.19-20 | sec=results | ci=34

```
The implications highlight that real-world deployment introduces complex
challenges for LM4Code systems.
7 RQ3-IMPLICATIONS
The implications of pitfalls in LM4Code span across multiple dimensions, from direct technical impacts to
broader research validity concerns.

The ramifications of these pitfalls and biases extend beyond merely impacting
research performance and reproducibility from an evaluative standpoint.

They also contribute to misleading
benchmarksandpotentialsecurityvulnerabilitieswi
```

**#19** — 2650eec6c284fd61 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.12-12 | sec=results | ci=0

```
The performance evaluation stage focuses on precisely assessing and analyzing the model’s performance using
predefinedtestsetsandevaluationmetrics.

Additionally,comparativeperformanceevaluationagainstbenchmarks
provides insights into a model’s strengths and weaknesses on specific code-related tasks.

However, potential
pitfalls can emerge from factors such as improper baselines, test sets, and performance metrics.

These challenges
must be thoroughly examined and addressed to ensure that the ev
```

**#20** — da8b2a79f0f17e81 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.2-2 | sec=introduction | ci=3

```
As LMs become increasingly prevalent in code intelligence despite increasing obstacles, there emerges an
urgent need for a comprehensive understanding of potential pitfalls within LM4Code systems.

This is not limited
to pitfall identification; it demands a deeper exploration into the understanding of the implications of these
pitfalls, current solutions, and possible challenges.

Although there is a growing body of research concerning or
addressing pitfalls in LM4Code [97, 143, 148, 191], the d
```

### Missed Chunks (5 — expected but NOT in top-20)

### e22e391ecb25e743

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 10 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
During the review process, the first two authors independently examined and extracted information from
each paper, developing an initial classification scheme for pitfalls based on thematic analysis.

Guided by prior
literatureonmachinelearningsystemworkflows[ 7,54],westructuredourtaxonomyaroundfourkeystages:data
collection and labeling, system design and learning, performance evaluation, and deployment and maintenance,
as illustrated in Figure 3.

Categorization disagreements were resolved through structured discussions among
all authors until consensus was reached.

A similar process guided the development of implication categories
in Section 7.

Additionally, we also conducted snowballing backward and forward [71] to complement database
searchesandavoidexcludingimportantworks.

Throughthissystematiccombinationofsearchstrategies,selection
criteria, and quality checks, we identified 121 high-quality studies investigating the pitfalls and challenges of
LM4Code.
```

### 5e3a10550389184d

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 11 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The complete review protocol, including detailed search strategies, selection criteria, and quality
assessment procedures, is available in the Appendix A.
2.3 Statistics of Collected Publications
Figure 1 displays the distribution of the collected research studies across the published year and published venues.

From Figure 1a, we have noted that there is a significant increase in the number of relevant research studies
published annually from 2021.

Prior studies, such as Watsonet al. [172] and Yanget al. [183], have acknowledged
the prevalence of language models in code-related tasks between 2014 and 2020.

However, our results indicate
that limited attention has been paid to the identification and analysis of pitfalls in LM4Code.

Nevertheless,
Figure 1a shows a rising trend over the last three years, indicating an increasing interest in research within the
research community about the potential pitfalls in LM4Code.

Figure 1b shows the distribution of publications
across Software Engineering (SE), Security (SEC), and Artificial Intelligence (AI) domains.
```

### 58a91a46accb3900

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 4 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Through a rigorous systematic literature review (SLR) protocol as
outlined by [70, 72] and after an in-depth analysis of the primary studies, we collected 121 primary papers
(spanning 2018 to 2024) closely related to evaluating or addressing LM4Code pitfalls.

Comprehensive
details on our review process and the collected papers are available online1.
• Comprehensive Taxonomy.

We conducted a qualitative and quantitative synthesis of the collected studies.

We present a taxonomy of the collected studies according to the LM4Code lifecycle, including data
collectionandlabeling,systemdesignandlearning,performanceevaluation,deployment,andmaintenance.

Our synthesis investigates the pitfalls present in LM4Code, summarizes the implications of these pitfalls,
investigates how these issues are addressed, and outlines future challenges in this field.
1https://github.com/yueyueL/ReliableLM4Code
ACM Trans.

Softw.

Eng.

Methodol.
```

### 8940d9ce37888e6f

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Their superior
performance stems from the fact that many LMs are trained on vast and diverse code repositories, enabling LMs
to discern complex syntax, comprehend semantic context, and effectively predict code sequences [162].

However, the lack of transparency, often termed “black-box”, poses significant challenges and concerns [151,
153].

In other words, while language models for code intelligence (LM4Code) approaches offer powerful capabili-
ties,theyoftenlacktransparencyintheirunderlyingreasoninganddecision-makingprocess.

Tantithamthavorn et
al. [65, 153] also raised concerns that such a lack of transparency often leads to a lack of adoption of LM4Code
in practice.

Consequently, hidden or neglected pitfalls in data or algorithms may persist, leading to unrealistic
performance evaluation and unreliable code recommendations [55, 152].
```

### 316a1c2233137437

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 13 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The temporal analysis in Figure 2
reveals LSTM’s dominance before 2020, followed by a significant shift toward transformer-based language
models in the past four years, particularly pre-trained models like CodeBERT and Codex.

Recent years have seen
increased investigation into large language models such as GPT-4 and CodeLlama, aligning with observations
from previous surveys in learning-based software engineering [54, 165, 172].

Table 1 summarizes the distribution
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 5
0 5 10 15 20 25 30OthersGPT-4CodeLlamaGPT-3.5CodeBERTCodeT5CodeXBERTGPT-2General TransformerLSTMRNN
N of Papers
2018201920202021202220232024
Figure 2.
```

### False Positives (20 — in top-20 but NOT expected)

### ea2a2e488a871826

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 10 |
| page_end | 11 |
| chunk_index | 5 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Meanwhile, spurious correlations have become more prominent
with the advent of explainable artificial intelligence (XAI) techniques for elucidating model reasoning [22,
151, 153].

Discussions around inappropriate model design remain ongoing as new frameworks and learning
strategies continue to emerge.

Similar to our observations regarding the data collection and labeling process,
Figure 7 reveals a greater emphasis on modern Transformer-based language models and GPT series compared to
conventionalarchitectures.

Thisdistributionhighlightsashifttowardsexaminingpotentialpitfallsinsophisticated
language models for code intelligence tasks, setting the stage for continued research focused on enhancing model
transparency, interpretability, and reliability.

ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 11
4.2 RQ2-Solutions
To address the three pitfalls related to the system design and learning process, researchers have employed a
variety of approaches which we describe as follows.
```

### b6092ceb2394c280

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 0 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
This section examines pitfalls in the system design and learning process for LM4Code.

The training of these
LM4Code models directly impacts their quality and efficacy for empowering code intelligence.

However, several
challenges arise in crafting optimal model architectures, formulating strategic training-testing approaches,
refining data preprocessing techniques, and selecting suitable learning algorithms.

Each design decision risks
introducing pitfalls that can undermine model robustness and effectiveness.
4.1 RQ1-Pitfalls
We have identified 43 research studies dedicated to the exploration of pitfalls introduced in the system design
and learning process.

These pitfalls can be broadly categorized into three categories: data snooping, spurious
ACM Trans.

Softw.

Eng.

Methodol.
10 • Xinyu She, Yue Liu, Yanjie Zhao, Yiling He, Li Li, Chakkrit Tantithamthavorn, Zhan Qin, and Haoyu Wang
correlations, and inappropriate model design.

In the following, we provide comprehensive descriptions of these
three pitfalls.
```

### 0d9684287a79f05b

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The implications of these pitfalls (RQ3) are discussed in
Section 7, and in Section 8, we further discuss open challenges and promising research directions.

This organized
structure enables a comprehensive analysis of pitfalls and considerations across the entire LM4Code pipeline.

Our taxonomy aims to provide crucial insights for developing more robust, reliable, and practical LM systems for
code intelligence tasks.
3 DATA COLLECTION AND LABELING
The data-hungry language models require large-scale and high-quality training datasets.

According to a survey
by Houet al. [54], the majority of LMs for code intelligence are trained using data from open-source platforms,
with GitHub and StackOverflow being the most popular options.

However, the data in these platforms are
user-contributed, varying significantly in the level of quality and reliability.

It leads to non-negligible noises,
bias, and errors in the training dataset and further affects the behavior of the models, which brings significant
pitfalls in LMs for code intelligence.
```

### 247013ec6baa4e33

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 3 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Actually, introducing advanced pre-trained models like CodeBERT has
not eliminated these pitfalls.

Specifically, if not fine-tuned appropriately for downstream tasks, these models
might still overemphasize basic elements like keywords over richer code semantics [198].

Inappropriate Model Design:Inappropriate model design in LM4Code arises when the underlying architecture
fails to capture critical characteristics of code, such as hierarchy and composition.

The inability to construct robust
semanticrepresentationsofcode’sintricatestructuralandlogicalattributeshindersmodelefficacyondownstream
code intelligence tasks.

Such design shortcomings can manifest in several ways.

For instance, in vulnerability
detection, models may exhibit a significant overlap in the feature space between classes, hindering precise
vulnerability identification [15].

Code search models might lean on coarse-grained representations, capturing
merely lexical or structural elements, often overlooking the true functionality of the code [163].
```

### 91a40a4af6d5eccf

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 9 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Secondly, model nnsembling is gaining
traction, where the strengths of multiple models are leveraged to offset individual biases, as seen in the work by
Zhanget al. [198]whichemploysmultipleviewsofthesamedataformorerobustpredictions.

Lastly,regularization
and fine-tuning techniques play a pivotal role.

Regularization, such as dropout or L2 regularization, helps in
preventing overfitting, while fine-tuning allows pre-trained models, like CodeBERT, to adapt to specific dataset
nuances, as demonstrated by Fanget al. [33].

By integrating these strategies, models can be better positioned to
achieve superior outcomes.

Summary - System Design and Learning
In this study, we uncover 43 research studies related to pitfalls in system design and learning.

These pitfalls
can be categorized into three main categories: data snooping, spurious correlations, and inappropriate model
design, leading to overestimated performance and compromised efficacy of LM4Code Systems.
```

### 63b73457012267c6

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 2 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
In this section, we provide a brief description of related studies and discuss
the implications and potential solutions during the data collection and labeling stages.
3.1 RQ1-Pitfalls
From the collected papers, we identified 22 research studies focusing on pitfalls during the data collection and
labeling process.

Table 2 presents the statistics of literature on this topic, where the pitfalls can be grouped into
three main categories.

Unbalanced Distribution:Unbalanced distribution arises when there is a lack of proper randomization in
the selection of samples, leading to certain populations being underrepresented or overrepresented [135].

In
code-related scenarios, it usually refers to the gap between the sample distribution of real-world practices and
training datasets.

For example, as emphasized by [15, 144, 182], vulnerable instances in vulnerability detection
studies are overwhelming while neutral code instances in real-world environments considerably outnumber their
vulnerable counterparts.

This imbalance extends to other code-based tasks.
```

### 6d72b38d82a9cec3

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 22 |
| page_end | 23 |
| chunk_index | 48 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Liet al. [83] demonstrate that imitation models
can even exceed the performance of the victim model.

Additionally, when models are deployed on user clients,
they face the potential threat of reverse engineering.

Zhouet al. [200] highlight that the on-device models may
leak their confidential information, such as hyper-parameters and weights.

The risk of copyright infringement
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 23
and intellectual property theft not only undermines incentives to develop innovative models, but also threatens
the commercialization prospects and trustworthiness of the LM4Code industry.

These security vulnerabilities, encompassing both untrustworthy outputs and intellectual property risks, pose
significant challenges to the widespread adoption of LM4Code systems.

The combination of external attacks,
internal model limitations, and copyright concerns creates a complex security landscape that requires careful
attention.
```

### f15adeaa0d343f2e

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 21 |
| page_end | 21 |
| chunk_index | 40 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 21
Data Collection Phase:High-quality training data serves as the foundation for trustworthy model training, yet
inherent noise and errors can severely compromise model efficacy by causing models to learn irrelevant patterns
or establish spurious correlations.

Sunet al. [148] demonstrated that when code search models are trained
on carefully cleaned datasets, their performance improves significantly, with MRR rising from 0.407 to 0.512.

Similarly, Nieet al. [108] revealed that labeling errors can drastically reduce the performance of vulnerability
detection models, leading to an average F1 score drop of 20.7%.

These examples underscore the importance of
high-quality data for ensuring reliable model performance.

System Design Phase:Inappropriate model design directly compromises the efficacy of models in practical
scenarios.

For example, token sequence-based vulnerability detection models might fail to capture the underlying
causes of vulnerabilities and instead focus on surface-level patterns, leaving a significant margin for improvement.
```

### d044b1089f599fe6

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 2 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Liuet al. [95] and Shiet al. [139] emphasize that pitfalls can emerge from the data
processing processes such as test prefix generation or concurrent use of same-class data.

Spurious Correlations:Spurious correlations arise when language models mistakenly depend on irrelevant
artifacts rather than the intrinsic logic or intent of code for decision-making, leading to misleading associations.

The artifacts vary across SE tasks.

For instance, in vulnerability detection, artifacts may manifest as recurring
code patterns, semantic redundancy or reliance on specific function names that LMs incorrectly associate with
vulnerabilities[15,136,144].

Incodesummarization,modelsmightfocusmoreonstringsorcertaincodestructures
while overlooking elements key for developers [119].

When generating commit messages in the context of code
review, models often produce outputs that adhere to a few simple patterns, potentially failing to capture the
nuances of the actual code changes [28].
```

### 7f16a532b9759a15

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 8 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
While Shiet al. [140]
unravels how transformer-based models allocate attention for code summarization, Wanet al. [160] probes into
the nuances of attention during code-to-code translation.

These XAI approaches can serve to identify and rectify
model pitfalls, ensuring the reliability of LM4Code applications.

Model Optimization Strategies:In light of the pitfalls introduced by inappropriate model design, researchers
have turned to model optimization strategies to address and minimize their effects.

These strategies encompass
several techniques designed to enhance a model’s structure, training process, and generalization capabilities.

Firstly, model design adjustments involve refining the architecture to better capture data intricacies.

Studies
like that by Wanet al. [161] have demonstrated the benefits of introducing novel layers or structures to better
understand the tree structure of code, yielding improved performance.
```

### 187fbd5de9fc878c

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 7 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
While related research evaluating LM4Code [16, 93, 108, 178] identifies some issues, our
work distinguishes itself in two key ways: (1) we employ a rigorous SLR methodology that systematically
identifies and categorizes pitfalls, and (2) we present a comprehensive taxonomy structured around the entire
LLM lifecycle, from dataset construction to deployment.

This approach enables us to systematically analyze not
only the identified issues but also their corresponding solutions and practical impacts, providing an integrative
perspective that supports both researchers and practitioners in developing more reliable code intelligence systems.

Ensuring the robustness, reliability, and trustworthy deployment of LMs is important for their effective
integration into the software development lifecycle.

Consequently, it is crucial to discern the nature of these
pitfalls, comprehend their implications, and examine existing solutions.

Thus, we aim to answer the following
research questions in this study:
• RQ1: What types of pitfalls are prevalent in language models for code intelligence?
```

### e21d4c9a69b6a80d

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | discussion |
| section_title | 8 DISCUSSION |
| page_start | 24 |
| page_end | 25 |
| chunk_index | 7 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Ensuring that these models are robust and trustworthy is essential.

This does not just relate to their
prediction accuracy but extends to the reliability, interpretability, and generalization capacity of the model,
especially in diverse and evolving coding environments [111, 167].

Building Interpretable LM4Code.

The black-box nature of language models has been a long-term concern,
especially when LM4Code applications directly influence software development outcomes [22, 151, 167, 172].

Transparency in LM4Code requires an in-depth examination of the correlations and reasoning processes that
models depend on, instead of just knowing the model’s predictions.

Our review results show that pitfalls can
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 25
exist throughout the entire LM4Code lifecycle, potentially resulting in spurious correlations.

These misleading
correlations are based on wrong artifacts for generating predictions, presenting significant challenges for practical
real-world applications.
```

### 734a7fcf2cbba4e9

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 8 |
| page_end | 9 |
| chunk_index | 12 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Compared with the code snippets in open-source repositories, which can be
difficult to classify by task and slice accurately, such human-written code tasks are closer to the real user requests
in practice, which better reflects the performance of the model.

For instance, Linet al. [85] use a real-world
dataset composed of human-written programming exercises with multiple solutions.

Similarly, Mozannaret
al. [105, 106] uses user behavior data to demonstrate the effectiveness of their proposed methods.

ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 9
02468101214161820222426
2018201920202021202220232024
Nof Papers
Published Year
Inappropriate Model DesignSpurious CorrelationsData Snooping
Figure 6.
```

### c55d4bbedea5c375

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 18 |
| page_end | 19 |
| chunk_index | 30 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
This model boasts a lean
memory footprint, consuming just 6 MB of RAM — a significant 19x reduction compared to previous models.

It
can generate a single piece of code completion in a mere 8 ms and delivers an impressive 90% accuracy rate for
its top five suggestions.
6.2.3 Privacy and Copyright Protection.

The ability of large language models to memorize and reproduce training
dataraisescriticalprivacyandcopyrightconcerns.

Thus,developingeffectiveprotectionforprivacyandcopyright
has been widely investigated.

Privacy-preserving Techniques:The memorization and regeneration capabilities of large language models
raise critical privacy concerns that demand research attention.

Some state-of-the-art models like StarCoder
employed human annotators to mask any personal information such as keys and addresses present in the training
data, in an effort to mitigate privacy risks [77].

In addition, differential privacy techniques have emerged as
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 19
promising strategies for mitigating privacy risks.
```

### a26ce090645b26fd

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 5 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 3
2 1 2 10
05101520253035404550
2018201920202021202220232024
N of Papers
Published Year
(a) Distribution of papers over years
ICSE, 29
ASE, 15ISSTA, 12TSE, 14
FSE/ESEC, 11
TOSEM, 12
S&P, 4USENIX Security, 3ACL, 6SANER, 2 ISSRE, 2 Others, 10 (b) Distribution of papers across venues
Figure 1.

Overview of papers
• Insightful Findings and Recommendations.

In addition to identifying and analyzing pitfalls, we distilled
practical insights and recommendations for researchers and practitioners in the field of LM4Code.
```

### e556a06e05abdc0b

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 12 |
| page_end | 13 |
| chunk_index | 3 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
However, they argue that this assumption overlooks the continuous evolution
of software vulnerabilities and projects, leading to the Cross-Domain issue, where test sets should contain novel
vulnerabilities or projects.

Furthermore, Nonget al. [113] further reveal that vulnerability datasets like SARD [12]
ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 13
comprise unrealistic synthetic examples, which exhibit smaller vocabulary, smaller program length, and higher
pattern frequency compared to real-world code.

Zenget al. [192] claim that the state-of-the-art Just-in-Time
(JIT) defect prediction tool, CC2Vec [53], was only evaluated on a limited dataset with marginal improvements
to demonstrate generalizability and scalability.

Overall, common benchmarks in code-based research utilize
inappropriate test sets that fail to capture real-world complexities, leading to unrealistic performance evaluation.
```

### f70e48b81eb48682

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 8 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
This research
question aims to identify the prevalent pitfalls in LM4Code systems, exploring how they could affect
various stages of the learning-based system lifecycle.
• RQ2: What solutions have been proposed to address these pitfalls?

This research question reviews
the existing body of literature to identify proposed approaches for solving the identified pitfalls.

ACM Trans.

Softw.

Eng.

Methodol.
4 • Xinyu She, Yue Liu, Yanjie Zhao, Yiling He, Li Li, Chakkrit Tantithamthavorn, Zhan Qin, and Haoyu Wang
• RQ3: What are the implications of these pitfalls?
```

### 1e7857e3861e9475

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 19 |
| page_end | 20 |
| chunk_index | 34 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The implications highlight that real-world deployment introduces complex
challenges for LM4Code systems.
7 RQ3-IMPLICATIONS
The implications of pitfalls in LM4Code span across multiple dimensions, from direct technical impacts to
broader research validity concerns.

The ramifications of these pitfalls and biases extend beyond merely impacting
research performance and reproducibility from an evaluative standpoint.

They also contribute to misleading
benchmarksandpotentialsecurityvulnerabilitieswithinthegeneratedcode,whenviewedfromtheperspectiveof
content generation.

Furthermore, concerning research performance, a distinction can be made based on whether
the evaluation or the model itself is affected, leading to categories such as performance overestimation and
compromised model efficacy.

These implications collectively demonstrate how pitfalls encountered at various
stages of the lifecycle can undermine the reliability and practical applicability of LM4Code systems.

ACM Trans.

Softw.

Eng.
```

### 2650eec6c284fd61

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 0 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The performance evaluation stage focuses on precisely assessing and analyzing the model’s performance using
predefinedtestsetsandevaluationmetrics.

Additionally,comparativeperformanceevaluationagainstbenchmarks
provides insights into a model’s strengths and weaknesses on specific code-related tasks.

However, potential
pitfalls can emerge from factors such as improper baselines, test sets, and performance metrics.

These challenges
must be thoroughly examined and addressed to ensure that the evaluation is unbiased, comprehensive, and
representative of a model’s true capabilities.

Thus, this section provides a brief description of related studies and
discusses the implications and potential solutions during the performance evaluation stages.
5.1 RQ1-Pitfalls
Fromthecollectedstudies,weidentified35researchstudiesfocusingonpitfallsduringtheperformanceevaluation
phase.

We have methodically categorized the collected literature into four categories, as shown in Figure 8.
```

### da8b2a79f0f17e81

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
As LMs become increasingly prevalent in code intelligence despite increasing obstacles, there emerges an
urgent need for a comprehensive understanding of potential pitfalls within LM4Code systems.

This is not limited
to pitfall identification; it demands a deeper exploration into the understanding of the implications of these
pitfalls, current solutions, and possible challenges.

Although there is a growing body of research concerning or
addressing pitfalls in LM4Code [97, 143, 148, 191], the domain lacks a comprehensive and systematic overview of
theseefforts.

Withoutsuchanoverview,researchers,developers,andpractitionerspotentiallyoverlooksignificant
pitfalls identified in previous studies.

In this study, we conducted a systematic literature review, adhering to a
well-defined approach that identifies, evaluates, and interprets the relevant literature focusing on the pitfalls
within LM4Code.

Our contributions of this paper are as follows:
• Paper Collection of Pitfalls in LM4Code.
```

---

## 5. [cross_002_zh] PoisonedRAG 的攻击策略与 FlippedRAG 操纵 RAG 输出的方法有何不同？哪一种需要访问知识库？

**Type**: `comparison` | **Lang**: `ZH` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.0000 |
| 20 | 0.0000 | 0.0000 |

**Expected sources**: PoisonedRAG, FlippedRAG

### Expected Chunks (5)

### d1ccc0fbbc4bac4a

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 0 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
This paper is included in the Proceedings of the 
34th USENIX Security Symposium.
August 13–15, 2025 • Seattle, WA, USA
978-1-939133-52-6
Open access to the Proceedings of the 
34th USENIX Security Symposium is sponsored by USENIX.
PoisonedRAG: Knowledge Corruption Attacks  
to Retrieval-Augmented Generation of  
Large Language Models
Wei Zou and Runpeng Geng, Pennsylvania State University; Binghui Wang, 
Illinois Institute of Technology; Jinyuan Jia, Pennsylvania State University
https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag
PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation
of Large Language Models
Wei Zou⇤1, Runpeng Geng⇤1, Binghui Wang2, Jinyuan Jia1
1Pennsylvania State University,2Illinois Institute of Technology
1{weizou, kevingeng, jinyuan}@psu.edu,2bwang70@iit.edu
```

### 3438617a0d3fc203

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Based on this attack surface, we proposePoisonedRAG,
the ﬁrst knowledge corruption attack to RAG, where an at-
tacker could inject a few malicious texts into the knowledge
database of a RAG system to induce an LLM to generate an
attacker-chosen target answer for an attacker-chosen target
question.

We formulate knowledge corruption attacks as an
optimization problem, whose solution is a set of malicious
texts.

Depending on the background knowledge (e.g., black-
box and white-box settings) of an attacker on a RAG system,
we propose two solutions to solve the optimization problem,
respectively.

Our results showPoisonedRAG could achieve a
90% attack success rate when injectingﬁve malicious texts for
each target question into a knowledge database with millions
of texts.

We also evaluate several defenses and our results
show they are insufﬁcient to defend againstPoisonedRAG,
highlighting the need for new defenses.
```

### 8e93b4a44b56b30c

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 1 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Keywords
RAG; Black-box Adversarial Attack; Opinion Manipulation
ACM Reference Format:
Zhuo Chen, Yuyang Gong, Jiawei Liu, Miaokun Chen, Haotan Liu, Qikai 
Cheng, Fan Zhang, Wei Lu, and Xiaozhong Liu. 2025.

FlippedRAG: Black-
Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented 
Generation Models.

In Proceedings of the 2025 ACM SIGSAC Conference 
on Computer and Communications Security (CCS ’25), October 13–17, 2025, 
Taipei.

ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/ 
3719027.3765023
```

### 48c5ba99d2aa63ac

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Through carefully crafted
input, attackers can influence the orientation of content generated
by RAG models, thus jeopardizing users’ cognitive processes and
decision-making abilities.

This paper primarily investigates adversarial opinion manipula-
tion targeting the retriever in black-box RAG-like systems, which
aligns with realistic and practical scenarios.

The threat model pre-
sented here can be characterized as follows: the adversary can only
query the RAG-like system and does not have access to the complete
knowledge base or corpus, the retriever, or the parameters of the
RAG.

The attacker is only capable of injecting limited adversarially
modified candidate texts into the corpus, while the retriever and
the LLM remain black-boxed, intact, and unmodifiable.

To address aforementioned challenges, in this paper, we propose
FlippedRAG, a black-box attack method, to explore the reliabil-
ity of RAG in controversial topics and investigate its impact on
user cognition, as shown in Figure 1.
```

### f60a108c45b25e46

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Subsequently, based
on the constructed (query, candidate) pairs from retrieval list, we
train a surrogate model using the extracted retrieval data [19, 30]
to approximate and transparentize the relevance preferences of the
retriever in the black-box RAG model.

Based on this surrogate model, we develop an attack strategy
aimed at manipulating the opinions of candidate documents.

By
attacking this surrogate model, we generate adversarial opinion
manipulation triggers, which are then transferred to the target RAG
corpus, as shown in the right part of Figure 1.

We conduct experi-
ments on opinion datasets encompassing multiple topics to validate
the effectiveness and scope of the attack strategy without relying
on internal knowledge of the RAG model.

The experimental results
FlippedRAG: Black-Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented Generation Models CCS ’25, October 13–17, 2025, Taipei
Table 1: Comparison of existing RAG attacks.
```

### Retrieved Top-20

**#1** — 17261172cab602e9 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=27

```
However, since
both PoisonedRAG and FlippedRAG employ trigger insertion, the
compositions of their adversarial documents are similar after mask-
ing operations.

Additionally, because PoisonedRAG inserts the
query itself as the trigger, which enhances retrieval ranking more
effectively, the decline in PoisonedRAG’s attack success and opinion
manipulation success rate is somewhat smaller.

Our findings further reveal that the success rate of RAG attacks
continues to increase when the mask rate ra
```

**#2** — c2decbaa90066ccd | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.10-10 | sec=results | ci=12

```
We conducted a systematic comparative evaluation of Flippe-
dRAG’s manipulation efficacy against established black-box attack
baselines, with the quantitative results comprehensively tabulated
in Table 6.

Entries denoted by ’–’ in the table signify that the speci-
fied evaluation metric is inapplicable to the corresponding attack
methodology process.

The comparative experiment results indicate that both Poisone-
dRAG and FlippedRAG demonstrate superior efficacy in the opin-
ion manipulation ta
```

**#3** — 969318f3587628ef | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.12-12 | sec=results | ci=22

```
Figure 5: Distributions of log perplexity (PPL) calculated by GPT-2 on clean documents and attacked documents by FlippedRAG
and the baselines.
0.1 0.3 0.5 0.7 0.9
Mask Rate
100OMSR (%)
Ensemble Number: 5
PoisonedRAG
Disinformation
FlippedRAG
0.1 0.3 0.5 0.7 0.9
Mask Rate
100OMSR (%)
Ensemble Number: 20
PoisonedRAG
Disinformation
FlippedRAG
0.1 0.3 0.5 0.7 0.9
Mask Rate
100OMSR (%)
Ensemble Number: 50
PoisonedRAG
Disinformation
FlippedRAG
Figure 6: OMSR(%) under different mask rates and ensemble 
```

**#4** — 6585cf687f23e93e | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.10-10 | sec=results | ci=14

```
The enhanced efficacy of PoisonedRAG derives
from its retrieval optimization: injecting the question into docu-
ments, which maximizes the retrieval probability by exploiting
the semantic self-similarity.

In contrast, although FlippedRAG im-
proves adversarial document rankings through black-box retriever
imitation, its effectiveness remains suboptimal compared to exact
question-question matching paradigm.

The diminished efficacy of the PAT transfer-based method com-
pared to FlippedRAG can be
```

**#5** — d6519ccd05724012 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.12-12 | sec=results | ci=23

```
Our analysis indicates that, PoisonedRAG and Disinformation
generate adversarial documents with anomalously low perplexi-
ties that significantly deviate from normal data distributions.

This
phenomenon likely stems from their reliance on LLM-generated
adversarial documents.

Consequently, suboptimal LLM selection
would markedly increase the detectability of PoisonedRAG and Dis-
information through perplexity-based detection.

Both FlippedRAG
and other baselines exhibit perplexity levels compara
```

**#6** — fe491b7edf6060b7 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.12-12 | sec=results | ci=25

```
Attack Paraphrasing Manipulation
Performance
OMSR(%) ASV
Disinformation w/o 40.0
0.43
w/ 20.0 0.20
PAT Transfer-based w/o 43.3 0.50
w/ 30.0 0.30
PoisonedRAG w/o 56.7 0.76
w/ 43.3 0.53
FlippedRAG w/o 63.3 0.70
w/ 40.0 0.43
Given that paraphrasing primarily targets the retrieval phase, the
comparative analysis excludes prompt injection attacks and static
text manipulation, as they exclusively focus on the generation.

We
also exclude the evaluation of GARAG for its inefficacy in opinion
manipulati
```

**#7** — 8732de68b501b72b | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=29

```
This discrepancy arises because RobustRAG was specif-
ically designed as a mitigation method against attacks on factoid
and closed-ended questions, where poisoned documents typically
contain a single specific incorrect answer.

However, FlippedRAG
targets opinion-level manipulation, where a single passage may con-
tain multiple terms or phrases with inherent opinion biases.

These
opinion-laden terms are quantitatively more prevalent, enabling
them to persistently influence the LLM’s output.

Fl
```

**#8** — 0ab16fa7873b1838 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.4-5 | sec=method | ci=3

```
Modifying the prompt templates used by the LLM in RAG is also
prohibited.

Targeted traps necessitate adversary selection of contro-
versial topics for manipulation, so adversaries possess awareness
of user query intents input to the target retriever in RAG.

FlippedRAG: Black-Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented Generation Models CCS ’25, October 13–17, 2025, Taipei
Figure 3: The framework for obtaining ranking imitation
data of retrieval model and constructing co
```

**#9** — b341292a2dbb629d | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=32

```
Privacy leakage detection based on LLMs and prompt engineer-
ing exhibits inherent vulnerabilities, enabling attackers to itera-
tively refine malicious instructions until identifying blind spots in
detection mechanisms or overwriting defensive prompts to achieve
context extraction.

Consequently, such detection demonstrates lim-
ited efficacy against FlippedRAG.

Our research findings provide critical insights for designers of
RAG-like applications.

Context disclosure vulnerabilities must be
p
```

**#10** — 9633acf1869ed77d | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.12-12 | sec=results | ci=24

```
The keyword density of adversarial documents generated by
FlippedRAG and other baselines is comparable to that of natural
documents in clean data.

In contrast, the keyword density of docu-
ments generated by PoisonedRAG is significantly higher than that
of natural documents, making PoisonedRAG more susceptible to
being filtered out by search engine SEO review mechanisms.
5.4.4 Mitigation Based on Paraphrasing.

Cheng et al. [6] and Zou
et al. [42] attempt to employ paraphrasing defense to test 
```

**#11** — a20e9e907b657a95 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.12-13 | sec=results | ci=26

```
Poisone-
dRAG demonstrates a less reduction in attack effectiveness under
paraphrasing defense attributed to the direct insertion of queries.
5.4.5 Mitigation Based on Randomized Mask Smoothing.

Random-
ized smoothing is a defense method aiming at achieving certified
robustness against adversarial examples.

It constructs a smoothed
composite function by introducing random variables to the original
function or the model, enabling the certification of its robustness
FlippedRAG: Black-Box Opinion
```

**#12** — 0c320ee74c198ef8 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.10-10 | sec=results | ci=13

```
In the generation
phase, PoisonedRAG leverages LLMs to synthesize content engi-
neered to steer target systems, while FlippedRAG adopts a minimal
data perturbation strategy by curating opinion-specific documents
that guide RAG systems to extrapolate desired stances through
Table 7: The controlled user experimental results on opinion
manipulation in controversial topics.

Mean ±SD represents
the arithmetic mean and standard deviation of user opinion
polarity values. * denotes statistical signific
```

**#13** — 20e8798b71cb4c4c | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.10-10 | sec=results | ci=11

```
Target
Attack Method Retriever Opinion
𝑇𝑜𝑝3𝑣 𝑅𝐴𝑆𝑅% 𝑂𝑀𝑆𝑅% 𝐴𝑆𝑉
Pro
Pr
ompt Injection Attack – – 26.67 0.03
Disinformation 0.26 – 40.00 0.43
Static Text – – 40.00 0.40
Disinformation + Static text 0.26 – 46.67 0.53
PAT Transfer-based 0.31 70.73 43.33 0.50
GARAG 0.02 2.40 10.00 0.03
PoisonedRAG 0.46 – 56.67 0.76
FlippedRAG 0.37 74.22 63.33 0.70
Con
Prompt
Injection Attack – – 50.00 0.47
Disinformation 0.21 – 36.67 0.33
Static Text – – 26.67 0.17
Disinformation + Static text 0.21 – 43.33 0.47
PAT Tra
```

**#14** — bf0262ddc5f7745a | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.11-11 | sec=results | ci=20

```
Documents
K
eyword Density(%)
Overall Window size
20 50 100
Prompt
Injection Attack 4.75 10.37 6.29 5.12
Disinformation 5.28 7.67 5.28 5.28
Static Text 4.49 10.42 6.33 4.94
PAT Transfer-based 6.16 13.03 8.38 6.64
GARAG 4.39 10.00 6.04 4.78
PoisonedRAG 18.39 52.90 24.41 18.39
FlippedRAG 6.35 13.23 8.51 6.82
Clean 4.39
10.01 6.04 4.78
calculate the probability of these adversarial documents being de-
tected as spam by the spamicity detection system under various
thresholds, referred to as the dete
```

**#15** — 49c86881d9dc051e | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.8-8 | sec=results | ci=4

```
After the black-box imitation training, we conduct opinion manip-
ulation experiments across different RAGblack (based on Llama-3,
Mixtral, or Vicuna) with FlippedRAG.

We also conducted a com-
parative evaluation of FlippedRAG against established baselines to
assess its relative efficacy in executing opinion manipulation on
black-box RAG architectures.

As shown in Table 4, FlippedRAG achieves a significant opinion
manipulation effect on all three LLMs.

As a whole, it has a 40% –
50% chance of
```

**#16** — 16d3697f23e556ed | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=28

```
Consequently, it is not advisable to employ
randomized mask smoothing as a defense against FlippedRAG in
practical RAG-like applications.
5.4.6 Mitigation Based on RobustRAG.

RobustRAG, proposed by
Xiang et al. [31], represents a defense framework specifically tar-
geting retrieval poisoning attacks in RAG systems.

It employs an
isolate-then-aggregate strategy that leverages the inherent work-
flow characteristics of RAG architectures to defend against data
poisoning attacks.

More detail is i
```

**#17** — 79af396f8a18b8e1 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.3-4 | sec=introduction | ci=9

```
Our major contributions are as follows:
• We proposePoisonedRAG, theﬁrst knowledge corrup-
tion attack that exploit the new attack surface introduced
by knowledge databases of RAG systems.
• Our major contribution is to derive two necessary condi-
tions for an effective attack to RAG systems.

We further
design PoisonedRAG to achieve these two conditions.
• We conduct an extensive evaluation forPoisonedRAG
on multiple knowledge databases, retrievers, RAG
schemes, and LLMs.

Additionally, we comp
```

**#18** — 77e4304dd6d218e0 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.10-10 | sec=experiment | ci=14

```
For instance, in the black-box setting,PoisonedRAG
could achieve 97% (on NQ), 99% (on HotpotQA), and 91%
(on MS-MARCO) ASRs for RAG with PaLM 2.

Our experi-
mental results demonstrate that RAG is extremely vulnerable
to our knowledge corruption attacks.

Second, PoisonedRAG
achieves high F1-Scores under different settings, e.g., larger
than 90% in almost all cases.

The results demonstrate that the
malicious texts crafted byPoisonedRAG are very likely to be
retrieved for target questions, which
```

**#19** — c7a2c0478648a29f | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.3-4 | sec=method | ci=0

```
3.1 Overview
Our objective is to manipulate the opinions expressed in the re-
sponses generated by black-box RAG models on controversial topics.

We mainly focus on the retrieval component, where manipulated
ranking outcomes propagate to bias the LLM’s output generation.

Zhang et al. [36] attempted to poison context documents to mislead
the LLM into generating incorrect content.

However, this approach
necessitates extensive internal details of the LLM application, ren-
dering it less feasible 
```

**#20** — 9a9724b42d43ce28 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.10-10 | sec=experiment | ci=18

```
Dataset Attack Metrics
ASR F1-Score
NQ
Naive Attack 0.03 1.0
Corpus Poisoning Attack 0.01 0.99
Disinformation Attack 0.69 0.48
Prompt Injection Attack 0.62 0.73
GCG Attack 0.02 0.0
PoisonedRAG (Black-Box) 0.97 0.96
PoisonedRAG (White-Box) 0.97 1.0
HotpotQA
Naive Attack 0.06 1.0
Corpus Poisoning Attack 0.01 1.0
Disinformation Attack 1.0 0.99
Prompt Injection Attack 0.93 0.99
GCG Attack 0.01 0.0
PoisonedRAG (Black-Box) 0.99 1.0
PoisonedRAG (White-Box) 0.94 1.0
MS-MARCO
Naive Attack 0.02 1.0
Corpus
```

### Missed Chunks (5 — expected but NOT in top-20)

### d1ccc0fbbc4bac4a

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 0 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
This paper is included in the Proceedings of the 
34th USENIX Security Symposium.
August 13–15, 2025 • Seattle, WA, USA
978-1-939133-52-6
Open access to the Proceedings of the 
34th USENIX Security Symposium is sponsored by USENIX.
PoisonedRAG: Knowledge Corruption Attacks  
to Retrieval-Augmented Generation of  
Large Language Models
Wei Zou and Runpeng Geng, Pennsylvania State University; Binghui Wang, 
Illinois Institute of Technology; Jinyuan Jia, Pennsylvania State University
https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag
PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation
of Large Language Models
Wei Zou⇤1, Runpeng Geng⇤1, Binghui Wang2, Jinyuan Jia1
1Pennsylvania State University,2Illinois Institute of Technology
1{weizou, kevingeng, jinyuan}@psu.edu,2bwang70@iit.edu
```

### 3438617a0d3fc203

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Based on this attack surface, we proposePoisonedRAG,
the ﬁrst knowledge corruption attack to RAG, where an at-
tacker could inject a few malicious texts into the knowledge
database of a RAG system to induce an LLM to generate an
attacker-chosen target answer for an attacker-chosen target
question.

We formulate knowledge corruption attacks as an
optimization problem, whose solution is a set of malicious
texts.

Depending on the background knowledge (e.g., black-
box and white-box settings) of an attacker on a RAG system,
we propose two solutions to solve the optimization problem,
respectively.

Our results showPoisonedRAG could achieve a
90% attack success rate when injectingﬁve malicious texts for
each target question into a knowledge database with millions
of texts.

We also evaluate several defenses and our results
show they are insufﬁcient to defend againstPoisonedRAG,
highlighting the need for new defenses.
```

### 8e93b4a44b56b30c

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 1 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Keywords
RAG; Black-box Adversarial Attack; Opinion Manipulation
ACM Reference Format:
Zhuo Chen, Yuyang Gong, Jiawei Liu, Miaokun Chen, Haotan Liu, Qikai 
Cheng, Fan Zhang, Wei Lu, and Xiaozhong Liu. 2025.

FlippedRAG: Black-
Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented 
Generation Models.

In Proceedings of the 2025 ACM SIGSAC Conference 
on Computer and Communications Security (CCS ’25), October 13–17, 2025, 
Taipei.

ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/ 
3719027.3765023
```

### 48c5ba99d2aa63ac

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Through carefully crafted
input, attackers can influence the orientation of content generated
by RAG models, thus jeopardizing users’ cognitive processes and
decision-making abilities.

This paper primarily investigates adversarial opinion manipula-
tion targeting the retriever in black-box RAG-like systems, which
aligns with realistic and practical scenarios.

The threat model pre-
sented here can be characterized as follows: the adversary can only
query the RAG-like system and does not have access to the complete
knowledge base or corpus, the retriever, or the parameters of the
RAG.

The attacker is only capable of injecting limited adversarially
modified candidate texts into the corpus, while the retriever and
the LLM remain black-boxed, intact, and unmodifiable.

To address aforementioned challenges, in this paper, we propose
FlippedRAG, a black-box attack method, to explore the reliabil-
ity of RAG in controversial topics and investigate its impact on
user cognition, as shown in Figure 1.
```

### f60a108c45b25e46

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Subsequently, based
on the constructed (query, candidate) pairs from retrieval list, we
train a surrogate model using the extracted retrieval data [19, 30]
to approximate and transparentize the relevance preferences of the
retriever in the black-box RAG model.

Based on this surrogate model, we develop an attack strategy
aimed at manipulating the opinions of candidate documents.

By
attacking this surrogate model, we generate adversarial opinion
manipulation triggers, which are then transferred to the target RAG
corpus, as shown in the right part of Figure 1.

We conduct experi-
ments on opinion datasets encompassing multiple topics to validate
the effectiveness and scope of the attack strategy without relying
on internal knowledge of the RAG model.

The experimental results
FlippedRAG: Black-Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented Generation Models CCS ’25, October 13–17, 2025, Taipei
Table 1: Comparison of existing RAG attacks.
```

### False Positives (20 — in top-20 but NOT expected)

### 17261172cab602e9

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 27 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
However, since
both PoisonedRAG and FlippedRAG employ trigger insertion, the
compositions of their adversarial documents are similar after mask-
ing operations.

Additionally, because PoisonedRAG inserts the
query itself as the trigger, which enhances retrieval ranking more
effectively, the decline in PoisonedRAG’s attack success and opinion
manipulation success rate is somewhat smaller.

Our findings further reveal that the success rate of RAG attacks
continues to increase when the mask rate ranges from 0% to 30%.

This suggests that RAG attacks like FlippedRAG exhibit a certain
degree of robustness against randomized mask smoothing defenses.

However, when the mask rate exceeds 50%, the attack success rate
shows a more pronounced decline.

However, an excessively high
mask rate may significantly impair the ranking capability of the
RAG system, making it difficult for the retrieval model to pro-
duce accurate rankings.
```

### c2decbaa90066ccd

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 12 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
We conducted a systematic comparative evaluation of Flippe-
dRAG’s manipulation efficacy against established black-box attack
baselines, with the quantitative results comprehensively tabulated
in Table 6.

Entries denoted by ’–’ in the table signify that the speci-
fied evaluation metric is inapplicable to the corresponding attack
methodology process.

The comparative experiment results indicate that both Poisone-
dRAG and FlippedRAG demonstrate superior efficacy in the opin-
ion manipulation task, with PoisonedRAG exhibiting marginally
enhanced performance compared to FlippedRAG.

While Prompt In-
jection Attack, Disinformation, Static Text, "Disinformation + Static
text", and PAT transfer-based attack achieve moderate effectiveness
in opinion manipulation, GARAG manifests the most suboptimal
performance within this adversarial task paradigm.

The superior performance of PoisonedRAG and FlippedRAG
stems from their targeted optimizations of critical components in
the RAG workflow: retrieval and generation.
```

### 969318f3587628ef

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 22 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Figure 5: Distributions of log perplexity (PPL) calculated by GPT-2 on clean documents and attacked documents by FlippedRAG
and the baselines.
0.1 0.3 0.5 0.7 0.9
Mask Rate
100OMSR (%)
Ensemble Number: 5
PoisonedRAG
Disinformation
FlippedRAG
0.1 0.3 0.5 0.7 0.9
Mask Rate
100OMSR (%)
Ensemble Number: 20
PoisonedRAG
Disinformation
FlippedRAG
0.1 0.3 0.5 0.7 0.9
Mask Rate
100OMSR (%)
Ensemble Number: 50
PoisonedRAG
Disinformation
FlippedRAG
Figure 6: OMSR(%) under different mask rates and ensemble numbers for FlippedRAG and the baselines.
et al.[28] utilized perplexity calculated by GPT-2 in an attempt to
distinguish between synthetic text and natural text.

We utilized GPT-2 to measure the perplexity of documents in
clean data, documents attacked by the baselines, and documents
attacked by FlippedRAG.

The distributions are depicted in Figure 5.
```

### 6585cf687f23e93e

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 14 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
The enhanced efficacy of PoisonedRAG derives
from its retrieval optimization: injecting the question into docu-
ments, which maximizes the retrieval probability by exploiting
the semantic self-similarity.

In contrast, although FlippedRAG im-
proves adversarial document rankings through black-box retriever
imitation, its effectiveness remains suboptimal compared to exact
question-question matching paradigm.

The diminished efficacy of the PAT transfer-based method com-
pared to FlippedRAG can be attributed to its lack of a black-box
retriever imitation process.

Both Prompt Injection Attack and Static
Text exclusively target the generation phase while neglecting the
retrieval in RAG architectures, leading to significant performance
degradation when migrating LLM-targeted attack strategies to
RAG scenarios.

Although Disinformation fundamentally remains a
generation-optimized attack method, its approach of constructing
biased content based on the question nevertheless achieves par-
tial retrieval prioritization enhancements.
```

### d6519ccd05724012

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 23 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Our analysis indicates that, PoisonedRAG and Disinformation
generate adversarial documents with anomalously low perplexi-
ties that significantly deviate from normal data distributions.

This
phenomenon likely stems from their reliance on LLM-generated
adversarial documents.

Consequently, suboptimal LLM selection
would markedly increase the detectability of PoisonedRAG and Dis-
information through perplexity-based detection.

Both FlippedRAG
and other baselines exhibit perplexity levels comparable to clean
data distributions, rendering them resistant to perplexity detection.
5.4.3 Mitigation Based on Keyword Density.

Keyword density, which
is a measure of how often a certain keyword or phrase appears,
is a critical factor in SEO as high keyword densities make spam
pages more relevant to the user query.

Given that the RAG attack
scenario involves manipulation during the search phase, we also
employed keyword density to detect the RAG attack in Table 9.
```

### fe491b7edf6060b7

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 25 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Attack Paraphrasing Manipulation
Performance
OMSR(%) ASV
Disinformation w/o 40.0
0.43
w/ 20.0 0.20
PAT Transfer-based w/o 43.3 0.50
w/ 30.0 0.30
PoisonedRAG w/o 56.7 0.76
w/ 43.3 0.53
FlippedRAG w/o 63.3 0.70
w/ 40.0 0.43
Given that paraphrasing primarily targets the retrieval phase, the
comparative analysis excludes prompt injection attacks and static
text manipulation, as they exclusively focus on the generation.

We
also exclude the evaluation of GARAG for its inefficacy in opinion
manipulation.

The attack effectiveness of FlippedRAG and other baselines
against paraphrasing is presented in Table 10.

Both the baselines
and FlippedRAG exhibit a decline in attack effectiveness when con-
fronted with paraphrasing, yet PoisonedRAG’s and FlippedRAG’s
overall attack performance remains notably significant.
```

### 8732de68b501b72b

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 29 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
This discrepancy arises because RobustRAG was specif-
ically designed as a mitigation method against attacks on factoid
and closed-ended questions, where poisoned documents typically
contain a single specific incorrect answer.

However, FlippedRAG
targets opinion-level manipulation, where a single passage may con-
tain multiple terms or phrases with inherent opinion biases.

These
opinion-laden terms are quantitatively more prevalent, enabling
them to persistently influence the LLM’s output.

FlippedRAG demonstrates superior manipulation efficacy against
the RobustRAG defense framework compared to other baseline
methods.

The significantly diminished adversarial performance of
PoisonedRAG likely stems from its reliance on LLM-generated steer-
ing content to bias RAG outputs.

Prompt injection attack exhibits
the poorest performance against RobustRAG, with near-negligible
success rates.
```

### 0ab16fa7873b1838

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | method |
| section_title | 3.2 Threat Model |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 3 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Modifying the prompt templates used by the LLM in RAG is also
prohibited.

Targeted traps necessitate adversary selection of contro-
versial topics for manipulation, so adversaries possess awareness
of user query intents input to the target retriever in RAG.

FlippedRAG: Black-Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented Generation Models CCS ’25, October 13–17, 2025, Taipei
Figure 3: The framework for obtaining ranking imitation
data of retrieval model and constructing contrastive pairs in
black-box RAG.

Following [4, 6, 27, 42], FlippedRAG presents realistic threats
to RAG-like systems using data from public platforms that allow
user edits.

Adversaries can compromise RAG output objectivity
by injecting malicious modifications into knowledge sources in-
cluding Wikipedia, user-generated content (UGC) platforms, and
other publicly accessible web resources.
```

### b341292a2dbb629d

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 32 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Privacy leakage detection based on LLMs and prompt engineer-
ing exhibits inherent vulnerabilities, enabling attackers to itera-
tively refine malicious instructions until identifying blind spots in
detection mechanisms or overwriting defensive prompts to achieve
context extraction.

Consequently, such detection demonstrates lim-
ited efficacy against FlippedRAG.

Our research findings provide critical insights for designers of
RAG-like applications.

Context disclosure vulnerabilities must be
prioritized for mitigation.

Failure to address these vulnerabilities
enables attackers to exploit leaked context data, even in black-
box systems, exposing the knowledge of internal components and
ultimately enabling manipulation attacks.
5.4.8 Mitigation Analysis Conclusion.

FlippedRAG exhibits pro-
nounced adversarial resilience against existing defense mechanisms.

In contrast, PoisonedRAG’s reliance on simple heuristic approaches,
e.g., keyword stuffing, renders it vulnerable to SEO detection meth-
ods.
```

### 9633acf1869ed77d

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 24 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
The keyword density of adversarial documents generated by
FlippedRAG and other baselines is comparable to that of natural
documents in clean data.

In contrast, the keyword density of docu-
ments generated by PoisonedRAG is significantly higher than that
of natural documents, making PoisonedRAG more susceptible to
being filtered out by search engine SEO review mechanisms.
5.4.4 Mitigation Based on Paraphrasing.

Cheng et al. [6] and Zou
et al. [42] attempt to employ paraphrasing defense to test the ef-
fectiveness of the RAG attack they proposed.

The implementation
detail of paraphrasing in our experiment is in Appendix B.5.

Table 10: Manipulation effect of the baselines and Flippe-
dRAG against paraphrasing defense. w/o and w/ denote with-
out and with, respectively.
```

### a20e9e907b657a95

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 12 |
| page_end | 13 |
| chunk_index | 26 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Poisone-
dRAG demonstrates a less reduction in attack effectiveness under
paraphrasing defense attributed to the direct insertion of queries.
5.4.5 Mitigation Based on Randomized Mask Smoothing.

Random-
ized smoothing is a defense method aiming at achieving certified
robustness against adversarial examples.

It constructs a smoothed
composite function by introducing random variables to the original
function or the model, enabling the certification of its robustness
FlippedRAG: Black-Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented Generation Models CCS ’25, October 13–17, 2025, Taipei
under certain conditions.

We explore randomized mask smoothing
as a defense mechanism to counteract RAG attacks in Figure 6.

More detail is provided in Appendix B.5.

The experimental results indicate that both PoisonedRAG and
FlippedRAG experience a slight decline in attack effectiveness when
confronted with randomized masking smoothing.
```

### 0c320ee74c198ef8

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 13 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
In the generation
phase, PoisonedRAG leverages LLMs to synthesize content engi-
neered to steer target systems, while FlippedRAG adopts a minimal
data perturbation strategy by curating opinion-specific documents
that guide RAG systems to extrapolate desired stances through
Table 7: The controlled user experimental results on opinion
manipulation in controversial topics.

Mean ±SD represents
the arithmetic mean and standard deviation of user opinion
polarity values. * denotes statistical significance at p < 0.05.

Topic
Target Subject Mean ±SD
Genetically Mo
dified
Organisms Pro↑ Control 4.88±1.25
Experimental 5.55±1.05*
Corporate
Income
Tax Con↓ Control 3.59±1.30
Experimental 2.70±1.13*
Medical
Aid
in Dying Con↓ Control 4.70±1.85
Experimental 2.66±1.66*
summarization.
```

### 20e8798b71cb4c4c

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 11 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Target
Attack Method Retriever Opinion
𝑇𝑜𝑝3𝑣 𝑅𝐴𝑆𝑅% 𝑂𝑀𝑆𝑅% 𝐴𝑆𝑉
Pro
Pr
ompt Injection Attack – – 26.67 0.03
Disinformation 0.26 – 40.00 0.43
Static Text – – 40.00 0.40
Disinformation + Static text 0.26 – 46.67 0.53
PAT Transfer-based 0.31 70.73 43.33 0.50
GARAG 0.02 2.40 10.00 0.03
PoisonedRAG 0.46 – 56.67 0.76
FlippedRAG 0.37 74.22 63.33 0.70
Con
Prompt
Injection Attack – – 50.00 0.47
Disinformation 0.21 – 36.67 0.33
Static Text – – 26.67 0.17
Disinformation + Static text 0.21 – 43.33 0.47
PAT Transfer-based 0.27 71.93 40.00 0.27
GARAG 0.00 1.67 13.33 0.07
PoisonedRAG 0.47 – 66.67 0.83
FlippedRAG 0.37 78.26 53.33 0.70
its opinion in the response.

However, the manipulation effect varies
across different themes.

The detailed discussion is in Appendix B.3.
```

### bf0262ddc5f7745a

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 20 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Documents
K
eyword Density(%)
Overall Window size
20 50 100
Prompt
Injection Attack 4.75 10.37 6.29 5.12
Disinformation 5.28 7.67 5.28 5.28
Static Text 4.49 10.42 6.33 4.94
PAT Transfer-based 6.16 13.03 8.38 6.64
GARAG 4.39 10.00 6.04 4.78
PoisonedRAG 18.39 52.90 24.41 18.39
FlippedRAG 6.35 13.23 8.51 6.82
Clean 4.39
10.01 6.04 4.78
calculate the probability of these adversarial documents being de-
tected as spam by the spamicity detection system under various
thresholds, referred to as the detection rate.

Under all threshold conditions, the detection rate of triggers
generated by FlippedRAG is significantly lower than those gen-
erated by PoisonedRAG and exhibits minimal divergence from
those observed in clean data.

While other baselines demonstrate
consistently low detection rates across experimental thresholds,
PoisonedRAG exhibited persistently the highest detection rates.
```

### 49c86881d9dc051e

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 4 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
After the black-box imitation training, we conduct opinion manip-
ulation experiments across different RAGblack (based on Llama-3,
Mixtral, or Vicuna) with FlippedRAG.

We also conducted a com-
parative evaluation of FlippedRAG against established baselines to
assess its relative efficacy in executing opinion manipulation on
black-box RAG architectures.

As shown in Table 4, FlippedRAG achieves a significant opinion
manipulation effect on all three LLMs.

As a whole, it has a 40% –
50% chance of successful opinion flipping and realizes about 0.46 in
the opinion polarity shift of range 0 to 2.

Moreover, it reveals that
FlippedRAG based on 𝑀𝐶𝑜𝑛𝑡𝑟𝑖𝑒𝑣𝑒𝑟 and 𝑀𝐴𝑁𝐶𝐸 are more effective
in manipulating the RAG opinion with relatively higher OMSR
and ASV values.

That is because these attacks exhibit superior
performance on ranking distortion.

We also observe that the impact of FlippedRAG varies in opin-
ion manipulation effectiveness across different LLMs.
```

### 16d3697f23e556ed

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 28 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Consequently, it is not advisable to employ
randomized mask smoothing as a defense against FlippedRAG in
practical RAG-like applications.
5.4.6 Mitigation Based on RobustRAG.

RobustRAG, proposed by
Xiang et al. [31], represents a defense framework specifically tar-
geting retrieval poisoning attacks in RAG systems.

It employs an
isolate-then-aggregate strategy that leverages the inherent work-
flow characteristics of RAG architectures to defend against data
poisoning attacks.

More detail is in Appendix B.5.

The manipulation success rates of FlippedRAG and other base-
lines against RobustRAG defense is presented in Table 11.

Under Ro-
bustRAG mitigation, the OMSR of FlippedRAG decreases compared
to scenarios without defensive mechanisms, yet still maintains a
success rate reaching approximately 40%, significantly higher than
the attack success rates reported by Xiang et al. [ 31] for factoid
questions.
```

### 79af396f8a18b8e1

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 9 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Our major contributions are as follows:
• We proposePoisonedRAG, theﬁrst knowledge corrup-
tion attack that exploit the new attack surface introduced
by knowledge databases of RAG systems.
• Our major contribution is to derive two necessary condi-
tions for an effective attack to RAG systems.

We further
design PoisonedRAG to achieve these two conditions.
• We conduct an extensive evaluation forPoisonedRAG
on multiple knowledge databases, retrievers, RAG
schemes, and LLMs.

Additionally, we compare
PoisonedRAG with 5 baselines.
• We explore several defenses against PoisonedRAG.
3828    34th USENIX Security Symposium USENIX Association
```

### 77e4304dd6d218e0

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | experiment |
| section_title | 5.1 Experimental Setup |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 14 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
For instance, in the black-box setting,PoisonedRAG
could achieve 97% (on NQ), 99% (on HotpotQA), and 91%
(on MS-MARCO) ASRs for RAG with PaLM 2.

Our experi-
mental results demonstrate that RAG is extremely vulnerable
to our knowledge corruption attacks.

Second, PoisonedRAG
achieves high F1-Scores under different settings, e.g., larger
than 90% in almost all cases.

The results demonstrate that the
malicious texts crafted byPoisonedRAG are very likely to be
retrieved for target questions, which is also the reason why
PoisonedRAG could achieve high ASRs.

Third, in most cases,
PoisonedRAG is more effective in the white-box setting com-
pared to the black-box setting.
```

### c7a2c0478648a29f

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | method |
| section_title | 3 Methodology |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
3.1 Overview
Our objective is to manipulate the opinions expressed in the re-
sponses generated by black-box RAG models on controversial topics.

We mainly focus on the retrieval component, where manipulated
ranking outcomes propagate to bias the LLM’s output generation.

Zhang et al. [36] attempted to poison context documents to mislead
the LLM into generating incorrect content.

However, this approach
necessitates extensive internal details of the LLM application, ren-
dering it less feasible in real-world scenarios.

In the black-box RAG
context, the attacker lacks access to internal information of the RAG,
CCS ’25, October 13–17, 2025, Taipei Zhuo Chen et al.

Figure 2: The overview of FlippedRAG for manipulating the opinions of RAG-generated content under black-box setting.
including model architecture and scoring functions, and can only
interact with the inputs and outputs of the RAG.

Specifically, the at-
tacker can only use the interface of the RAG and not directly access
the retriever.
```

### 9a9724b42d43ce28

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | experiment |
| section_title | 5.1 Experimental Setup |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 18 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Dataset Attack Metrics
ASR F1-Score
NQ
Naive Attack 0.03 1.0
Corpus Poisoning Attack 0.01 0.99
Disinformation Attack 0.69 0.48
Prompt Injection Attack 0.62 0.73
GCG Attack 0.02 0.0
PoisonedRAG (Black-Box) 0.97 0.96
PoisonedRAG (White-Box) 0.97 1.0
HotpotQA
Naive Attack 0.06 1.0
Corpus Poisoning Attack 0.01 1.0
Disinformation Attack 1.0 0.99
Prompt Injection Attack 0.93 0.99
GCG Attack 0.01 0.0
PoisonedRAG (Black-Box) 0.99 1.0
PoisonedRAG (White-Box) 0.94 1.0
MS-MARCO
Naive Attack 0.02 1.0
Corpus Poisoning Attack 0.03 0.97
Disinformation Attack 0.57 0.36
Prompt Injection Attack 0.71 0.75
GCG Attack 0.02 0.0
PoisonedRAG (Black-Box) 0.91 0.89
PoisonedRAG (White-Box) 0.90 0.94
Table 5: Impact of retriever in RAG on PoisonedRAG.
```

---

## 6. [single_001_zh] DnD 反编译 DNN 二进制文件的核心工作流程包括哪些主要步骤？

**Type**: `method` | **Lang**: `ZH` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.0000 |
| 20 | 0.0000 | 0.0000 |

**Expected sources**: DnD

### Expected Chunks (5)

### 9bdf3eaa138e61a4

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 9 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
To check the property (iii), after reaching the DNN oper-
ator’s most outer loop’s exit point (e.g., Line 2 in Figure 3b),
DND inspects each IV’s corresponding register to check if
its register is updated with a constant (i.e., step size).

At last,
DNDconsidersanIVcandidateasanIVwhenitsatisﬁesboth
properties (ii) and (iii) (Line 18).

Finally,DND recovers IVs’ initial values, step sizes, and
loopcounts(Line19).

Inparticular,loopcountsarecomputed
from initial values, step sizes, and the collected loop exit con-
ditions.

For example, the initial value, step size and loop exit
conditions ofi in Figure 3b are 0, 1, andi<2, respectively.

Then, the loop count is derived by inquiring the solver with
these information.
```

### 20ac523f29224b53

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 6 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the break edges (denoting the edges in CFG that
jump out of the current loop).
```

### 16dc5ceb2dad79e0

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how to identify IVs using the
aforementioned three properties by symbolically executing
each DNN operator from its entry point to its exit point (Line
2,16-17).

Leveragingtheproperty(i), DND symbolizesevery
general register initialized by a constant in the loop’s entry
block (Line 10-12).
```

### 1fba7167150e9c4c

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 10 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Algorithm 1Loop analysis
1: procedureLOOPANALYSIS(op: operator)
2: symEngine ← SymbolicEngine(op.entryAddr)
3: candidates←ç
4: while symEngine.hasActive()do
5: symEngine.step()
6: for eachstate∈ symEngine.statesdo
7: inst ← state.lastInst
8: addr ← state.addr
9: if addr ∈ op.entryBlocks then
10: if isRegWrite(inst)andisConstant(inst.writeVal)then
11: inst.writeVal← createSym()
12: candidates.add((addr, inst.writeReg))
13: if addr ∈ op.breakEdgeSrcAddrthen
14: symEngine.record(state.branch.condition.get_IV())
15: symEngine.keep(getBreakState(state.succ))
16: if addr ∉ op.addrRangethen
17: symEngine.stash(state)
18: IVs ← checkConditionAndUpdate(candidates)
19: IVs.getLoopCount()
20: ReturnIVs
5.2.2 Symbolic Expression Extraction
ADNNoperatortypicallyperformstensorcomputation,which
takes its input and parameters, and generates the computed
output transferring to its successor DNN operators as the in-
put.
```

### 8d4c6565f46d91f8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 8 |
| chunk_index | 11 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
As such, we can represent the output of a DNN opera-
tor as symbolic expressions of the operator’s input and the
2140    31st USENIX Security Symposium USENIX Association
operator’s parameters.

These expressions contain the math-
ematical semanticsDND needs to recover.

To extract such
symbolic expressions,DND performs customized selective
symbolic execution with the IVs (identiﬁed in Section 5.2.1)
as symbolic variables.

This is because making IVs as sym-
bolicvariablesbringsthetwofollowingbeneﬁts:(1)itenables
DND to symbolize the mathematical expressions of the DNN
operator’s output as symbolic expressions. (2) it allowsDND
to eﬃciently extract the symbolic expressions of a DNN op-
erator’s output by only executing one iteration of each loop,
as discussed inSolution 2of Section 4.

We will explain those
beneﬁts using Figure 3b.
```

### Retrieved Top-20

**#1** — af71c06234f1d1ad | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=2

```
Speciﬁcally,DND ﬁrst matches the AST in
each operator summary with a template AST to determine
its DNN operator type (Step).

Then,DND recovers the
DNN topology by identifying the data dependencies between
DNN operators (Step).

Finally,DND recovers each DNN
operator’s attributes and parameters leveraging the identiﬁed
DNNoperatortypeandDNNtopology,andconvertsthefully-
recovered DNN model to an ONNX model (Step).
5.1 DNN Operator Location Identiﬁcation
In this step,DND identiﬁes the locations
```

**#2** — 342aa149b5e318b2 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=3

```
Speciﬁcally,DND ﬁrst identiﬁes the locations of the func-
tionswithpossibletensorcomputation(i.e.,containingtwoor
more nested loops or invoking math functions in the standard
library) as DNN operator candidates.

Then,DND collects the
caller functions of each function in the candidate list.

Among
these caller functions, the one calling most candidates is con-
sidered as the “inference function” (i.e., acting as the DNN
binary’sdispatchfunction).

Finally, DND ﬁltersoutthecandi-
datefunctionstha
```

**#3** — 24e8108a850d9c01 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.11-11 | sec=method | ci=0

```
We implementDND with over 7.5K lines of Python code on
top ofangr [47].

DNNOperatorLocationIdentiﬁcation DNNoperatorloca-
tion identiﬁcation requires recovering CFGs and identifying
loop locations.

DND uses angr’s to recover CFG, which is
essential to ﬁnd the locations of DNN operators.

Loop Analysis.

DND requires ﬁnding all the loops and their
nested loops in each DNN binary to perform loop analysis in
Section 5.2.1.

For that, we use angr’s loop ﬁnder.

Operator Summary Generation.

We imp
```

**#4** — a284a70309317971 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.11-11 | sec=method | ci=1

```
In some cases, some DNN opera-
tors(e.g., Softmax)callspeciﬁcmathematicalfunctions( exp,
pow, sqrt, tanh, log) in standard libraries (libc and libm).

Inthesecases, DND needstoidentifythecalledmathematical
functions.

To this aim,DND can use a function signature-
based approach [21] if those functions are statically linked.

Because those functions are pre-built, compilers insert those
pre-built functions into DNN binaries without being changed.

Alternatively,ananalystcansearchforsuchfunctionsb
```

**#5** — bb0638a512de426a | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=19

```
Solution 3:ForanunknownDNNoperator,wematchtheAST
included in its generated operator summary with operators’
template ASTs to identify its operator type.

DND ﬁrst builds
a template AST database, which maps each DNN operator to
its corresponding AST.

Speciﬁcally,DND leverages an up-
to-date DNN compiler to compile each DNN operator and
generate the template AST of each compiled DNN operator,
representedwiththeIRwedesign.

Then,giventhepreviously
generated operator summary of an unknown DNN opera
```

**#6** — 4b4a4ad864c4b875 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=12

```
On the
contrary,DND candecompileaDNNmodelembeddedinthe
binary program and generate a high-level representation (i.e.,
in the ONNX format [9]), including both the model hyper-
parameters and parameters of the embedded DNN model.
3 Scope
In this section, we describe the input/output ofDND, and the
standard and realistic assumptions on which DND relies.

Input.

DND supports (stripped) DNN binaries (i.e., the bi-
nary programs where a compiled DNN model is embedded)
compiled by the AOT compilation 
```

**#7** — 46c3664565691654 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.9-10 | sec=method | ci=25

```
We will show the DNN operators from which
we are able to generate the template ASTs in Section 7.1.
5.4 DNN Model Lifting
In this section, we describe how to further lift the operator
summary of each DNN operator to the high-level representa-
tionofaDNNmodel(i.e.,ONNXformat).

DNDﬁrstrecovers
types of DNN operators using AST matching (Section 5.4.1).

Then,DND recovers the DNN topology leveraging the inter-
operator data dependencies (Section 5.4.2).

Finally,DND re-
covers DNN operators’ attrib
```

**#8** — bdb01ae674531972 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=0

```
DND’s workﬂow is composed of three components, as illus-
tratedinFigure2.

Speciﬁcally,thesethreecomponentsare(1)
DNNOperatorLocationIdentiﬁcation ,(2) OperatorSummary
Generation, and (3)DNN Model Lifting.

In the ﬁrst stage,DND recovers the control ﬂow graph
(CFG) and identiﬁes the location of inference function and
DNN operators from the input (stripped) DNN binary (Step
in Figure 2, details in Section 5.1).

Next,DNDgeneratesoperatorsummaryofeachDNNoper-
ator (Section 5.2).

To do so,DND ﬁrs
```

**#9** — b38c7fe2bea104fd | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.8-8 | sec=method | ci=14

```
When-
ever encountering a conditional statement that can exit a
loop, DND follows the path exiting the loop (Line 15-16).

Furthermore, when reading an operator input or parameter
with the symbolic address,DND returns the expression of
symbolic address itself (e.g., the address offilter[u][v])
(Line 11-12).

In this way,DND can keep track of each
symbolic expression’s provenance (i.e., the symbolic ad-
dress where it is read from).

To extract the symbolic expres-
sions of DNN operator output, w
```

**#10** — a0a782ed2ec8a898 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.10-11 | sec=method | ci=31

```
At last,
DND iterates the DNN operator execution sequence from the
ﬁrst DNN operator to the last DNN operator, identiﬁes the
data dependencies between adjacent operators, and connects
them accordingly.

Furthermore, from the data dependencies,DND can also
recognize theinput term(i.e., the term which is the output of
USENIX Association 31st USENIX Security Symposium    2143
thepreviousDNNoperator)and parameterterm (i.e.,theterm
which is the parameters of the DNN operator) in the operator
summary’
```

**#11** — 49fe88a7eaee3e40 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=13

```
We can easily infer DNN models
from those ﬁles because they contain the information on the
modelhyper-parametersandparametersofthedeployedDNN
model. (ii) static analysis cannot extract DNN models from
DNN binaries compiled by the interpreter-based compilation
without the DNN conﬁguration ﬁle because DNNs are con-
ﬁgured dynamically.

Furthermore,DND does not support the
DNNbinariesrunningonDNNacceleratorsbecauseDNNac-
celerators have very diverse ISAs, and they are not supported
by the general-p
```

**#12** — 529d6e6b64ce0783 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.9-9 | sec=method | ci=19

```
Each operator summary contains three parts:addr,
expr and IVs, denoting the symbolic addresses of a DNN
operator output, the AST of a DNN operator output, and the
IVs information (i.e., initialization value, step size, and loop
count), respectively.

We show an example of generated opera-
tor summary in Figure 3d.

To lift addr, DND simply uses the DNN operator out-
put address in the extracted symbolic expression (e.g.,
output[i][j] in Figure 3c).

Forexpr, DND recursively
parses the extracted 
```

**#13** — 17bd53439cd2266e | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=16

```
Solution 1:We use a dedicated IR which is able to represent
eachDNNoperatorasanoperatorsummary,includinganAST
of algebraic operations.

DND ﬁrst identiﬁes the location of
each DNN operator in a DNN binary and then uses selective
symbolic execution to generate an operator summary with an
AST of algebraic operations of each DNN operator, which is
represented with the IR we design.

Because a DNN operator
hasthesamemathematicalsemanticevenwithdiﬀerentDNN
compilers and ISAs, and our IR and operator 
```

**#14** — a1922c6875e023e8 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=14

```
We can use this output to reveal the DNN
model’s details and conduct security analysis, such as model
extraction, adversarial examples discovery, and model hard-
ening.

DND does not recover the algorithm hyper-parameters
(deﬁned in Section 2.1) because they neither aﬀect the infer-
ence process nor are recoverable from the binary.

Assumptions.

DND relies on the following assumptions:
1.

We have access to a DNN binary (e.g., dumping DNN
binaries running on an embedded system).
2.

The control
```

**#15** — 59064e7102f59087 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.9-9 | sec=method | ci=23

```
Speciﬁcally,
DND recognizesasimilarpatternamongthesymbolicexpres-
sions representing each one of the rolled iterations (e.g., Line
1 and Line 2 in Figure 4c), and recovers the rolled loop (e.g.,
the loop iterating over the ﬁlter length in Line 5 in Figure 4a)
by creating a loop index (e.g.,v_reroll in Figure 4d).

Sec-
ond, to divide a combined DNN operator into two separate
DNN operators,DND leverages the heuristic that the com-
bined second operator is usually an activation operator (e.g.,
Rel
```

**#16** — 176e2eecee048a9f | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.8-8 | sec=method | ci=13

```
Furthermore, in order to keep track of the symbolic con-
straints related to memory reads and writes,DND’s cus-
tomized concretization strategy does not concretize mem-
ory addresses.

Instead, when reading from symbolic memory,
DND returns the symbolic memory address together with a
proper annotation.

For instance, when reading from address
input+i, DND returns input+i with MemReadVal annota-
tion,denotingwherethevalueisreadfrom.

Usingthisannota-
tion,DNDkeepstrackofmemoryreadvalues,andrecord
```

**#17** — ec71df9e40361439 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.3-3 | sec=introduction | ci=5

```
We further
demonstrate thatDND can successfully decompile a DNN bi-
nary used by a real-world micro-controller, and the recovered
DNN model can be used to boost adversarial attacks against
the original DNN, enabling the usage of white-box attacks, in
place of less eﬃcient black-box ones.

In summary, our main contributions are as follows:
• We design and implement DND, the ﬁrst compiler- and
ISA-agnostic decompiler for compiled DNN models.

DND can decompile a (stripped) DNN binary to recover
th
```

**#18** — 784da26bfe4a09ce | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.11-11 | sec=method | ci=32

```
Forexample,forthe Mul
functioninthe FC operator’ssummary(Line2-3inFigure5b),
DNDidentiﬁesthatthe input[i] istheoutputoftheprevious
DNN operator (i.e., its address range overlaps with previous
DNN operator’s output range), and that theweight[j][i]
is the parameter (i.e., its address range does not overlap with
any previous DNN operator’s output range).
5.4.3 Attributes and Parameters Recovery
In the last step,DND recovers the attributes and parameters
of each DNN operator by leveraging the genera
```

**#19** — 3be90e01110a7bd6 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=1

```
Then,DND leverages loop’s
information to perform selective symbolic execution that ex-
tractstheoutputofaDNNoperatorassymbolicexpressionsof
itsinputandparameters(e.g., ......[.] =.....[.] ∗.....[.]),
which capture the mathematical semantic of a DNN operator
(Step).

The extracted symbolic expressions are then lifted
to the operator summary in our IR format (Step).

The op-
erator summary of a DNN operator includes the ASTs and
other information extracted from Stepand Step.

Note
that DND als
```

**#20** — 419fc6373eaa3a11 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.2-2 | sec=abstract | ci=2

```
Then, DND matchesthe
extracted mathematical DNN operations with template math-
ematical DNN operations, and it recovers hyper-parameters
and parameters of all the identiﬁed DNN operators, as well as
the overall DNN topology.

Our evaluation shows thatDND
can perfectly recover diﬀerent DNN models, extracting them
from binaries compiled by two diﬀerent compilers (Glow and
TVM)forthreediﬀerentISAs(Thumb,AArch64,andx86-64).

Moreover,DND enables extracting the DNN models used by
real-world micro-con
```

### Missed Chunks (5 — expected but NOT in top-20)

### 9bdf3eaa138e61a4

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 9 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
To check the property (iii), after reaching the DNN oper-
ator’s most outer loop’s exit point (e.g., Line 2 in Figure 3b),
DND inspects each IV’s corresponding register to check if
its register is updated with a constant (i.e., step size).

At last,
DNDconsidersanIVcandidateasanIVwhenitsatisﬁesboth
properties (ii) and (iii) (Line 18).

Finally,DND recovers IVs’ initial values, step sizes, and
loopcounts(Line19).

Inparticular,loopcountsarecomputed
from initial values, step sizes, and the collected loop exit con-
ditions.

For example, the initial value, step size and loop exit
conditions ofi in Figure 3b are 0, 1, andi<2, respectively.

Then, the loop count is derived by inquiring the solver with
these information.
```

### 20ac523f29224b53

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 6 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the break edges (denoting the edges in CFG that
jump out of the current loop).
```

### 16dc5ceb2dad79e0

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how to identify IVs using the
aforementioned three properties by symbolically executing
each DNN operator from its entry point to its exit point (Line
2,16-17).

Leveragingtheproperty(i), DND symbolizesevery
general register initialized by a constant in the loop’s entry
block (Line 10-12).
```

### 1fba7167150e9c4c

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 10 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Algorithm 1Loop analysis
1: procedureLOOPANALYSIS(op: operator)
2: symEngine ← SymbolicEngine(op.entryAddr)
3: candidates←ç
4: while symEngine.hasActive()do
5: symEngine.step()
6: for eachstate∈ symEngine.statesdo
7: inst ← state.lastInst
8: addr ← state.addr
9: if addr ∈ op.entryBlocks then
10: if isRegWrite(inst)andisConstant(inst.writeVal)then
11: inst.writeVal← createSym()
12: candidates.add((addr, inst.writeReg))
13: if addr ∈ op.breakEdgeSrcAddrthen
14: symEngine.record(state.branch.condition.get_IV())
15: symEngine.keep(getBreakState(state.succ))
16: if addr ∉ op.addrRangethen
17: symEngine.stash(state)
18: IVs ← checkConditionAndUpdate(candidates)
19: IVs.getLoopCount()
20: ReturnIVs
5.2.2 Symbolic Expression Extraction
ADNNoperatortypicallyperformstensorcomputation,which
takes its input and parameters, and generates the computed
output transferring to its successor DNN operators as the in-
put.
```

### 8d4c6565f46d91f8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 8 |
| chunk_index | 11 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
As such, we can represent the output of a DNN opera-
tor as symbolic expressions of the operator’s input and the
2140    31st USENIX Security Symposium USENIX Association
operator’s parameters.

These expressions contain the math-
ematical semanticsDND needs to recover.

To extract such
symbolic expressions,DND performs customized selective
symbolic execution with the IVs (identiﬁed in Section 5.2.1)
as symbolic variables.

This is because making IVs as sym-
bolicvariablesbringsthetwofollowingbeneﬁts:(1)itenables
DND to symbolize the mathematical expressions of the DNN
operator’s output as symbolic expressions. (2) it allowsDND
to eﬃciently extract the symbolic expressions of a DNN op-
erator’s output by only executing one iteration of each loop,
as discussed inSolution 2of Section 4.

We will explain those
beneﬁts using Figure 3b.
```

### False Positives (20 — in top-20 but NOT expected)

### af71c06234f1d1ad

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 2 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Speciﬁcally,DND ﬁrst matches the AST in
each operator summary with a template AST to determine
its DNN operator type (Step).

Then,DND recovers the
DNN topology by identifying the data dependencies between
DNN operators (Step).

Finally,DND recovers each DNN
operator’s attributes and parameters leveraging the identiﬁed
DNNoperatortypeandDNNtopology,andconvertsthefully-
recovered DNN model to an ONNX model (Step).
5.1 DNN Operator Location Identiﬁcation
In this step,DND identiﬁes the locations of the inference
function and the DNN operators.

Since DNN operators are
essentially tensor computations, they are implemented and
compiledasmultiplenestedloopswithanumberofnumerical
computations inside.

Furthermore, DNN operators reside in
eithertheinferencefunctionoritscalleefunctions.

DNDlever-
ages these two properties to identify the locations of DNN
operators and the inference function.
```

### 342aa149b5e318b2

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 3 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Speciﬁcally,DND ﬁrst identiﬁes the locations of the func-
tionswithpossibletensorcomputation(i.e.,containingtwoor
more nested loops or invoking math functions in the standard
library) as DNN operator candidates.

Then,DND collects the
caller functions of each function in the candidate list.

Among
these caller functions, the one calling most candidates is con-
sidered as the “inference function” (i.e., acting as the DNN
binary’sdispatchfunction).

Finally, DND ﬁltersoutthecandi-
datefunctionsthatarenotthecalleesoftheinferencefunction.
5.2 Operator Summary Generation
After identifying the locations of DNN operators,DND ex-
tracts the symbolic expressions from each DNN operator and
lifts them to operator summary in the IR we design.

To do
so,DND ﬁrst conducts loop analysis for each DNN operator
(StepdescribedinSection5.2.1).
```

### 24e8108a850d9c01

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 6 Implementation |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 0 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We implementDND with over 7.5K lines of Python code on
top ofangr [47].

DNNOperatorLocationIdentiﬁcation DNNoperatorloca-
tion identiﬁcation requires recovering CFGs and identifying
loop locations.

DND uses angr’s to recover CFG, which is
essential to ﬁnd the locations of DNN operators.

Loop Analysis.

DND requires ﬁnding all the loops and their
nested loops in each DNN binary to perform loop analysis in
Section 5.2.1.

For that, we use angr’s loop ﬁnder.

Operator Summary Generation.

We implement the cus-
tomizedsymbolicexecutionontopofangrsimulationmanager
and angr under-constrained symbolic execution functionality.

Thissymbolicexecutionengineisresponsibleforsymbolizing
variables(e.g.,IVs)andcollectingthesymbolicexpressionsof
each DNN operator output.
```

### a284a70309317971

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 6 Implementation |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 1 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
In some cases, some DNN opera-
tors(e.g., Softmax)callspeciﬁcmathematicalfunctions( exp,
pow, sqrt, tanh, log) in standard libraries (libc and libm).

Inthesecases, DND needstoidentifythecalledmathematical
functions.

To this aim,DND can use a function signature-
based approach [21] if those functions are statically linked.

Because those functions are pre-built, compilers insert those
pre-built functions into DNN binaries without being changed.

Alternatively,ananalystcansearchforsuchfunctionsbycheck-
ing calledfunctions’ names iffunction names are notstripped
from the binary or those functions are dynamically linked.
```

### bb0638a512de426a

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 19 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Solution 3:ForanunknownDNNoperator,wematchtheAST
included in its generated operator summary with operators’
template ASTs to identify its operator type.

DND ﬁrst builds
a template AST database, which maps each DNN operator to
its corresponding AST.

Speciﬁcally,DND leverages an up-
to-date DNN compiler to compile each DNN operator and
generate the template AST of each compiled DNN operator,
representedwiththeIRwedesign.

Then,giventhepreviously
generated operator summary of an unknown DNN operator,
DND matches its AST to one of the AST in the template
AST database, and determines the type of the unknown DNN
operator.
```

### 4b4a4ad864c4b875

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 12 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
On the
contrary,DND candecompileaDNNmodelembeddedinthe
binary program and generate a high-level representation (i.e.,
in the ONNX format [9]), including both the model hyper-
parameters and parameters of the embedded DNN model.
3 Scope
In this section, we describe the input/output ofDND, and the
standard and realistic assumptions on which DND relies.

Input.

DND supports (stripped) DNN binaries (i.e., the bi-
nary programs where a compiled DNN model is embedded)
compiled by the AOT compilation scheme running on CPU
without hardware accelerators.

This conﬁguration is common
on edge devices [53].

DND does not support DNN binaries
compiled by interpreter-based compilation schemes because
of the following reasons: (i) DNN binaries compiled by the
interpreter-based compilation scheme usually accompany the
DNN conﬁguration ﬁles.
```

### 46c3664565691654

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 25 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We will show the DNN operators from which
we are able to generate the template ASTs in Section 7.1.
5.4 DNN Model Lifting
In this section, we describe how to further lift the operator
summary of each DNN operator to the high-level representa-
tionofaDNNmodel(i.e.,ONNXformat).

DNDﬁrstrecovers
types of DNN operators using AST matching (Section 5.4.1).

Then,DND recovers the DNN topology leveraging the inter-
operator data dependencies (Section 5.4.2).

Finally,DND re-
covers DNN operators’ attributes and parameters leveraging
both the DNN operator type and DNN topology, and converts
the fully-recovered model into ONNX format (Section 5.4.3).
5.4.1 AST Matching
For each identiﬁed DNN operator,DND matches the ASTs
(i.e., expr) in its operator summary with one of the template
ASTs to determine its DNN operator type.
```

### bdb01ae674531972

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 0 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
DND’s workﬂow is composed of three components, as illus-
tratedinFigure2.

Speciﬁcally,thesethreecomponentsare(1)
DNNOperatorLocationIdentiﬁcation ,(2) OperatorSummary
Generation, and (3)DNN Model Lifting.

In the ﬁrst stage,DND recovers the control ﬂow graph
(CFG) and identiﬁes the location of inference function and
DNN operators from the input (stripped) DNN binary (Step
in Figure 2, details in Section 5.1).

Next,DNDgeneratesoperatorsummaryofeachDNNoper-
ator (Section 5.2).

To do so,DND ﬁrst conducts loop analysis
(Step ) to identify loops’ information.

Such information
is essential for further analysis.
```

### b38c7fe2bea104fd

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 14 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
When-
ever encountering a conditional statement that can exit a
loop, DND follows the path exiting the loop (Line 15-16).

Furthermore, when reading an operator input or parameter
with the symbolic address,DND returns the expression of
symbolic address itself (e.g., the address offilter[u][v])
(Line 11-12).

In this way,DND can keep track of each
symbolic expression’s provenance (i.e., the symbolic ad-
dress where it is read from).

To extract the symbolic expres-
sions of DNN operator output, when the DNN operator out-
put is updated,DND collects the symbolic address of the
DNN operator output and its corresponding symbolic expres-
sions(i.e., += input[i+u][j+v]*filter[u][v])(Line13-
14).

Figure 3b shows the output example.
```

### a0a782ed2ec8a898

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 10 |
| page_end | 11 |
| chunk_index | 31 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
At last,
DND iterates the DNN operator execution sequence from the
ﬁrst DNN operator to the last DNN operator, identiﬁes the
data dependencies between adjacent operators, and connects
them accordingly.

Furthermore, from the data dependencies,DND can also
recognize theinput term(i.e., the term which is the output of
USENIX Association 31st USENIX Security Symposium    2143
thepreviousDNNoperator)and parameterterm (i.e.,theterm
which is the parameters of the DNN operator) in the operator
summary’sexpr, which can be leveraged for attributes and
parametersrecoveryinthenextstep.
```

### 49fe88a7eaee3e40

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 13 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We can easily infer DNN models
from those ﬁles because they contain the information on the
modelhyper-parametersandparametersofthedeployedDNN
model. (ii) static analysis cannot extract DNN models from
DNN binaries compiled by the interpreter-based compilation
without the DNN conﬁguration ﬁle because DNNs are con-
ﬁgured dynamically.

Furthermore,DND does not support the
DNNbinariesrunningonDNNacceleratorsbecauseDNNac-
celerators have very diverse ISAs, and they are not supported
by the general-purpose disassemblers.

Section 9 discusses
more details whyDND does not support decompiling DNN
binaries on accelerators.

Output.

DND can decompile a DNN model embedded in an
input binary.

The output is in the ONNX format [9] (e.g., Fig-
ure 1) including the DNN model’s model hyper-parameters
and parameters.
```

### 529d6e6b64ce0783

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 19 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Each operator summary contains three parts:addr,
expr and IVs, denoting the symbolic addresses of a DNN
operator output, the AST of a DNN operator output, and the
IVs information (i.e., initialization value, step size, and loop
count), respectively.

We show an example of generated opera-
tor summary in Figure 3d.

To lift addr, DND simply uses the DNN operator out-
put address in the extracted symbolic expression (e.g.,
output[i][j] in Figure 3c).

Forexpr, DND recursively
parses the extracted symbolic expressions and then builds
the AST in our IR format.

Speciﬁcally, during the parsing
process, DND analyzes the extracted symbolic expressions
to identify their correspondingreducing function and its
elements and index.
```

### 17bd53439cd2266e

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 16 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Solution 1:We use a dedicated IR which is able to represent
eachDNNoperatorasanoperatorsummary,includinganAST
of algebraic operations.

DND ﬁrst identiﬁes the location of
each DNN operator in a DNN binary and then uses selective
symbolic execution to generate an operator summary with an
AST of algebraic operations of each DNN operator, which is
represented with the IR we design.

Because a DNN operator
hasthesamemathematicalsemanticevenwithdiﬀerentDNN
compilers and ISAs, and our IR and operator summary are
able to capture the mathematical semantic,DND can identify
them in a compiler- and ISA-agnostic manner.

Challenge 2: Vectorized Mathematical Computation and
Complicated Loop Structure.

DNN operators, as tensor op-
erations,arealwaysimplementedandcompiledasnestedloops
with vectorized mathematical computations inside the loop
bodies.
```

### a1922c6875e023e8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 14 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We can use this output to reveal the DNN
model’s details and conduct security analysis, such as model
extraction, adversarial examples discovery, and model hard-
ening.

DND does not recover the algorithm hyper-parameters
(deﬁned in Section 2.1) because they neither aﬀect the infer-
ence process nor are recoverable from the binary.

Assumptions.

DND relies on the following assumptions:
1.

We have access to a DNN binary (e.g., dumping DNN
binaries running on an embedded system).
2.

The control-ﬂow graph (CFG) recovery is reliable.

Our
evaluation shows that the recovered CFGs, though impre-
cise, are suﬃcient enough for our decompilation purpose.
3.

DNN compilers do not use obfuscation technique.
```

### 59064e7102f59087

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 23 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Speciﬁcally,
DND recognizesasimilarpatternamongthesymbolicexpres-
sions representing each one of the rolled iterations (e.g., Line
1 and Line 2 in Figure 4c), and recovers the rolled loop (e.g.,
the loop iterating over the ﬁlter length in Line 5 in Figure 4a)
by creating a loop index (e.g.,v_reroll in Figure 4d).

Sec-
ond, to divide a combined DNN operator into two separate
DNN operators,DND leverages the heuristic that the com-
bined second operator is usually an activation operator (e.g.,
Relu).
```

### 176e2eecee048a9f

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 13 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Furthermore, in order to keep track of the symbolic con-
straints related to memory reads and writes,DND’s cus-
tomized concretization strategy does not concretize mem-
ory addresses.

Instead, when reading from symbolic memory,
DND returns the symbolic memory address together with a
proper annotation.

For instance, when reading from address
input+i, DND returns input+i with MemReadVal annota-
tion,denotingwherethevalueisreadfrom.

Usingthisannota-
tion,DNDkeepstrackofmemoryreadvalues,andrecordsthe
written expressions when the code write to symbolic memory.

We explain the detailed procedure to extract symbolic
expressions in Algorithm 2.

In particular,DND symboli-
cally executes each DNN operator starting from its entry
point (Line 3).

When reaching the identiﬁed IV initializa-
tion code,DND symbolizes IVs’ corresponding registers in-
stead of initializing them with a constant (Line 9-10).
```

### ec71df9e40361439

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 5 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We further
demonstrate thatDND can successfully decompile a DNN bi-
nary used by a real-world micro-controller, and the recovered
DNN model can be used to boost adversarial attacks against
the original DNN, enabling the usage of white-box attacks, in
place of less eﬃcient black-box ones.

In summary, our main contributions are as follows:
• We design and implement DND, the ﬁrst compiler- and
ISA-agnostic decompiler for compiled DNN models.

DND can decompile a (stripped) DNN binary to recover
thefulldetailsofthecompiledDNNmodelandrepresent
them using the ONNX high-level modeling language.
• We design a dedicated IR to represent each DNN oper-
ator and develop a novel technique that uses symbolic
execution to lift the DNN binary to IR expressions.
```

### 784da26bfe4a09ce

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 32 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Forexample,forthe Mul
functioninthe FC operator’ssummary(Line2-3inFigure5b),
DNDidentiﬁesthatthe input[i] istheoutputoftheprevious
DNN operator (i.e., its address range overlaps with previous
DNN operator’s output range), and that theweight[j][i]
is the parameter (i.e., its address range does not overlap with
any previous DNN operator’s output range).
5.4.3 Attributes and Parameters Recovery
In the last step,DND recovers the attributes and parameters
of each DNN operator by leveraging the generated operator
summary and recovered DNN topology, and it then generates
a high-level DNN representation in the ONNX format.

Attribute Recovery.

For DNN operators with only shape-
related attributes (e.g., ﬁlter length ofAveragePool),DND
recovers their attributes by checking the nesting structure of
their loops and the loops’ counts (e.g., the ﬁlter length is the
loop count of the loop that iterates over the inputs).
```

### 3be90e01110a7bd6

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 1 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then,DND leverages loop’s
information to perform selective symbolic execution that ex-
tractstheoutputofaDNNoperatorassymbolicexpressionsof
itsinputandparameters(e.g., ......[.] =.....[.] ∗.....[.]),
which capture the mathematical semantic of a DNN operator
(Step).

The extracted symbolic expressions are then lifted
to the operator summary in our IR format (Step).

The op-
erator summary of a DNN operator includes the ASTs and
other information extracted from Stepand Step.

Note
that DND also generates template ASTs through the afore-
mentioned operator summary generation procedure (Step,
 and ) that will be used in the next step (Section 5.3).

After the operator summary generation, the next step is to
lifteachoperatorsummarytoaDNNoperatorandconvertitto
a high-level DNN representation (i.e., an ONNX model [11])
(Section 5.4).
```

### 419fc6373eaa3a11

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND matchesthe
extracted mathematical DNN operations with template math-
ematical DNN operations, and it recovers hyper-parameters
and parameters of all the identiﬁed DNN operators, as well as
the overall DNN topology.

Our evaluation shows thatDND
can perfectly recover diﬀerent DNN models, extracting them
from binaries compiled by two diﬀerent compilers (Glow and
TVM)forthreediﬀerentISAs(Thumb,AArch64,andx86-64).

Moreover,DND enables extracting the DNN models used by
real-world micro-controllers and attacking them using white-
box adversarial machine learning techniques.
```

---

## 7. [single_002_zh] BTD 的三步恢复方法是什么？它如何对 DNN 算子进行分类？

**Type**: `method` | **Lang**: `ZH` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.2000 | 0.4000 |
| 20 | 0.4000 | 0.6000 |

**Expected sources**: all-Decompiling+x86

### Expected Chunks (5)

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### be1c6ddebe8e6fc5

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 3 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Some operators are too costly for symbolic exe-
cution to analyze.

We use taint analysis to keep only tainted
sub-traces for more expensive symbolic execution to ana-
lyze (R3), as noted in Sec. 4.3.1.

BTD is an end-to-end, fully
automated DNN decompiler (R4).

BTD produces model spec-
iﬁcations that behave identically to original models, whose
focus and addressed challenges are distinct from C/C++ de-
compilation.

BTD does not guarantee 100% correct outputs.

In Sec. 5, we discuss procedures users can follow to ﬁx errors.

Dimensions and parameters conﬁgure DNN operators.

We
show representative cases in Fig. 3(b).

Type I operators, in-
cluding activation functions like ReLU and element-wise
arithmetic operators, do not ship with parameters; recovering
their dimensions is trivial, as clariﬁed in the caption of Fig. 3.

Type II and III operators require dimensions or parameters,
such as Pooling’s stride S and kernel size K.
```

### c54826ab77483b01

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 4 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In addition to
simple arithmetic operators, BiasAdd involves biasB, as extra
parameters.

Type IV operators require both parameters and di-
mensions.

These operators form most DNN models.

Sec. 7.1
empirically demonstrates “comprehensivness” of our study.

BTD recovers dimensions/parameters of all DNN opera-
tors used by CV models in ONNX Zoo (see Sec. 7.1).

Due to
limited space, Sec. 4.3 only discusses decompiling the most
challenging operator, Conv.

The core techniques explained in
Sec. 4.3 are utilized to decompile other DNN operators.

How-
ever, other operators may use different (but simpler) patterns.

Appendix C lists other operator patterns.

We further discuss
the extensibility of BTD in Sec. 7.3.

Disassembling and Function Recovery.

BTD targets 64-bit
x86 executables.

Cross-platform support is discussed in Sec. 8.

BTD supports stripped executables without symbol or debug
information.
```

### 0d4b4c26fb96274a

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 6 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We extend our learning-based method from Sec. 4.1 to predict
compilation provenance from assembly code.

Our evaluation
of over all CV models in ONNX Zoo ﬁnds no errors.

Overall,
we assume that compilation provenance is known to BTD .

Therefore, some patterns can be designed separately for Glow-
and TVM-emitted executables; see details in Appendix C.

To
show e’s decompilation is ﬂawless, wemust recompile decom-
piled DNN models with the same provenance (see Sec. 7.1.4).

Using different compilation provenances may induce (small)
numerical accuracy discrepancies and is undesirable.

This section focuses on decompilation of self-contained
DNN executables compiled by TVM and Glow.

Decompila-
tion of NNFusion-emitted executables is easier because of its
distinct code generation paradigm.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### Retrieved Top-20

**#1** — 5f882e74e4b278f2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=3

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive 
```

**#2** — 74238bd6bc7e40c9 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=3

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of Neuro
```

**#3** — dc55b42b1816487a | Hardening Deep Neural Network Binaries against ReverseEngine | p.4-5 | sec=method | ci=11

```
With the symbolic expression
and input/output buffers identified in previous steps, we use the
heuristics in [37] to reconstruct the semantics of the whole operator.

Our proof-of-concept attack is mostly aligned with the BTD
attack [37], with the following extensions: (1) BTD stops trace log-
ging after completing executing the first iteration of the outermost
loop, while we stop logging after the last memory write to the first
output element is finished; (2) We extend BTD’s symbolic engine
to 
```

**#4** — a56d6a08d27f78a8 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.2-2 | sec=introduction | ci=7

```
In summary, we
contribute the following:
• This paper, for the ﬁrst time1, advocates for reverse engi-
neering DNN executables.

BTD accepts as input (stripped)
executables generated by production DL compilers and out-
puts complete model speciﬁcations.

BTD can be used to aid
in the comprehension, migration, hardening, and exploita-
tion of DNN executables.
• BTD features a three-step approach to recovering high-
level DNN models.

It incorporates various design principles
and techniques to del
```

**#5** — aa21a57fe3ed9643 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.1-1 | sec=abstract | ci=1

```
BTD de-
livers a practical framework to process DNN executables
compiled by different DL compilers and with full optimiza-
tions enabled on x86 platforms.

It employs learning-based
techniques to infer DNN operators, dynamic analysis to reveal
network architectures, and symbolic execution to facilitate
inferring dimensions and parameters of DNN operators.

Our evaluation reveals that BTD enables accurate recov-
ery of full speciﬁcations of complex DNNs with millions of
parameters (e.g., ResNet).
```

**#6** — d0a14750cdbd2932 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-9 | sec=experiment | ci=5

```
We employ 100 inputs
for the Emotion and SuperRes models and 500 inputs for all
TABLE IV: Comparison of TRA between BTD and NeuroDeX (all value in %)
Model
EfficientNet Inceptionv1 MobileNetv2 ResNet18 ShuffleNetv2 VGG16
BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX
TVM v0.7 O0 72.48 97.96 97.1 100 80.47 100 76.56 100 70.05 98.87 84.85 100
TVM v0.8 O0 39.91 99.28 87.85 100 66.85 100 46.88 100 49.83 98.97 63.64 100
TVM v0.9dev O0 40.7 100 86.06 100 64.32 100 34.92 
```

**#7** **[HIT]** — c54826ab77483b01 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.5-5 | sec=method | ci=4

```
In addition to
simple arithmetic operators, BiasAdd involves biasB, as extra
parameters.

Type IV operators require both parameters and di-
mensions.

These operators form most DNN models.

Sec. 7.1
empirically demonstrates “comprehensivness” of our study.

BTD recovers dimensions/parameters of all DNN opera-
tors used by CV models in ONNX Zoo (see Sec. 7.1).

Due to
limited space, Sec. 4.3 only discusses decompiling the most
challenging operator, Conv.

The core techniques explained in
Sec. 4.3
```

**#8** — 9ffb67a4e003ef15 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.2-2 | sec=introduction | ci=6

```
BTD is scalable to recover DNN models from 65
DNN executables, including nearly 3 million instructions, in
60 hours with negligible errors.

BTD , in particular, can re-
cover over 100 million parameters from VGG, a large DNN
model, with an error rate of less than 0.1% (for TVM-emitted
executable) or none (for Glow-emitted executable).

More-
over, to demonstrate BTD ’s correctness, we rebuild decom-
piled model speciﬁcations with PyTorch.

The results show
that almost all decompiled DNN models 
```

**#9** — 7c20d122b7ceac18 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.9-9 | sec=experiment | ci=0

```
In this section, we evaluate BTD by exploring the following
four research questions (RQs) below:
RQ1 (Comprehensiveness and Correctness): Is BTD com-
prehensive and correct to process all operators used in com-
mon DL models compiled with different compilers and opti-
mization options?

RQ2 (Robustness): Is BTD robust to survive frequent DL
compiler implementation changes?

RQ3 (Extensibility): Can BTD be easily extended to support
new operators and models?

What efforts are needed?

RQ4 (Error 
```

**#10** — f26a99fcb242d371 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.3-3 | sec=introduction | ci=13

```
Cloud service providers like Amazon and
Google include DL compilers into their DL services to boost
performance [14,101].

Amazon uses DL compilers to compile
DNN models on Intel x86 CPUs [49, 61].

Facebook deploys
Glow-compiled DNN models on Intel CPUs [69].

Overall, DL
compilers are increasingly vital to boost DL on Intel CPUs,
embedded devices, and other heterogeneous hardware back-
ends.

We design BTD, a decompiler for Intel x86 DNN exe-
cutables.

We show how BTD can accelerate common DN
```

**#11** — 09438ea197379114 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.14-14 | sec=discussion | ci=0

```
Downstream Applications & Countermeasures.

Previous
model extraction attacks rely on repetitive queries or side
channels to leak parts of DNNs.

BTD , as a decompiler, re-
veals a new and practical attack surface to recover full DNNs
when DNN executables are accessible.

Appendix D will show
that BTD can boost DNN attacks.

In addition, legacy DNN
executables can be inspected, hardened, and migrated to new
platforms.

To show the feasibility, we migrated decompiled
x86 DNN executables onto GPUs
```

**#12** — a2c1086d6d3af91e | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.14-14 | sec=experiment | ci=29

```
We an-
ticipate that compiler changes are unlikely to affect the
robustness of BTD in the near future.
7.3 RQ3: Extensibility
As stated in Sec. 7.1, BTD can cover all operators used in the
CV models from ONNX Zoo.

This section measures BTD’s
extensibility through the lens of all DNN operators supported
by ONNX Zoo (RQ3).

Note that not all operators are for CV
models, and not all operators have been used in DNN models;
some of them are rarely used in common models.

Overall,
while most techniqu
```

**#13** — 2f16806f8de9f01b | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.10-10 | sec=experiment | ci=6

```
With
BTD, we demonstrate two attacks: adversarial example (AE)
generation [71] and knowledge stealing [42] in a white-box
setting.

The results suggest that the white-box attacks enabled
by BTD are much more powerful than the black-box settings.

BTD enables recovering 151.4×more AEs than the black-
box setting within 20 minutes, and the knowledge stolen from
white-box models are of much higher quality than from the
black-box executables; see details in Appendix D.

Table 3: Average accuracy of 
```

**#14** — dbc57fec26a36a2a | Hardening Deep Neural Network Binaries against ReverseEngine | p.11-11 | sec=experiment | ci=16

```
The majority of additional memory comes from the increase of
workspace size, with an overhead of 2.89% - 42.15%.
6.3 Resilience against Existing Reverse
Engineering Attacks
To compare the effectiveness of general obfuscators andNeuroShield
on DNN binaries, we evaluate them against two state-of-the-art
DNN decompilers, DnD and BTD.

Note that the BTD attack is the
extended version we mentioned in Section 3.2.

Table 5 reports the
attack time and the number of operator functions reconstructed by
D
```

**#15** — de221c0b75c3c99b | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.8-9 | sec=method | ci=0

```
BTD is primarily written in Python with about 11K LOC.

Our Pin plugins contain about 3.1K C++ code.

The current
implementation decompiles 64-bit executables in the ELF
format on x86 platforms, See discussion on cross-platform
support in Sec. 8.

We use LSTM for DNN operators inference
in an “out-of-the-box” manner to deal with distinct optimized
low-level code of the same type of operator resulting from
different dimensions.

The model is a one-layer LSTM [43]
whose hidden dimension is 128.

T
```

**#16** — 29f5506e12ee1371 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.3-3 | sec=introduction | ci=14

```
BTD decompiles DL executables to recover DNN
high-level speciﬁcations.

The full speciﬁcations include: 1
DNN operators (e.g., ReLU, Pooling, and Conv) and their
topological connectivity, 2 dimensions of each DNN oper-
ator, such as #channels in Conv, and 3 parameters of each
DNN operator, such as weights and biases, which are im-
portant conﬁgurations learned during model training.

Sec. 4
details BTD’s processes to recover each component.

Query-Based Model Extraction.

Given a (remote) DNN
mo
```

**#17** — 8b2f1dfb72bfacf4 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.2-2 | sec=related_work | ci=2

```
The general workflow of a
DL compiler involves three steps:frontend processing, which
converts general model representations, such as ONNX [11],
into computational graphs supported by the compiler’s fron-
tend;compilation optimization, applying various optimization
techniques, including high-level optimizations like operator
fusion and constant folding, and low-level optimizations such
TABLE I: Comparison with Existing DNN Decompilers
Works Optimization Cross Arch Quantization
Libsteal [6]# # #

```

**#18** — 7239db13863247cd | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.15-15 | sec=conclusion | ci=0

```
We presented BTD , a decompiler for x86 DNN executables.

BTD recovers full DNN models from executables, including
operator types, network topology, dimensions, and parame-
ters.

Our evaluation reports promising results by successfully
decompiling and further recompiling executables compiled
from popular DNN models using different DL compilers.

Acknowledgments
We thank the anonymous reviewers for their valuable com-
ments.

HKUST authors are supported in part by a RGC ECS
grant under the contr
```

**#19** **[HIT]** — be1c6ddebe8e6fc5 | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.5-5 | sec=method | ci=3

```
Some operators are too costly for symbolic exe-
cution to analyze.

We use taint analysis to keep only tainted
sub-traces for more expensive symbolic execution to ana-
lyze (R3), as noted in Sec. 4.3.1.

BTD is an end-to-end, fully
automated DNN decompiler (R4).

BTD produces model spec-
iﬁcations that behave identically to original models, whose
focus and addressed challenges are distinct from C/C++ de-
compilation.

BTD does not guarantee 100% correct outputs.

In Sec. 5, we discuss procedures
```

**#20** — 386354b4000c16ad | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf | p.2-2 | sec=introduction | ci=5

```
BTD is comprehensive as it handles all DNN operators
used in forming computer vision (CV) models in ONNX
Zoo [77].

BTD processes x86 executables, though its core
technique is mostly platform-independent.

Decompiling ex-
ecutables on other architectures requires vendor support for
reverse engineering toolchains ﬁrst.

We also ﬁnd that DNN
“executables” on some other architectures are not in stan-
dalone executable formats.

See the last paragraph of Sec. 2
for the signiﬁcance of decompiling x86
```

### Missed Chunks (3 — expected but NOT in top-20)

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### 0d4b4c26fb96274a

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 6 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We extend our learning-based method from Sec. 4.1 to predict
compilation provenance from assembly code.

Our evaluation
of over all CV models in ONNX Zoo ﬁnds no errors.

Overall,
we assume that compilation provenance is known to BTD .

Therefore, some patterns can be designed separately for Glow-
and TVM-emitted executables; see details in Appendix C.

To
show e’s decompilation is ﬂawless, wemust recompile decom-
piled DNN models with the same provenance (see Sec. 7.1.4).

Using different compilation provenances may induce (small)
numerical accuracy discrepancies and is undesirable.

This section focuses on decompilation of self-contained
DNN executables compiled by TVM and Glow.

Decompila-
tion of NNFusion-emitted executables is easier because of its
distinct code generation paradigm.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### False Positives (18 — in top-20 but NOT expected)

### 5f882e74e4b278f2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive experiments across different optimization
levels and different compiler versions, which demonstrates its
effectiveness.

Overall, BTD is currently the SOTA method
available.

As shown in Table III, to ease of comparison, we evaluate
NeuroDeX on six different DL models, comprising a total of
54 DNN executables (varying in compiler, optimization level,
and compiler version) that are analyzed in BTD.
```

### 74238bd6bc7e40c9

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of NeuroDeX
with BTD and analyze the underlying reasons.

We choose four models: EfficientNet, ResNet18, Incep-
tionv1 and ShuffleNetv2.

These models cover a range of
weights size and topological complexities, enabling a compre-
hensive evaluation of the overhead associated with BTD and
NeuroDeX.

The model reconstruction strategies for NeuroDeX
and BTD are identical.

Therefore, we only compare the time
associated with operator type recognition and operator attribute
recovery processes.
```

### dc55b42b1816487a

| Field | Value |
|-------|-------|
| source_file | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks.pdf |
| section | method |
| section_title | 3 Motivation |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 11 |
| paper_id | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks |

```
With the symbolic expression
and input/output buffers identified in previous steps, we use the
heuristics in [37] to reconstruct the semantics of the whole operator.

Our proof-of-concept attack is mostly aligned with the BTD
attack [37], with the following extensions: (1) BTD stops trace log-
ging after completing executing the first iteration of the outermost
loop, while we stop logging after the last memory write to the first
output element is finished; (2) We extend BTD’s symbolic engine
to support more instructions that appear in the obfuscated binaries
but not in the original binaries.

Experimental results show that our proof-of-concept attack can
successfully recover 98.5% of compiled operator functions among
six DNN models obfuscated by four general obfuscators, which
proves the effectiveness of our extended BTD attack.

We discuss
the details in Section 6.
```

### a56d6a08d27f78a8

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 7 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In summary, we
contribute the following:
• This paper, for the ﬁrst time1, advocates for reverse engi-
neering DNN executables.

BTD accepts as input (stripped)
executables generated by production DL compilers and out-
puts complete model speciﬁcations.

BTD can be used to aid
in the comprehension, migration, hardening, and exploita-
tion of DNN executables.
• BTD features a three-step approach to recovering high-
level DNN models.

It incorporates various design principles
and techniques to deliver an effective pipeline.
• We evaluate BTD against executables compiled from large-
scale DNN models using production DL compilers.

BTD
achieves high accuracy in recovering (nearly) full speciﬁca-
tions of complex DNN models.

We also demonstrate how
common attacks are boosted by BTD.
2 Preliminary
Fig. 1(a) depicts DNN model compilation.

DNN compila-
tion can be divided into two phases [58], with each phase
manipulates one or several intermediate representations (IR).
```

### aa21a57fe3ed9643

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
BTD de-
livers a practical framework to process DNN executables
compiled by different DL compilers and with full optimiza-
tions enabled on x86 platforms.

It employs learning-based
techniques to infer DNN operators, dynamic analysis to reveal
network architectures, and symbolic execution to facilitate
inferring dimensions and parameters of DNN operators.

Our evaluation reveals that BTD enables accurate recov-
ery of full speciﬁcations of complex DNNs with millions of
parameters (e.g., ResNet).

The recovered DNN speciﬁcations
can be re-compiled into a new DNN executable exhibiting
identical behavior to the input executable.

We show thatBTD
can boost two representative attacks, adversarial example gen-
eration and knowledge stealing, against DNN executables.

We also demonstrate cross-architecture legacy code reuse us-
ing BTD , and envision BTD being used for other critical
downstream tasks like DNN security hardening and patching.
```

### d0a14750cdbd2932

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 9 |
| chunk_index | 5 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
We employ 100 inputs
for the Emotion and SuperRes models and 500 inputs for all
TABLE IV: Comparison of TRA between BTD and NeuroDeX (all value in %)
Model
EfficientNet Inceptionv1 MobileNetv2 ResNet18 ShuffleNetv2 VGG16
BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX
TVM v0.7 O0 72.48 97.96 97.1 100 80.47 100 76.56 100 70.05 98.87 84.85 100
TVM v0.8 O0 39.91 99.28 87.85 100 66.85 100 46.88 100 49.83 98.97 63.64 100
TVM v0.9dev O0 40.7 100 86.06 100 64.32 100 34.92 100 39.06 100 53.12 100
TVM v0.7 O3 35.14 97.3 97.66 98.73 42.86 100 78.79 96.97 77.78 94.44 59.26 88.9
TVM v0.8 O3 5 90 79.77 92.68 11.76 100 54.55 100 77.14 97.14 70.37 100
TVM v0.9dev O3 5.41 100 79.22 100 2.94 100 57.58 100 71.43 100 55.56 100
GLOW 2020 54.24 96.61 77.19 99.04 70.45 95.45 57.14 96.43 86.27 96.08 68.18 86.36
GLOW 2021 58.62 96.55 87.18 98.06 76.74 95.35 54.29 100 94 100 90 95
GLOW 2022 58.62 96.55 87.18 100 76.74 97.67 54.29 100 92 100 90 95
other models, calculating Model Inference Accuracy (MIA).
```

### 9ffb67a4e003ef15

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 6 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
BTD is scalable to recover DNN models from 65
DNN executables, including nearly 3 million instructions, in
60 hours with negligible errors.

BTD , in particular, can re-
cover over 100 million parameters from VGG, a large DNN
model, with an error rate of less than 0.1% (for TVM-emitted
executable) or none (for Glow-emitted executable).

More-
over, to demonstrate BTD ’s correctness, we rebuild decom-
piled model speciﬁcations with PyTorch.

The results show
that almost all decompiled DNN models can be recompiled
into new executables that behave identically to the reference
executables.

We further demonstrate that BTD , by decom-
piling executables into DNN models, can boost two attacks,
adversarial example generation and knowledge stealing.

We
also migrate decompiled x86 DNN executables to GPUs, and
discuss limits and potential future works.
```

### 7c20d122b7ceac18

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 0 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In this section, we evaluate BTD by exploring the following
four research questions (RQs) below:
RQ1 (Comprehensiveness and Correctness): Is BTD com-
prehensive and correct to process all operators used in com-
mon DL models compiled with different compilers and opti-
mization options?

RQ2 (Robustness): Is BTD robust to survive frequent DL
compiler implementation changes?

RQ3 (Extensibility): Can BTD be easily extended to support
new operators and models?

What efforts are needed?

RQ4 (Error Fixing): How does BTD handle decompilation
errors?

We evaluated BTD with seven real-world CV models and
an NLP model compiled with eight versions of compilers
to provide a comprehensive evaluation.

BTD can produce
correct model speciﬁcations on 59 of 65 DNN executables,
and experienced users can quickly ﬁx 3 of 6 remaining errors.

Nevertheless, we recognize that some errors cannot be easily
ﬁxed by normal users.
```

### f26a99fcb242d371

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 13 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Cloud service providers like Amazon and
Google include DL compilers into their DL services to boost
performance [14,101].

Amazon uses DL compilers to compile
DNN models on Intel x86 CPUs [49, 61].

Facebook deploys
Glow-compiled DNN models on Intel CPUs [69].

Overall, DL
compilers are increasingly vital to boost DL on Intel CPUs,
embedded devices, and other heterogeneous hardware back-
ends.

We design BTD, a decompiler for Intel x86 DNN exe-
cutables.

We show how BTD can accelerate common DNN
attacks (Appendix D) and migrate DNN executables to GPUs
(Sec. 8).

Sec. 8 explains why BTD does not decompile ex-
ecutables on GPUs/accelerators.

GPU/accelerator platforms
lack disassemblers/dynamic instrumentation infrastructures,
and the DL compiler support for GPU platforms is immature
(e.g., cannot generate standalone executables).
3 Decompiling DNN Executables
Deﬁnition.
```

### 09438ea197379114

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | discussion |
| section_title | 8 Discussion |
| page_start | 14 |
| page_end | 14 |
| chunk_index | 0 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Downstream Applications & Countermeasures.

Previous
model extraction attacks rely on repetitive queries or side
channels to leak parts of DNNs.

BTD , as a decompiler, re-
veals a new and practical attack surface to recover full DNNs
when DNN executables are accessible.

Appendix D will show
that BTD can boost DNN attacks.

In addition, legacy DNN
executables can be inspected, hardened, and migrated to new
platforms.

To show the feasibility, we migrated decompiled
x86 DNN executables onto GPUs.

This step only requires
to use different compiler options over our recovered DNN
models.

DNNs may provide business advantages.

Potential security
concerns raised by BTD may be mitigated using obfusca-
tion [54]; particularly, code obfuscation could likely impede
DNN operator inference whereas data obfuscation may likely
undermine our patterns over memory layouts.

Cross-Platform.

As reviewed in Sec. 2, DL compiler can
generate executables on various platforms.
```

### a2c1086d6d3af91e

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 14 |
| page_end | 14 |
| chunk_index | 29 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We an-
ticipate that compiler changes are unlikely to affect the
robustness of BTD in the near future.
7.3 RQ3: Extensibility
As stated in Sec. 7.1, BTD can cover all operators used in the
CV models from ONNX Zoo.

This section measures BTD’s
extensibility through the lens of all DNN operators supported
by ONNX Zoo (RQ3).

Note that not all operators are for CV
models, and not all operators have been used in DNN models;
some of them are rarely used in common models.

Overall,
while most techniques (i.e., operator inference and symbolic
execution) used in BTD are independent of operator types,
patterns described in Sec. 4.3.3 are designed for each complex
operator to recover their parameters/dimensions.

Supporting
a new operator may need new or existing patterns.

Symbolic
constraints are generally human readable, and we typically
need several hours to design and validate a new pattern for
operators without complex optimization, like BiasAdd and
Pooling.
```

### 2f16806f8de9f01b

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 6 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
With
BTD, we demonstrate two attacks: adversarial example (AE)
generation [71] and knowledge stealing [42] in a white-box
setting.

The results suggest that the white-box attacks enabled
by BTD are much more powerful than the black-box settings.

BTD enables recovering 151.4×more AEs than the black-
box setting within 20 minutes, and the knowledge stolen from
white-box models are of much higher quality than from the
black-box executables; see details in Appendix D.

Table 3: Average accuracy of DNN operator inference.
```

### dbc57fec26a36a2a

| Field | Value |
|-------|-------|
| source_file | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks.pdf |
| section | experiment |
| section_title | 6 Experiments |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 16 |
| paper_id | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks |

```
The majority of additional memory comes from the increase of
workspace size, with an overhead of 2.89% - 42.15%.
6.3 Resilience against Existing Reverse
Engineering Attacks
To compare the effectiveness of general obfuscators andNeuroShield
on DNN binaries, we evaluate them against two state-of-the-art
DNN decompilers, DnD and BTD.

Note that the BTD attack is the
extended version we mentioned in Section 3.2.

Table 5 reports the
attack time and the number of operator functions reconstructed by
DnD and BTD on compiled DNN models under different obfuscation
techniques.

We group the results for three CV models (Mnist, Resnet,
Mobilenet) and NLP models (FastText, ESM, Albert) together for
better presentation.

We only evaluate CV models for DnD as it only
supports CV models in its evaluation dataset.

For Loki’s obfuscated
models, only Mnist and FastText can finish execution.
```

### de221c0b75c3c99b

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 5 Implementation |
| page_start | 8 |
| page_end | 9 |
| chunk_index | 0 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
BTD is primarily written in Python with about 11K LOC.

Our Pin plugins contain about 3.1K C++ code.

The current
implementation decompiles 64-bit executables in the ELF
format on x86 platforms, See discussion on cross-platform
support in Sec. 8.

We use LSTM for DNN operators inference
in an “out-of-the-box” manner to deal with distinct optimized
low-level code of the same type of operator resulting from
different dimensions.

The model is a one-layer LSTM [43]
whose hidden dimension is 128.

The LSTM is implemented
using PyTorch [80], with CUDA 10.0 [72] and cuDNN [24].
6 Usage & Error Fixing
BTD offers an end-to-end, automated decompilation.

All
tasks of Fig. 3(a) require no human intervention.

However,
decompilation is inherently challenging, and BTD may make
mistakes.

This section ﬁrst explains how a user use BTD in
practice, and then discuss error ﬁxing.

Usage.
```

### 29f5506e12ee1371

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 14 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
BTD decompiles DL executables to recover DNN
high-level speciﬁcations.

The full speciﬁcations include: 1
DNN operators (e.g., ReLU, Pooling, and Conv) and their
topological connectivity, 2 dimensions of each DNN oper-
ator, such as #channels in Conv, and 3 parameters of each
DNN operator, such as weights and biases, which are im-
portant conﬁgurations learned during model training.

Sec. 4
details BTD’s processes to recover each component.

Query-Based Model Extraction.

Given a (remote) DNN
model with obscure speciﬁcations, adversaries can continu-
ously feed inputs x to the model and collect its prediction
outputs y.

This way, adversaries can gradually assemble a
training dataset (x,y) to train a local model [79, 96].
```

### 8b2f1dfb72bfacf4

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The general workflow of a
DL compiler involves three steps:frontend processing, which
converts general model representations, such as ONNX [11],
into computational graphs supported by the compiler’s fron-
tend;compilation optimization, applying various optimization
techniques, including high-level optimizations like operator
fusion and constant folding, and low-level optimizations such
TABLE I: Comparison with Existing DNN Decompilers
Works Optimization Cross Arch Quantization
Libsteal [6]# # #
Shi et al [9]# # #
DND [7]#  #
Neuroscope [10]#  #
BTD [8] # #
NeuroDeX   
as layout rearrangement;code generation, which generates
executables adapted for the target device’s hardware.

B.

DNN Executables Decompiler
The goal of DNN decompiler is to reverse DNN executables
into identical high-level models.
```

### 7239db13863247cd

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | conclusion |
| section_title | 10 Conclusion |
| page_start | 15 |
| page_end | 15 |
| chunk_index | 0 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We presented BTD , a decompiler for x86 DNN executables.

BTD recovers full DNN models from executables, including
operator types, network topology, dimensions, and parame-
ters.

Our evaluation reports promising results by successfully
decompiling and further recompiling executables compiled
from popular DNN models using different DL compilers.

Acknowledgments
We thank the anonymous reviewers for their valuable com-
ments.

HKUST authors are supported in part by a RGC ECS
grant under the contract 26206520.

Lei Ma’s research is sup-
ported in part by the Canada First Research Excellence Fund
as part of the University of Alberta’s Future Energy Sys-
tems research initiative, Canada CIFAR AI Chairs Program,
Amii RAP program, the Natural Sciences and Engineering Re-
search Council of Canada (NSERC No.

RGPIN-2021-02549,
No.

RGPAS-2021-00034, No.

DGECR-2021-00019), as well
as JSPS KAKENHI Grant No.

JP20H04168, No.
```

### 386354b4000c16ad

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 5 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
BTD is comprehensive as it handles all DNN operators
used in forming computer vision (CV) models in ONNX
Zoo [77].

BTD processes x86 executables, though its core
technique is mostly platform-independent.

Decompiling ex-
ecutables on other architectures requires vendor support for
reverse engineering toolchains ﬁrst.

We also ﬁnd that DNN
“executables” on some other architectures are not in stan-
dalone executable formats.

See the last paragraph of Sec. 2
for the signiﬁcance of decompiling x86 DNN executables,
and see Sec. 8 for discussions on cross-platform support.

BTD was evaluated by decompiling 64-bit x86 executables
emitted by eight versions of three production DL compil-
ers, TVM [22], Glow [85], NNFusion [64], which are de-
veloped by Amazon, Facebook, and Microsoft, respectively.

These compilers enable full optimizations during our eval-
uation.
```

---

## 8. [single_003_zh] LLM 在 NeuroDeX 的反编译管道中扮演什么角色？它达到了怎样的准确率？

**Type**: `method` | **Lang**: `ZH` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.2000 |
| 20 | 0.2000 | 0.6000 |

**Expected sources**: NeuroDeX

### Expected Chunks (5)

### 03e5ee11ed5284cb

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from DNN exe-
cutables using ghidra.

Inspired by previous works [6], [9], NeuroDeX can identify
the dimensions of operator parameters from disassembled
code in TVM compiler.

NeuroDeX further expands on their
methods, NeuroDeX also extracts the types of operator param-
eters and recover the optimized parameters’ dimensions.
```

### 2f2cb9ddcb1914fa

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute recovery, where it leverages dynamic anal-
ysis and code semantic understanding from LLMs to support
compatibility with various types of models.

Dynamic analysis
aims to monitor the runtime information of operator functions.

Dynamic analysis in NeuroDeX requires only trivial input that
satisfies the expected input format.

This is due to the fact
that any input can guarantee full coverage of the whole DNN
model, and the mathematical dependencies of intermediate
features are fixed.
```

### da2e9320264c822e

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The parameters of the function correspond sequentially to the
inputs and outputs of the operator.

Each type operator has
a fixed number of inputs and outputs, and NeuroDeX can
accurately recover parameters’ dimensions.

We validate this
characteristic across both historical and recent TVM versions,
ensuring the generality and robustness of our approach.

B.

Operator Type Recognition
The purpose of operator type recognition is to determine
the specific type of the operator function.

We manually analyze DL compiler’s support for DNN
operators [1], [2] and align it with the practice of general
DL frameworks like ONNX [11] to classify operators.

The
operators can be divided into four types as shown in Table II.

Type 1 isLayout Transformation.

This type of operator adjusts
TABLE II: Operator Classification
Type Operators Description
1.

Layout
Transformation
1.1 concat,split...
1.2 flatten,reshape,
transpose...

Inter-tensor layout transforma-
tion
Intra-tensor layout transforma-
tion
2.
```

### 09693a185e42519d

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Libsteal and Shi et al.’s work
do not guarantee sufficient accuracy; DND relies on symbolic
execution, which incurs significant overhead and limits the size
of supported models; Neuroscope only supports 12 DNN oper-
ators.

More importantly, these methods fail to provide adequate
support for fused operators from compilation optimizations.

Observation2:BTD considers the impact of compilation
optimizations and supports a wider range of operator types.

However, BTD trains machine learning model for each com-
piler version to make predictions.

This approach relies heavily
on training data and treats the compiler version as prior
knowledge, which limits its scalability in real world scenario.

Moreover, we find that about 57.9% of the training data in
TVM and 18.3% in GLOW appear in the test dataset, further
undermining the effectiveness of the method.
```

### 6647adfcb117af59

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 9 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The decompiler should also have cross-architecture
support capabilities.

C3:Quantized compiled models exhibit
new characteristics different from standard models, involving
quantization scaling factors between integer and float domains.

The decompiler needs to be compatible with these differences.

To address these challenges, we design NeuroDeX to imple-
ment a more comprehensive decompiler for DNN executables.

For C1:We systematically analyze the characteristics of oper-
ators in DL compilers and design a progressive operator type
recognition strategy.

NeuroDeX leverages dynamic analysis
and code semantic understanding from LLMs to support com-
patibility with various types of operators and fused operators.

For C2:Based on the operator type recognition method, we
subsequently implement operator attribute recovery and model
reconstruction, forming a complete decompilation pipeline
compatibility with various types of different models.

The
core technology of NeuroDeX is hardware-platform indepen-
dent, ensuring its cross-architecture support capabilities.
```

### Retrieved Top-20

**#1** — 49c598a0d4c59151 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.11-12 | sec=results | ci=16

```
To demonstrate the effectiveness of NeuroDeX on different
LLMs, we also compare the performance of different LLMs
including GPT-4.1 [38], Deepseekv3 [39], GPT-4o mini [40],
Gemini2.5 flash [41].

The selection of LLMs will affect TRA
directly.

Results are shown in Table IX.

Deepseekv3 and
GPT-4.1 perform well in all models across different compiler
settings.

Gemini2.5 flash struggles to identify operators of
GLOW, GPT-4o mini fails to identify TVM optimization
operators and GLOW operators.

I
```

**#2** — c88a1a6168cbec88 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.10-10 | sec=results | ci=5

```
The overhead of BTD and
NeuroDeX is shown in Table VI.

For TVM O0, TVM O3 and GLOW, the average time spent
by BTD is about6.79times,2.77times, and12.76times
that of NeuroDeX respectively.

The main time overhead for
NeuroDeX comes from network request to LLM and dynamic
memory monitor.

The time of LLM requests can fluctuate
due to network conditions.

However, in our implementation,
requests to LLM are executed through a single thread.

Using
a multi-threaded approach could easily optimize the
```

**#3** — e8d85764315c72e4 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-1 | sec=introduction | ci=2

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

N
```

**#4** — dd6347b07eaca9c2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-4 | sec=related_work | ci=11

```
The threat model used in our study is consistent with previ-
ous works [7]–[10] and is generally common and practical
in real-world scenarios.

The design of NeuroDeX aims to
highlight security risks of DNN executables and promote the
safe use of DL compilers.

Operator Recovery
DNN 
Executable
Operator Function 
Extraction
Dynamic 
Analysis 
LLM
Operator Type 
Recognition
Operator Attribute 
Recovery
Computational 
Graph Recovery
Model Weights 
Recovery
Model Reconstruction
High-level 
Model
Fi
```

**#5** — 6f0f7d6275f908ad | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-10 | sec=results | ci=4

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O
```

**#6** — ab34bb9750cf1e98 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.5-5 | sec=method | ci=9

```
Oth-
erwise, NeuroDeX starts recording the memory access during
the operator function execution, identifying the instruction that
initially accesses the parameter address.

From this instruction,
NeuroDeX performs taint analysis, tracking relevant registers
until first encounter a multiply or add instruction.

Activation
functions likeReluandClipare often attached to the tail of
the fused operator with repeated patterns in decompiled code.

NeuroDeX extracts the tail part of the decompiled code 
```

**#7** — 2c7d44730d74e147 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-3 | sec=related_work | ci=10

```
For
C3:NeuroDeX specifically adapts the model reconstruction
method to convert integer domain weights back to float do-
main.

NeuroDeX employs a learning-based weights recovery
approach that requires only a small amount of training data to
recover functionally very similar models.

D.

Threat Model
NeuroDeX is designed towards DNN executables deployed
on edge devices, where NeuroDeX can access DNN exe-
cutables compiled by DL compilers and extract the complete
executables.

DNN executables are 
```

**#8** — 7a9e9e6eeae883c2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.5-6 | sec=method | ci=10

```
NeuroDeX directly performs operator
type recognition by classifying the decompiled code with
LLM, which considers all operators as the candidate list and
determines the specific operator types within the candidate list
based on the mathematical semantics of operators.

Currently, NeuroDeX supports the most common operators
of ONNX (including but not limited to operators analyzed in
previous works), the complete list of operators is shown below.
```

**#9** — de39e46413babeba | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-1 | sec=abstract | ci=1

```
In this paper, we present NeuroDeX to unlock diverse sup-
port in decompiling DNN executables.

NeuroDeX leverages the
semantic understanding capabilities of LLMs along with dynamic
analysis to accurately and efficiently perform operator type
recognition, operator attribute recovery and model reconstruc-
tion.

NeuroDeX can recover DNN executables into high-level
models towards compilation optimizations, different architectures
and quantized compiled models.

We conduct experiments on
96 DNN exe
```

**#10** — e528851b2d3e6168 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.6-6 | sec=method | ci=13

```
Operator Attribute Recovery
Some operators contain specific attribute value, such as
the stride and padding ofConv.

To ensure the functional
consistency of the reconstructed model, it is essential to accu-
rately recover these attributes.

NeuroDeX combines dynamic
analysis and code semantic understanding from LLM to design
attribute recovery methods for different operators.

ForConv, NeuroDeX utilizes parameters’ dimensions of
these operators to recover attributes.

For TVM, dimensions
have be
```

**#11** — 2db892db94ebe962 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.7-7 | sec=method | ci=18

```
However, these attributes are often obvious in
the decompiled code, which can be extracted directly by
LLM.

RegardingConcat, the sequence of multiple inputs is
an attribute that should be extracted.

Moreover, at the O3
optimization level in TVM,Transposemay be fused afterCon-
cat.

NeuroDeX instruments the executable to record input and
output tensors ofConcat.

By enumerating the input order and
the number of channel shuffle groups inTranspose, NeuroDeX
simulates the forward ofConcatuntil the
```

**#12** — f04fd3863c6fcf65 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.10-10 | sec=results | ci=7

```
The repository of GLOW has
been marked as public archive now.

Therefore, we also use
NeuroDeX to analyze the latest TVM version (v0.17).

We
utilize NeuroDeX to decompile RQ1’s six models in TVM
0.17 repeatedly.

We evaluate NeuroDeX on six more different
models in TVM v0.17, aiming to cover more model structures
and varying hyperparameters for same model structure.

The
results are shown in Table VII.

NeuroDeX can recover nearly identical high-level models
for these 12 models across different
```

**#13** — e0b75a7c3a534224 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.10-10 | sec=results | ci=6

```
Moreover, it is noteworthy that NeuroDeX’s approach does
not involve heavy analysis constrained by hardware resources.

In contrast, the methods utilized by BTD demand considerable
memory and CPU resources, which can lead to performance
degradation on consumer-grade devices.

Answer to RQ2:NeuroDeX can decompile DNN executa-
bles with a shorter time overhead than SOTA methods and
NeuroDeX does not rely heavily on hardware resources.

C.

RQ3: Comprehensiveness
To answer RQ3, we aim to evaluate N
```

**#14** — 176226c123544195 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.11-11 | sec=results | ci=13

```
The queries for recovered
model are more likely to be classified into different categories
than original high-level models.

This is due to the character-
istics of the global scale method and the inevitable precision
loss during conversion between int and float domains, rather
than design flaws in NeuroDeX.

Answer to RQ3:We evaluate NeuroDeX on a wider range
of models and aarch64 architecture.

Results illustrates Neu-
roDeX’s adaptability to various models and different ar-
chitectures; Neuro
```

**#15** — fe80626d0b613db0 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.7-7 | sec=method | ci=17

```
NeuroDeX then enumerates different combinations
of kernel size, stride and padding, simulates the forward of
theMaxpooluntil the computed tensor exactly matches the
actual output tensor.

It is worth noting that any trivial input
can achieve full coverage, so NeuroDeX only needs one trivial
input to simulate forward.

In the case ofAvgpool, kernel size
is evidently reflected in the decompiled code.

For example,
patterns like “∗0.020408(1/49)” repeatedly appear, indicating
that kernel size is 7.
```

**#16** — 74238bd6bc7e40c9 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=3

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of Neuro
```

**#17** — 05e588c3d8436d1d | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.11-11 | sec=results | ci=15

```
NeuroDeX can fix them by matching predefined patterns of
operator split.

Type 2:These errors can be handled during model recon-
struction.

By comparing the value of intermediate layer in
high-level models with those from instrumented executables,
NeuroDeX can locate the different operators and update the
activation function according to value difference.

After fixing
the activation function, NeuroDeX can continuously record the
output value of the error operator until it matches the expected

```

**#18** **[HIT]** — 03e5ee11ed5284cb | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.4-4 | sec=method | ci=1

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from D
```

**#19** — cdce554512cc3586 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=0

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implement
```

**#20** — cd7444c98cc84207 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.12-12 | sec=conclusion | ci=0

```
In this work, we design NeuroDeX to provide diverse
support in decompiling DNN executables. NeuroDeX recovers
DNN executables back into high-level models through oper-
ator type recognition, operator attribute recovery and model
reconstruction. NeuroDeX leverages the semantic understand-
ing capabilities of LLMs along with dynamic analysis to
construct a comprehensive and robust decompilation pipeline.
Our evaluations demonstrate that NeuroDeX can successfully
decompile DNN executables across di
```

### Missed Chunks (4 — expected but NOT in top-20)

### 2f2cb9ddcb1914fa

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute recovery, where it leverages dynamic anal-
ysis and code semantic understanding from LLMs to support
compatibility with various types of models.

Dynamic analysis
aims to monitor the runtime information of operator functions.

Dynamic analysis in NeuroDeX requires only trivial input that
satisfies the expected input format.

This is due to the fact
that any input can guarantee full coverage of the whole DNN
model, and the mathematical dependencies of intermediate
features are fixed.
```

### da2e9320264c822e

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The parameters of the function correspond sequentially to the
inputs and outputs of the operator.

Each type operator has
a fixed number of inputs and outputs, and NeuroDeX can
accurately recover parameters’ dimensions.

We validate this
characteristic across both historical and recent TVM versions,
ensuring the generality and robustness of our approach.

B.

Operator Type Recognition
The purpose of operator type recognition is to determine
the specific type of the operator function.

We manually analyze DL compiler’s support for DNN
operators [1], [2] and align it with the practice of general
DL frameworks like ONNX [11] to classify operators.

The
operators can be divided into four types as shown in Table II.

Type 1 isLayout Transformation.

This type of operator adjusts
TABLE II: Operator Classification
Type Operators Description
1.

Layout
Transformation
1.1 concat,split...
1.2 flatten,reshape,
transpose...

Inter-tensor layout transforma-
tion
Intra-tensor layout transforma-
tion
2.
```

### 09693a185e42519d

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Libsteal and Shi et al.’s work
do not guarantee sufficient accuracy; DND relies on symbolic
execution, which incurs significant overhead and limits the size
of supported models; Neuroscope only supports 12 DNN oper-
ators.

More importantly, these methods fail to provide adequate
support for fused operators from compilation optimizations.

Observation2:BTD considers the impact of compilation
optimizations and supports a wider range of operator types.

However, BTD trains machine learning model for each com-
piler version to make predictions.

This approach relies heavily
on training data and treats the compiler version as prior
knowledge, which limits its scalability in real world scenario.

Moreover, we find that about 57.9% of the training data in
TVM and 18.3% in GLOW appear in the test dataset, further
undermining the effectiveness of the method.
```

### 6647adfcb117af59

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 9 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The decompiler should also have cross-architecture
support capabilities.

C3:Quantized compiled models exhibit
new characteristics different from standard models, involving
quantization scaling factors between integer and float domains.

The decompiler needs to be compatible with these differences.

To address these challenges, we design NeuroDeX to imple-
ment a more comprehensive decompiler for DNN executables.

For C1:We systematically analyze the characteristics of oper-
ators in DL compilers and design a progressive operator type
recognition strategy.

NeuroDeX leverages dynamic analysis
and code semantic understanding from LLMs to support com-
patibility with various types of operators and fused operators.

For C2:Based on the operator type recognition method, we
subsequently implement operator attribute recovery and model
reconstruction, forming a complete decompilation pipeline
compatibility with various types of different models.

The
core technology of NeuroDeX is hardware-platform indepen-
dent, ensuring its cross-architecture support capabilities.
```

### False Positives (19 — in top-20 but NOT expected)

### 49c598a0d4c59151

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 11 |
| page_end | 12 |
| chunk_index | 16 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
To demonstrate the effectiveness of NeuroDeX on different
LLMs, we also compare the performance of different LLMs
including GPT-4.1 [38], Deepseekv3 [39], GPT-4o mini [40],
Gemini2.5 flash [41].

The selection of LLMs will affect TRA
directly.

Results are shown in Table IX.

Deepseekv3 and
GPT-4.1 perform well in all models across different compiler
settings.

Gemini2.5 flash struggles to identify operators of
GLOW, GPT-4o mini fails to identify TVM optimization
operators and GLOW operators.

In summary, NeuroDeX does
not rely on a specific LLM.

LLMs that perform well in general
domains are equally suitable for completing the operator type
recognition task.

Answer to RQ4:NeuroDeX has a stable error-fix mech-
anism that effectively addresses different types of errors.

NeuroDeX is not sensitive to the selection of LLMs, and
various different LLMs are suitable for NeuroDeX.
```

### c88a1a6168cbec88

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 5 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The overhead of BTD and
NeuroDeX is shown in Table VI.

For TVM O0, TVM O3 and GLOW, the average time spent
by BTD is about6.79times,2.77times, and12.76times
that of NeuroDeX respectively.

The main time overhead for
NeuroDeX comes from network request to LLM and dynamic
memory monitor.

The time of LLM requests can fluctuate
due to network conditions.

However, in our implementation,
requests to LLM are executed through a single thread.

Using
a multi-threaded approach could easily optimize the time
overhead.

EfficientNet represents high-capacity and compu-
tationally intensive models, while ShuffleNetv2 serves as an
example of lightweight model.

ResNet18 and InceptionV1 are
further included to encompass a broader range of distinct
architectural designs.

According to our evaluation results, Neu-
roDeX performs better than BTD in time overhead obviously
across all these various models.
```

### e8d85764315c72e4

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX begins by collecting operator function information
including disassembled and decompiled code from DNN exe-
cutables.

Next, NeuroDeX utilizes the semantic understanding
abilities of LLMs to design an accurate and scalable method
for operator type recognition.

Subsequently, NeuroDeX uti-
lizes dynamic analysis and LLM-based code understanding to
finish operator attribute recovery.

Finally, NeuroDeX recon-
structs the model’s computational graph and weights through
dynamic analysis.

NeuroDeX features an accurate operator
type recognition and operator attribute recovery mechanism
that does not rely on prior knowledge such as compiler ver-
sions or training data.

NeuroDeX can accurately recover fused
operators and its core components do not depend on resource-
intensive analysis techniques like symbolic execution, allowing
for rapid and efficient analysis.

Furthermore, NeuroDeX is
extendable to different architectures, different DL compilers,
and quantized models.
```

### dd6347b07eaca9c2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 11 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The threat model used in our study is consistent with previ-
ous works [7]–[10] and is generally common and practical
in real-world scenarios.

The design of NeuroDeX aims to
highlight security risks of DNN executables and promote the
safe use of DL compilers.

Operator Recovery
DNN 
Executable
Operator Function 
Extraction
Dynamic 
Analysis 
LLM
Operator Type 
Recognition
Operator Attribute 
Recovery
Computational 
Graph Recovery
Model Weights 
Recovery
Model Reconstruction
High-level 
Model
Fig. 3: Workflow of NeuroDeX
```

### 6f0f7d6275f908ad

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW
BTD 676.3 265.0 2904.7 468.7 681.2 2416.3 982.8 705.6 4328.8 152.7 92.8 296.2
NeuroDeX 76.9 122.2 204.5 41.4 127.9 129.2 208.3 288.8 304.7 66.0 80.9 75.4
for fair comparison.

The compiler version for our experiment
is TVM v0.9dev and GLOW 2022.
```

### ab34bb9750cf1e98

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 9 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Oth-
erwise, NeuroDeX starts recording the memory access during
the operator function execution, identifying the instruction that
initially accesses the parameter address.

From this instruction,
NeuroDeX performs taint analysis, tracking relevant registers
until first encounter a multiply or add instruction.

Activation
functions likeReluandClipare often attached to the tail of
the fused operator with repeated patterns in decompiled code.

NeuroDeX extracts the tail part of the decompiled code and
uses LLM to verify if activation is accompanied by the fused
operator.

NeuroDeX employs the same processing method for
other fused operators like the operator consisting ofConcat
and activation.

NeuroDeX provides more comprehensive anal-
ysis and support for fused operators than previous works.

For GLOW, the disassembled code does not contain dimen-
sion information, but the optimization strategy in GLOW is
relatively simple.

Operator fusion almost only occurs after
Convwith activation.
```

### 2c7d44730d74e147

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 10 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
For
C3:NeuroDeX specifically adapts the model reconstruction
method to convert integer domain weights back to float do-
main.

NeuroDeX employs a learning-based weights recovery
approach that requires only a small amount of training data to
recover functionally very similar models.

D.

Threat Model
NeuroDeX is designed towards DNN executables deployed
on edge devices, where NeuroDeX can access DNN exe-
cutables compiled by DL compilers and extract the complete
executables.

DNN executables are generated through standard
DL compiler pipeline with optional compiler optimization.

NeuroDeX has the capability to execute the executables and
monitor memory status during execution.

NeuroDeX requires
no prior knowledge of model architecture or weights, it only
needs trivial inputs that satisfy the expected input format.

The
ultimate goal of NeuroDeX is to decompile executables into
identical white-box high-level DL models, effectively extract-
ing the computational graph, weights and other information.
```

### 7a9e9e6eeae883c2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 5 |
| page_end | 6 |
| chunk_index | 10 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX directly performs operator
type recognition by classifying the decompiled code with
LLM, which considers all operators as the candidate list and
determines the specific operator types within the candidate list
based on the mathematical semantics of operators.

Currently, NeuroDeX supports the most common operators
of ONNX (including but not limited to operators analyzed in
previous works), the complete list of operators is shown below.
```

### de39e46413babeba

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | abstract |
| section_title | Abstract/摘要 |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In this paper, we present NeuroDeX to unlock diverse sup-
port in decompiling DNN executables.

NeuroDeX leverages the
semantic understanding capabilities of LLMs along with dynamic
analysis to accurately and efficiently perform operator type
recognition, operator attribute recovery and model reconstruc-
tion.

NeuroDeX can recover DNN executables into high-level
models towards compilation optimizations, different architectures
and quantized compiled models.

We conduct experiments on
96 DNN executables across 12 common DNN models.

Extensive
experimental results demonstrate that NeuroDeX can decompile
non-quantized executables into nearly identical high-level models.

NeuroDeX can recover functionally similar high-level models
for quantized executables, achieving an average top-1 accuracy
of 72%.

NeuroDeX offers a more comprehensive and effective
solution compared to previous DNN executables decompilers.

Index Terms—DL compiler, decompiler, model stealing.
```

### e528851b2d3e6168

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 13 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Operator Attribute Recovery
Some operators contain specific attribute value, such as
the stride and padding ofConv.

To ensure the functional
consistency of the reconstructed model, it is essential to accu-
rately recover these attributes.

NeuroDeX combines dynamic
analysis and code semantic understanding from LLM to design
attribute recovery methods for different operators.

ForConv, NeuroDeX utilizes parameters’ dimensions of
these operators to recover attributes.

For TVM, dimensions
have been collected from disassembled code introduced in
operator function extraction.

For GLOW, NeuroDeX employs
dynamic analysis to collect parameters’ dimensions.

TheConv
in GLOW has four parameters:out,in,weightandbias.
```

### 2db892db94ebe962

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 18 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
However, these attributes are often obvious in
the decompiled code, which can be extracted directly by
LLM.

RegardingConcat, the sequence of multiple inputs is
an attribute that should be extracted.

Moreover, at the O3
optimization level in TVM,Transposemay be fused afterCon-
cat.

NeuroDeX instruments the executable to record input and
output tensors ofConcat.

By enumerating the input order and
the number of channel shuffle groups inTranspose, NeuroDeX
simulates the forward ofConcatuntil the computed tensor
exactly matches the actual output tensor.

Similarly,Transform
may also involveTransposefused afterward, NeuroDeX deter-
mines the attribute values same withConcat.

NeuroDeX only
requires straightforward prompt for operator attribute recovery.

Here is the simplified prompt in operator attribute recovery:
Simplified prompt of operator attribute recovery
You are an AI assistant specialized in analyzing opera-
tors.

Given the decompiled code of a{type}operator:
{pseudocode}, infer the{attribute}.
```

### f04fd3863c6fcf65

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 7 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The repository of GLOW has
been marked as public archive now.

Therefore, we also use
NeuroDeX to analyze the latest TVM version (v0.17).

We
utilize NeuroDeX to decompile RQ1’s six models in TVM
0.17 repeatedly.

We evaluate NeuroDeX on six more different
models in TVM v0.17, aiming to cover more model structures
and varying hyperparameters for same model structure.

The
results are shown in Table VII.

NeuroDeX can recover nearly identical high-level models
for these 12 models across different optimization levels.
```

### e0b75a7c3a534224

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 6 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Moreover, it is noteworthy that NeuroDeX’s approach does
not involve heavy analysis constrained by hardware resources.

In contrast, the methods utilized by BTD demand considerable
memory and CPU resources, which can lead to performance
degradation on consumer-grade devices.

Answer to RQ2:NeuroDeX can decompile DNN executa-
bles with a shorter time overhead than SOTA methods and
NeuroDeX does not rely heavily on hardware resources.

C.

RQ3: Comprehensiveness
To answer RQ3, we aim to evaluate NeuroDeX on a wider
range of models and on aarch64 architecture to demonstrate
its versatility.

We also discuss the compatibility with quantized
compiled models of NeuroDeX.

We first evaluate NeuroDeX on the latest compiler verison
to verify its scalability.

According to our observations, TVM
is a project that is frequently maintained; GLOW is a stable
project, we have counted the commits since 2023, which
total only about 100, and the majority are related to feature
maintenance and bug fixes.
```

### 176226c123544195

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 13 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The queries for recovered
model are more likely to be classified into different categories
than original high-level models.

This is due to the character-
istics of the global scale method and the inevitable precision
loss during conversion between int and float domains, rather
than design flaws in NeuroDeX.

Answer to RQ3:We evaluate NeuroDeX on a wider range
of models and aarch64 architecture.

Results illustrates Neu-
roDeX’s adaptability to various models and different ar-
chitectures; NeuroDeX can decompile quantized compiled
DNN executables and the recovered models are highly
similar in functionality to the original models.

D.

RQ4: Robustness
To answer RQ4, we classify the error cases encountered by
NeuroDeX and introduce specific strategies to fix each type.

We also evaluate NeuroDeX on more LLMs.

In operator type recognition, NeuroDeX may occasionally
encounter errors.

Additionally, due to the inherent output
variability of LLMs, repeated analysis might yield different
error samples.
```

### fe80626d0b613db0

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 17 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX then enumerates different combinations
of kernel size, stride and padding, simulates the forward of
theMaxpooluntil the computed tensor exactly matches the
actual output tensor.

It is worth noting that any trivial input
can achieve full coverage, so NeuroDeX only needs one trivial
input to simulate forward.

In the case ofAvgpool, kernel size
is evidently reflected in the decompiled code.

For example,
patterns like “∗0.020408(1/49)” repeatedly appear, indicating
that kernel size is 7.

LLM can extract kernel size from
decompiled code to reduce the overhead of dynamic analysis.

NeuroDeX infers stride and padding ofAvgpoolthrough the
constraint enumeration method same withConv.

Local response normalization (lrn) has attributes:size,β,α,
biasandCliphas attributes:min,max.

The attributes of lrn
and clip generally have a large search space, making them
unsuitable for simulation execution using dynamic analysis
enumeration.
```

### 74238bd6bc7e40c9

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of NeuroDeX
with BTD and analyze the underlying reasons.

We choose four models: EfficientNet, ResNet18, Incep-
tionv1 and ShuffleNetv2.

These models cover a range of
weights size and topological complexities, enabling a compre-
hensive evaluation of the overhead associated with BTD and
NeuroDeX.

The model reconstruction strategies for NeuroDeX
and BTD are identical.

Therefore, we only compare the time
associated with operator type recognition and operator attribute
recovery processes.
```

### 05e588c3d8436d1d

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 15 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX can fix them by matching predefined patterns of
operator split.

Type 2:These errors can be handled during model recon-
struction.

By comparing the value of intermediate layer in
high-level models with those from instrumented executables,
NeuroDeX can locate the different operators and update the
activation function according to value difference.

After fixing
the activation function, NeuroDeX can continuously record the
output value of the error operator until it matches the expected
value of the executable.

Type 3:These errors can directly lead to crash of model
construction.

We can observe the exception information of
the high-level model to locate error operators.

NeuroDeX can
locate error operators and fix them by manually checking the
decompiled code.

After fixing the error operator, NeuroDeX
can continuously record the output value of error operator until
it matches the expected value of executable.
```

### cdce554512cc3586

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In the evaluation, we intend to answer the following ques-
tions:
RQ1 (Correctness):How does NeuroDeX’s performance
in correctness compare to State-of-the-Art (SOTA)
method?

RQ2 (Efficiency):What is the overhead of NeuroDeX com-
pared to SOTA method?

RQ3 (Comprehensiveness):Can NeuroDeX cover a wider
range of models and different architectures?

RQ4 (Robustness):Can NeuroDeX fix errors encountered
during the decompile process and what is the impact
of different LLMs on NeuroDeX?

A.

Implementation & Environment
We implement NeuroDeX with about 8K LOC Python code
and about 1K LOC C++ code.

In our experiments, we select
GPT-4o [20] for its superior performance in code understand-
ing [21], [22] and the large size (128K) of context window,
which is sufficient to cover the operator functions.
```

### cd7444c98cc84207

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | conclusion |
| section_title | VIII. CONCLUSION |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In this work, we design NeuroDeX to provide diverse
support in decompiling DNN executables. NeuroDeX recovers
DNN executables back into high-level models through oper-
ator type recognition, operator attribute recovery and model
reconstruction. NeuroDeX leverages the semantic understand-
ing capabilities of LLMs along with dynamic analysis to
construct a comprehensive and robust decompilation pipeline.
Our evaluations demonstrate that NeuroDeX can successfully
decompile DNN executables across different DL compiler set-
tings, different architectures and quantized compiled models.
```

---

## 9. [single_006_zh] 根据 Pitfalls 综述，使用 LLM 进行代码智能的主要陷阱有哪些类别？

**Type**: `fact` | **Lang**: `ZH` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.2000 | 0.8000 |
| 20 | 0.4000 | 0.8000 |

**Expected sources**: Pitfalls

### Expected Chunks (5)

### 8940d9ce37888e6f

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Their superior
performance stems from the fact that many LMs are trained on vast and diverse code repositories, enabling LMs
to discern complex syntax, comprehend semantic context, and effectively predict code sequences [162].

However, the lack of transparency, often termed “black-box”, poses significant challenges and concerns [151,
153].

In other words, while language models for code intelligence (LM4Code) approaches offer powerful capabili-
ties,theyoftenlacktransparencyintheirunderlyingreasoninganddecision-makingprocess.

Tantithamthavorn et
al. [65, 153] also raised concerns that such a lack of transparency often leads to a lack of adoption of LM4Code
in practice.

Consequently, hidden or neglected pitfalls in data or algorithms may persist, leading to unrealistic
performance evaluation and unreliable code recommendations [55, 152].
```

### bb1fcd8c4944f008

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
For example, Shiet al. [143] found
that noisy data (e.g., empty methods or duplicated code) was prevalent in widely-used benchmark datasets for
code summarization, with contamination levels ranging between 31% to 66%.

By filtering out this noisy data,
performance metrics like the BLEU-4 score witnessed a substantial increase (e.g., from 11.36% to 16.48%).

Similarly,
Sun et al. [148] highlighted a substantial amount of noise in user queries across various code search benchmark
datasets.

Such instances underscore the hidden data noise that might undermine the trustworthiness of code
produced or recommended by LMs.

What is more concerning is when these pitfalls go unnoticed, which raises
significant questions about the reliability and integrity of the LM4Code systems built on them, thereby preventing
the adoption of research advances in academia and industry.
```

### da8b2a79f0f17e81

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
As LMs become increasingly prevalent in code intelligence despite increasing obstacles, there emerges an
urgent need for a comprehensive understanding of potential pitfalls within LM4Code systems.

This is not limited
to pitfall identification; it demands a deeper exploration into the understanding of the implications of these
pitfalls, current solutions, and possible challenges.

Although there is a growing body of research concerning or
addressing pitfalls in LM4Code [97, 143, 148, 191], the domain lacks a comprehensive and systematic overview of
theseefforts.

Withoutsuchanoverview,researchers,developers,andpractitionerspotentiallyoverlooksignificant
pitfalls identified in previous studies.

In this study, we conducted a systematic literature review, adhering to a
well-defined approach that identifies, evaluates, and interprets the relevant literature focusing on the pitfalls
within LM4Code.

Our contributions of this paper are as follows:
• Paper Collection of Pitfalls in LM4Code.
```

### 58a91a46accb3900

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 4 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Through a rigorous systematic literature review (SLR) protocol as
outlined by [70, 72] and after an in-depth analysis of the primary studies, we collected 121 primary papers
(spanning 2018 to 2024) closely related to evaluating or addressing LM4Code pitfalls.

Comprehensive
details on our review process and the collected papers are available online1.
• Comprehensive Taxonomy.

We conducted a qualitative and quantitative synthesis of the collected studies.

We present a taxonomy of the collected studies according to the LM4Code lifecycle, including data
collectionandlabeling,systemdesignandlearning,performanceevaluation,deployment,andmaintenance.

Our synthesis investigates the pitfalls present in LM4Code, summarizes the implications of these pitfalls,
investigates how these issues are addressed, and outlines future challenges in this field.
1https://github.com/yueyueL/ReliableLM4Code
ACM Trans.

Softw.

Eng.

Methodol.
```

### f70e48b81eb48682

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 8 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
This research
question aims to identify the prevalent pitfalls in LM4Code systems, exploring how they could affect
various stages of the learning-based system lifecycle.
• RQ2: What solutions have been proposed to address these pitfalls?

This research question reviews
the existing body of literature to identify proposed approaches for solving the identified pitfalls.

ACM Trans.

Softw.

Eng.

Methodol.
4 • Xinyu She, Yue Liu, Yanjie Zhao, Yiling He, Li Li, Chakkrit Tantithamthavorn, Zhan Qin, and Haoyu Wang
• RQ3: What are the implications of these pitfalls?
```

### Retrieved Top-20

**#1** — b6092ceb2394c280 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.9-10 | sec=method | ci=0

```
This section examines pitfalls in the system design and learning process for LM4Code.

The training of these
LM4Code models directly impacts their quality and efficacy for empowering code intelligence.

However, several
challenges arise in crafting optimal model architectures, formulating strategic training-testing approaches,
refining data preprocessing techniques, and selecting suitable learning algorithms.

Each design decision risks
introducing pitfalls that can undermine model robustness an
```

**#2** — fc069a30deb2a23a | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.9-9 | sec=method | ci=14

```
They found that, compared
to the high performance on standard benchmarks like HUMANEVAL [19], popular LLMs experienced a significant
performance drop (an average of 39.4%) on EVOEVAL, highlighting the limitations of standard benchmarks and
the effectiveness of their approach.

Additionally, EvalPlus [90] combines emerging LLM-based methods with
traditional mutation-based approaches for test case generation.

It continuously expands inputs using LLM and
applies a greedy set-covering approach for 
```

**#3** — ea2a2e488a871826 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.10-11 | sec=method | ci=5

```
Meanwhile, spurious correlations have become more prominent
with the advent of explainable artificial intelligence (XAI) techniques for elucidating model reasoning [22,
151, 153].

Discussions around inappropriate model design remain ongoing as new frameworks and learning
strategies continue to emerge.

Similar to our observations regarding the data collection and labeling process,
Figure 7 reveals a greater emphasis on modern Transformer-based language models and GPT series compared to
conventi
```

**#4** — 7f16a532b9759a15 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.11-11 | sec=method | ci=8

```
While Shiet al. [140]
unravels how transformer-based models allocate attention for code summarization, Wanet al. [160] probes into
the nuances of attention during code-to-code translation.

These XAI approaches can serve to identify and rectify
model pitfalls, ensuring the reliability of LM4Code applications.

Model Optimization Strategies:In light of the pitfalls introduced by inappropriate model design, researchers
have turned to model optimization strategies to address and minimize their effe
```

**#5** — 91a40a4af6d5eccf | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.11-11 | sec=method | ci=9

```
Secondly, model nnsembling is gaining
traction, where the strengths of multiple models are leveraged to offset individual biases, as seen in the work by
Zhanget al. [198]whichemploysmultipleviewsofthesamedataformorerobustpredictions.

Lastly,regularization
and fine-tuning techniques play a pivotal role.

Regularization, such as dropout or L2 regularization, helps in
preventing overfitting, while fine-tuning allows pre-trained models, like CodeBERT, to adapt to specific dataset
nuances, as demons
```

**#6** — 90f870888cde247f | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.10-10 | sec=method | ci=4

```
Similarly, the
encoder-decoder framework used in code summarization might neglect the hierarchical nature of code or struggle
with sequence generation, leading to inadequate summaries [161, 170].

This issue is not limited to traditional
architectures.

Even modern program repair models, adapted from neural machine translation, face design-related
challenges that affect their translation accuracy and diversity [27, 103].

While there are innovative attempts such
as leveraging deep reinforcement 
```

**#7** — 7a4d8a93cbd46f78 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.23-23 | sec=discussion | ci=2

```
Addressing the identified pitfalls is vital for advancing robust and reliable
LM4Code techniques.

As our study reveals, solutions like data cleaning, model explainability, optimized model
design, and rigorous benchmarking have shown promise in mitigating certain pitfalls.

However, these solutions,
although effective in specific contexts, may not be universally applicable due to the complexity and ever-evolving
nature of the software engineering landscape.

A coordinated effort by the community
```

**#8** — 7e9d2ce0a19b56c5 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.23-23 | sec=discussion | ci=0

```
8.1 Recommendations for LM4Code Research
Our systematic literature review reveals numerous pitfalls that can undermine the realistic performance and
real-world effectiveness of LM4Code systems.

These pitfalls span the data, models, evaluation, and deployment
phases of the LM4Code lifecycle.

LM4Code has become an increasingly prominent research area, evidenced by
the rapid increase in publications.

A prior survey by Houet al. [54] uncovered 229 papers on large language
models for software engi
```

**#9** **[HIT]** — da8b2a79f0f17e81 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.2-2 | sec=introduction | ci=3

```
As LMs become increasingly prevalent in code intelligence despite increasing obstacles, there emerges an
urgent need for a comprehensive understanding of potential pitfalls within LM4Code systems.

This is not limited
to pitfall identification; it demands a deeper exploration into the understanding of the implications of these
pitfalls, current solutions, and possible challenges.

Although there is a growing body of research concerning or
addressing pitfalls in LM4Code [97, 143, 148, 191], the d
```

**#10** — 187fbd5de9fc878c | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.3-3 | sec=introduction | ci=7

```
While related research evaluating LM4Code [16, 93, 108, 178] identifies some issues, our
work distinguishes itself in two key ways: (1) we employ a rigorous SLR methodology that systematically
identifies and categorizes pitfalls, and (2) we present a comprehensive taxonomy structured around the entire
LLM lifecycle, from dataset construction to deployment.

This approach enables us to systematically analyze not
only the identified issues but also their corresponding solutions and practical impac
```

**#11** **[HIT]** — f70e48b81eb48682 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.3-4 | sec=introduction | ci=8

```
This research
question aims to identify the prevalent pitfalls in LM4Code systems, exploring how they could affect
various stages of the learning-based system lifecycle.
• RQ2: What solutions have been proposed to address these pitfalls?

This research question reviews
the existing body of literature to identify proposed approaches for solving the identified pitfalls.

ACM Trans.

Softw.

Eng.

Methodol.
4 • Xinyu She, Yue Liu, Yanjie Zhao, Yiling He, Li Li, Chakkrit Tantithamthavorn, Zhan Qin, 
```

**#12** — 570772c1a3095dcc | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.23-23 | sec=discussion | ci=1

```
Inthisstudy,wesummarizedmultiplecommonpitfallsassociatedwithLM4Code.

These pitfalls, each with distinct implications, highlight the inherent complexities in applying LM4Code to real-
world software engineering problems.

As our review results demonstrate, pitfalls can introduce unrealistic
performance evaluation, compromise model efficacy, and raise security concerns.

Thus, it becomes important
for future LM4Code research to recognize and avoid potential pitfalls when building LM4Code systems 
```

**#13** — dde2030a747deee1 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.15-15 | sec=results | ci=15

```
There exist various challenges when such LM4Code systems are deployed in practice, like security threats and
how LM4Code systems should be updated to adapt the rapidly changing software practices.

This section discusses
pitfalls, implications, and current solutions when deploying and maintaining LM4Code.
6.1 RQ1-Pitfalls
In our literature review, we identified 38 research papers involving the pitfalls of LM4Code deployment and
maintenance.

This number of identified publications surpasses that 
```

**#14** — 58e05fafbfcae8cb | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.6-6 | sec=method | ci=0

```
ØData SnoopingØSpurious CorrelationsØInappropriate Model Design
Performance evaluation (35)ØInappropriate BaselineØInappropriate Evaluation DatasetØLack of Stability EvaluationØInappropriate Performance Measures
Deployment and maintenance (38)
ØReal-World ConstraintsØAttack ThreatsØSecurity Concerns in Generated Code
Figure 3.

The overview of pitfalls of LMs for code intelligence
specific, we segment the pitfalls into four key aspects of the LM pipeline based on the LM4Code lifecycle: data
coll
```

**#15** — 1e7857e3861e9475 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.19-20 | sec=results | ci=34

```
The implications highlight that real-world deployment introduces complex
challenges for LM4Code systems.
7 RQ3-IMPLICATIONS
The implications of pitfalls in LM4Code span across multiple dimensions, from direct technical impacts to
broader research validity concerns.

The ramifications of these pitfalls and biases extend beyond merely impacting
research performance and reproducibility from an evaluative standpoint.

They also contribute to misleading
benchmarksandpotentialsecurityvulnerabilitieswi
```

**#16** — 4d0b270a9126b9b1 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.1-1 | sec=abstract | ci=1

```
Such challenges drive the need for a comprehensive understanding - not just identifying these issues but delving
into their possible implications and existing solutions to build more reliable language models tailored to code intelligence.

Based on a well-defined systematic research approach, we conducted an extensive literature review to uncover the pitfalls
inherent in LM4Code.

Finally, 121 primary studies from top-tier venues have been identified.

After carefully examining these
studies, we
```

**#17** — 247013ec6baa4e33 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.10-10 | sec=method | ci=3

```
Actually, introducing advanced pre-trained models like CodeBERT has
not eliminated these pitfalls.

Specifically, if not fine-tuned appropriately for downstream tasks, these models
might still overemphasize basic elements like keywords over richer code semantics [198].

Inappropriate Model Design:Inappropriate model design in LM4Code arises when the underlying architecture
fails to capture critical characteristics of code, such as hierarchy and composition.

The inability to construct robust
sem
```

**#18** — 63b73457012267c6 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.6-6 | sec=method | ci=2

```
In this section, we provide a brief description of related studies and discuss
the implications and potential solutions during the data collection and labeling stages.
3.1 RQ1-Pitfalls
From the collected papers, we identified 22 research studies focusing on pitfalls during the data collection and
labeling process.

Table 2 presents the statistics of literature on this topic, where the pitfalls can be grouped into
three main categories.

Unbalanced Distribution:Unbalanced distribution arises when
```

**#19** — 0d9684287a79f05b | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.6-6 | sec=method | ci=1

```
The implications of these pitfalls (RQ3) are discussed in
Section 7, and in Section 8, we further discuss open challenges and promising research directions.

This organized
structure enables a comprehensive analysis of pitfalls and considerations across the entire LM4Code pipeline.

Our taxonomy aims to provide crucial insights for developing more robust, reliable, and practical LM systems for
code intelligence tasks.
3 DATA COLLECTION AND LABELING
The data-hungry language models require large-s
```

**#20** — ab25112d13aae5d7 | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.11-11 | sec=method | ci=7

```
Model Interpretability:To address the biases inherent in LM4Code, especially spurious correlations, improving
model interpretability has emerged as a crucial solution [151].

By examining the decision-making process of
LM4Code models, researchers are better positioned to pinpoint and mitigate pitfalls, leading to more reliable
predictions [50].

Within vulnerability detection, Fuet al. [38], Liet al. [80], and Zouet al. [203] proposed methods
to enhance explanation accuracy, leveraging sophistic
```

### Missed Chunks (3 — expected but NOT in top-20)

### 8940d9ce37888e6f

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Their superior
performance stems from the fact that many LMs are trained on vast and diverse code repositories, enabling LMs
to discern complex syntax, comprehend semantic context, and effectively predict code sequences [162].

However, the lack of transparency, often termed “black-box”, poses significant challenges and concerns [151,
153].

In other words, while language models for code intelligence (LM4Code) approaches offer powerful capabili-
ties,theyoftenlacktransparencyintheirunderlyingreasoninganddecision-makingprocess.

Tantithamthavorn et
al. [65, 153] also raised concerns that such a lack of transparency often leads to a lack of adoption of LM4Code
in practice.

Consequently, hidden or neglected pitfalls in data or algorithms may persist, leading to unrealistic
performance evaluation and unreliable code recommendations [55, 152].
```

### bb1fcd8c4944f008

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
For example, Shiet al. [143] found
that noisy data (e.g., empty methods or duplicated code) was prevalent in widely-used benchmark datasets for
code summarization, with contamination levels ranging between 31% to 66%.

By filtering out this noisy data,
performance metrics like the BLEU-4 score witnessed a substantial increase (e.g., from 11.36% to 16.48%).

Similarly,
Sun et al. [148] highlighted a substantial amount of noise in user queries across various code search benchmark
datasets.

Such instances underscore the hidden data noise that might undermine the trustworthiness of code
produced or recommended by LMs.

What is more concerning is when these pitfalls go unnoticed, which raises
significant questions about the reliability and integrity of the LM4Code systems built on them, thereby preventing
the adoption of research advances in academia and industry.
```

### 58a91a46accb3900

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 4 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Through a rigorous systematic literature review (SLR) protocol as
outlined by [70, 72] and after an in-depth analysis of the primary studies, we collected 121 primary papers
(spanning 2018 to 2024) closely related to evaluating or addressing LM4Code pitfalls.

Comprehensive
details on our review process and the collected papers are available online1.
• Comprehensive Taxonomy.

We conducted a qualitative and quantitative synthesis of the collected studies.

We present a taxonomy of the collected studies according to the LM4Code lifecycle, including data
collectionandlabeling,systemdesignandlearning,performanceevaluation,deployment,andmaintenance.

Our synthesis investigates the pitfalls present in LM4Code, summarizes the implications of these pitfalls,
investigates how these issues are addressed, and outlines future challenges in this field.
1https://github.com/yueyueL/ReliableLM4Code
ACM Trans.

Softw.

Eng.

Methodol.
```

### False Positives (18 — in top-20 but NOT expected)

### b6092ceb2394c280

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 0 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
This section examines pitfalls in the system design and learning process for LM4Code.

The training of these
LM4Code models directly impacts their quality and efficacy for empowering code intelligence.

However, several
challenges arise in crafting optimal model architectures, formulating strategic training-testing approaches,
refining data preprocessing techniques, and selecting suitable learning algorithms.

Each design decision risks
introducing pitfalls that can undermine model robustness and effectiveness.
4.1 RQ1-Pitfalls
We have identified 43 research studies dedicated to the exploration of pitfalls introduced in the system design
and learning process.

These pitfalls can be broadly categorized into three categories: data snooping, spurious
ACM Trans.

Softw.

Eng.

Methodol.
10 • Xinyu She, Yue Liu, Yanjie Zhao, Yiling He, Li Li, Chakkrit Tantithamthavorn, Zhan Qin, and Haoyu Wang
correlations, and inappropriate model design.

In the following, we provide comprehensive descriptions of these
three pitfalls.
```

### fc069a30deb2a23a

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 14 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
They found that, compared
to the high performance on standard benchmarks like HUMANEVAL [19], popular LLMs experienced a significant
performance drop (an average of 39.4%) on EVOEVAL, highlighting the limitations of standard benchmarks and
the effectiveness of their approach.

Additionally, EvalPlus [90] combines emerging LLM-based methods with
traditional mutation-based approaches for test case generation.

It continuously expands inputs using LLM and
applies a greedy set-covering approach for constraint handling, fully harnessing the capabilities of large models.

Summary - Data Collection and Labeling
Based on 22 relevant studies, our literature review reveals three prevalent pitfalls (i.e., unbalanced distribution,
data noise, and labeling errors) in the data collection and labeling process.

These pitfalls propagate, causing
overestimated performance and compromised model efficacy.
```

### ea2a2e488a871826

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 10 |
| page_end | 11 |
| chunk_index | 5 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Meanwhile, spurious correlations have become more prominent
with the advent of explainable artificial intelligence (XAI) techniques for elucidating model reasoning [22,
151, 153].

Discussions around inappropriate model design remain ongoing as new frameworks and learning
strategies continue to emerge.

Similar to our observations regarding the data collection and labeling process,
Figure 7 reveals a greater emphasis on modern Transformer-based language models and GPT series compared to
conventionalarchitectures.

Thisdistributionhighlightsashifttowardsexaminingpotentialpitfallsinsophisticated
language models for code intelligence tasks, setting the stage for continued research focused on enhancing model
transparency, interpretability, and reliability.

ACM Trans.

Softw.

Eng.

Methodol.

Pitfalls in Language Models for Code Intelligence: A Taxonomy and Survey • 11
4.2 RQ2-Solutions
To address the three pitfalls related to the system design and learning process, researchers have employed a
variety of approaches which we describe as follows.
```

### 7f16a532b9759a15

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 8 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
While Shiet al. [140]
unravels how transformer-based models allocate attention for code summarization, Wanet al. [160] probes into
the nuances of attention during code-to-code translation.

These XAI approaches can serve to identify and rectify
model pitfalls, ensuring the reliability of LM4Code applications.

Model Optimization Strategies:In light of the pitfalls introduced by inappropriate model design, researchers
have turned to model optimization strategies to address and minimize their effects.

These strategies encompass
several techniques designed to enhance a model’s structure, training process, and generalization capabilities.

Firstly, model design adjustments involve refining the architecture to better capture data intricacies.

Studies
like that by Wanet al. [161] have demonstrated the benefits of introducing novel layers or structures to better
understand the tree structure of code, yielding improved performance.
```

### 91a40a4af6d5eccf

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 9 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Secondly, model nnsembling is gaining
traction, where the strengths of multiple models are leveraged to offset individual biases, as seen in the work by
Zhanget al. [198]whichemploysmultipleviewsofthesamedataformorerobustpredictions.

Lastly,regularization
and fine-tuning techniques play a pivotal role.

Regularization, such as dropout or L2 regularization, helps in
preventing overfitting, while fine-tuning allows pre-trained models, like CodeBERT, to adapt to specific dataset
nuances, as demonstrated by Fanget al. [33].

By integrating these strategies, models can be better positioned to
achieve superior outcomes.

Summary - System Design and Learning
In this study, we uncover 43 research studies related to pitfalls in system design and learning.

These pitfalls
can be categorized into three main categories: data snooping, spurious correlations, and inappropriate model
design, leading to overestimated performance and compromised efficacy of LM4Code Systems.
```

### 90f870888cde247f

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 4 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Similarly, the
encoder-decoder framework used in code summarization might neglect the hierarchical nature of code or struggle
with sequence generation, leading to inadequate summaries [161, 170].

This issue is not limited to traditional
architectures.

Even modern program repair models, adapted from neural machine translation, face design-related
challenges that affect their translation accuracy and diversity [27, 103].

While there are innovative attempts such
as leveraging deep reinforcement learning or shared encoder-decoder architectures [85], these approaches still
exhibit shortcomings in addressing the diverse needs of various LM4Code applications.

To summarize, Figure 6 and 7 display the distribution of papers that discuss LM4Code pitfalls in the system
design and learning stage.

Figure 6 indicates that while inappropriate model design was first identified in 2018,
research efforts on addressing key pitfalls have increased over the past three years.

Among these, data snooping
has garnered increasing research attention.
```

### 7a4d8a93cbd46f78

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | discussion |
| section_title | 8 DISCUSSION |
| page_start | 23 |
| page_end | 23 |
| chunk_index | 2 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Addressing the identified pitfalls is vital for advancing robust and reliable
LM4Code techniques.

As our study reveals, solutions like data cleaning, model explainability, optimized model
design, and rigorous benchmarking have shown promise in mitigating certain pitfalls.

However, these solutions,
although effective in specific contexts, may not be universally applicable due to the complexity and ever-evolving
nature of the software engineering landscape.

A coordinated effort by the community is required to establish
guidelines and best practices that enable mitigating pitfalls in data construction, model design, performance
evaluation, and deployment.

Uncovering New Pitfalls.

The dynamic nature of the LM4Code field means novel pitfalls will likely emerge as
techniques rapidly evolve.

Specifically, the ever-evolving software engineering landscape, increasingly complex
codebases, and new LM4Code techniques provide fertile ground for novel pitfalls to emerge.

Thus, identifying
emerging pitfalls is critical.

The community needs to continuously analyze model reasoning, behaviors, and
performance under realistic experimental settings to uncover new pitfalls in a timely manner.
```

### 7e9d2ce0a19b56c5

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | discussion |
| section_title | 8 DISCUSSION |
| page_start | 23 |
| page_end | 23 |
| chunk_index | 0 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
8.1 Recommendations for LM4Code Research
Our systematic literature review reveals numerous pitfalls that can undermine the realistic performance and
real-world effectiveness of LM4Code systems.

These pitfalls span the data, models, evaluation, and deployment
phases of the LM4Code lifecycle.

LM4Code has become an increasingly prominent research area, evidenced by
the rapid increase in publications.

A prior survey by Houet al. [54] uncovered 229 papers on large language
models for software engineering between 2020-2023, while Wanget al. [168] uncovered 350 papers on deep
learning for software engineering between 2015-2020.

However, our focused study on LM4Code pitfalls only
identified 121 relevant papers.

This indicates that research attention to pitfalls in LM4Code is still insufficient,
compared to the overall research volume.

Thus, future LM4Code research must not overlook the pitfalls when
applying LM4Code models to software engineering tasks.

Recognizing Existing Pitfalls.
```

### 187fbd5de9fc878c

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 7 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
While related research evaluating LM4Code [16, 93, 108, 178] identifies some issues, our
work distinguishes itself in two key ways: (1) we employ a rigorous SLR methodology that systematically
identifies and categorizes pitfalls, and (2) we present a comprehensive taxonomy structured around the entire
LLM lifecycle, from dataset construction to deployment.

This approach enables us to systematically analyze not
only the identified issues but also their corresponding solutions and practical impacts, providing an integrative
perspective that supports both researchers and practitioners in developing more reliable code intelligence systems.

Ensuring the robustness, reliability, and trustworthy deployment of LMs is important for their effective
integration into the software development lifecycle.

Consequently, it is crucial to discern the nature of these
pitfalls, comprehend their implications, and examine existing solutions.

Thus, we aim to answer the following
research questions in this study:
• RQ1: What types of pitfalls are prevalent in language models for code intelligence?
```

### 570772c1a3095dcc

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | discussion |
| section_title | 8 DISCUSSION |
| page_start | 23 |
| page_end | 23 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Inthisstudy,wesummarizedmultiplecommonpitfallsassociatedwithLM4Code.

These pitfalls, each with distinct implications, highlight the inherent complexities in applying LM4Code to real-
world software engineering problems.

As our review results demonstrate, pitfalls can introduce unrealistic
performance evaluation, compromise model efficacy, and raise security concerns.

Thus, it becomes important
for future LM4Code research to recognize and avoid potential pitfalls when building LM4Code systems for SE
tasks.

To ensure trustworthy findings of LM4Code research, it is essential to demonstrate effectiveness through a
rigorous and reliable experimental design that reflects real-world scenarios.

Furthermore, although our review
has summarized common pitfalls, as previous surveys like Houet al. [54] present, there exist more than 50
specific large language models tailored to over 55 software engineering scenarios.

So while we report general
implications in some common settings using prevalent models, further investigation is required to discern more
specific implications in specific or unconventional scenarios.

Addressing Existing Pitfalls.
```

### dde2030a747deee1

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 15 |
| page_end | 15 |
| chunk_index | 15 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
There exist various challenges when such LM4Code systems are deployed in practice, like security threats and
how LM4Code systems should be updated to adapt the rapidly changing software practices.

This section discusses
pitfalls, implications, and current solutions when deploying and maintaining LM4Code.
6.1 RQ1-Pitfalls
In our literature review, we identified 38 research papers involving the pitfalls of LM4Code deployment and
maintenance.

This number of identified publications surpasses that related to other stages, highlighting the fact
that deploying and maintaining LM4Code presents a complex set of challenges that have gained considerable
attention from the research community.

Figure 10 and Figure 11 present the distribution of these 38 research studies over time and different types of
LM4Code.

From Figure 10, we can observe that there has been a significant increase in the number of research
papers focusing on the pitfalls in the deployment and maintenance of LM4Code, especially in the past three
years.
```

### 58e05fafbfcae8cb

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 0 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
ØData SnoopingØSpurious CorrelationsØInappropriate Model Design
Performance evaluation (35)ØInappropriate BaselineØInappropriate Evaluation DatasetØLack of Stability EvaluationØInappropriate Performance Measures
Deployment and maintenance (38)
ØReal-World ConstraintsØAttack ThreatsØSecurity Concerns in Generated Code
Figure 3.

The overview of pitfalls of LMs for code intelligence
specific, we segment the pitfalls into four key aspects of the LM pipeline based on the LM4Code lifecycle: data
collection and labeling (Section 3), system design and learning (Section 4), performance evaluation (Section 5),
and deployment and maintenance (Section 6).

This framework is depicted in Figure 3.

For each aspect, we first
summarize the types of prevalent pitfalls discussed in the collected studies (RQ1) and explore potential solutions
and best practices recommended in the literature (RQ2).
```

### 1e7857e3861e9475

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | results |
| section_title | 5 PERFORMANCE EV ALUATION |
| page_start | 19 |
| page_end | 20 |
| chunk_index | 34 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The implications highlight that real-world deployment introduces complex
challenges for LM4Code systems.
7 RQ3-IMPLICATIONS
The implications of pitfalls in LM4Code span across multiple dimensions, from direct technical impacts to
broader research validity concerns.

The ramifications of these pitfalls and biases extend beyond merely impacting
research performance and reproducibility from an evaluative standpoint.

They also contribute to misleading
benchmarksandpotentialsecurityvulnerabilitieswithinthegeneratedcode,whenviewedfromtheperspectiveof
content generation.

Furthermore, concerning research performance, a distinction can be made based on whether
the evaluation or the model itself is affected, leading to categories such as performance overestimation and
compromised model efficacy.

These implications collectively demonstrate how pitfalls encountered at various
stages of the lifecycle can undermine the reliability and practical applicability of LM4Code systems.

ACM Trans.

Softw.

Eng.
```

### 4d0b270a9126b9b1

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | abstract |
| section_title | Abstract/摘要 |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Such challenges drive the need for a comprehensive understanding - not just identifying these issues but delving
into their possible implications and existing solutions to build more reliable language models tailored to code intelligence.

Based on a well-defined systematic research approach, we conducted an extensive literature review to uncover the pitfalls
inherent in LM4Code.

Finally, 121 primary studies from top-tier venues have been identified.

After carefully examining these
studies, we designed a taxonomy of pitfalls in LM4Code research and conducted a systematic study to summarize the issues,
current solutions, implications, and challenges of different pitfalls for LM4Code systems.

We developed a comprehensive
classification scheme that dissects pitfalls across four crucial aspects: data collection and labeling, system design and learning,
performance evaluation, and deployment and maintenance.

Through this study, we aim to provide a roadmap for researchers
and practitioners, facilitating their understanding and utilization of LM4Code in reliable and trustworthy ways.
```

### 247013ec6baa4e33

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 3 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Actually, introducing advanced pre-trained models like CodeBERT has
not eliminated these pitfalls.

Specifically, if not fine-tuned appropriately for downstream tasks, these models
might still overemphasize basic elements like keywords over richer code semantics [198].

Inappropriate Model Design:Inappropriate model design in LM4Code arises when the underlying architecture
fails to capture critical characteristics of code, such as hierarchy and composition.

The inability to construct robust
semanticrepresentationsofcode’sintricatestructuralandlogicalattributeshindersmodelefficacyondownstream
code intelligence tasks.

Such design shortcomings can manifest in several ways.

For instance, in vulnerability
detection, models may exhibit a significant overlap in the feature space between classes, hindering precise
vulnerability identification [15].

Code search models might lean on coarse-grained representations, capturing
merely lexical or structural elements, often overlooking the true functionality of the code [163].
```

### 63b73457012267c6

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 2 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
In this section, we provide a brief description of related studies and discuss
the implications and potential solutions during the data collection and labeling stages.
3.1 RQ1-Pitfalls
From the collected papers, we identified 22 research studies focusing on pitfalls during the data collection and
labeling process.

Table 2 presents the statistics of literature on this topic, where the pitfalls can be grouped into
three main categories.

Unbalanced Distribution:Unbalanced distribution arises when there is a lack of proper randomization in
the selection of samples, leading to certain populations being underrepresented or overrepresented [135].

In
code-related scenarios, it usually refers to the gap between the sample distribution of real-world practices and
training datasets.

For example, as emphasized by [15, 144, 182], vulnerable instances in vulnerability detection
studies are overwhelming while neutral code instances in real-world environments considerably outnumber their
vulnerable counterparts.

This imbalance extends to other code-based tasks.
```

### 0d9684287a79f05b

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 1 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
The implications of these pitfalls (RQ3) are discussed in
Section 7, and in Section 8, we further discuss open challenges and promising research directions.

This organized
structure enables a comprehensive analysis of pitfalls and considerations across the entire LM4Code pipeline.

Our taxonomy aims to provide crucial insights for developing more robust, reliable, and practical LM systems for
code intelligence tasks.
3 DATA COLLECTION AND LABELING
The data-hungry language models require large-scale and high-quality training datasets.

According to a survey
by Houet al. [54], the majority of LMs for code intelligence are trained using data from open-source platforms,
with GitHub and StackOverflow being the most popular options.

However, the data in these platforms are
user-contributed, varying significantly in the level of quality and reliability.

It leads to non-negligible noises,
bias, and errors in the training dataset and further affects the behavior of the models, which brings significant
pitfalls in LMs for code intelligence.
```

### ab25112d13aae5d7

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | 4 SYSTEM DESIGN AND LEARNING |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 7 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Model Interpretability:To address the biases inherent in LM4Code, especially spurious correlations, improving
model interpretability has emerged as a crucial solution [151].

By examining the decision-making process of
LM4Code models, researchers are better positioned to pinpoint and mitigate pitfalls, leading to more reliable
predictions [50].

Within vulnerability detection, Fuet al. [38], Liet al. [80], and Zouet al. [203] proposed methods
to enhance explanation accuracy, leveraging sophisticated visualization tools to correlate the internal dynamics
of neural models with code structures, thus providing a comprehensive understanding of model reasoning.

Citoet
al. [23] offers a distinctive perspective, centering on elucidating mispredictions.

Their approach, which integrates
neural predictions with symbolic logic, allows for precise error detection accompanied by rule-based explanations.

Additionally, attention mechanisms to explain pre-trained models have also been analyzed.
```

---

## 10. [single_001_en] What are the main steps in DnD's core workflow for decompiling a DNN binary?

**Type**: `method` | **Lang**: `EN` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.2000 | 0.4000 |
| 10 | 0.2000 | 0.4000 |
| 20 | 0.4000 | 0.6000 |

**Expected sources**: DnD

### Expected Chunks (5)

### 8d4c6565f46d91f8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 8 |
| chunk_index | 11 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
As such, we can represent the output of a DNN opera-
tor as symbolic expressions of the operator’s input and the
2140    31st USENIX Security Symposium USENIX Association
operator’s parameters.

These expressions contain the math-
ematical semanticsDND needs to recover.

To extract such
symbolic expressions,DND performs customized selective
symbolic execution with the IVs (identiﬁed in Section 5.2.1)
as symbolic variables.

This is because making IVs as sym-
bolicvariablesbringsthetwofollowingbeneﬁts:(1)itenables
DND to symbolize the mathematical expressions of the DNN
operator’s output as symbolic expressions. (2) it allowsDND
to eﬃciently extract the symbolic expressions of a DNN op-
erator’s output by only executing one iteration of each loop,
as discussed inSolution 2of Section 4.

We will explain those
beneﬁts using Figure 3b.
```

### 0fe413d265df53df

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 7 |
| chunk_index | 5 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We will explain how we handle
common compiler optimizations and advanced attributes in
USENIX Association 31st USENIX Security Symposium    2139
I00 I01 I02
I10 I11 I12
I20 I21 I22
F00 F01
F10 F11
O00 O01
O10 O11
Input 1x3x3 Filter 1x2x2 Output 1x2x2
(a) Conv operator
1 void Conv(PTR ∗ input, PTR ∗ filter, PTR ∗ output){
2 for(i=0;i<2;i++) // output width index
3 for(j=0;j<2;j++) // output length index
4 for(u=0;u<2;u++) // filter width index
5 for(v=0;v<2;v++) // filter length index
6 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
7 }
(b) Simplifed decompiled code ofConv
1 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
(c) Extracted symbolic expression ofConv
1 addr: output[i][j]
2 expr: Sum( element =Mul(input[i+u][j+v],
3 filter[u][v]),
4 index =(u, v))
5 IVs: (u, init=0,inc=1,count=2)
6 (v, init=0,inc=1,count=2)
7 (i, init=0,inc=1,count=2)
8 (j, init=0,inc=1,count=2)
(d) Generated operator summary
Figure 3: Operator summary generation ofConv
Sections 5.2.4 and 5.4.3, respectively.
5.2.1 Loop Analysis
The main goal of loop analysis is to identify the information
on the basic induction variable (IV), or informally loop index
variable of each loop in a DNN operator.
```

### 1fba7167150e9c4c

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 10 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Algorithm 1Loop analysis
1: procedureLOOPANALYSIS(op: operator)
2: symEngine ← SymbolicEngine(op.entryAddr)
3: candidates←ç
4: while symEngine.hasActive()do
5: symEngine.step()
6: for eachstate∈ symEngine.statesdo
7: inst ← state.lastInst
8: addr ← state.addr
9: if addr ∈ op.entryBlocks then
10: if isRegWrite(inst)andisConstant(inst.writeVal)then
11: inst.writeVal← createSym()
12: candidates.add((addr, inst.writeReg))
13: if addr ∈ op.breakEdgeSrcAddrthen
14: symEngine.record(state.branch.condition.get_IV())
15: symEngine.keep(getBreakState(state.succ))
16: if addr ∉ op.addrRangethen
17: symEngine.stash(state)
18: IVs ← checkConditionAndUpdate(candidates)
19: IVs.getLoopCount()
20: ReturnIVs
5.2.2 Symbolic Expression Extraction
ADNNoperatortypicallyperformstensorcomputation,which
takes its input and parameters, and generates the computed
output transferring to its successor DNN operators as the in-
put.
```

### 20ac523f29224b53

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 6 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the break edges (denoting the edges in CFG that
jump out of the current loop).
```

### 16dc5ceb2dad79e0

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how to identify IVs using the
aforementioned three properties by symbolically executing
each DNN operator from its entry point to its exit point (Line
2,16-17).

Leveragingtheproperty(i), DND symbolizesevery
general register initialized by a constant in the loop’s entry
block (Line 10-12).
```

### Retrieved Top-20

**#1** — 342aa149b5e318b2 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=3

```
Speciﬁcally,DND ﬁrst identiﬁes the locations of the func-
tionswithpossibletensorcomputation(i.e.,containingtwoor
more nested loops or invoking math functions in the standard
library) as DNN operator candidates.

Then,DND collects the
caller functions of each function in the candidate list.

Among
these caller functions, the one calling most candidates is con-
sidered as the “inference function” (i.e., acting as the DNN
binary’sdispatchfunction).

Finally, DND ﬁltersoutthecandi-
datefunctionstha
```

**#2** — ec71df9e40361439 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.3-3 | sec=introduction | ci=5

```
We further
demonstrate thatDND can successfully decompile a DNN bi-
nary used by a real-world micro-controller, and the recovered
DNN model can be used to boost adversarial attacks against
the original DNN, enabling the usage of white-box attacks, in
place of less eﬃcient black-box ones.

In summary, our main contributions are as follows:
• We design and implement DND, the ﬁrst compiler- and
ISA-agnostic decompiler for compiled DNN models.

DND can decompile a (stripped) DNN binary to recover
th
```

**#3** — bdb01ae674531972 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=0

```
DND’s workﬂow is composed of three components, as illus-
tratedinFigure2.

Speciﬁcally,thesethreecomponentsare(1)
DNNOperatorLocationIdentiﬁcation ,(2) OperatorSummary
Generation, and (3)DNN Model Lifting.

In the ﬁrst stage,DND recovers the control ﬂow graph
(CFG) and identiﬁes the location of inference function and
DNN operators from the input (stripped) DNN binary (Step
in Figure 2, details in Section 5.1).

Next,DNDgeneratesoperatorsummaryofeachDNNoper-
ator (Section 5.2).

To do so,DND ﬁrs
```

**#4** **[HIT]** — 16dc5ceb2dad79e0 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.7-7 | sec=method | ci=7

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how
```

**#5** — a5fcaee22f63a543 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.14-14 | sec=discussion | ci=4

```
As future work, to support these additional compilers, we
will need to implement a dedicated analysis to identify these
tensor-speciﬁc library functions.

This analysis could take ad-
vantage of function matching approaches [55].

Decompiling Binary on DNN Accelerators.

DND does not
supportdecompilingDNNbinariesrunningonDNNaccelera-
tors(e.g.,GPUs,FPGAs).

Thislimitationiscausedbythefact
thatDNN accelerators have very diverse ISAs thatare usually
not supported by the general-purpose disassemble
```

**#6** — 49fe88a7eaee3e40 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=13

```
We can easily infer DNN models
from those ﬁles because they contain the information on the
modelhyper-parametersandparametersofthedeployedDNN
model. (ii) static analysis cannot extract DNN models from
DNN binaries compiled by the interpreter-based compilation
without the DNN conﬁguration ﬁle because DNNs are con-
ﬁgured dynamically.

Furthermore,DND does not support the
DNNbinariesrunningonDNNacceleratorsbecauseDNNac-
celerators have very diverse ISAs, and they are not supported
by the general-p
```

**#7** — 24e8108a850d9c01 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.11-11 | sec=method | ci=0

```
We implementDND with over 7.5K lines of Python code on
top ofangr [47].

DNNOperatorLocationIdentiﬁcation DNNoperatorloca-
tion identiﬁcation requires recovering CFGs and identifying
loop locations.

DND uses angr’s to recover CFG, which is
essential to ﬁnd the locations of DNN operators.

Loop Analysis.

DND requires ﬁnding all the loops and their
nested loops in each DNN binary to perform loop analysis in
Section 5.2.1.

For that, we use angr’s loop ﬁnder.

Operator Summary Generation.

We imp
```

**#8** — e298ceaffa743993 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.9-9 | sec=method | ci=24

```
Therefore,DND ﬁrst identiﬁes the activation operator
intheextractedsymbolicexpressions(Line3intheFigure4c),
andthendividesandliftstheexpressionsinLine1-2andLine
3separately,resultingintwo expr (Line2and5inFigure4d).
5.3 Template ASTs Generation
The template ASTs are the references that are matched with
the AST in an unknown DNN operator’s operator summary,
to determine its operator type.

To generate a template AST
of a DNN operator, we ﬁrst manually construct an instance
of the operator in the 
```

**#9** — 46c3664565691654 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.9-10 | sec=method | ci=25

```
We will show the DNN operators from which
we are able to generate the template ASTs in Section 7.1.
5.4 DNN Model Lifting
In this section, we describe how to further lift the operator
summary of each DNN operator to the high-level representa-
tionofaDNNmodel(i.e.,ONNXformat).

DNDﬁrstrecovers
types of DNN operators using AST matching (Section 5.4.1).

Then,DND recovers the DNN topology leveraging the inter-
operator data dependencies (Section 5.4.2).

Finally,DND re-
covers DNN operators’ attrib
```

**#10** — 0f14c20102c4d5b7 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.9-9 | sec=method | ci=22

```
On the other hand, the DNN operator fusion
optimization embeds theRelu operator (Line 9-12 in Fig-
ure 4a) into the loop body of theConv operator (Line 2-7 in
Figure 4a).

In this context,Relu is applied tooutput[i][j] (Line
10-11 in Figure 4b) when the loop with the IVu (Line 4-8) is
ﬁnished, and the loop withi,j as the IV (Line 4-8) are still
ongoing.

In this way, given a certaini and j, Relu is applied
after the accumulation ofoutput[i][j] is ﬁnished.

To lift the generated symbolic expressi
```

**#11** — a284a70309317971 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.11-11 | sec=method | ci=1

```
In some cases, some DNN opera-
tors(e.g., Softmax)callspeciﬁcmathematicalfunctions( exp,
pow, sqrt, tanh, log) in standard libraries (libc and libm).

Inthesecases, DND needstoidentifythecalledmathematical
functions.

To this aim,DND can use a function signature-
based approach [21] if those functions are statically linked.

Because those functions are pre-built, compilers insert those
pre-built functions into DNN binaries without being changed.

Alternatively,ananalystcansearchforsuchfunctionsb
```

**#12** — a1922c6875e023e8 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=14

```
We can use this output to reveal the DNN
model’s details and conduct security analysis, such as model
extraction, adversarial examples discovery, and model hard-
ening.

DND does not recover the algorithm hyper-parameters
(deﬁned in Section 2.1) because they neither aﬀect the infer-
ence process nor are recoverable from the binary.

Assumptions.

DND relies on the following assumptions:
1.

We have access to a DNN binary (e.g., dumping DNN
binaries running on an embedded system).
2.

The control
```

**#13** **[HIT]** — 20ac523f29224b53 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.7-7 | sec=method | ci=6

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the brea
```

**#14** — af71c06234f1d1ad | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.6-6 | sec=method | ci=2

```
Speciﬁcally,DND ﬁrst matches the AST in
each operator summary with a template AST to determine
its DNN operator type (Step).

Then,DND recovers the
DNN topology by identifying the data dependencies between
DNN operators (Step).

Finally,DND recovers each DNN
operator’s attributes and parameters leveraging the identiﬁed
DNNoperatortypeandDNNtopology,andconvertsthefully-
recovered DNN model to an ONNX model (Step).
5.1 DNN Operator Location Identiﬁcation
In this step,DND identiﬁes the locations
```

**#15** — a0a782ed2ec8a898 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.10-11 | sec=method | ci=31

```
At last,
DND iterates the DNN operator execution sequence from the
ﬁrst DNN operator to the last DNN operator, identiﬁes the
data dependencies between adjacent operators, and connects
them accordingly.

Furthermore, from the data dependencies,DND can also
recognize theinput term(i.e., the term which is the output of
USENIX Association 31st USENIX Security Symposium    2143
thepreviousDNNoperator)and parameterterm (i.e.,theterm
which is the parameters of the DNN operator) in the operator
summary’
```

**#16** — 784da26bfe4a09ce | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.11-11 | sec=method | ci=32

```
Forexample,forthe Mul
functioninthe FC operator’ssummary(Line2-3inFigure5b),
DNDidentiﬁesthatthe input[i] istheoutputoftheprevious
DNN operator (i.e., its address range overlaps with previous
DNN operator’s output range), and that theweight[j][i]
is the parameter (i.e., its address range does not overlap with
any previous DNN operator’s output range).
5.4.3 Attributes and Parameters Recovery
In the last step,DND recovers the attributes and parameters
of each DNN operator by leveraging the genera
```

**#17** — 176e2eecee048a9f | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.8-8 | sec=method | ci=13

```
Furthermore, in order to keep track of the symbolic con-
straints related to memory reads and writes,DND’s cus-
tomized concretization strategy does not concretize mem-
ory addresses.

Instead, when reading from symbolic memory,
DND returns the symbolic memory address together with a
proper annotation.

For instance, when reading from address
input+i, DND returns input+i with MemReadVal annota-
tion,denotingwherethevalueisreadfrom.

Usingthisannota-
tion,DNDkeepstrackofmemoryreadvalues,andrecord
```

**#18** — 3e6e3c0edb175f52 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.13-13 | sec=experiment | ci=6

```
Thumb (Arm) AArch64 (Arm) x86-64
MNIST ResNet v1 MobileNets v2 MNIST ResNet v1 MobileNets v2 MNIST ResNet v1 MobileNets v2
Glow 100% 100% 100% 100% 100% 100% 100% 100% 100%
TVM 100% 100% 100% N/A N/A N/A 100% 100% 100%
build an application classifying images from the CIFAR-10
dataset using the ResNet v1 DNN model, and we install this
application on the board.
8.1 Extraction Attack
To conduct a DNN extraction attack, we useDND to decom-
pile the DNN model embedded in the DNN binary installed
on t
```

**#19** — e6fa0a5eab9324b8 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.2-3 | sec=introduction | ci=4

```
Third,DND identiﬁes the
USENIX Association 31st USENIX Security Symposium    2135
type and location of the DNN operators in a target binary by
matchingtheextractedmathematicaloperationswithtemplate
mathematical DNN operations, recovering hyper-parameters
and parameters of all the identiﬁed DNN operators, as well as
the overall network topology.

Our evaluation shows thatDND is bothgenericandaccu-
rate.

ItsupportsdecompilingdiﬀerentDNNmodelscompiled
by two diﬀerent compilers for three diﬀerent I
```

**#20** — 4b4a4ad864c4b875 | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf | p.5-5 | sec=method | ci=12

```
On the
contrary,DND candecompileaDNNmodelembeddedinthe
binary program and generate a high-level representation (i.e.,
in the ONNX format [9]), including both the model hyper-
parameters and parameters of the embedded DNN model.
3 Scope
In this section, we describe the input/output ofDND, and the
standard and realistic assumptions on which DND relies.

Input.

DND supports (stripped) DNN binaries (i.e., the bi-
nary programs where a compiled DNN model is embedded)
compiled by the AOT compilation 
```

### Missed Chunks (3 — expected but NOT in top-20)

### 8d4c6565f46d91f8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 8 |
| chunk_index | 11 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
As such, we can represent the output of a DNN opera-
tor as symbolic expressions of the operator’s input and the
2140    31st USENIX Security Symposium USENIX Association
operator’s parameters.

These expressions contain the math-
ematical semanticsDND needs to recover.

To extract such
symbolic expressions,DND performs customized selective
symbolic execution with the IVs (identiﬁed in Section 5.2.1)
as symbolic variables.

This is because making IVs as sym-
bolicvariablesbringsthetwofollowingbeneﬁts:(1)itenables
DND to symbolize the mathematical expressions of the DNN
operator’s output as symbolic expressions. (2) it allowsDND
to eﬃciently extract the symbolic expressions of a DNN op-
erator’s output by only executing one iteration of each loop,
as discussed inSolution 2of Section 4.

We will explain those
beneﬁts using Figure 3b.
```

### 0fe413d265df53df

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 7 |
| chunk_index | 5 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We will explain how we handle
common compiler optimizations and advanced attributes in
USENIX Association 31st USENIX Security Symposium    2139
I00 I01 I02
I10 I11 I12
I20 I21 I22
F00 F01
F10 F11
O00 O01
O10 O11
Input 1x3x3 Filter 1x2x2 Output 1x2x2
(a) Conv operator
1 void Conv(PTR ∗ input, PTR ∗ filter, PTR ∗ output){
2 for(i=0;i<2;i++) // output width index
3 for(j=0;j<2;j++) // output length index
4 for(u=0;u<2;u++) // filter width index
5 for(v=0;v<2;v++) // filter length index
6 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
7 }
(b) Simplifed decompiled code ofConv
1 output[i][j]+=input[i+u][j+v] ∗filter[u][v]
(c) Extracted symbolic expression ofConv
1 addr: output[i][j]
2 expr: Sum( element =Mul(input[i+u][j+v],
3 filter[u][v]),
4 index =(u, v))
5 IVs: (u, init=0,inc=1,count=2)
6 (v, init=0,inc=1,count=2)
7 (i, init=0,inc=1,count=2)
8 (j, init=0,inc=1,count=2)
(d) Generated operator summary
Figure 3: Operator summary generation ofConv
Sections 5.2.4 and 5.4.3, respectively.
5.2.1 Loop Analysis
The main goal of loop analysis is to identify the information
on the basic induction variable (IV), or informally loop index
variable of each loop in a DNN operator.
```

### 1fba7167150e9c4c

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 10 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Algorithm 1Loop analysis
1: procedureLOOPANALYSIS(op: operator)
2: symEngine ← SymbolicEngine(op.entryAddr)
3: candidates←ç
4: while symEngine.hasActive()do
5: symEngine.step()
6: for eachstate∈ symEngine.statesdo
7: inst ← state.lastInst
8: addr ← state.addr
9: if addr ∈ op.entryBlocks then
10: if isRegWrite(inst)andisConstant(inst.writeVal)then
11: inst.writeVal← createSym()
12: candidates.add((addr, inst.writeReg))
13: if addr ∈ op.breakEdgeSrcAddrthen
14: symEngine.record(state.branch.condition.get_IV())
15: symEngine.keep(getBreakState(state.succ))
16: if addr ∉ op.addrRangethen
17: symEngine.stash(state)
18: IVs ← checkConditionAndUpdate(candidates)
19: IVs.getLoopCount()
20: ReturnIVs
5.2.2 Symbolic Expression Extraction
ADNNoperatortypicallyperformstensorcomputation,which
takes its input and parameters, and generates the computed
output transferring to its successor DNN operators as the in-
put.
```

### False Positives (18 — in top-20 but NOT expected)

### 342aa149b5e318b2

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 3 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Speciﬁcally,DND ﬁrst identiﬁes the locations of the func-
tionswithpossibletensorcomputation(i.e.,containingtwoor
more nested loops or invoking math functions in the standard
library) as DNN operator candidates.

Then,DND collects the
caller functions of each function in the candidate list.

Among
these caller functions, the one calling most candidates is con-
sidered as the “inference function” (i.e., acting as the DNN
binary’sdispatchfunction).

Finally, DND ﬁltersoutthecandi-
datefunctionsthatarenotthecalleesoftheinferencefunction.
5.2 Operator Summary Generation
After identifying the locations of DNN operators,DND ex-
tracts the symbolic expressions from each DNN operator and
lifts them to operator summary in the IR we design.

To do
so,DND ﬁrst conducts loop analysis for each DNN operator
(StepdescribedinSection5.2.1).
```

### ec71df9e40361439

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 5 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We further
demonstrate thatDND can successfully decompile a DNN bi-
nary used by a real-world micro-controller, and the recovered
DNN model can be used to boost adversarial attacks against
the original DNN, enabling the usage of white-box attacks, in
place of less eﬃcient black-box ones.

In summary, our main contributions are as follows:
• We design and implement DND, the ﬁrst compiler- and
ISA-agnostic decompiler for compiled DNN models.

DND can decompile a (stripped) DNN binary to recover
thefulldetailsofthecompiledDNNmodelandrepresent
them using the ONNX high-level modeling language.
• We design a dedicated IR to represent each DNN oper-
ator and develop a novel technique that uses symbolic
execution to lift the DNN binary to IR expressions.
```

### bdb01ae674531972

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 0 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
DND’s workﬂow is composed of three components, as illus-
tratedinFigure2.

Speciﬁcally,thesethreecomponentsare(1)
DNNOperatorLocationIdentiﬁcation ,(2) OperatorSummary
Generation, and (3)DNN Model Lifting.

In the ﬁrst stage,DND recovers the control ﬂow graph
(CFG) and identiﬁes the location of inference function and
DNN operators from the input (stripped) DNN binary (Step
in Figure 2, details in Section 5.1).

Next,DNDgeneratesoperatorsummaryofeachDNNoper-
ator (Section 5.2).

To do so,DND ﬁrst conducts loop analysis
(Step ) to identify loops’ information.

Such information
is essential for further analysis.
```

### a5fcaee22f63a543

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | discussion |
| section_title | 9 Discussion and Limitations |
| page_start | 14 |
| page_end | 14 |
| chunk_index | 4 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
As future work, to support these additional compilers, we
will need to implement a dedicated analysis to identify these
tensor-speciﬁc library functions.

This analysis could take ad-
vantage of function matching approaches [55].

Decompiling Binary on DNN Accelerators.

DND does not
supportdecompilingDNNbinariesrunningonDNNaccelera-
tors(e.g.,GPUs,FPGAs).

Thislimitationiscausedbythefact
thatDNN accelerators have very diverse ISAs thatare usually
not supported by the general-purpose disassemblers and the
symbolic execution framework, whichDND relies on.

For in-
stance,althoughNvidiaprovidesclosed-sourcedisassemblers
cuobjdump and nvidiaasm, which translate the CUDA binary
into SASS assembly code, most details of the SASS assembly
code are kept secret, which hinders further analysis.
```

### 49fe88a7eaee3e40

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 13 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We can easily infer DNN models
from those ﬁles because they contain the information on the
modelhyper-parametersandparametersofthedeployedDNN
model. (ii) static analysis cannot extract DNN models from
DNN binaries compiled by the interpreter-based compilation
without the DNN conﬁguration ﬁle because DNNs are con-
ﬁgured dynamically.

Furthermore,DND does not support the
DNNbinariesrunningonDNNacceleratorsbecauseDNNac-
celerators have very diverse ISAs, and they are not supported
by the general-purpose disassemblers.

Section 9 discusses
more details whyDND does not support decompiling DNN
binaries on accelerators.

Output.

DND can decompile a DNN model embedded in an
input binary.

The output is in the ONNX format [9] (e.g., Fig-
ure 1) including the DNN model’s model hyper-parameters
and parameters.
```

### 24e8108a850d9c01

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 6 Implementation |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 0 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We implementDND with over 7.5K lines of Python code on
top ofangr [47].

DNNOperatorLocationIdentiﬁcation DNNoperatorloca-
tion identiﬁcation requires recovering CFGs and identifying
loop locations.

DND uses angr’s to recover CFG, which is
essential to ﬁnd the locations of DNN operators.

Loop Analysis.

DND requires ﬁnding all the loops and their
nested loops in each DNN binary to perform loop analysis in
Section 5.2.1.

For that, we use angr’s loop ﬁnder.

Operator Summary Generation.

We implement the cus-
tomizedsymbolicexecutionontopofangrsimulationmanager
and angr under-constrained symbolic execution functionality.

Thissymbolicexecutionengineisresponsibleforsymbolizing
variables(e.g.,IVs)andcollectingthesymbolicexpressionsof
each DNN operator output.
```

### e298ceaffa743993

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 24 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Therefore,DND ﬁrst identiﬁes the activation operator
intheextractedsymbolicexpressions(Line3intheFigure4c),
andthendividesandliftstheexpressionsinLine1-2andLine
3separately,resultingintwo expr (Line2and5inFigure4d).
5.3 Template ASTs Generation
The template ASTs are the references that are matched with
the AST in an unknown DNN operator’s operator summary,
to determine its operator type.

To generate a template AST
of a DNN operator, we ﬁrst manually construct an instance
of the operator in the ONNX format, leveraging the usage
examples of each ONNX operator [11].

Then,DND uses a
DNN compiler to compile this ONNX operator instance to a
binary.

Atlast, DNDgeneratestheoperatorsummaryfromthe
compiledbinary,usingthesameoperatorsummarygeneration
procedure(describedinSection5.2),andtakesits expr asthe
template AST.
```

### 46c3664565691654

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 25 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We will show the DNN operators from which
we are able to generate the template ASTs in Section 7.1.
5.4 DNN Model Lifting
In this section, we describe how to further lift the operator
summary of each DNN operator to the high-level representa-
tionofaDNNmodel(i.e.,ONNXformat).

DNDﬁrstrecovers
types of DNN operators using AST matching (Section 5.4.1).

Then,DND recovers the DNN topology leveraging the inter-
operator data dependencies (Section 5.4.2).

Finally,DND re-
covers DNN operators’ attributes and parameters leveraging
both the DNN operator type and DNN topology, and converts
the fully-recovered model into ONNX format (Section 5.4.3).
5.4.1 AST Matching
For each identiﬁed DNN operator,DND matches the ASTs
(i.e., expr) in its operator summary with one of the template
ASTs to determine its DNN operator type.
```

### 0f14c20102c4d5b7

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 22 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
On the other hand, the DNN operator fusion
optimization embeds theRelu operator (Line 9-12 in Fig-
ure 4a) into the loop body of theConv operator (Line 2-7 in
Figure 4a).

In this context,Relu is applied tooutput[i][j] (Line
10-11 in Figure 4b) when the loop with the IVu (Line 4-8) is
ﬁnished, and the loop withi,j as the IV (Line 4-8) are still
ongoing.

In this way, given a certaini and j, Relu is applied
after the accumulation ofoutput[i][j] is ﬁnished.

To lift the generated symbolic expression of the aforemen-
tioned heavily-optimized binary code in Figure 4c,DND in-
troducestwotechniques.

First,in ordertomake the expr (i.e.,
AST)in the resultoperatorsummarysuccinct, DND conducts
alooprerollinganalysis[39]ontheextractedsymbolicexpres-
sion to handle the loop unrolling optimization.
```

### a284a70309317971

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 6 Implementation |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 1 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
In some cases, some DNN opera-
tors(e.g., Softmax)callspeciﬁcmathematicalfunctions( exp,
pow, sqrt, tanh, log) in standard libraries (libc and libm).

Inthesecases, DND needstoidentifythecalledmathematical
functions.

To this aim,DND can use a function signature-
based approach [21] if those functions are statically linked.

Because those functions are pre-built, compilers insert those
pre-built functions into DNN binaries without being changed.

Alternatively,ananalystcansearchforsuchfunctionsbycheck-
ing calledfunctions’ names iffunction names are notstripped
from the binary or those functions are dynamically linked.
```

### a1922c6875e023e8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 14 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
We can use this output to reveal the DNN
model’s details and conduct security analysis, such as model
extraction, adversarial examples discovery, and model hard-
ening.

DND does not recover the algorithm hyper-parameters
(deﬁned in Section 2.1) because they neither aﬀect the infer-
ence process nor are recoverable from the binary.

Assumptions.

DND relies on the following assumptions:
1.

We have access to a DNN binary (e.g., dumping DNN
binaries running on an embedded system).
2.

The control-ﬂow graph (CFG) recovery is reliable.

Our
evaluation shows that the recovered CFGs, though impre-
cise, are suﬃcient enough for our decompilation purpose.
3.

DNN compilers do not use obfuscation technique.
```

### af71c06234f1d1ad

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 2 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Speciﬁcally,DND ﬁrst matches the AST in
each operator summary with a template AST to determine
its DNN operator type (Step).

Then,DND recovers the
DNN topology by identifying the data dependencies between
DNN operators (Step).

Finally,DND recovers each DNN
operator’s attributes and parameters leveraging the identiﬁed
DNNoperatortypeandDNNtopology,andconvertsthefully-
recovered DNN model to an ONNX model (Step).
5.1 DNN Operator Location Identiﬁcation
In this step,DND identiﬁes the locations of the inference
function and the DNN operators.

Since DNN operators are
essentially tensor computations, they are implemented and
compiledasmultiplenestedloopswithanumberofnumerical
computations inside.

Furthermore, DNN operators reside in
eithertheinferencefunctionoritscalleefunctions.

DNDlever-
ages these two properties to identify the locations of DNN
operators and the inference function.
```

### a0a782ed2ec8a898

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 10 |
| page_end | 11 |
| chunk_index | 31 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
At last,
DND iterates the DNN operator execution sequence from the
ﬁrst DNN operator to the last DNN operator, identiﬁes the
data dependencies between adjacent operators, and connects
them accordingly.

Furthermore, from the data dependencies,DND can also
recognize theinput term(i.e., the term which is the output of
USENIX Association 31st USENIX Security Symposium    2143
thepreviousDNNoperator)and parameterterm (i.e.,theterm
which is the parameters of the DNN operator) in the operator
summary’sexpr, which can be leveraged for attributes and
parametersrecoveryinthenextstep.
```

### 784da26bfe4a09ce

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 32 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Forexample,forthe Mul
functioninthe FC operator’ssummary(Line2-3inFigure5b),
DNDidentiﬁesthatthe input[i] istheoutputoftheprevious
DNN operator (i.e., its address range overlaps with previous
DNN operator’s output range), and that theweight[j][i]
is the parameter (i.e., its address range does not overlap with
any previous DNN operator’s output range).
5.4.3 Attributes and Parameters Recovery
In the last step,DND recovers the attributes and parameters
of each DNN operator by leveraging the generated operator
summary and recovered DNN topology, and it then generates
a high-level DNN representation in the ONNX format.

Attribute Recovery.

For DNN operators with only shape-
related attributes (e.g., ﬁlter length ofAveragePool),DND
recovers their attributes by checking the nesting structure of
their loops and the loops’ counts (e.g., the ﬁlter length is the
loop count of the loop that iterates over the inputs).
```

### 176e2eecee048a9f

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 13 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Furthermore, in order to keep track of the symbolic con-
straints related to memory reads and writes,DND’s cus-
tomized concretization strategy does not concretize mem-
ory addresses.

Instead, when reading from symbolic memory,
DND returns the symbolic memory address together with a
proper annotation.

For instance, when reading from address
input+i, DND returns input+i with MemReadVal annota-
tion,denotingwherethevalueisreadfrom.

Usingthisannota-
tion,DNDkeepstrackofmemoryreadvalues,andrecordsthe
written expressions when the code write to symbolic memory.

We explain the detailed procedure to extract symbolic
expressions in Algorithm 2.

In particular,DND symboli-
cally executes each DNN operator starting from its entry
point (Line 3).

When reaching the identiﬁed IV initializa-
tion code,DND symbolizes IVs’ corresponding registers in-
stead of initializing them with a constant (Line 9-10).
```

### 3e6e3c0edb175f52

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | experiment |
| section_title | 7.2.1 Evaluation Setup |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 6 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Thumb (Arm) AArch64 (Arm) x86-64
MNIST ResNet v1 MobileNets v2 MNIST ResNet v1 MobileNets v2 MNIST ResNet v1 MobileNets v2
Glow 100% 100% 100% 100% 100% 100% 100% 100% 100%
TVM 100% 100% 100% N/A N/A N/A 100% 100% 100%
build an application classifying images from the CIFAR-10
dataset using the ResNet v1 DNN model, and we install this
application on the board.
8.1 Extraction Attack
To conduct a DNN extraction attack, we useDND to decom-
pile the DNN model embedded in the DNN binary installed
on the board.

In our case, we obtained the DNN application
by connecting the GDB debugger to the board’s GDB port
and then dumping the DNN application.

Afterobtainingthebinary, DND locatestheinferencefunc-
tionintheDNNbinary,decompilesitsDNNmodel,andrecov-
ers its model hyper-parameters and parameters.
```

### e6fa0a5eab9324b8

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 4 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Third,DND identiﬁes the
USENIX Association 31st USENIX Security Symposium    2135
type and location of the DNN operators in a target binary by
matchingtheextractedmathematicaloperationswithtemplate
mathematical DNN operations, recovering hyper-parameters
and parameters of all the identiﬁed DNN operators, as well as
the overall network topology.

Our evaluation shows thatDND is bothgenericandaccu-
rate.

ItsupportsdecompilingdiﬀerentDNNmodelscompiled
by two diﬀerent compilers for three diﬀerent ISAs, without
requiringmanualeﬀort.

Moreover,thedecompiledDNNmod-
els are structurally equivalent to the original ones, and, after
re-compiling the decompiled DNNs, the generated binaries
classify samples exactly as the original binaries.
```

### 4b4a4ad864c4b875

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 2 Background and Motivation |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 12 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
On the
contrary,DND candecompileaDNNmodelembeddedinthe
binary program and generate a high-level representation (i.e.,
in the ONNX format [9]), including both the model hyper-
parameters and parameters of the embedded DNN model.
3 Scope
In this section, we describe the input/output ofDND, and the
standard and realistic assumptions on which DND relies.

Input.

DND supports (stripped) DNN binaries (i.e., the bi-
nary programs where a compiled DNN model is embedded)
compiled by the AOT compilation scheme running on CPU
without hardware accelerators.

This conﬁguration is common
on edge devices [53].

DND does not support DNN binaries
compiled by interpreter-based compilation schemes because
of the following reasons: (i) DNN binaries compiled by the
interpreter-based compilation scheme usually accompany the
DNN conﬁguration ﬁles.
```

---

## 11. [single_004_en] What is the core technique FlatD uses to protect DNN programs, and how is it integrated into the compilation pipeline?

**Type**: `method` | **Lang**: `EN` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.2000 | 0.6000 |
| 5 | 0.2000 | 0.6000 |
| 10 | 0.2000 | 0.6000 |
| 20 | 0.6000 | 1.0000 |

**Expected sources**: FlatD

### Expected Chunks (5)

### 241543cef9ddd0b4

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 5 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
We implemented FlatD on the top of O-LLVM [41] and em-
bedded it into the code generation part of TVM [11].

We used
O-LLVM as the baseline and evaluated FlatD on eight real-
world pre-trained models and one self-trained model from four
frameworks.

Our experiment results show that compared to the
traditional Control Flow Flattening, FlatD can more effectively
counterwork state-of-the-art reversing-based model extraction
attacks while preserving the functionality of the original DNN
programs.

Moreover, the DNN program transformed by FlatD
performs similarly to the one using traditional Control Flow
Flattening in most cases and always has a lower scale.

In summary, we make the following contributions:
• We investigate four state-of-the-art reversing-based model
extraction attacks and identify a key component shared
across the attack frameworks.

This component guides the
provision of protection and contributes to future research
on DNN program safety.
```

### f73b5f75aac3ec83

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 7 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
FlatD conceals the orig-
inal Control Flow Graph of DNN programs based on
Control Flow Flattening and ensures minimal information
gained by attackers through statistical analysis.
• We successfully apply FlatD on DNN programs compiled
from large-scale models using TVM to evaluate these
DNN programs regarding functionality, performance, and
resilience.

We use O-LLVM as the baseline to compare
the results.

Our experiment demonstrates that DNN pro-
grams transformed by FlatD can prevent leaking informa-
tion from reversing-based model extraction attacks more
effectively than traditional Control Flow Flattening with
similar performance and lower scale.
```

### 347cb9d0884d62c1

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
This feature helps attackers infer
the operator type by using binary similarity comparison.

On
the other hand, it also guides the protection of DNN programs
because we found that the Control Flow Graph (CFG) plays
a vital role in all attack frameworks.
f(x) =x+ = max(0, x) =x + |x|
2 (1)
f(x) =ex + e−x
ex − e−x (2)
Based on our observations, this paper proposes FlatD, an
advanced defense framework based on Control Flow Flat-
tening, for DNN programs to protect them from reversing-
based model extraction attacks.

Unlike the traditional Control
Flow Flattening, we leverage the opaque predicate, one-way
cryptographic hashing, and indirect jump to conceal the control
flow further so that attackers cannot quickly recover the
original CFG and apply more inference analysis.

We also use
several strategies to preserve the DNN program’s performance
and reduce the overall time overhead.
```

### 9993bde5022b6c59

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Fortunately, most
state-of-the-art DL Compilers [11], [13] support third-party
code-gen tools (e.g., LLVM [15]) for users to apply the
customized transformation, which leaves us the window to
shield DNN programs.

We carefully investigated attacking frameworks’ basic logic
and workflow to gain more insight into the reversing-based
model extraction attack.

These frameworks include the same
components to rebuild the model: operator-type recovery,
topology recovery, and metadata recovery (including dimen-
sions, parameters, and attributes).

Although the methodologies
vary from framework to framework, they share the idea of
using the computation pattern to recover the operator type.

Specifically, each kind of operator in the DNN model has a
formula for transforming the input data to the next operator.

For instance, the ReLU activation function uses the formula
1, and the Tanh activation function uses the formula 2.

They
exhibit entirely different syntax and semantics meanings when
represented in the program.
```

### 2e79fb7bed8a4c7a

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 6 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Model From Frameworks Computational Graph 
Representation High-level Graph IR
Low Level IRScheduling & 
Tuning
Target Translation 
(Code Gen)DNN Programs
Frontend
Backend
Fig. 1: Compilation Flow of the Deep Learning Compiler.

The input of the DL compiler is a DNN model.

The compiler
frontend transforms the model description into a computational
graph representation and further conveys it into graph IR to
apply graph- and node-level optimizations.

At the compiler
backend, it does hardware-specific optimization on low-level
IR.

Finally, the compiler generates the DNN Programs for the
target platform.
• We design and implement FlatD, the advanced defense
framework targeting compiled models toward reversing-
based model extraction attacks.
```

### Retrieved Top-20

**#1** — 8cefd0858ce58581 | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=1

```
FlatD and O-LLVM are both applied during the
compilation and optimization.

A.

Experimental Setup
We implement FlatD on the top of O-LLVM [15], [41]
(version 8.0), primarily written in C++ with about 5K LOC.

The current implementation obfuscates and evaluates DNN
Programs in the ELF format on x86 platforms.

In the evaluation, we use TVM [11] as the state-of-the-art
DL compiler to compile the models into DNN programs.

For
most of our evaluation, we used TVM v0.13.0 with the highest
optimizati
```

**#2** — 6307e991f8d86b11 | FlatD: Protecting Deep Neural Network Program.pdf | p.10-10 | sec=experiment | ci=13

```
Compared to O-LLVM, the programs
generated by FlatD have a lower scale while maintaining a
similar performance.
1) Inference Time Overhead: Since the time overhead is
sensitive to the runtime environment and can fluctuate wildly
due to unexpected reasons, we run each DNN program,
including the programs generated by O-LLVM and FlatD and
the original program, in an isolated environment to mitigate
the influence of the runtime environment and reduce such
fluctuation.

Moreover, we randomly chose on
```

**#3** **[HIT]** — 2e79fb7bed8a4c7a | FlatD: Protecting Deep Neural Network Program.pdf | p.2-2 | sec=introduction | ci=6

```
Model From Frameworks Computational Graph 
Representation High-level Graph IR
Low Level IRScheduling & 
Tuning
Target Translation 
(Code Gen)DNN Programs
Frontend
Backend
Fig. 1: Compilation Flow of the Deep Learning Compiler.

The input of the DL compiler is a DNN model.

The compiler
frontend transforms the model description into a computational
graph representation and further conveys it into graph IR to
apply graph- and node-level optimizations.

At the compiler
backend, it does hardware-spe
```

**#4** — 12666ddaf8f0c84b | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=2

```
All
these models, except MNIST-convnet, are pre-trained models
loaded from different frameworks.

Among them, MNIST-
convnet is a self-construct and self-trained model following
the guide from [73], and ResNet18 is used to evaluate the
effect of FlatD across the frameworks, so we loaded it from
PyTorch [44], ONNX [78], and MXNet [10] respectively.

The
rest of the models are all loaded from the Keras application
zoo [7], [79].

We perform all the evaluations on an Ubuntu 22.04 system
on a machin
```

**#5** — bc2be347fca010c6 | FlatD: Protecting Deep Neural Network Program.pdf | p.10-11 | sec=conclusion | ci=0

```
In this paper, we design and implement FlatD, an ad-
vanced defense framework for protecting DNN programs from
reversing-based model extraction attacks based on control flow
flattening. FlatD makes it challenging for attackers to re-
cover the CFG statically and gain necessary information from
DNN programs. Compared to the traditional Control Flow
Flattening, our evaluation shows that FlatD is an effective,
adequate, and practical defense framework that prevents DNN
programs from leaking essenti
```

**#6** — 18454bfa5fb87598 | FlatD: Protecting Deep Neural Network Program.pdf | p.3-3 | sec=related_work | ci=3

```
Giant AI providers like Amazon and Google also
include DL compilers in their AI services to boost perfor-
mance [17]–[19], [21].

As the need for DL-based services has
increased, DL compilers play a more critical role in deploying
DNN models, and the safety of DNN programs becomes
increasingly vital.

B.

Control Flow Obfuscation
Obfuscation is a technique that software developers have
used for a long time to protect their intellectual property.

The
basic idea behind obfuscation is to transform
```

**#7** — a99828379ba568e2 | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=0

```
In this section, we evaluate FlatD by answering the follow-
ing research questions (RQs) through empirical evaluation.
• RQ1: (Correctness) After applying FlatD to the DNN
programs from different DL frameworks, can they still
apply the inference functionality properly?
• RQ2: (Resilience) Does FlatD effectively counterwork
against the state-of-the-art reversing-based extraction at-
tack?
• RQ3: (Performance and Scale)How does FlatD affect
the performance and scale of the DNN programs?

To explor
```

**#8** — cfe38cd33d273d0a | FlatD: Protecting Deep Neural Network Program.pdf | p.3-3 | sec=related_work | ci=2

```
Recent advancements [11], [43], [49], [50] introduce
automated scheduling and tuning to improve optimization,
reducing manual efforts.

Code Generation.

Finally, these low-level IRs are compiled
into code for different hardware targets.

Before that, the DL
compilers can also integrate with existing infrastructure like
LLVM [15] and CUDA [16] to leverage third-party toolchains
and further manipulate the generated code, which also provides
the opportunity for us to apply defense mechanisms to pr
```

**#9** — 5197bb55c183f05b | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=3

```
The primary metric
for this comparison is to check if the prediction results of
the two models are identical.

We assumed the original DNN
program results were the ground truth and computed the
identical percentage for the programs generated from FlatD
and O-LLVM.

To ensure a diverse and representative sample
of test inputs, we sourced the test dataset from the ImageNet
obtained from TorchVision [80].

We randomly select10, 000
test inputs from this dataset as our evaluation set.

Moreover, to

```

**#10** — 116bf184afa8506d | FlatD: Protecting Deep Neural Network Program.pdf | p.10-10 | sec=discussion | ci=1

```
Karchmer [85] discusses the
possibility of providing provable security against model ex-
traction attacks.

To detect such an attack, the author proposes
a theoretical framework for analyzing observational model
extraction defenses (OMEDs) that examine the distribution of
queries made by adversaries.

They introduce the concepts of
complete and sound OMEDs and show that achieving provable
security against model extraction through these defenses is
possible using average-case hardness assumptions
```

**#11** — 3e9c3b52a90bf04f | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=7

```
Attack Framework
MNIST VGG16
TVM -O0 TVM -O3 TVM -O0 TVM -O3
Orig O-LLVM FlatD Orig O-LLVM FlatD Orig O-LLVM FlatD orig O-LLVM FlatD
BTD [33] 100% 91.67% 50% 100% 92.31% 38.46% 100% 96.88 % 40.63% 100% 91.23% 64.91%
LibSteal [35] 100% 58.34% 25.00% N/A 100% 40.63% 9.38% N/A
TABLE VI: Comparison between the performance of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the time overhead of the original program as the baseline (100%).

This table r
```

**#12** — 815cd321ec8ac7ee | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=10

```
We
apply the same metrics to compute the accuracy of each
attack used, where the prediction of operator type is regarded
as correct only when the predicted result describes precisely
the same operation as the ground truth.

Since LibSteal [35]
cannot deal with the situation when multiply operators are
fused into one operator function, we only evaluate the DNN
programs compiled with configuration -O3 on BTD [33].

As
we can see, compared to the O-LLVM, FlatD can effectively
reduce accuracy in DNN
```

**#13** — 5ed46f026fae5958 | FlatD: Protecting Deep Neural Network Program.pdf | p.1-1 | sec=abstract | ci=0

```
FlatD: Protecting Deep Neural Network Program
from Reversing Attacks
Jinquan Zhang
The Pennsylvania State University
University Park, USA
jxz372@psu.edu
Zihao Wang
The Pennsylvania State University
University Park, USA
zihao@psu.edu
Dinghao Wu
The Pennsylvania State University
University Park, USA
dinghao@psu.edu
Pei Wang
Individual Researcher
San Jose, USA
uraj@apache.org
Rui Zhong
Palo Alto Network
Santa Clara, USA
reversezr33@gmail.com
Abstract—The emergence of Deep Learning compilers provide
```

**#14** — 8fea83d2795a1cd0 | FlatD: Protecting Deep Neural Network Program.pdf | p.1-1 | sec=abstract | ci=1

```
To address the issue, we investigate all of the state-of-the-
art reversing-based model extraction attacks and identify an
essential component shared across the frameworks.

Based on this
observation, we propose FlatD, the first defense framework for
DNN programs toward reversing-based model extraction attacks.

FlatD manipulates and conceals the original Control Flow Graphs
of DNN programs based on Control Flow Flattening.

Unlike
traditional Control Flow Flattening, FlatD ensures the DNN
progr
```

**#15** — c3742f8b77889850 | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=8

```
VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 162% 166% 181% 170% 176% 176% 228% 147% 149% 146%
FlatD 188% 183% 280% 169% 163% 161% 231% 138% 138% 134%
TABLE VII: Comparison between the scale of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the original DNN program size as the baseline (100%).

This table shows the increased
percentage between transformed DNN programs and original DNN programs.

Here,P refers
```

**#16** — 69052d09957be415 | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=9

```
Diff (%) VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 27.90 27.57 34.71 28.59 28.44 28.88 34.24 36.73 35.53 35.72
FlatD 17.43 17.48 18.76 12.91 12.91 12.90 17.04 22/45 21.93 21.94
of Operator functions, which is only related to the Operator
Type recovery, we only evaluate our defense mechanism on
how it can affect the inference of Operator Type of each
reversing-based model extraction attack.

Moreover, Operator-
type recovery is the most essential and fundam
```

**#17** **[HIT]** — 347cb9d0884d62c1 | FlatD: Protecting Deep Neural Network Program.pdf | p.2-2 | sec=introduction | ci=4

```
This feature helps attackers infer
the operator type by using binary similarity comparison.

On
the other hand, it also guides the protection of DNN programs
because we found that the Control Flow Graph (CFG) plays
a vital role in all attack frameworks.
f(x) =x+ = max(0, x) =x + |x|
2 (1)
f(x) =ex + e−x
ex − e−x (2)
Based on our observations, this paper proposes FlatD, an
advanced defense framework based on Control Flow Flat-
tening, for DNN programs to protect them from reversing-
based model e
```

**#18** — b85432db3e615e3f | FlatD: Protecting Deep Neural Network Program.pdf | p.8-9 | sec=experiment | ci=5

```
To test the effect
of our defense mechanism on a more diverse set of DNN
programs, we compile the two models above with two different
optimizations (O0 and O3).
2) Operator Type Inference: As mentioned in Section III,
all the reversing-based model extraction attacks fully or par-
tially include four parts: Operator-type recovery, Topology
recovery, Parameter recovery, and Dimensions (Attributes) Re-
covery.

Since FlatD mainly focuses on manipulating the CFG
TABLE IV: Comparison of the inference
```

**#19** — c5a41f9539bbbbb3 | FlatD: Protecting Deep Neural Network Program.pdf | p.4-4 | sec=related_work | ci=10

```
BTD uses the Intel
PinTool [72] to hook every call site as the operator function’s
inputs and outputs are transmitted via memory pointers in the
function arguments.

Subsequently, BTD seamlessly links the
operator function using the identical memory address.

As for
data recovery, BTD applies taint analysis and symbolic execu-
tion to collected execution traces to infer the parameters and
hyperparameters.

LibSteal heuristically searches for possible
topology combinations to link all the inferre
```

**#20** **[HIT]** — 241543cef9ddd0b4 | FlatD: Protecting Deep Neural Network Program.pdf | p.2-2 | sec=introduction | ci=5

```
We implemented FlatD on the top of O-LLVM [41] and em-
bedded it into the code generation part of TVM [11].

We used
O-LLVM as the baseline and evaluated FlatD on eight real-
world pre-trained models and one self-trained model from four
frameworks.

Our experiment results show that compared to the
traditional Control Flow Flattening, FlatD can more effectively
counterwork state-of-the-art reversing-based model extraction
attacks while preserving the functionality of the original DNN
programs.

M
```

### Missed Chunks (2 — expected but NOT in top-20)

### f73b5f75aac3ec83

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 7 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
FlatD conceals the orig-
inal Control Flow Graph of DNN programs based on
Control Flow Flattening and ensures minimal information
gained by attackers through statistical analysis.
• We successfully apply FlatD on DNN programs compiled
from large-scale models using TVM to evaluate these
DNN programs regarding functionality, performance, and
resilience.

We use O-LLVM as the baseline to compare
the results.

Our experiment demonstrates that DNN pro-
grams transformed by FlatD can prevent leaking informa-
tion from reversing-based model extraction attacks more
effectively than traditional Control Flow Flattening with
similar performance and lower scale.
```

### 9993bde5022b6c59

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Fortunately, most
state-of-the-art DL Compilers [11], [13] support third-party
code-gen tools (e.g., LLVM [15]) for users to apply the
customized transformation, which leaves us the window to
shield DNN programs.

We carefully investigated attacking frameworks’ basic logic
and workflow to gain more insight into the reversing-based
model extraction attack.

These frameworks include the same
components to rebuild the model: operator-type recovery,
topology recovery, and metadata recovery (including dimen-
sions, parameters, and attributes).

Although the methodologies
vary from framework to framework, they share the idea of
using the computation pattern to recover the operator type.

Specifically, each kind of operator in the DNN model has a
formula for transforming the input data to the next operator.

For instance, the ReLU activation function uses the formula
1, and the Tanh activation function uses the formula 2.

They
exhibit entirely different syntax and semantics meanings when
represented in the program.
```

### False Positives (17 — in top-20 but NOT expected)

### 8cefd0858ce58581

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 1 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
FlatD and O-LLVM are both applied during the
compilation and optimization.

A.

Experimental Setup
We implement FlatD on the top of O-LLVM [15], [41]
(version 8.0), primarily written in C++ with about 5K LOC.

The current implementation obfuscates and evaluates DNN
Programs in the ELF format on x86 platforms.

In the evaluation, we use TVM [11] as the state-of-the-art
DL compiler to compile the models into DNN programs.

For
most of our evaluation, we used TVM v0.13.0 with the highest
optimization level (O3) to compile the model.

However, for
the resilience evaluation, since the TVM version’s iteration
is relatively fast, in order to align the attack environment,
we chose TVM v0.9.0 to generate the victim DNN programs
with both the lowest optimization level (O0) and the highest
optimization level (O3).

Table III shows all DNN models used for evaluation.
```

### 6307e991f8d86b11

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 13 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Compared to O-LLVM, the programs
generated by FlatD have a lower scale while maintaining a
similar performance.
1) Inference Time Overhead: Since the time overhead is
sensitive to the runtime environment and can fluctuate wildly
due to unexpected reasons, we run each DNN program,
including the programs generated by O-LLVM and FlatD and
the original program, in an isolated environment to mitigate
the influence of the runtime environment and reduce such
fluctuation.

Moreover, we randomly chose one picture from
ImageNet and used it as input for all the inference tasks.

For
each DNN program, we run the inference 100 times and record
the mean value as the evaluation result.

As shown in Table VI,
the results demonstrate that the time overhead introduced by
FlatD is similar to O-LLVM for most DNN models except the
Xecption model.
2) Program Scale: Table VII shows the scale change be-
tween the transformed DNN programs generated by FlatD
and O-LLVM and the original DNN programs.
```

### 12666ddaf8f0c84b

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 2 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
All
these models, except MNIST-convnet, are pre-trained models
loaded from different frameworks.

Among them, MNIST-
convnet is a self-construct and self-trained model following
the guide from [73], and ResNet18 is used to evaluate the
effect of FlatD across the frameworks, so we loaded it from
PyTorch [44], ONNX [78], and MXNet [10] respectively.

The
rest of the models are all loaded from the Keras application
zoo [7], [79].

We perform all the evaluations on an Ubuntu 22.04 system
on a machine with an Intel(R) Xeon(R) Silver 4114 CPU (2.20
GHz), 40 cores, and 219GB RAM.

B. (RQ1) Correctness
To evaluate the impact of FlatD on preserving the inference
accuracy of DNN programs, we compare the inference out-
comes of the original DNN programs with the counterparts
transformed from FlatD and O-LLVM.
```

### bc2be347fca010c6

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | conclusion |
| section_title | VII. CONCLUSION |
| page_start | 10 |
| page_end | 11 |
| chunk_index | 0 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
In this paper, we design and implement FlatD, an ad-
vanced defense framework for protecting DNN programs from
reversing-based model extraction attacks based on control flow
flattening. FlatD makes it challenging for attackers to re-
cover the CFG statically and gain necessary information from
DNN programs. Compared to the traditional Control Flow
Flattening, our evaluation shows that FlatD is an effective,
adequate, and practical defense framework that prevents DNN
programs from leaking essential information while ensuring
their performance and program scale.
```

### 18454bfa5fb87598

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | related_work |
| section_title | II. BACKGROUND |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 3 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Giant AI providers like Amazon and Google also
include DL compilers in their AI services to boost perfor-
mance [17]–[19], [21].

As the need for DL-based services has
increased, DL compilers play a more critical role in deploying
DNN models, and the safety of DNN programs becomes
increasingly vital.

B.

Control Flow Obfuscation
Obfuscation is a technique that software developers have
used for a long time to protect their intellectual property.

The
basic idea behind obfuscation is to transform a program into
a new version that retains its functionality and semantics but
hides its high-level structures [54]–[56].

Obfuscation signifi-
cantly increases the difficulty of static program analysis [57]–
[59], reversing engineering [60], [61], and also higher the bar
of dynamic program analysis [62]–[66].

As an essential branch
of obfuscation, control flow obfuscation aims to conceal the
proper control flow and make the control flow graph as
complicated as possible to raise the bar of countermeasures.
```

### a99828379ba568e2

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 0 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
In this section, we evaluate FlatD by answering the follow-
ing research questions (RQs) through empirical evaluation.
• RQ1: (Correctness) After applying FlatD to the DNN
programs from different DL frameworks, can they still
apply the inference functionality properly?
• RQ2: (Resilience) Does FlatD effectively counterwork
against the state-of-the-art reversing-based extraction at-
tack?
• RQ3: (Performance and Scale)How does FlatD affect
the performance and scale of the DNN programs?

To explore the above RQs and provide a comprehensive
evaluation, we evaluate FlatD with eight real-world pre-trained
models and one self-trained model from four different frame-
works and use the well-known obfuscator, O-LLVM [41] as
the baseline.

We only use the control flow flattening (-fla)
obfuscation of O-LLVM to transform the program.

All models
are optimized and compiled by TVM [11] to generate DNN
programs.
```

### cfe38cd33d273d0a

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | related_work |
| section_title | II. BACKGROUND |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 2 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Recent advancements [11], [43], [49], [50] introduce
automated scheduling and tuning to improve optimization,
reducing manual efforts.

Code Generation.

Finally, these low-level IRs are compiled
into code for different hardware targets.

Before that, the DL
compilers can also integrate with existing infrastructure like
LLVM [15] and CUDA [16] to leverage third-party toolchains
and further manipulate the generated code, which also provides
the opportunity for us to apply defense mechanisms to protect
DNN programs from reversing-based model extraction attack.

We implement FlatD on the top of LLVM to protect DNN
programs from reversing-based model extraction attacks.

Thanks to the appearance of the DL compilers, the DNN
model can be deployed on edge devices and low-power pro-
cessors [51]–[53] having limited hardware resources with low
overhead, while the popular DL frameworks like Tensorflow
[8] only provide optimization for a narrow range of server-
class GPUs.
```

### 5197bb55c183f05b

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 3 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
The primary metric
for this comparison is to check if the prediction results of
the two models are identical.

We assumed the original DNN
program results were the ground truth and computed the
identical percentage for the programs generated from FlatD
and O-LLVM.

To ensure a diverse and representative sample
of test inputs, we sourced the test dataset from the ImageNet
obtained from TorchVision [80].

We randomly select10, 000
test inputs from this dataset as our evaluation set.

Moreover, to
illustrate the adaptability of FlatD, we evaluated ten versions.

Within this set, three versions of ResNet18 were sourced
from three distinct frameworks: PyTorch, ONNX, and MXNet.

The remaining seven models were obtained from the Keras
Application Zoo.

The summarized results are presented in Table IV.

The
findings from this table indicate that the inference results
of the transformed DNN programs generated by FlatD align
perfectly with those of the original programs across all the
sampled inputs, which is under the expectation.
```

### 116bf184afa8506d

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | discussion |
| section_title | VI. RELATED WORK AND DISCUSSION |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 1 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Karchmer [85] discusses the
possibility of providing provable security against model ex-
traction attacks.

To detect such an attack, the author proposes
a theoretical framework for analyzing observational model
extraction defenses (OMEDs) that examine the distribution of
queries made by adversaries.

They introduce the concepts of
complete and sound OMEDs and show that achieving provable
security against model extraction through these defenses is
possible using average-case hardness assumptions for PAC
learning.

The framework provides a way to abstract current
techniques used in the literature to achieve provable security.

Protect other characteristics.

The primary purpose of FlatD
is to protect the Control Flow Graph of the operator function
so that attackers cannot infer the operator types accordingly.

However, we do not protect other model characteristics, such
as graph topology, operator attributes, and parameters, which
should be protected from different views.

For example, the
data flow of DNN programs is also an essential feature
attackers use to extract model information, like graph topology.
```

### 3e9c3b52a90bf04f

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 7 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Attack Framework
MNIST VGG16
TVM -O0 TVM -O3 TVM -O0 TVM -O3
Orig O-LLVM FlatD Orig O-LLVM FlatD Orig O-LLVM FlatD orig O-LLVM FlatD
BTD [33] 100% 91.67% 50% 100% 92.31% 38.46% 100% 96.88 % 40.63% 100% 91.23% 64.91%
LibSteal [35] 100% 58.34% 25.00% N/A 100% 40.63% 9.38% N/A
TABLE VI: Comparison between the performance of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the time overhead of the original program as the baseline (100%).

This table reports the time
overhead of each DNN program running the inference to one specific picture from ImageNet and compares it to the original
version to indicate the increasing time overhead.

Here,P refers to PyTorch, O refers to ONNX, and M refers to MXNet.
```

### 815cd321ec8ac7ee

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 10 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
We
apply the same metrics to compute the accuracy of each
attack used, where the prediction of operator type is regarded
as correct only when the predicted result describes precisely
the same operation as the ground truth.

Since LibSteal [35]
cannot deal with the situation when multiply operators are
fused into one operator function, we only evaluate the DNN
programs compiled with configuration -O3 on BTD [33].

As
we can see, compared to the O-LLVM, FlatD can effectively
reduce accuracy in DNN operator inference for each attack
framework.

Notably, while BTD can still achieve over 90%
accuracy decompiling the program transformed by O-LLVM,
FlatD decreases the accuracy to around 60% and even lower.
```

### 5ed46f026fae5958

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | abstract |
| section_title | Abstract/摘要 |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 0 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
FlatD: Protecting Deep Neural Network Program
from Reversing Attacks
Jinquan Zhang
The Pennsylvania State University
University Park, USA
jxz372@psu.edu
Zihao Wang
The Pennsylvania State University
University Park, USA
zihao@psu.edu
Dinghao Wu
The Pennsylvania State University
University Park, USA
dinghao@psu.edu
Pei Wang
Individual Researcher
San Jose, USA
uraj@apache.org
Rui Zhong
Palo Alto Network
Santa Clara, USA
reversezr33@gmail.com
Abstract—The emergence of Deep Learning compilers provides
automated optimization and compilation across Deep Learning
frameworks and hardware platforms, which enhances the perfor-
mance of AI service and benefits the deployment to edge devices
and low-power processors.

However, deep neural network (DNN)
programs generated by Deep Learning compilers introduce a
new attack interface.

They are targeted by new model extraction
attacks that can fully or partially rebuild the DNN model
by reversing the DNN programs.

Unfortunately, no defense
countermeasure is designed to hinder this kind of attack.
```

### 8fea83d2795a1cd0

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | abstract |
| section_title | Abstract/摘要 |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 1 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
To address the issue, we investigate all of the state-of-the-
art reversing-based model extraction attacks and identify an
essential component shared across the frameworks.

Based on this
observation, we propose FlatD, the first defense framework for
DNN programs toward reversing-based model extraction attacks.

FlatD manipulates and conceals the original Control Flow Graphs
of DNN programs based on Control Flow Flattening.

Unlike
traditional Control Flow Flattening, FlatD ensures the DNN
programs are challenging for attackers to recover their Control
Flow Graphs and gain necessary information statically.

Our
evaluation shows that, compared to the traditional Control Flow
Flattening (O-LLVM), FlatD provides more effective and stealthy
protection to DNN programs with similar performance and lower
scale.

Index Terms—Software Engineering, Protection mechanisms,
Artificial Intelligence
```

### c3742f8b77889850

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 8 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 162% 166% 181% 170% 176% 176% 228% 147% 149% 146%
FlatD 188% 183% 280% 169% 163% 161% 231% 138% 138% 134%
TABLE VII: Comparison between the scale of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the original DNN program size as the baseline (100%).

This table shows the increased
percentage between transformed DNN programs and original DNN programs.

Here,P refers to PyTorch, O refers to ONNX,
and M refers to MXNet.
```

### 69052d09957be415

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 9 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Diff (%) VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 27.90 27.57 34.71 28.59 28.44 28.88 34.24 36.73 35.53 35.72
FlatD 17.43 17.48 18.76 12.91 12.91 12.90 17.04 22/45 21.93 21.94
of Operator functions, which is only related to the Operator
Type recovery, we only evaluate our defense mechanism on
how it can affect the inference of Operator Type of each
reversing-based model extraction attack.

Moreover, Operator-
type recovery is the most essential and fundamental step in
reconstructing the final models because, in some attacks [32],
[34], [35], the recovery of other parts highly depends on the
recovery of Operator-type.

We report the difference in the accuracy of DNN operator
inference between the original version and the transformed
version generated from O-LLVM and FlatD in Table V.
```

### b85432db3e615e3f

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 9 |
| chunk_index | 5 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
To test the effect
of our defense mechanism on a more diverse set of DNN
programs, we compile the two models above with two different
optimizations (O0 and O3).
2) Operator Type Inference: As mentioned in Section III,
all the reversing-based model extraction attacks fully or par-
tially include four parts: Operator-type recovery, Topology
recovery, Parameter recovery, and Dimensions (Attributes) Re-
covery.

Since FlatD mainly focuses on manipulating the CFG
TABLE IV: Comparison of the inference results of the obfuscated DNN programs from O-LLVM and FlatD to the original
DNN programs.
```

### c5a41f9539bbbbb3

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | related_work |
| section_title | II. BACKGROUND |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 10 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
BTD uses the Intel
PinTool [72] to hook every call site as the operator function’s
inputs and outputs are transmitted via memory pointers in the
function arguments.

Subsequently, BTD seamlessly links the
operator function using the identical memory address.

As for
data recovery, BTD applies taint analysis and symbolic execu-
tion to collected execution traces to infer the parameters and
hyperparameters.

LibSteal heuristically searches for possible
topology combinations to link all the inferred operators.

It also
extracts the dimensions and partially recovers hyperparameters
by analyzing the data flow of the DNN program.

Inspiration Our analysis of reverse-engineering-based extrac-
tion attacks reveals that the type of operator is a crucial ele-
ment to protect.

As shown in Fig.2, the unique computational
patterns of each operator lead to specific features in the Control
Flow Graph (CFG), particularly loop structures.
```

---

## 12. [single_004_zh] FlatD 使用什么核心技术来保护 DNN 程序？它是如何集成到编译流水线中的？

**Type**: `method` | **Lang**: `ZH` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.2000 | 0.2000 |
| 10 | 0.4000 | 0.6000 |
| 20 | 0.4000 | 0.6000 |

**Expected sources**: FlatD

### Expected Chunks (5)

### 241543cef9ddd0b4

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 5 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
We implemented FlatD on the top of O-LLVM [41] and em-
bedded it into the code generation part of TVM [11].

We used
O-LLVM as the baseline and evaluated FlatD on eight real-
world pre-trained models and one self-trained model from four
frameworks.

Our experiment results show that compared to the
traditional Control Flow Flattening, FlatD can more effectively
counterwork state-of-the-art reversing-based model extraction
attacks while preserving the functionality of the original DNN
programs.

Moreover, the DNN program transformed by FlatD
performs similarly to the one using traditional Control Flow
Flattening in most cases and always has a lower scale.

In summary, we make the following contributions:
• We investigate four state-of-the-art reversing-based model
extraction attacks and identify a key component shared
across the attack frameworks.

This component guides the
provision of protection and contributes to future research
on DNN program safety.
```

### f73b5f75aac3ec83

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 7 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
FlatD conceals the orig-
inal Control Flow Graph of DNN programs based on
Control Flow Flattening and ensures minimal information
gained by attackers through statistical analysis.
• We successfully apply FlatD on DNN programs compiled
from large-scale models using TVM to evaluate these
DNN programs regarding functionality, performance, and
resilience.

We use O-LLVM as the baseline to compare
the results.

Our experiment demonstrates that DNN pro-
grams transformed by FlatD can prevent leaking informa-
tion from reversing-based model extraction attacks more
effectively than traditional Control Flow Flattening with
similar performance and lower scale.
```

### 2338dcc55b3e6bfb

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | related_work |
| section_title | II. BACKGROUND |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 0 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
A.

Deep Learning Compiler
The objective of deep learning compilers, such as XLA [14],
TVM [11], Intel nGraph [42], and Tensor Comprehension [43],
is to simplify the process of deploying DNN models on differ-
ent hardware platforms, by automating the optimization and
transformation.

These compilers can take models described
within popular frameworks like TensorFlow [8], PyTorch
[44], MXNet [10], Caffe2 [9], and Keras [45] as inputs and
generate standalone DNN programs or kernel libraries that can
be statically linked with executables for CPUs, GPUs, and
TPU-like accelerators.

As shown in Fig.1, the DL compiler
architecture can be divided into two main phases: frontend
and backend, each manipulating one or several Intermediate
Representations (IR).

Frontend.

DL compilers first transform high-level model
descriptions into computational graph representations and con-
vert them into graph IRs.
```

### 9993bde5022b6c59

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Fortunately, most
state-of-the-art DL Compilers [11], [13] support third-party
code-gen tools (e.g., LLVM [15]) for users to apply the
customized transformation, which leaves us the window to
shield DNN programs.

We carefully investigated attacking frameworks’ basic logic
and workflow to gain more insight into the reversing-based
model extraction attack.

These frameworks include the same
components to rebuild the model: operator-type recovery,
topology recovery, and metadata recovery (including dimen-
sions, parameters, and attributes).

Although the methodologies
vary from framework to framework, they share the idea of
using the computation pattern to recover the operator type.

Specifically, each kind of operator in the DNN model has a
formula for transforming the input data to the next operator.

For instance, the ReLU activation function uses the formula
1, and the Tanh activation function uses the formula 2.

They
exhibit entirely different syntax and semantics meanings when
represented in the program.
```

### 347cb9d0884d62c1

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
This feature helps attackers infer
the operator type by using binary similarity comparison.

On
the other hand, it also guides the protection of DNN programs
because we found that the Control Flow Graph (CFG) plays
a vital role in all attack frameworks.
f(x) =x+ = max(0, x) =x + |x|
2 (1)
f(x) =ex + e−x
ex − e−x (2)
Based on our observations, this paper proposes FlatD, an
advanced defense framework based on Control Flow Flat-
tening, for DNN programs to protect them from reversing-
based model extraction attacks.

Unlike the traditional Control
Flow Flattening, we leverage the opaque predicate, one-way
cryptographic hashing, and indirect jump to conceal the control
flow further so that attackers cannot quickly recover the
original CFG and apply more inference analysis.

We also use
several strategies to preserve the DNN program’s performance
and reduce the overall time overhead.
```

### Retrieved Top-20

**#1** — 3e9c3b52a90bf04f | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=7

```
Attack Framework
MNIST VGG16
TVM -O0 TVM -O3 TVM -O0 TVM -O3
Orig O-LLVM FlatD Orig O-LLVM FlatD Orig O-LLVM FlatD orig O-LLVM FlatD
BTD [33] 100% 91.67% 50% 100% 92.31% 38.46% 100% 96.88 % 40.63% 100% 91.23% 64.91%
LibSteal [35] 100% 58.34% 25.00% N/A 100% 40.63% 9.38% N/A
TABLE VI: Comparison between the performance of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the time overhead of the original program as the baseline (100%).

This table r
```

**#2** — 8fea83d2795a1cd0 | FlatD: Protecting Deep Neural Network Program.pdf | p.1-1 | sec=abstract | ci=1

```
To address the issue, we investigate all of the state-of-the-
art reversing-based model extraction attacks and identify an
essential component shared across the frameworks.

Based on this
observation, we propose FlatD, the first defense framework for
DNN programs toward reversing-based model extraction attacks.

FlatD manipulates and conceals the original Control Flow Graphs
of DNN programs based on Control Flow Flattening.

Unlike
traditional Control Flow Flattening, FlatD ensures the DNN
progr
```

**#3** — a99828379ba568e2 | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=0

```
In this section, we evaluate FlatD by answering the follow-
ing research questions (RQs) through empirical evaluation.
• RQ1: (Correctness) After applying FlatD to the DNN
programs from different DL frameworks, can they still
apply the inference functionality properly?
• RQ2: (Resilience) Does FlatD effectively counterwork
against the state-of-the-art reversing-based extraction at-
tack?
• RQ3: (Performance and Scale)How does FlatD affect
the performance and scale of the DNN programs?

To explor
```

**#4** — bc2be347fca010c6 | FlatD: Protecting Deep Neural Network Program.pdf | p.10-11 | sec=conclusion | ci=0

```
In this paper, we design and implement FlatD, an ad-
vanced defense framework for protecting DNN programs from
reversing-based model extraction attacks based on control flow
flattening. FlatD makes it challenging for attackers to re-
cover the CFG statically and gain necessary information from
DNN programs. Compared to the traditional Control Flow
Flattening, our evaluation shows that FlatD is an effective,
adequate, and practical defense framework that prevents DNN
programs from leaking essenti
```

**#5** **[HIT]** — f73b5f75aac3ec83 | FlatD: Protecting Deep Neural Network Program.pdf | p.2-2 | sec=introduction | ci=7

```
FlatD conceals the orig-
inal Control Flow Graph of DNN programs based on
Control Flow Flattening and ensures minimal information
gained by attackers through statistical analysis.
• We successfully apply FlatD on DNN programs compiled
from large-scale models using TVM to evaluate these
DNN programs regarding functionality, performance, and
resilience.

We use O-LLVM as the baseline to compare
the results.

Our experiment demonstrates that DNN pro-
grams transformed by FlatD can prevent leaking i
```

**#6** — 6307e991f8d86b11 | FlatD: Protecting Deep Neural Network Program.pdf | p.10-10 | sec=experiment | ci=13

```
Compared to O-LLVM, the programs
generated by FlatD have a lower scale while maintaining a
similar performance.
1) Inference Time Overhead: Since the time overhead is
sensitive to the runtime environment and can fluctuate wildly
due to unexpected reasons, we run each DNN program,
including the programs generated by O-LLVM and FlatD and
the original program, in an isolated environment to mitigate
the influence of the runtime environment and reduce such
fluctuation.

Moreover, we randomly chose on
```

**#7** — c3742f8b77889850 | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=8

```
VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 162% 166% 181% 170% 176% 176% 228% 147% 149% 146%
FlatD 188% 183% 280% 169% 163% 161% 231% 138% 138% 134%
TABLE VII: Comparison between the scale of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the original DNN program size as the baseline (100%).

This table shows the increased
percentage between transformed DNN programs and original DNN programs.

Here,P refers
```

**#8** — d5077666e66959e8 | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=6

```
Here P refers to PyTorch, O refers to ONNX, M refers to MXNet
VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
FlatD 100% 100% 100% 100% 100% 100% 100% 100% 100% 100%
O-LLVM 100% 100% 100% 100% 100% 100% 0% 100% 100% 100%
TABLE V: The accuracy change in DNN operator inference before and after applying FlatD and O-LLVM. “N/A” means the
attack framework does not support the DNN programs with the settings.
```

**#9** **[HIT]** — 241543cef9ddd0b4 | FlatD: Protecting Deep Neural Network Program.pdf | p.2-2 | sec=introduction | ci=5

```
We implemented FlatD on the top of O-LLVM [41] and em-
bedded it into the code generation part of TVM [11].

We used
O-LLVM as the baseline and evaluated FlatD on eight real-
world pre-trained models and one self-trained model from four
frameworks.

Our experiment results show that compared to the
traditional Control Flow Flattening, FlatD can more effectively
counterwork state-of-the-art reversing-based model extraction
attacks while preserving the functionality of the original DNN
programs.

M
```

**#10** — b85432db3e615e3f | FlatD: Protecting Deep Neural Network Program.pdf | p.8-9 | sec=experiment | ci=5

```
To test the effect
of our defense mechanism on a more diverse set of DNN
programs, we compile the two models above with two different
optimizations (O0 and O3).
2) Operator Type Inference: As mentioned in Section III,
all the reversing-based model extraction attacks fully or par-
tially include four parts: Operator-type recovery, Topology
recovery, Parameter recovery, and Dimensions (Attributes) Re-
covery.

Since FlatD mainly focuses on manipulating the CFG
TABLE IV: Comparison of the inference
```

**#11** — 84c0fb24cb2d6e3b | FlatD: Protecting Deep Neural Network Program.pdf | p.10-10 | sec=experiment | ci=14

```
Since the
transformation process does not affect the parameter part of
the DNN program, we only compare the scale change of the
shared library files, which only contain the operator functions.

To note, Diff = (St
So
−1)∗100(%) where St refers to the scale
of a transformed DNN program and So refers to the scale of its
original version.

As we can see, the final percentages increased
by FlatD to the DNN programs are much less than O-LLVM.

While the size increased by FlatD can range less than 20%
```

**#12** — 12666ddaf8f0c84b | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=2

```
All
these models, except MNIST-convnet, are pre-trained models
loaded from different frameworks.

Among them, MNIST-
convnet is a self-construct and self-trained model following
the guide from [73], and ResNet18 is used to evaluate the
effect of FlatD across the frameworks, so we loaded it from
PyTorch [44], ONNX [78], and MXNet [10] respectively.

The
rest of the models are all loaded from the Keras application
zoo [7], [79].

We perform all the evaluations on an Ubuntu 22.04 system
on a machin
```

**#13** — 5197bb55c183f05b | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=3

```
The primary metric
for this comparison is to check if the prediction results of
the two models are identical.

We assumed the original DNN
program results were the ground truth and computed the
identical percentage for the programs generated from FlatD
and O-LLVM.

To ensure a diverse and representative sample
of test inputs, we sourced the test dataset from the ImageNet
obtained from TorchVision [80].

We randomly select10, 000
test inputs from this dataset as our evaluation set.

Moreover, to

```

**#14** — 8cefd0858ce58581 | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=1

```
FlatD and O-LLVM are both applied during the
compilation and optimization.

A.

Experimental Setup
We implement FlatD on the top of O-LLVM [15], [41]
(version 8.0), primarily written in C++ with about 5K LOC.

The current implementation obfuscates and evaluates DNN
Programs in the ELF format on x86 platforms.

In the evaluation, we use TVM [11] as the state-of-the-art
DL compiler to compile the models into DNN programs.

For
most of our evaluation, we used TVM v0.13.0 with the highest
optimizati
```

**#15** — 815cd321ec8ac7ee | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=10

```
We
apply the same metrics to compute the accuracy of each
attack used, where the prediction of operator type is regarded
as correct only when the predicted result describes precisely
the same operation as the ground truth.

Since LibSteal [35]
cannot deal with the situation when multiply operators are
fused into one operator function, we only evaluate the DNN
programs compiled with configuration -O3 on BTD [33].

As
we can see, compared to the O-LLVM, FlatD can effectively
reduce accuracy in DNN
```

**#16** — ca07840aba57c408 | FlatD: Protecting Deep Neural Network Program.pdf | p.8-8 | sec=experiment | ci=4

```
However, we
surprisingly found that after being obfuscated by O-LLVM,
the MobileNet Program lost functionality.

This outcome un-
derscores the effectiveness of FlatD in preserving the original
functionality and prediction accuracy of the DNN models.

C. (RQ2) Resilience
In this section, we evaluate the resilience of our defense
framework.

We first describe our evaluation setup (Section
V-C1).

Then, we show how FlatD influences the operator-type
inference to the reversing-based extraction atta
```

**#17** — 69052d09957be415 | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=9

```
Diff (%) VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 27.90 27.57 34.71 28.59 28.44 28.88 34.24 36.73 35.53 35.72
FlatD 17.43 17.48 18.76 12.91 12.91 12.90 17.04 22/45 21.93 21.94
of Operator functions, which is only related to the Operator
Type recovery, we only evaluate our defense mechanism on
how it can affect the inference of Operator Type of each
reversing-based model extraction attack.

Moreover, Operator-
type recovery is the most essential and fundam
```

**#18** — 2e79fb7bed8a4c7a | FlatD: Protecting Deep Neural Network Program.pdf | p.2-2 | sec=introduction | ci=6

```
Model From Frameworks Computational Graph 
Representation High-level Graph IR
Low Level IRScheduling & 
Tuning
Target Translation 
(Code Gen)DNN Programs
Frontend
Backend
Fig. 1: Compilation Flow of the Deep Learning Compiler.

The input of the DL compiler is a DNN model.

The compiler
frontend transforms the model description into a computational
graph representation and further conveys it into graph IR to
apply graph- and node-level optimizations.

At the compiler
backend, it does hardware-spe
```

**#19** — cfe38cd33d273d0a | FlatD: Protecting Deep Neural Network Program.pdf | p.3-3 | sec=related_work | ci=2

```
Recent advancements [11], [43], [49], [50] introduce
automated scheduling and tuning to improve optimization,
reducing manual efforts.

Code Generation.

Finally, these low-level IRs are compiled
into code for different hardware targets.

Before that, the DL
compilers can also integrate with existing infrastructure like
LLVM [15] and CUDA [16] to leverage third-party toolchains
and further manipulate the generated code, which also provides
the opportunity for us to apply defense mechanisms to pr
```

**#20** — c7af5be285d241d2 | FlatD: Protecting Deep Neural Network Program.pdf | p.9-9 | sec=experiment | ci=11

```
Specifically, for MNIST with TVM -O0, the accuracy of
BTD reduces to 50.00%; for VGG16 with TVM -O0, the
accuracy of BTD reduces to 40.63%; for the optimization
level -O3, BTD only gets 38.46% accuracy when targeting
the transformed MNIST program compared to 92.31% tar-
geting the MNIST program obfuscated by O-LLVM.

BTD
can achieve 61.54% accuracy when targeting the VGG16
program transformed by FlatD.

When facing the LibSteal
Attack, although O-LLVM has already significantly reduced
the accura
```

### Missed Chunks (3 — expected but NOT in top-20)

### 2338dcc55b3e6bfb

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | related_work |
| section_title | II. BACKGROUND |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 0 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
A.

Deep Learning Compiler
The objective of deep learning compilers, such as XLA [14],
TVM [11], Intel nGraph [42], and Tensor Comprehension [43],
is to simplify the process of deploying DNN models on differ-
ent hardware platforms, by automating the optimization and
transformation.

These compilers can take models described
within popular frameworks like TensorFlow [8], PyTorch
[44], MXNet [10], Caffe2 [9], and Keras [45] as inputs and
generate standalone DNN programs or kernel libraries that can
be statically linked with executables for CPUs, GPUs, and
TPU-like accelerators.

As shown in Fig.1, the DL compiler
architecture can be divided into two main phases: frontend
and backend, each manipulating one or several Intermediate
Representations (IR).

Frontend.

DL compilers first transform high-level model
descriptions into computational graph representations and con-
vert them into graph IRs.
```

### 9993bde5022b6c59

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Fortunately, most
state-of-the-art DL Compilers [11], [13] support third-party
code-gen tools (e.g., LLVM [15]) for users to apply the
customized transformation, which leaves us the window to
shield DNN programs.

We carefully investigated attacking frameworks’ basic logic
and workflow to gain more insight into the reversing-based
model extraction attack.

These frameworks include the same
components to rebuild the model: operator-type recovery,
topology recovery, and metadata recovery (including dimen-
sions, parameters, and attributes).

Although the methodologies
vary from framework to framework, they share the idea of
using the computation pattern to recover the operator type.

Specifically, each kind of operator in the DNN model has a
formula for transforming the input data to the next operator.

For instance, the ReLU activation function uses the formula
1, and the Tanh activation function uses the formula 2.

They
exhibit entirely different syntax and semantics meanings when
represented in the program.
```

### 347cb9d0884d62c1

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
This feature helps attackers infer
the operator type by using binary similarity comparison.

On
the other hand, it also guides the protection of DNN programs
because we found that the Control Flow Graph (CFG) plays
a vital role in all attack frameworks.
f(x) =x+ = max(0, x) =x + |x|
2 (1)
f(x) =ex + e−x
ex − e−x (2)
Based on our observations, this paper proposes FlatD, an
advanced defense framework based on Control Flow Flat-
tening, for DNN programs to protect them from reversing-
based model extraction attacks.

Unlike the traditional Control
Flow Flattening, we leverage the opaque predicate, one-way
cryptographic hashing, and indirect jump to conceal the control
flow further so that attackers cannot quickly recover the
original CFG and apply more inference analysis.

We also use
several strategies to preserve the DNN program’s performance
and reduce the overall time overhead.
```

### False Positives (18 — in top-20 but NOT expected)

### 3e9c3b52a90bf04f

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 7 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Attack Framework
MNIST VGG16
TVM -O0 TVM -O3 TVM -O0 TVM -O3
Orig O-LLVM FlatD Orig O-LLVM FlatD Orig O-LLVM FlatD orig O-LLVM FlatD
BTD [33] 100% 91.67% 50% 100% 92.31% 38.46% 100% 96.88 % 40.63% 100% 91.23% 64.91%
LibSteal [35] 100% 58.34% 25.00% N/A 100% 40.63% 9.38% N/A
TABLE VI: Comparison between the performance of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the time overhead of the original program as the baseline (100%).

This table reports the time
overhead of each DNN program running the inference to one specific picture from ImageNet and compares it to the original
version to indicate the increasing time overhead.

Here,P refers to PyTorch, O refers to ONNX, and M refers to MXNet.
```

### 8fea83d2795a1cd0

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | abstract |
| section_title | Abstract/摘要 |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 1 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
To address the issue, we investigate all of the state-of-the-
art reversing-based model extraction attacks and identify an
essential component shared across the frameworks.

Based on this
observation, we propose FlatD, the first defense framework for
DNN programs toward reversing-based model extraction attacks.

FlatD manipulates and conceals the original Control Flow Graphs
of DNN programs based on Control Flow Flattening.

Unlike
traditional Control Flow Flattening, FlatD ensures the DNN
programs are challenging for attackers to recover their Control
Flow Graphs and gain necessary information statically.

Our
evaluation shows that, compared to the traditional Control Flow
Flattening (O-LLVM), FlatD provides more effective and stealthy
protection to DNN programs with similar performance and lower
scale.

Index Terms—Software Engineering, Protection mechanisms,
Artificial Intelligence
```

### a99828379ba568e2

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 0 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
In this section, we evaluate FlatD by answering the follow-
ing research questions (RQs) through empirical evaluation.
• RQ1: (Correctness) After applying FlatD to the DNN
programs from different DL frameworks, can they still
apply the inference functionality properly?
• RQ2: (Resilience) Does FlatD effectively counterwork
against the state-of-the-art reversing-based extraction at-
tack?
• RQ3: (Performance and Scale)How does FlatD affect
the performance and scale of the DNN programs?

To explore the above RQs and provide a comprehensive
evaluation, we evaluate FlatD with eight real-world pre-trained
models and one self-trained model from four different frame-
works and use the well-known obfuscator, O-LLVM [41] as
the baseline.

We only use the control flow flattening (-fla)
obfuscation of O-LLVM to transform the program.

All models
are optimized and compiled by TVM [11] to generate DNN
programs.
```

### bc2be347fca010c6

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | conclusion |
| section_title | VII. CONCLUSION |
| page_start | 10 |
| page_end | 11 |
| chunk_index | 0 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
In this paper, we design and implement FlatD, an ad-
vanced defense framework for protecting DNN programs from
reversing-based model extraction attacks based on control flow
flattening. FlatD makes it challenging for attackers to re-
cover the CFG statically and gain necessary information from
DNN programs. Compared to the traditional Control Flow
Flattening, our evaluation shows that FlatD is an effective,
adequate, and practical defense framework that prevents DNN
programs from leaking essential information while ensuring
their performance and program scale.
```

### 6307e991f8d86b11

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 13 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Compared to O-LLVM, the programs
generated by FlatD have a lower scale while maintaining a
similar performance.
1) Inference Time Overhead: Since the time overhead is
sensitive to the runtime environment and can fluctuate wildly
due to unexpected reasons, we run each DNN program,
including the programs generated by O-LLVM and FlatD and
the original program, in an isolated environment to mitigate
the influence of the runtime environment and reduce such
fluctuation.

Moreover, we randomly chose one picture from
ImageNet and used it as input for all the inference tasks.

For
each DNN program, we run the inference 100 times and record
the mean value as the evaluation result.

As shown in Table VI,
the results demonstrate that the time overhead introduced by
FlatD is similar to O-LLVM for most DNN models except the
Xecption model.
2) Program Scale: Table VII shows the scale change be-
tween the transformed DNN programs generated by FlatD
and O-LLVM and the original DNN programs.
```

### c3742f8b77889850

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 8 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 162% 166% 181% 170% 176% 176% 228% 147% 149% 146%
FlatD 188% 183% 280% 169% 163% 161% 231% 138% 138% 134%
TABLE VII: Comparison between the scale of the transformed DNN programs generated by FlatD and O-LLVM and the
original DNN programs.

We use the original DNN program size as the baseline (100%).

This table shows the increased
percentage between transformed DNN programs and original DNN programs.

Here,P refers to PyTorch, O refers to ONNX,
and M refers to MXNet.
```

### d5077666e66959e8

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 6 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Here P refers to PyTorch, O refers to ONNX, M refers to MXNet
VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
FlatD 100% 100% 100% 100% 100% 100% 100% 100% 100% 100%
O-LLVM 100% 100% 100% 100% 100% 100% 0% 100% 100% 100%
TABLE V: The accuracy change in DNN operator inference before and after applying FlatD and O-LLVM. “N/A” means the
attack framework does not support the DNN programs with the settings.
```

### b85432db3e615e3f

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 9 |
| chunk_index | 5 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
To test the effect
of our defense mechanism on a more diverse set of DNN
programs, we compile the two models above with two different
optimizations (O0 and O3).
2) Operator Type Inference: As mentioned in Section III,
all the reversing-based model extraction attacks fully or par-
tially include four parts: Operator-type recovery, Topology
recovery, Parameter recovery, and Dimensions (Attributes) Re-
covery.

Since FlatD mainly focuses on manipulating the CFG
TABLE IV: Comparison of the inference results of the obfuscated DNN programs from O-LLVM and FlatD to the original
DNN programs.
```

### 84c0fb24cb2d6e3b

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 14 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Since the
transformation process does not affect the parameter part of
the DNN program, we only compare the scale change of the
shared library files, which only contain the operator functions.

To note, Diff = (St
So
−1)∗100(%) where St refers to the scale
of a transformed DNN program and So refers to the scale of its
original version.

As we can see, the final percentages increased
by FlatD to the DNN programs are much less than O-LLVM.

While the size increased by FlatD can range less than 20%,
the program generated from O-LLVM may increase over 30%.
```

### 12666ddaf8f0c84b

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 2 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
All
these models, except MNIST-convnet, are pre-trained models
loaded from different frameworks.

Among them, MNIST-
convnet is a self-construct and self-trained model following
the guide from [73], and ResNet18 is used to evaluate the
effect of FlatD across the frameworks, so we loaded it from
PyTorch [44], ONNX [78], and MXNet [10] respectively.

The
rest of the models are all loaded from the Keras application
zoo [7], [79].

We perform all the evaluations on an Ubuntu 22.04 system
on a machine with an Intel(R) Xeon(R) Silver 4114 CPU (2.20
GHz), 40 cores, and 219GB RAM.

B. (RQ1) Correctness
To evaluate the impact of FlatD on preserving the inference
accuracy of DNN programs, we compare the inference out-
comes of the original DNN programs with the counterparts
transformed from FlatD and O-LLVM.
```

### 5197bb55c183f05b

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 3 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
The primary metric
for this comparison is to check if the prediction results of
the two models are identical.

We assumed the original DNN
program results were the ground truth and computed the
identical percentage for the programs generated from FlatD
and O-LLVM.

To ensure a diverse and representative sample
of test inputs, we sourced the test dataset from the ImageNet
obtained from TorchVision [80].

We randomly select10, 000
test inputs from this dataset as our evaluation set.

Moreover, to
illustrate the adaptability of FlatD, we evaluated ten versions.

Within this set, three versions of ResNet18 were sourced
from three distinct frameworks: PyTorch, ONNX, and MXNet.

The remaining seven models were obtained from the Keras
Application Zoo.

The summarized results are presented in Table IV.

The
findings from this table indicate that the inference results
of the transformed DNN programs generated by FlatD align
perfectly with those of the original programs across all the
sampled inputs, which is under the expectation.
```

### 8cefd0858ce58581

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 1 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
FlatD and O-LLVM are both applied during the
compilation and optimization.

A.

Experimental Setup
We implement FlatD on the top of O-LLVM [15], [41]
(version 8.0), primarily written in C++ with about 5K LOC.

The current implementation obfuscates and evaluates DNN
Programs in the ELF format on x86 platforms.

In the evaluation, we use TVM [11] as the state-of-the-art
DL compiler to compile the models into DNN programs.

For
most of our evaluation, we used TVM v0.13.0 with the highest
optimization level (O3) to compile the model.

However, for
the resilience evaluation, since the TVM version’s iteration
is relatively fast, in order to align the attack environment,
we chose TVM v0.9.0 to generate the victim DNN programs
with both the lowest optimization level (O0) and the highest
optimization level (O3).

Table III shows all DNN models used for evaluation.
```

### 815cd321ec8ac7ee

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 10 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
We
apply the same metrics to compute the accuracy of each
attack used, where the prediction of operator type is regarded
as correct only when the predicted result describes precisely
the same operation as the ground truth.

Since LibSteal [35]
cannot deal with the situation when multiply operators are
fused into one operator function, we only evaluate the DNN
programs compiled with configuration -O3 on BTD [33].

As
we can see, compared to the O-LLVM, FlatD can effectively
reduce accuracy in DNN operator inference for each attack
framework.

Notably, while BTD can still achieve over 90%
accuracy decompiling the program transformed by O-LLVM,
FlatD decreases the accuracy to around 60% and even lower.
```

### ca07840aba57c408

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 4 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
However, we
surprisingly found that after being obfuscated by O-LLVM,
the MobileNet Program lost functionality.

This outcome un-
derscores the effectiveness of FlatD in preserving the original
functionality and prediction accuracy of the DNN models.

C. (RQ2) Resilience
In this section, we evaluate the resilience of our defense
framework.

We first describe our evaluation setup (Section
V-C1).

Then, we show how FlatD influences the operator-type
inference to the reversing-based extraction attacks (Section
V-C2) by comparing the result between FlatD and O-LLVM.
1) Evaluation Setup: To align with the attack environment
of prior reversing-based model extraction attacks [33], [35],
we choose the TVM with released version v0.9.0 and use
MNIST [81] and VGG16 [75] as two of our test models.

We acquire MNIST by following the guide from [73] and
VGG16 from Keras Application Zoo [79].
```

### 69052d09957be415

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 9 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Diff (%) VGG16 VGG19 Xecption ResNet50 ResNet101 ResNet152 MobileNet ResNet18
P O M
O-LLVM 27.90 27.57 34.71 28.59 28.44 28.88 34.24 36.73 35.53 35.72
FlatD 17.43 17.48 18.76 12.91 12.91 12.90 17.04 22/45 21.93 21.94
of Operator functions, which is only related to the Operator
Type recovery, we only evaluate our defense mechanism on
how it can affect the inference of Operator Type of each
reversing-based model extraction attack.

Moreover, Operator-
type recovery is the most essential and fundamental step in
reconstructing the final models because, in some attacks [32],
[34], [35], the recovery of other parts highly depends on the
recovery of Operator-type.

We report the difference in the accuracy of DNN operator
inference between the original version and the transformed
version generated from O-LLVM and FlatD in Table V.
```

### 2e79fb7bed8a4c7a

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 6 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Model From Frameworks Computational Graph 
Representation High-level Graph IR
Low Level IRScheduling & 
Tuning
Target Translation 
(Code Gen)DNN Programs
Frontend
Backend
Fig. 1: Compilation Flow of the Deep Learning Compiler.

The input of the DL compiler is a DNN model.

The compiler
frontend transforms the model description into a computational
graph representation and further conveys it into graph IR to
apply graph- and node-level optimizations.

At the compiler
backend, it does hardware-specific optimization on low-level
IR.

Finally, the compiler generates the DNN Programs for the
target platform.
• We design and implement FlatD, the advanced defense
framework targeting compiled models toward reversing-
based model extraction attacks.
```

### cfe38cd33d273d0a

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | related_work |
| section_title | II. BACKGROUND |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 2 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Recent advancements [11], [43], [49], [50] introduce
automated scheduling and tuning to improve optimization,
reducing manual efforts.

Code Generation.

Finally, these low-level IRs are compiled
into code for different hardware targets.

Before that, the DL
compilers can also integrate with existing infrastructure like
LLVM [15] and CUDA [16] to leverage third-party toolchains
and further manipulate the generated code, which also provides
the opportunity for us to apply defense mechanisms to protect
DNN programs from reversing-based model extraction attack.

We implement FlatD on the top of LLVM to protect DNN
programs from reversing-based model extraction attacks.

Thanks to the appearance of the DL compilers, the DNN
model can be deployed on edge devices and low-power pro-
cessors [51]–[53] having limited hardware resources with low
overhead, while the popular DL frameworks like Tensorflow
[8] only provide optimization for a narrow range of server-
class GPUs.
```

### c7af5be285d241d2

| Field | Value |
|-------|-------|
| source_file | FlatD: Protecting Deep Neural Network Program.pdf |
| section | experiment |
| section_title | V. EVALUATION |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 11 |
| paper_id | FlatD: Protecting Deep Neural Network Program |

```
Specifically, for MNIST with TVM -O0, the accuracy of
BTD reduces to 50.00%; for VGG16 with TVM -O0, the
accuracy of BTD reduces to 40.63%; for the optimization
level -O3, BTD only gets 38.46% accuracy when targeting
the transformed MNIST program compared to 92.31% tar-
geting the MNIST program obfuscated by O-LLVM.

BTD
can achieve 61.54% accuracy when targeting the VGG16
program transformed by FlatD.

When facing the LibSteal
Attack, although O-LLVM has already significantly reduced
the accuracy, FlatD can still outperform it (58.34% compared
to 25.00% for MNIST TVM -O0 and 40.63% compared to
9.38% for VGG TVM -O0).

LibSteal and BTD rely heavily on the complete CFG infor-
mation to infer the operator type.

However, FlatD completely
conceals the CFG by breaking the visible control flow between
basic blocks.
```

---

## 13. [single_005_zh] 描述 PatchAgent 自动化程序修复的工作流程。它是如何识别、定位和修复 bug 的？

**Type**: `method` | **Lang**: `ZH` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.2000 | 0.4000 |
| 3 | 0.2000 | 0.4000 |
| 5 | 0.2000 | 0.4000 |
| 10 | 0.4000 | 0.6000 |
| 20 | 0.4000 | 0.6000 |

**Expected sources**: PatchAgent

### Expected Chunks (5)

### aa2dbbd3cb711194

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Automated program repair (APR) techniques, which aim
to triage and fix software bugs autonomously, have emerged
as powerful tools against vulnerable code.

Recent advance-
ments in large language models (LLMs) have further shown
promising results when applied to APR, especially on patch
generation.

However, without effective fault localization and
patch validation, APR tools specialized in patching alone can-
not handle a more practical and end-to-end setting—given a
concrete input that triggers a vulnerability, how to patch the
program without breaking existing tests?

In this paper, we introduce PATCH AGENT , a novel LLM-
based APR tool that seamlessly integrates fault localization,
patch generation, and validation within a single autonomous
agent.

PATCH AGENT employs a language server, a patch
verifier, and interaction optimization techniques to mimic
human-like reasoning during vulnerability repair.

Evaluated
on a dataset of 178 real-world vulnerabilities, PATCH AGENT
successfully repairs over 90% of the cases, outperforming
state-of-the-art APR tools where applicable.
```

### 64fa7ff620cfa9e9

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
More recently, the research on patch generator has en-
tered the era of large language models (LLMs) [23, 102, 103],
especially when LLM-based patch generators have outper-
formed conventional ones in results [102].

However, patch generation is only a midstream task in
APR.

Most patch generators require effective fault localiza-
tion (FL)—some even assume perfect FL [96, 103, 104] —to
pinpoint the buggy code snippet.

This introduces two chal-
lenges when applying end-to-end APR to real-world software:
1) FL techniques based on static analysis are prone to high
false positive rates [52], and patching correct code is not only
dangerous but also creates extra work for developers. 2) FL
techniques based on dynamic execution of proof-of-concept
(PoC) test cases face the challenge of slicing a real-world
program into a small bug-enclosing snippet.
```

### 18b869161e5d43f4

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Automated Program Repair (APR) aims to reduce the manual
effort required to fix vulnerabilities.

In this work, we focus on
4382    34th USENIX Security Symposium USENIX Association
scenarios where a proof-of-concept (PoC) input is available,
accompanied by a vulnerability description and a functional
test suite to ensure the integrity of core logic, thus eliminating
the need for static analysis.

It is important to note that not all
APR approaches adhere to this setting; many rely on static
analysis [31, 105] or exact fault localization [96, 103, 104].

Our PoC-driven approach streamlines integration with fuzzing
which provides PoC inputs, and boosts practicality especially
considering the sheer volume of bugs found in industry-scale
fuzzing campaigns like OSS-Fuzz [85] and syzkaller [91].
2.1 Workflow for PoC-driven APR
Under this setting, the APR process typically involves three
key steps, as described below:
Fault localization.
```

### fe679032b0285f24

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
In
contrast, Automated Program Repair (APR) [46]—especially
source code-based APR tools—aim to patch the buggy code
directly without distorting functionalities nor introducing un-
necessary overhead.

Effective APR tools can significantly
reduce if not eliminate manual effort in patching a security
vulnerability [40], and hence, may help shorten the time frame
between vulnerability discovery and fix rollout.

Over the past decade, APR has received much attention
from researchers [46, 58, 114], especially on patch generation
techniques.

Briefly, a patch generator takes both the buggy
code snippet and some form of bug description (a.k.a., bug
metadata) as input and produces a patch that fixes this bug
without violating generic requirements for patches (e.g., edit
distance [13], idiomaticity [87], or functional specifications
[37]).
```

### 5345ebf2356ec23a

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 2 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Broadly categorized, a patch generator
can be ① search-based [45, 80], which search for a correct
patch in a predefined patch space scoped by heuristics; ②
constraint-based [24, 31], which employ advanced constraint
solvers or program synthesis techniques to generate candidate
patches that toggle the bug-triggering condition; ③ pattern-
based [54, 97], which applies program fixed templates (a.k.a.,
transformation schema) to buggy code to generate patches,
where the templates can be either manually defined or mined
automatically; ④ learning-based [36, 111], which learns a
mapping between a buggy code snippet (with optional meta-
data) and the corresponding patch via training and applies
the learned model to generate patches.

It is different from
pattern-based APRs primarily because fix templates are never
explicitly defined in the process.

Patch validation.

Fixation [28] uses distance-bounded weak-
est preconditions to identify partially fixed exceptions in Java
programs.
```

### Retrieved Top-20

**#1** **[HIT]** — fe679032b0285f24 | PatchAgent: A Practical Program Repair Agent .pdf | p.2-2 | sec=introduction | ci=1

```
In
contrast, Automated Program Repair (APR) [46]—especially
source code-based APR tools—aim to patch the buggy code
directly without distorting functionalities nor introducing un-
necessary overhead.

Effective APR tools can significantly
reduce if not eliminate manual effort in patching a security
vulnerability [40], and hence, may help shorten the time frame
between vulnerability discovery and fix rollout.

Over the past decade, APR has received much attention
from researchers [46, 58, 114], e
```

**#2** — 6e29a5dcbe7cbef5 | PatchAgent: A Practical Program Repair Agent .pdf | p.12-12 | sec=experiment | ci=7

```
F.), Zero-Shot (Z.

S.), andPATCH A-
GENT (P.

A.).  indicates that the patch successfully fixed the
vulnerability and passed the functional test.

G #denotes a patch
that fixed the bug but failed the functional tests. #represents
a patch that failed to fix the bug.

For cases where results are
unavailable, a ’/’ is used to denote this.
strong performance across all bug types by leveraging diverse
models, excelling particularly in numeric errors and null deref-
erence with a perfect 100% success
```

**#3** — a9249393634419ba | PatchAgent: A Practical Program Repair Agent .pdf | p.3-3 | sec=introduction | ci=4

```
In this paper, we take a holistic view of APR and propose
PATCH AGENT , a push-button APR tool that handles FL,
patch generation, and patch validation in an integrated LLM
agent which manages the entire context during APR.

In par-
ticular, PATCH AGENT tackles a practical issue—patching a
vulnerable program based on a single PoC test case (i.e., a
guaranteed true positive bug report).

This is modeled after
realistic settings such as 1) a fuzzer finds a bug or 2) a commu-
nity member files a bug
```

**#4** — 719cd803c69ba024 | PatchAgent: A Practical Program Repair Agent .pdf | p.10-10 | sec=method | ci=18

```
This issue demonstrates
the lack of ability of LLMs to self-reflect and improve their
performance within multiple rounds.

We demonstrate this is-
sue in Listing 2, where the original code bug arises from mis-
handling a null pointer.
```

**#5** — c95ef81655610464 | PatchAgent: A Practical Program Repair Agent .pdf | p.15-15 | sec=discussion | ci=1

```
However, We believePATCH AGENT
can handle various types of vulnerabilities and languages.

Supporting new languages only requires replacing the LSP
(a universal protocol for 50+ languages) backend.

In fact,
the versatility of LSP is why PatchAgent uses it.

Supporting
new vulnerability types requires implementing new parsers
to purify vulnerability-specific reports.

Limited Validation.

Our patch validation method employs
security and functional tests, a widely adopted practice in
software dev
```

**#6** — e7d34f8b3ac56876 | PatchAgent: A Practical Program Repair Agent .pdf | p.5-5 | sec=related_work | ci=13

```
However, at this moment, we
are unable to compare with it because (1) Their workflow is
built for Java projects, which differs from our C/C++ targets.
(2) Currently, their project is not open-sourced.
3 Motivation: Human vs Vanilla LLM Agent
In this section, through a concrete example, we show that a
vanilla LLM agent that merely shadows the abilities of human
developers produce only substandard patches.

This hints at
the importance of (subtle) human expertise in program repair
that are yet to 
```

**#7** **[HIT]** — 5345ebf2356ec23a | PatchAgent: A Practical Program Repair Agent .pdf | p.4-4 | sec=related_work | ci=2

```
Broadly categorized, a patch generator
can be ① search-based [45, 80], which search for a correct
patch in a predefined patch space scoped by heuristics; ②
constraint-based [24, 31], which employ advanced constraint
solvers or program synthesis techniques to generate candidate
patches that toggle the bug-triggering condition; ③ pattern-
based [54, 97], which applies program fixed templates (a.k.a.,
transformation schema) to buggy code to generate patches,
where the templates can be either manual
```

**#8** — c9e6462093fe0cf1 | PatchAgent: A Practical Program Repair Agent .pdf | p.6-6 | sec=related_work | ci=17

```
In this process, the human expert primarily relies on three
abilities that are natively built into LLM: comprehending
sanitizer report (in ①,④) and code (in①,②,④), and generating
code (in ⑤), and uses three additional abilities: retrieve code
snippet (in ①, ③), locate a symbol’s definition (in ③), and
validate patch (in ⑥), to effectively complete the repair task.

Repair by a vanilla agent.

To fairly compare how an LLM
agent patches a bug with the human approach, we developed
a vanilla agent e
```

**#9** — 6c220ba91ceeaadc | PatchAgent: A Practical Program Repair Agent .pdf | p.3-3 | sec=introduction | ci=5

```
The key principle behind PATCH AGENT is to mimic how
human developers might triage and patch a bug, which typ-
ically includes a mixed ordering of actions ranging from ①
comprehending bug reports, ② comprehending code snippets,
③ resolving definitions of symbols, ④ writing a patch, and ⑤
applying the patch for validation.

As most pre-trained LLMs
only support ①, ②, and ④ natively, we additionally program
a language server (for ③), and a patch verifier (for ⑤) as abili-
ties into the LLM agent.

```

**#10** — b003f2caf8b5d5c0 | PatchAgent: A Practical Program Repair Agent .pdf | p.12-12 | sec=experiment | ci=5

```
The Union row aggregates the results from all mod-
els, showcasing PATCH AGENT ’s repair performance through
the collaborative use of multiple models.

From Table 1, we can find that PATCH AGENT delivers
Prog.

CVE/Issue Bug Type E.

F.

Z.

S.

P.
```

**#11** — bfd77dcd7068c969 | PatchAgent: A Practical Program Repair Agent .pdf | p.3-3 | sec=introduction | ci=6

```
However, merely providing the abilities to the LLM agent
does not empower the agent to “reason” like a developer
(shown in §3), which could be caused by the contrast that
bug triaging and patching usually involves heavy code analy-
sis [31, 105] while LLMs do not have robust reasoning capa-
bilities [32].

To address this issue, we introduce an assisted
reasoning middleware between the LLM agent and the APIs
for the provided abilities.

The middleware contains four mech-
anisms: ❶ report purific
```

**#12** — 6b907a0e23fccfbd | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.5-5 | sec=introduction | ci=14

```
Distribution of papers across LMs
SE activities SE tasks Total
Software development
Code Generation(37) Code Classification(5)
Code Summarization(20) Code Representation(3)
Code Search(10) Code Comment Generation(3)
Code Completion(8) Authorship Attribution(1)
Code Translation(7) Named Entity Recognition(1)
Software quality assurance Vulnerability Detection(19) Test generation(2) 21
Software maintenance
Clone Detection(15) Duplicate Bug Report Detection(1)
Program Repair(13) Bug Report Summariza
```

**#13** — bd60000d2a7a315b | PatchAgent: A Practical Program Repair Agent .pdf | p.14-14 | sec=experiment | ci=17

```
According to the OpenAI API documen-
tation [73], the training data of this model includes informa-
tion only up to December 2023.

Consequently, the patches
for these vulnerabilities are not part of gpt-4-0125-preview’s
training dataset.

This allows us to evaluate PATCH AGENT ’s
ability to repair newly discovered vulnerabilities without con-
cerns about prior knowledge or memorization of the patches.

The results are summarized in Table 4, demonstrating that
PATCH AGENT successfully repaired 8
```

**#14** — 056048242bbcea77 | PatchAgent: A Practical Program Repair Agent .pdf | p.13-13 | sec=experiment | ci=11

```
In this study, we systematically deactivated each
optimization within PATCH AGENT , focusing on report purifi-
cation (RP), chain compression (CC), auto correction (AC)
and counterexample feedback (CF).

We sampled 75 cases,
primarily due to the high cost associated with running the
full dataset.

Running these 75 cases alone costs over $1500,
highlighting the financial constraints.

This approach is also
consistent with previous best practices [110].

Furthermore, we
ensure that the distributio
```

**#15** — 64371491fcf896dc | Pitfalls in Language Models for Code Intelligence: A Taxonom | p.6-7 | sec=method | ci=3

```
In software defect prediction, where
defective modules are scarce compared with non-defective cases in real-world environments [81, 189].

Similarly,
bug report classification suffers from underrepresentation of the minority bug class [81].

In Code Summarization,
the absence of low-frequency identifiers in the training set can lead to a lack of relevant knowledge [84], which
may result in hallucinations or be exploited to cause harm.

Additionally, the skew in programming languages, the
uneven 
```

**#16** — eb4bffe2bf985e8a | PatchAgent: A Practical Program Repair Agent .pdf | p.10-10 | sec=method | ci=20

```
The first two patches
address the bug by adding checks to ensure t->text is not
null before calling gf_strdup.

The first patch uses an if-else
structure: if t->text is not null, it duplicates the text; other-
wise, it setsname[i] to NULL.

The second patch uses a ternary
operator to achieve the same logic.

Both patches set name[i]
to NULL, which poses a potential issue since name[i] is re-
quired to remain non-null in other parts of the program.

This
is evident in the second code snippet in L
```

**#17** — 2efd03f1d740e834 | LLMs: Understanding Code Syntax and Semantics for Code.pdf | p.2-2 | sec=method | ci=1

```
Concretely, we used ChatGPT playground [12] with 𝑡𝑒𝑚𝑝𝑒𝑟𝑎𝑡𝑢𝑟𝑒
of value 0 to perform the conversation in May, 2023.

As shown
in Figure 1, there is a buggy function “bucketsort” obtained from
QuixBugs [13].

The Bucketsort algorithm requires splitting the ar-
ray (i.e., “arr” in this function) into several buckets (i.e., “counts”)
and then sorting each bucket individually.

Hence, we can find that
the correct version to fix this bug function is to replace the variable
“arr” in the second loop with
```

**#18** — 9a5daeb32b75f791 | PatchAgent: A Practical Program Repair Agent .pdf | p.13-13 | sec=experiment | ci=14

```
Turning off chain compression (CC)
resulted in a drop in the repair ratio to 62.67%, with a no-
table impact on Spatial errors, where the ratio decreased from
72.73% to 60.00%.

Disabling auto correction (AC) caused
significant degradation, as without this optimization, we ob-
served that the LLM even struggled to generate correctly
formatted patches.
7.4 Repair Unseen Vulnerability
To assess PATCH AGENT ’s capability in repairing vulnerabili-
ties that LLMs have never encountered before, we col
```

**#19** — 7739b87332e3f7f6 | PatchAgent: A Practical Program Repair Agent .pdf | p.3-3 | sec=introduction | ci=8

```
To demonstrate the effectiveness of PATCH AGENT in re-
pairing real-world vulnerabilities, we created a dataset com-
prising 178 cases sourced from OSS-Fuzz [85], Huntr [34]
and ExtractFix [24] on 9 distinct bug types: stack overflow,
heap overflow, integer overflow, use-after-free, double free,
global overflow, divide by zero, invalid free, and null deref-
erence.

PATCH AGENT is built upon the GPT-4 series from
OpenAI [72] and the Claude-3 series from Anthropic [10].

PATCH AGENT exhibited rem
```

**#20** — e57eb7f98caccd8e | PatchAgent: A Practical Program Repair Agent .pdf | p.2-3 | sec=introduction | ci=3

```
Previous studies
have shown that the execute traces of bug-triggering inputs are
typically excessively long [11, 77], ruling out straightforward
adoption of program slicing techniques [39, 59] .

The downstream task of patch generation is patch vali-
dation, which is often left to either manual review [100] or
automated testing [78] where in the latter case a patch is
considered “correct” when all the tests pass, including the
mitigation of the PoC, if exists.

While this is arguably the
state-o
```

### Missed Chunks (3 — expected but NOT in top-20)

### aa2dbbd3cb711194

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Automated program repair (APR) techniques, which aim
to triage and fix software bugs autonomously, have emerged
as powerful tools against vulnerable code.

Recent advance-
ments in large language models (LLMs) have further shown
promising results when applied to APR, especially on patch
generation.

However, without effective fault localization and
patch validation, APR tools specialized in patching alone can-
not handle a more practical and end-to-end setting—given a
concrete input that triggers a vulnerability, how to patch the
program without breaking existing tests?

In this paper, we introduce PATCH AGENT , a novel LLM-
based APR tool that seamlessly integrates fault localization,
patch generation, and validation within a single autonomous
agent.

PATCH AGENT employs a language server, a patch
verifier, and interaction optimization techniques to mimic
human-like reasoning during vulnerability repair.

Evaluated
on a dataset of 178 real-world vulnerabilities, PATCH AGENT
successfully repairs over 90% of the cases, outperforming
state-of-the-art APR tools where applicable.
```

### 64fa7ff620cfa9e9

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
More recently, the research on patch generator has en-
tered the era of large language models (LLMs) [23, 102, 103],
especially when LLM-based patch generators have outper-
formed conventional ones in results [102].

However, patch generation is only a midstream task in
APR.

Most patch generators require effective fault localiza-
tion (FL)—some even assume perfect FL [96, 103, 104] —to
pinpoint the buggy code snippet.

This introduces two chal-
lenges when applying end-to-end APR to real-world software:
1) FL techniques based on static analysis are prone to high
false positive rates [52], and patching correct code is not only
dangerous but also creates extra work for developers. 2) FL
techniques based on dynamic execution of proof-of-concept
(PoC) test cases face the challenge of slicing a real-world
program into a small bug-enclosing snippet.
```

### 18b869161e5d43f4

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Automated Program Repair (APR) aims to reduce the manual
effort required to fix vulnerabilities.

In this work, we focus on
4382    34th USENIX Security Symposium USENIX Association
scenarios where a proof-of-concept (PoC) input is available,
accompanied by a vulnerability description and a functional
test suite to ensure the integrity of core logic, thus eliminating
the need for static analysis.

It is important to note that not all
APR approaches adhere to this setting; many rely on static
analysis [31, 105] or exact fault localization [96, 103, 104].

Our PoC-driven approach streamlines integration with fuzzing
which provides PoC inputs, and boosts practicality especially
considering the sheer volume of bugs found in industry-scale
fuzzing campaigns like OSS-Fuzz [85] and syzkaller [91].
2.1 Workflow for PoC-driven APR
Under this setting, the APR process typically involves three
key steps, as described below:
Fault localization.
```

### False Positives (18 — in top-20 but NOT expected)

### 6e29a5dcbe7cbef5

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 7 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
F.), Zero-Shot (Z.

S.), andPATCH A-
GENT (P.

A.).  indicates that the patch successfully fixed the
vulnerability and passed the functional test.

G #denotes a patch
that fixed the bug but failed the functional tests. #represents
a patch that failed to fix the bug.

For cases where results are
unavailable, a ’/’ is used to denote this.
strong performance across all bug types by leveraging diverse
models, excelling particularly in numeric errors and null deref-
erence with a perfect 100% success rate.

For temporal and
spatial errors, the success rates are slightly lower, at 86.96%
and 91.20%, respectively.

These outcomes are consistent with
previous studies [24,31,33,105], which suggest that most null
dereference and numeric errors can often be resolved with a
simple if-check, whereas temporal and spatial bugs typically
require more complex solutions.
```

### a9249393634419ba

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 4 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
In this paper, we take a holistic view of APR and propose
PATCH AGENT , a push-button APR tool that handles FL,
patch generation, and patch validation in an integrated LLM
agent which manages the entire context during APR.

In par-
ticular, PATCH AGENT tackles a practical issue—patching a
vulnerable program based on a single PoC test case (i.e., a
guaranteed true positive bug report).

This is modeled after
realistic settings such as 1) a fuzzer finds a bug or 2) a commu-
nity member files a bug report with a PoC test case included.

More specifically, PATCH AGENT targets large and complex
software with source code available and requires that:
• at least one PoC test case to trigger the vulnerability
• a (textual) description of the vulnerability triggered
• a functional test suite to validate integrity of core logic
Static analysis reports, on the other hand, are not required by
PATCH AGENT although they can be integrated as additional
metadata on the vulnerability triggered.
```

### 719cd803c69ba024

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | method |
| section_title | 4.1 Framework |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 18 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
This issue demonstrates
the lack of ability of LLMs to self-reflect and improve their
performance within multiple rounds.

We demonstrate this is-
sue in Listing 2, where the original code bug arises from mis-
handling a null pointer.
```

### c95ef81655610464

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | discussion |
| section_title | 8 Discussion and Limitation |
| page_start | 15 |
| page_end | 15 |
| chunk_index | 1 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
However, We believePATCH AGENT
can handle various types of vulnerabilities and languages.

Supporting new languages only requires replacing the LSP
(a universal protocol for 50+ languages) backend.

In fact,
the versatility of LSP is why PatchAgent uses it.

Supporting
new vulnerability types requires implementing new parsers
to purify vulnerability-specific reports.

Limited Validation.

Our patch validation method employs
security and functional tests, a widely adopted practice in
software development, such as github CI [25].

While this
method is effective and scalable for addressing many vul-
nerability repair scenarios, it has notable limitations.

From
a security standpoint, prior works [100] have revealed that
approximately 5% of security patches written by human in the
Linux kernel may not fully mitigate the vulnerabilities they
aim to address, which suggests that patches generated by AI
agents may also contain similar issues.

Regarding functional-
ity, some projects often update or expand their test cases along-
side patches, which hints that simply using existing functional
tests may not be sufficient.
```

### e7d34f8b3ac56876

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 13 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
However, at this moment, we
are unable to compare with it because (1) Their workflow is
built for Java projects, which differs from our C/C++ targets.
(2) Currently, their project is not open-sourced.
3 Motivation: Human vs Vanilla LLM Agent
In this section, through a concrete example, we show that a
vanilla LLM agent that merely shadows the abilities of human
developers produce only substandard patches.

This hints at
the importance of (subtle) human expertise in program repair
that are yet to be provisioned into the vanilla LLM agent.
3.1 Motivating Example
Issue-33078.

Listing 1 presents an out-of-bound (OOB) ac-
cess bug that causes issue-33078 [35], which was discovered
by OSS-Fuzz [85].

The OOB access is flagged by Address-
Sanitizer [84] at line 22 in function Compile_BlockStat
when the OOB pointer opinfo is dereferenced. opinfo is
produced in function GetOpInfo, which fails to validate the
opcode properly—the root cause.
```

### c9e6462093fe0cf1

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 17 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
In this process, the human expert primarily relies on three
abilities that are natively built into LLM: comprehending
sanitizer report (in ①,④) and code (in①,②,④), and generating
code (in ⑤), and uses three additional abilities: retrieve code
snippet (in ①, ③), locate a symbol’s definition (in ③), and
validate patch (in ⑥), to effectively complete the repair task.

Repair by a vanilla agent.

To fairly compare how an LLM
agent patches a bug with the human approach, we developed
a vanilla agent equipped with the three additional abilities—
retrieving code snippets by range, locating a symbol’s defini-
tion, and validating a patch—by coupling a language server
and patch verifier to the agent (see §4.1 for details).

One sample run of the repair process by the agent is shown
on the left side of Figure 1.

The agent identifies that the over-
flow occurs at line 22 in m3_compile.c but attempts to view
the surrounding code with a very narrow range.
```

### 6c220ba91ceeaadc

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 5 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
The key principle behind PATCH AGENT is to mimic how
human developers might triage and patch a bug, which typ-
ically includes a mixed ordering of actions ranging from ①
comprehending bug reports, ② comprehending code snippets,
③ resolving definitions of symbols, ④ writing a patch, and ⑤
applying the patch for validation.

As most pre-trained LLMs
only support ①, ②, and ④ natively, we additionally program
a language server (for ③), and a patch verifier (for ⑤) as abili-
ties into the LLM agent.

Note that we do not claim generality
nor optimality on the set of abilities provided in PATCH A-
GENT as they are based on self-reflection of how members in
the author team patch bugs and we look forward to seeing a
more principled approach in devising the set of abilities.
```

### b003f2caf8b5d5c0

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 5 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
The Union row aggregates the results from all mod-
els, showcasing PATCH AGENT ’s repair performance through
the collaborative use of multiple models.

From Table 1, we can find that PATCH AGENT delivers
Prog.

CVE/Issue Bug Type E.

F.

Z.

S.

P.
```

### bfd77dcd7068c969

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
However, merely providing the abilities to the LLM agent
does not empower the agent to “reason” like a developer
(shown in §3), which could be caused by the contrast that
bug triaging and patching usually involves heavy code analy-
sis [31, 105] while LLMs do not have robust reasoning capa-
bilities [32].

To address this issue, we introduce an assisted
reasoning middleware between the LLM agent and the APIs
for the provided abilities.

The middleware contains four mech-
anisms: ❶ report purification to facilitate an LLM in interpret-
ing bug reports;❷ chain compression to shorten the reasoning
chain of the LLM agent; ❸ auto correction to correct errors
that occur during the interaction between LLM and ability
APIs; and ❹ counterexample feedback to encourage the LLM
agent to generate diversified patches.

These optimizations
bring remarkable improvements as shown in §7.3.
```

### 6b907a0e23fccfbd

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 14 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
Distribution of papers across LMs
SE activities SE tasks Total
Software development
Code Generation(37) Code Classification(5)
Code Summarization(20) Code Representation(3)
Code Search(10) Code Comment Generation(3)
Code Completion(8) Authorship Attribution(1)
Code Translation(7) Named Entity Recognition(1)
Software quality assurance Vulnerability Detection(19) Test generation(2) 21
Software maintenance
Clone Detection(15) Duplicate Bug Report Detection(1)
Program Repair(13) Bug Report Summarization(1)
Defect Prediction(6) Bug-Fix Commit Identification(1)
Commit Message Generation(3) Bug Report Classification(1)
Table 1.

Distribution of papers across SE activities
of software engineering tasks addressed in the collected papers.

Code generation, code summarization, code
search, vulnerability detection, and clone detection emerge as the primary scenarios for investigating LM4Code
pitfalls, encompassing both classification and generation tasks.

Overall, our analysis underscores that LM4Code has been an increasing area of interest.
```

### bd60000d2a7a315b

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 14 |
| page_end | 14 |
| chunk_index | 17 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
According to the OpenAI API documen-
tation [73], the training data of this model includes informa-
tion only up to December 2023.

Consequently, the patches
for these vulnerabilities are not part of gpt-4-0125-preview’s
training dataset.

This allows us to evaluate PATCH AGENT ’s
ability to repair newly discovered vulnerabilities without con-
cerns about prior knowledge or memorization of the patches.

The results are summarized in Table 4, demonstrating that
PATCH AGENT successfully repaired 8 out of 10 previously
unseen vulnerabilities.

These findings align with the effec-
tiveness evaluation discussed in §7.2.

We note thatPATCH A-
GENT failed to repair CVE-2024-34246, a null dereference
bug.

Given PATCH AGENT ’s otherwise perfect performance in
repairing null dereference bugs during the effectiveness eval-
uation, we will conduct an in-depth analysis of this failure in
§A.1.

For another null dereference bug, PATCH AGENT effec-
tively repaired it by inserting a null check.
```

### 056048242bbcea77

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 11 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
In this study, we systematically deactivated each
optimization within PATCH AGENT , focusing on report purifi-
cation (RP), chain compression (CC), auto correction (AC)
and counterexample feedback (CF).

We sampled 75 cases,
primarily due to the high cost associated with running the
full dataset.

Running these 75 cases alone costs over $1500,
highlighting the financial constraints.

This approach is also
consistent with previous best practices [110].

Furthermore, we
ensure that the distribution of vulnerability types in the sam-
CVE/Issue Project Bug Type Fix Date P.
```

### 64371491fcf896dc

| Field | Value |
|-------|-------|
| source_file | Pitfalls in Language Models for Code Intelligence: A Taxonomy and.pdf |
| section | method |
| section_title | System design and learning (43) |
| page_start | 6 |
| page_end | 7 |
| chunk_index | 3 |
| paper_id | Pitfalls in Language Models for Code Intelligence: A Taxonomy and |

```
In software defect prediction, where
defective modules are scarce compared with non-defective cases in real-world environments [81, 189].

Similarly,
bug report classification suffers from underrepresentation of the minority bug class [81].

In Code Summarization,
the absence of low-frequency identifiers in the training set can lead to a lack of relevant knowledge [84], which
may result in hallucinations or be exploited to cause harm.

Additionally, the skew in programming languages, the
uneven granularity of code, and the absence of sophisticated features within training datasets can also impact
large models’ comprehension and generation capabilities in relevant tasks [13].

ACM Trans.

Softw.

Eng.

Methodol.
```

### eb4bffe2bf985e8a

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | method |
| section_title | 4.1 Framework |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 20 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
The first two patches
address the bug by adding checks to ensure t->text is not
null before calling gf_strdup.

The first patch uses an if-else
structure: if t->text is not null, it duplicates the text; other-
wise, it setsname[i] to NULL.

The second patch uses a ternary
operator to achieve the same logic.

Both patches set name[i]
to NULL, which poses a potential issue since name[i] is re-
quired to remain non-null in other parts of the program.

This
is evident in the second code snippet in Listing 2, where
name[i] is passed directly to the strlen function without
any null checks.

Similar patterns are observed throughout the
codebase, suggesting that numerous null checks would need
to be added to ensure the program’s correctness if we were to
follow the logic of the first two patches.

This could make the
patch overly complex and introduce redundancy.
```

### 2efd03f1d740e834

| Field | Value |
|-------|-------|
| source_file | LLMs: Understanding Code Syntax and Semantics for Code.pdf |
| section | method |
| section_title | 2 MOTIVATION |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | LLMs: Understanding Code Syntax and Semantics for Code |

```
Concretely, we used ChatGPT playground [12] with 𝑡𝑒𝑚𝑝𝑒𝑟𝑎𝑡𝑢𝑟𝑒
of value 0 to perform the conversation in May, 2023.

As shown
in Figure 1, there is a buggy function “bucketsort” obtained from
QuixBugs [13].

The Bucketsort algorithm requires splitting the ar-
ray (i.e., “arr” in this function) into several buckets (i.e., “counts”)
and then sorting each bucket individually.

Hence, we can find that
the correct version to fix this bug function is to replace the variable
“arr” in the second loop with the variable “counts”.

According to an
analysis from Sobania et al. [68], ChatGPT can automatically fix this
bug as shown in Figure 1.

Through this example, it seems that Chat-
GPT correctly comprehends this function semantics and finishes a
correct repair.

However, a simple mutation while maintaining the
original program semantics can lead ChatGPT to produce incorrect
results.
```

### 9a5daeb32b75f791

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 14 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Turning off chain compression (CC)
resulted in a drop in the repair ratio to 62.67%, with a no-
table impact on Spatial errors, where the ratio decreased from
72.73% to 60.00%.

Disabling auto correction (AC) caused
significant degradation, as without this optimization, we ob-
served that the LLM even struggled to generate correctly
formatted patches.
7.4 Repair Unseen Vulnerability
To assess PATCH AGENT ’s capability in repairing vulnerabili-
ties that LLMs have never encountered before, we collected
10 newly discovered vulnerabilities spanning 5 different bug
types across 5 distinct projects: (1) c-blosc2 [2], a fast bi-
nary compressor; (2) GPAC [27], a multimedia framework; (3)
libxml2 [9], an XML toolkit library; (4) wasm3 [3], a We-
bAssembly interpreter; and (5) vim [95], an improved version
of the UNIX editor Vi.
```

### 7739b87332e3f7f6

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 8 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
To demonstrate the effectiveness of PATCH AGENT in re-
pairing real-world vulnerabilities, we created a dataset com-
prising 178 cases sourced from OSS-Fuzz [85], Huntr [34]
and ExtractFix [24] on 9 distinct bug types: stack overflow,
heap overflow, integer overflow, use-after-free, double free,
global overflow, divide by zero, invalid free, and null deref-
erence.

PATCH AGENT is built upon the GPT-4 series from
OpenAI [72] and the Claude-3 series from Anthropic [10].

PATCH AGENT exhibited remarkable performance on the
dataset, successfully repairing 92.13% vulnerabilities.

Each
repairing solution passed both the security tests and func-
tional tests.

We also show that PATCH AGENT outperforms
two state-of-the-art APR methods (ExtractFix [24] and Pearce
et al. [78]) that are closely aligned with PATCH AGENT in the
overall goal.

Contributions.
```

### e57eb7f98caccd8e

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 3 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Previous studies
have shown that the execute traces of bug-triggering inputs are
typically excessively long [11, 77], ruling out straightforward
adoption of program slicing techniques [39, 59] .

The downstream task of patch generation is patch vali-
dation, which is often left to either manual review [100] or
automated testing [78] where in the latter case a patch is
considered “correct” when all the tests pass, including the
mitigation of the PoC, if exists.

While this is arguably the
state-of-the-practice [28, 44, 100] treating patch generation
USENIX Association 34th USENIX Security Symposium    4381
and validation as separate steps forgoes the opportunity to
harvest useful information in partially correct patch and the
reasons of failure, which could be used as a feedback for the
next round of patch generation.
```

---

## 14. [cross_001_zh] 比较 DnD、BTD 和 NeuroDeX 三种 DNN 反编译器的核心方法。它们共同使用了什么技术？各自的策略有何不同？

**Type**: `comparison` | **Lang**: `ZH` | **Expected chunks**: 9

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.2222 | 0.2222 |
| 10 | 0.2222 | 0.2222 |
| 20 | 0.2222 | 0.3333 |

**Expected sources**: DnD, all-Decompiling+x86, NeuroDeX

### Expected Chunks (9)

### 9bdf3eaa138e61a4

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 9 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
To check the property (iii), after reaching the DNN oper-
ator’s most outer loop’s exit point (e.g., Line 2 in Figure 3b),
DND inspects each IV’s corresponding register to check if
its register is updated with a constant (i.e., step size).

At last,
DNDconsidersanIVcandidateasanIVwhenitsatisﬁesboth
properties (ii) and (iii) (Line 18).

Finally,DND recovers IVs’ initial values, step sizes, and
loopcounts(Line19).

Inparticular,loopcountsarecomputed
from initial values, step sizes, and the collected loop exit con-
ditions.

For example, the initial value, step size and loop exit
conditions ofi in Figure 3b are 0, 1, andi<2, respectively.

Then, the loop count is derived by inquiring the solver with
these information.
```

### 20ac523f29224b53

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 6 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the break edges (denoting the edges in CFG that
jump out of the current loop).
```

### 16dc5ceb2dad79e0

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how to identify IVs using the
aforementioned three properties by symbolically executing
each DNN operator from its entry point to its exit point (Line
2,16-17).

Leveragingtheproperty(i), DND symbolizesevery
general register initialized by a constant in the loop’s entry
block (Line 10-12).
```

### c54826ab77483b01

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 4 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In addition to
simple arithmetic operators, BiasAdd involves biasB, as extra
parameters.

Type IV operators require both parameters and di-
mensions.

These operators form most DNN models.

Sec. 7.1
empirically demonstrates “comprehensivness” of our study.

BTD recovers dimensions/parameters of all DNN opera-
tors used by CV models in ONNX Zoo (see Sec. 7.1).

Due to
limited space, Sec. 4.3 only discusses decompiling the most
challenging operator, Conv.

The core techniques explained in
Sec. 4.3 are utilized to decompile other DNN operators.

How-
ever, other operators may use different (but simpler) patterns.

Appendix C lists other operator patterns.

We further discuss
the extensibility of BTD in Sec. 7.3.

Disassembling and Function Recovery.

BTD targets 64-bit
x86 executables.

Cross-platform support is discussed in Sec. 8.

BTD supports stripped executables without symbol or debug
information.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### 2f2cb9ddcb1914fa

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute recovery, where it leverages dynamic anal-
ysis and code semantic understanding from LLMs to support
compatibility with various types of models.

Dynamic analysis
aims to monitor the runtime information of operator functions.

Dynamic analysis in NeuroDeX requires only trivial input that
satisfies the expected input format.

This is due to the fact
that any input can guarantee full coverage of the whole DNN
model, and the mathematical dependencies of intermediate
features are fixed.
```

### 03e5ee11ed5284cb

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | method |
| section_title | III. APPROACH |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from DNN exe-
cutables using ghidra.

Inspired by previous works [6], [9], NeuroDeX can identify
the dimensions of operator parameters from disassembled
code in TVM compiler.

NeuroDeX further expands on their
methods, NeuroDeX also extracts the types of operator param-
eters and recover the optimized parameters’ dimensions.
```

### dd6347b07eaca9c2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 11 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The threat model used in our study is consistent with previ-
ous works [7]–[10] and is generally common and practical
in real-world scenarios.

The design of NeuroDeX aims to
highlight security risks of DNN executables and promote the
safe use of DL compilers.

Operator Recovery
DNN 
Executable
Operator Function 
Extraction
Dynamic 
Analysis 
LLM
Operator Type 
Recognition
Operator Attribute 
Recovery
Computational 
Graph Recovery
Model Weights 
Recovery
Model Reconstruction
High-level 
Model
Fig. 3: Workflow of NeuroDeX
```

### Retrieved Top-20

**#1** — 5f882e74e4b278f2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-8 | sec=experiment | ci=3

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive 
```

**#2** — 74238bd6bc7e40c9 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=3

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of Neuro
```

**#3** — 8b2f1dfb72bfacf4 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.2-2 | sec=related_work | ci=2

```
The general workflow of a
DL compiler involves three steps:frontend processing, which
converts general model representations, such as ONNX [11],
into computational graphs supported by the compiler’s fron-
tend;compilation optimization, applying various optimization
techniques, including high-level optimizations like operator
fusion and constant folding, and low-level optimizations such
TABLE I: Comparison with Existing DNN Decompilers
Works Optimization Cross Arch Quantization
Libsteal [6]# # #

```

**#4** **[HIT]** — 2f2cb9ddcb1914fa | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.4-4 | sec=method | ci=0

```
As shown in Figure 3, NeuroDeX is designed as an universal
pipeline for different types of DNN executables, enabling end-
to-end recovery of DNN executables into high-level models.

Specifically, NeuroDeX first extracts operator function infor-
mation, such as disassembled code, decompiled code and
parameter dimensions from DNN executables.

In this stage,
NeuroDeX utilizes Ghidra [19], a general-purpose decompiler.

Secondly, NeuroDeX completes operator type recognition and
operator attribute r
```

**#5** **[HIT]** — 03e5ee11ed5284cb | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.4-4 | sec=method | ci=1

```
LLMs can understand the mathematical
semantics of different operators in decompiled code without
relying on prior knowledge like compiler versions or training
data.

Finally, NeuroDeX performs model reconstruction by
computational graph and model weights recovery, recovering
high-level models.

Next, we will sequentially introduce the
components of NeuroDeX.

A.

Operator Function Extraction
NeuroDeX first collects operator function information in-
cluding disassembled and decompiled code from D
```

**#6** — d0a14750cdbd2932 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.8-9 | sec=experiment | ci=5

```
We employ 100 inputs
for the Emotion and SuperRes models and 500 inputs for all
TABLE IV: Comparison of TRA between BTD and NeuroDeX (all value in %)
Model
EfficientNet Inceptionv1 MobileNetv2 ResNet18 ShuffleNetv2 VGG16
BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX
TVM v0.7 O0 72.48 97.96 97.1 100 80.47 100 76.56 100 70.05 98.87 84.85 100
TVM v0.8 O0 39.91 99.28 87.85 100 66.85 100 46.88 100 49.83 98.97 63.64 100
TVM v0.9dev O0 40.7 100 86.06 100 64.32 100 34.92 
```

**#7** — 2eda3aacde4e38c8 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.2-2 | sec=related_work | ci=4

```
However, each of these methods has its limitations.

We summarize the previous works and compare them with
NeuroDeX in Table I.

Libsteal cannot decompile standalone
DNN executables and is unable to handle compilation opti-
mizations.

The accuracy of the models recovered by Libsteal
is relatively low.

The work by Shi et al. only supports x86
architecture and cannot recover models with high accuracy.

DND and Neuroscope do not effectively handle compila-
tion optimizations.

Although BTD consid
```

**#8** — e0b75a7c3a534224 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.10-10 | sec=results | ci=6

```
Moreover, it is noteworthy that NeuroDeX’s approach does
not involve heavy analysis constrained by hardware resources.

In contrast, the methods utilized by BTD demand considerable
memory and CPU resources, which can lead to performance
degradation on consumer-grade devices.

Answer to RQ2:NeuroDeX can decompile DNN executa-
bles with a shorter time overhead than SOTA methods and
NeuroDeX does not rely heavily on hardware resources.

C.

RQ3: Comprehensiveness
To answer RQ3, we aim to evaluate N
```

**#9** — 6f0f7d6275f908ad | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-10 | sec=results | ci=4

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O
```

**#10** — c88a1a6168cbec88 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.10-10 | sec=results | ci=5

```
The overhead of BTD and
NeuroDeX is shown in Table VI.

For TVM O0, TVM O3 and GLOW, the average time spent
by BTD is about6.79times,2.77times, and12.76times
that of NeuroDeX respectively.

The main time overhead for
NeuroDeX comes from network request to LLM and dynamic
memory monitor.

The time of LLM requests can fluctuate
due to network conditions.

However, in our implementation,
requests to LLM are executed through a single thread.

Using
a multi-threaded approach could easily optimize the
```

**#11** — de39e46413babeba | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-1 | sec=abstract | ci=1

```
In this paper, we present NeuroDeX to unlock diverse sup-
port in decompiling DNN executables.

NeuroDeX leverages the
semantic understanding capabilities of LLMs along with dynamic
analysis to accurately and efficiently perform operator type
recognition, operator attribute recovery and model reconstruc-
tion.

NeuroDeX can recover DNN executables into high-level
models towards compilation optimizations, different architectures
and quantized compiled models.

We conduct experiments on
96 DNN exe
```

**#12** — cd7444c98cc84207 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.12-12 | sec=conclusion | ci=0

```
In this work, we design NeuroDeX to provide diverse
support in decompiling DNN executables. NeuroDeX recovers
DNN executables back into high-level models through oper-
ator type recognition, operator attribute recovery and model
reconstruction. NeuroDeX leverages the semantic understand-
ing capabilities of LLMs along with dynamic analysis to
construct a comprehensive and robust decompilation pipeline.
Our evaluations demonstrate that NeuroDeX can successfully
decompile DNN executables across di
```

**#13** — 71c795d9bc036eb2 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=0

```
In this section, we show the experimental results to answer
the research questions.

A.

RQ1: Correctness
To answer RQ1, we compare NeuroDeX with the SOTA
method BTD, using the models involved in BTD experiments
to demonstrate the performance of NeuroDeX.

TABLE V: TRA and THA of BTD (consistent with Table IV)
on Different Compiler Versions (all value in %)
Metric
TVM O0 TVM O3 GLOW
v0.7 v0.8 v0.9dev v0.7 v0.8 v0.9dev 2020 2021 2022
TRA Avg 80.4 64.43 61.31 70.33 57.67 54.86 72.57 79.36 78.99
TH
```

**#14** — 2c7d44730d74e147 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-3 | sec=related_work | ci=10

```
For
C3:NeuroDeX specifically adapts the model reconstruction
method to convert integer domain weights back to float do-
main.

NeuroDeX employs a learning-based weights recovery
approach that requires only a small amount of training data to
recover functionally very similar models.

D.

Threat Model
NeuroDeX is designed towards DNN executables deployed
on edge devices, where NeuroDeX can access DNN exe-
cutables compiled by DL compilers and extract the complete
executables.

DNN executables are 
```

**#15** — cba88a60112f4554 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.9-9 | sec=results | ci=1

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the
```

**#16** — dbc57fec26a36a2a | Hardening Deep Neural Network Binaries against ReverseEngine | p.11-11 | sec=experiment | ci=16

```
The majority of additional memory comes from the increase of
workspace size, with an overhead of 2.89% - 42.15%.
6.3 Resilience against Existing Reverse
Engineering Attacks
To compare the effectiveness of general obfuscators andNeuroShield
on DNN binaries, we evaluate them against two state-of-the-art
DNN decompilers, DnD and BTD.

Note that the BTD attack is the
extended version we mentioned in Section 3.2.

Table 5 reports the
attack time and the number of operator functions reconstructed by
D
```

**#17** — 09693a185e42519d | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.3-3 | sec=related_work | ci=6

```
Libsteal and Shi et al.’s work
do not guarantee sufficient accuracy; DND relies on symbolic
execution, which incurs significant overhead and limits the size
of supported models; Neuroscope only supports 12 DNN oper-
ators.

More importantly, these methods fail to provide adequate
support for fused operators from compilation optimizations.

Observation2:BTD considers the impact of compilation
optimizations and supports a wider range of operator types.

However, BTD trains machine learning model f
```

**#18** — c679095422fa27bc | Hardening Deep Neural Network Binaries against ReverseEngine | p.11-11 | sec=experiment | ci=17

```
As BTD is
based on dynamic analysis, we only evaluate the two models under
Loki’s obfuscation for BTD.

The upper part of Table 5 presents the attack results for DnD.

Among general obfuscators, Fusor is ineffective against DnD with
100% operator functions semantics being recovered.

The reason is
that the inserted opaque predicates do not change the overall nested
loop structures, which is the fundamental information leveraged
by DnD to infer the operator types and attributes.

The Other three

```

**#19** — 75400e9cae287630 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.1-2 | sec=introduction | ci=3

```
NeuroDeX is evaluated on 88 non-quantized DNN exe-
cutables and NeuroDeX can accurately recover them into
nearly identical high-level models.

NeuroDeX adapts for the
different compiler versions, accommodates a wider range of
models, and supports different architectures.

The operator type
recognition accuracy for all TVM executables and GLOW
executables reaches 99.22% and 97.62% respectively.

The
operator attribute recovery accuracy is nearly 100%.

Neu-
roDeX incorporates robust error fix str
```

**#20** — 176226c123544195 | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neur | p.11-11 | sec=results | ci=13

```
The queries for recovered
model are more likely to be classified into different categories
than original high-level models.

This is due to the character-
istics of the global scale method and the inevitable precision
loss during conversion between int and float domains, rather
than design flaws in NeuroDeX.

Answer to RQ3:We evaluate NeuroDeX on a wider range
of models and aarch64 architecture.

Results illustrates Neu-
roDeX’s adaptability to various models and different ar-
chitectures; Neuro
```

### Missed Chunks (7 — expected but NOT in top-20)

### 9bdf3eaa138e61a4

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 9 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
To check the property (iii), after reaching the DNN oper-
ator’s most outer loop’s exit point (e.g., Line 2 in Figure 3b),
DND inspects each IV’s corresponding register to check if
its register is updated with a constant (i.e., step size).

At last,
DNDconsidersanIVcandidateasanIVwhenitsatisﬁesboth
properties (ii) and (iii) (Line 18).

Finally,DND recovers IVs’ initial values, step sizes, and
loopcounts(Line19).

Inparticular,loopcountsarecomputed
from initial values, step sizes, and the collected loop exit con-
ditions.

For example, the initial value, step size and loop exit
conditions ofi in Figure 3b are 0, 1, andi<2, respectively.

Then, the loop count is derived by inquiring the solver with
these information.
```

### 20ac523f29224b53

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 6 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
For example, the
i, j, u, v in Figure 3b are the IVs.

The output of this analy-
sis includes IVs, their initial values, their step sizes (i.e., the
increment constant) and their loop count (i.e., how many iter-
ations the loop is supposed to be repeatedly executed).

Then,
DND will use these IVs information to extract the symbolic
expressions in Section 5.2.2.

To do so,DND ﬁrst recovers loops’ structural information
in each DNN operator, including the entry points, the exit
points and the break edges (denoting the edges in CFG that
jump out of the current loop).
```

### 16dc5ceb2dad79e0

| Field | Value |
|-------|-------|
| source_file | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler.pdf |
| section | method |
| section_title | 5 System Design |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | DnD+A+Cross-Architecture+Deep+Neural+Network+Decompiler |

```
Then, DND leverages the IVs’
properties in the binary program that we observe to recover
the IVs, which are the following: (i) IVs are initialized with
constants and loaded into general registers in the loop’s entry
block (e.g.,. = 0in Line 2 in Figure 3b); (ii) IVs determine
the conditions of the break edges; (iii) a constant increments
the value of an IV (i.e., step size) within the execution of the
loop’s body (e.g., the step size is 1 for Line 2 in Figure 3b).

Let us show in Algorithm 1 how to identify IVs using the
aforementioned three properties by symbolically executing
each DNN operator from its entry point to its exit point (Line
2,16-17).

Leveragingtheproperty(i), DND symbolizesevery
general register initialized by a constant in the loop’s entry
block (Line 10-12).
```

### c54826ab77483b01

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 4 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
In addition to
simple arithmetic operators, BiasAdd involves biasB, as extra
parameters.

Type IV operators require both parameters and di-
mensions.

These operators form most DNN models.

Sec. 7.1
empirically demonstrates “comprehensivness” of our study.

BTD recovers dimensions/parameters of all DNN opera-
tors used by CV models in ONNX Zoo (see Sec. 7.1).

Due to
limited space, Sec. 4.3 only discusses decompiling the most
challenging operator, Conv.

The core techniques explained in
Sec. 4.3 are utilized to decompile other DNN operators.

How-
ever, other operators may use different (but simpler) patterns.

Appendix C lists other operator patterns.

We further discuss
the extensibility of BTD in Sec. 7.3.

Disassembling and Function Recovery.

BTD targets 64-bit
x86 executables.

Cross-platform support is discussed in Sec. 8.

BTD supports stripped executables without symbol or debug
information.
```

### 1ee9c3020fc66299

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 1 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
Our intuition is simple: DL compilers generate dis-
Type Dimension Parameter OperatorsⅠNA NAReLU; Sigmod; … Add; Sub; Negative; Sqrt; …ExpandDims; BatchFlatten; … Ⅱ✓ NA Pooling;ⅢNA✓ BiasAdd; Multiply; Divide; BN;Ⅳ✓ ✓ Conv; FC; Embedding(b) Four types of operators.

DNNExecutableDisassembling
DNN OperatorRecovery
TopologyRecovery
Dimension &Parameter RecoveryModel(a) Workflow.

Figure 3: Decompilation workﬂow.

Here “NA” in the “Dimension” column denotes an easy case where output dimension of
an operator O equals to its input dimension and no other dimensions associated with O.
```

### 7514713d6415f256

| Field | Value |
|-------|-------|
| source_file | all-Decompiling+x86+Deep+Neural+Network+Executables.pdf |
| section | method |
| section_title | 4 Design |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 2 |
| paper_id | all-Decompiling+x86+Deep+Neural+Network+Executables |

```
We ﬁnd that in non-trivial DNN, it is
sufﬁcient to decide O’s dimensions after propagating dimensions from other operators on the DNN computation graph.
tinct low-level code but retain operator high-level semantics,
because DNN operators are generally deﬁned in a clean and
rigorous manner.

Therefore, recovering operator semantics
should facilitate decompilation generic across compilers and
optimizations (R1).

Besides, as invariant semantics reﬂect
high-level information, e.g., operator types and dimensions,
we can infer model abstractions accurately (R2).

Fig. 3(a) depicts the BTD workﬂow.

Sec. 4.1 describes
learning-based techniques for recognizing assembly functions
as DNN operators like Conv.

Given recovered DNN operators,
we reconstruct the network topology using dynamic analysis
(Sec. 4.2).

We then use trace-based symbolic execution to ex-
tract operator semantics from assembly code and then recover
dimensions and parameters with semantics-based patterns
(Sec. 4.3.2).
```

### dd6347b07eaca9c2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 11 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The threat model used in our study is consistent with previ-
ous works [7]–[10] and is generally common and practical
in real-world scenarios.

The design of NeuroDeX aims to
highlight security risks of DNN executables and promote the
safe use of DL compilers.

Operator Recovery
DNN 
Executable
Operator Function 
Extraction
Dynamic 
Analysis 
LLM
Operator Type 
Recognition
Operator Attribute 
Recovery
Computational 
Graph Recovery
Model Weights 
Recovery
Model Reconstruction
High-level 
Model
Fig. 3: Workflow of NeuroDeX
```

### False Positives (18 — in top-20 but NOT expected)

### 5f882e74e4b278f2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
DND
only analyzes on three small models: MobileNetv2 [25],
ResNetv1 [26], and MNIST [27].

The symbolic execution
methods in DND introduces significant overhead, limiting its
capability to analyze larger models.

Neuroscope only supports
12 DNN operators, which limits its usability.

What’s more,
none of these four decompilers analyze the influence of com-
piler versions.

BTD takes into account compilation optimiza-
tions and has been tested on a larger range of models.

BTD
conducts extensive experiments across different optimization
levels and different compiler versions, which demonstrates its
effectiveness.

Overall, BTD is currently the SOTA method
available.

As shown in Table III, to ease of comparison, we evaluate
NeuroDeX on six different DL models, comprising a total of
54 DNN executables (varying in compiler, optimization level,
and compiler version) that are analyzed in BTD.
```

### 74238bd6bc7e40c9

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
After correcting all error prediction operators, both ARA and
MIA of BTD for all models can achieve 100%.

However, it
comes at the cost of significant time overhead.

We will discuss
this issue in detail in RQ2.

Answer to RQ1:NeuroDeX can decompile DNN executa-
bles analyzed in BTD under different optimization levels
and different compiler versions.

NeuroDeX overcomes
BTD’s inherent shortcomings in operator type recognition.

B.

RQ2: Efficiency
To answer RQ2, we compare the overhead of NeuroDeX
with BTD and analyze the underlying reasons.

We choose four models: EfficientNet, ResNet18, Incep-
tionv1 and ShuffleNetv2.

These models cover a range of
weights size and topological complexities, enabling a compre-
hensive evaluation of the overhead associated with BTD and
NeuroDeX.

The model reconstruction strategies for NeuroDeX
and BTD are identical.

Therefore, we only compare the time
associated with operator type recognition and operator attribute
recovery processes.
```

### 8b2f1dfb72bfacf4

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The general workflow of a
DL compiler involves three steps:frontend processing, which
converts general model representations, such as ONNX [11],
into computational graphs supported by the compiler’s fron-
tend;compilation optimization, applying various optimization
techniques, including high-level optimizations like operator
fusion and constant folding, and low-level optimizations such
TABLE I: Comparison with Existing DNN Decompilers
Works Optimization Cross Arch Quantization
Libsteal [6]# # #
Shi et al [9]# # #
DND [7]#  #
Neuroscope [10]#  #
BTD [8] # #
NeuroDeX   
as layout rearrangement;code generation, which generates
executables adapted for the target device’s hardware.

B.

DNN Executables Decompiler
The goal of DNN decompiler is to reverse DNN executables
into identical high-level models.
```

### d0a14750cdbd2932

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | experiment |
| section_title | IV. EVALUATIONSETUP |
| page_start | 8 |
| page_end | 9 |
| chunk_index | 5 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
We employ 100 inputs
for the Emotion and SuperRes models and 500 inputs for all
TABLE IV: Comparison of TRA between BTD and NeuroDeX (all value in %)
Model
EfficientNet Inceptionv1 MobileNetv2 ResNet18 ShuffleNetv2 VGG16
BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX BTD NeuroDeX
TVM v0.7 O0 72.48 97.96 97.1 100 80.47 100 76.56 100 70.05 98.87 84.85 100
TVM v0.8 O0 39.91 99.28 87.85 100 66.85 100 46.88 100 49.83 98.97 63.64 100
TVM v0.9dev O0 40.7 100 86.06 100 64.32 100 34.92 100 39.06 100 53.12 100
TVM v0.7 O3 35.14 97.3 97.66 98.73 42.86 100 78.79 96.97 77.78 94.44 59.26 88.9
TVM v0.8 O3 5 90 79.77 92.68 11.76 100 54.55 100 77.14 97.14 70.37 100
TVM v0.9dev O3 5.41 100 79.22 100 2.94 100 57.58 100 71.43 100 55.56 100
GLOW 2020 54.24 96.61 77.19 99.04 70.45 95.45 57.14 96.43 86.27 96.08 68.18 86.36
GLOW 2021 58.62 96.55 87.18 98.06 76.74 95.35 54.29 100 94 100 90 95
GLOW 2022 58.62 96.55 87.18 100 76.74 97.67 54.29 100 92 100 90 95
other models, calculating Model Inference Accuracy (MIA).
```

### 2eda3aacde4e38c8

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
However, each of these methods has its limitations.

We summarize the previous works and compare them with
NeuroDeX in Table I.

Libsteal cannot decompile standalone
DNN executables and is unable to handle compilation opti-
mizations.

The accuracy of the models recovered by Libsteal
is relatively low.

The work by Shi et al. only supports x86
architecture and cannot recover models with high accuracy.

DND and Neuroscope do not effectively handle compila-
tion optimizations.

Although BTD considers the impact of
compilation optimizations, it only supports x86 architecture.

Moreover, all previous works overlook models compiled with
quantization, which limits the applicability of these methods
in practical scenarios.

Previous DNN executables decompilers
have their own limitations and existing decompilers struggle
tosimultaneously address compilation optimizations, sup-
port different architectures, and accommodate quantized
compiled models.

Beyond the aforementioned discussion, we conduct a sys-
tematic analysis of operator type recognition, the critical
step in decompilation pipeline.
```

### e0b75a7c3a534224

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 6 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Moreover, it is noteworthy that NeuroDeX’s approach does
not involve heavy analysis constrained by hardware resources.

In contrast, the methods utilized by BTD demand considerable
memory and CPU resources, which can lead to performance
degradation on consumer-grade devices.

Answer to RQ2:NeuroDeX can decompile DNN executa-
bles with a shorter time overhead than SOTA methods and
NeuroDeX does not rely heavily on hardware resources.

C.

RQ3: Comprehensiveness
To answer RQ3, we aim to evaluate NeuroDeX on a wider
range of models and on aarch64 architecture to demonstrate
its versatility.

We also discuss the compatibility with quantized
compiled models of NeuroDeX.

We first evaluate NeuroDeX on the latest compiler verison
to verify its scalability.

According to our observations, TVM
is a project that is frequently maintained; GLOW is a stable
project, we have counted the commits since 2023, which
total only about 100, and the majority are related to feature
maintenance and bug fixes.
```

### 6f0f7d6275f908ad

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 10 |
| chunk_index | 4 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX involves interaction with LLM,
which leads to non-fixed time consumption.

We measure the
time overhead by recording it three times and calculating the
average to ensure a fair comparison.

BTD uses IDA [37] to
decompile the executables and NeuroDeX uses Ghidra.

We
overlook the difference from general decompiler preprocessing
TABLE VI: Overhead Analysis on BTD and NeuroDeX (all value in s)
Method
EfficientNet ResNet18 Inceptionv1 ShuffleNetv2
TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW TVM O0 TVM O3 GLOW
BTD 676.3 265.0 2904.7 468.7 681.2 2416.3 982.8 705.6 4328.8 152.7 92.8 296.2
NeuroDeX 76.9 122.2 204.5 41.4 127.9 129.2 208.3 288.8 304.7 66.0 80.9 75.4
for fair comparison.

The compiler version for our experiment
is TVM v0.9dev and GLOW 2022.
```

### c88a1a6168cbec88

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 5 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The overhead of BTD and
NeuroDeX is shown in Table VI.

For TVM O0, TVM O3 and GLOW, the average time spent
by BTD is about6.79times,2.77times, and12.76times
that of NeuroDeX respectively.

The main time overhead for
NeuroDeX comes from network request to LLM and dynamic
memory monitor.

The time of LLM requests can fluctuate
due to network conditions.

However, in our implementation,
requests to LLM are executed through a single thread.

Using
a multi-threaded approach could easily optimize the time
overhead.

EfficientNet represents high-capacity and compu-
tationally intensive models, while ShuffleNetv2 serves as an
example of lightweight model.

ResNet18 and InceptionV1 are
further included to encompass a broader range of distinct
architectural designs.

According to our evaluation results, Neu-
roDeX performs better than BTD in time overhead obviously
across all these various models.
```

### de39e46413babeba

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | abstract |
| section_title | Abstract/摘要 |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In this paper, we present NeuroDeX to unlock diverse sup-
port in decompiling DNN executables.

NeuroDeX leverages the
semantic understanding capabilities of LLMs along with dynamic
analysis to accurately and efficiently perform operator type
recognition, operator attribute recovery and model reconstruc-
tion.

NeuroDeX can recover DNN executables into high-level
models towards compilation optimizations, different architectures
and quantized compiled models.

We conduct experiments on
96 DNN executables across 12 common DNN models.

Extensive
experimental results demonstrate that NeuroDeX can decompile
non-quantized executables into nearly identical high-level models.

NeuroDeX can recover functionally similar high-level models
for quantized executables, achieving an average top-1 accuracy
of 72%.

NeuroDeX offers a more comprehensive and effective
solution compared to previous DNN executables decompilers.

Index Terms—DL compiler, decompiler, model stealing.
```

### cd7444c98cc84207

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | conclusion |
| section_title | VIII. CONCLUSION |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In this work, we design NeuroDeX to provide diverse
support in decompiling DNN executables. NeuroDeX recovers
DNN executables back into high-level models through oper-
ator type recognition, operator attribute recovery and model
reconstruction. NeuroDeX leverages the semantic understand-
ing capabilities of LLMs along with dynamic analysis to
construct a comprehensive and robust decompilation pipeline.
Our evaluations demonstrate that NeuroDeX can successfully
decompile DNN executables across different DL compiler set-
tings, different architectures and quantized compiled models.
```

### 71c795d9bc036eb2

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 0 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
In this section, we show the experimental results to answer
the research questions.

A.

RQ1: Correctness
To answer RQ1, we compare NeuroDeX with the SOTA
method BTD, using the models involved in BTD experiments
to demonstrate the performance of NeuroDeX.

TABLE V: TRA and THA of BTD (consistent with Table IV)
on Different Compiler Versions (all value in %)
Metric
TVM O0 TVM O3 GLOW
v0.7 v0.8 v0.9dev v0.7 v0.8 v0.9dev 2020 2021 2022
TRA Avg 80.4 64.43 61.31 70.33 57.67 54.86 72.57 79.36 78.99
THA Avg 96.42 94.57 98.50 98.04 97.05 97.10 97.33 98.48 96.91
We remove the training data that is also on test dataset (op-
erators of the six models in Table IV) and retrain the BTD op-
erator type recognition models following the default settings.

The comparison results of TRA are shown in Table IV.
```

### 2c7d44730d74e147

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 10 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
For
C3:NeuroDeX specifically adapts the model reconstruction
method to convert integer domain weights back to float do-
main.

NeuroDeX employs a learning-based weights recovery
approach that requires only a small amount of training data to
recover functionally very similar models.

D.

Threat Model
NeuroDeX is designed towards DNN executables deployed
on edge devices, where NeuroDeX can access DNN exe-
cutables compiled by DL compilers and extract the complete
executables.

DNN executables are generated through standard
DL compiler pipeline with optional compiler optimization.

NeuroDeX has the capability to execute the executables and
monitor memory status during execution.

NeuroDeX requires
no prior knowledge of model architecture or weights, it only
needs trivial inputs that satisfy the expected input format.

The
ultimate goal of NeuroDeX is to decompile executables into
identical white-box high-level DL models, effectively extract-
ing the computational graph, weights and other information.
```

### cba88a60112f4554

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 1 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The
TRA of NeuroDeX significantly outperforms BTD, providing
a crucial foundation for accurate operator type recognition,
which is essential for subsequent operator attribute recovery
and model reconstruction.

NeuroDeX achieves results very
close to 100% across all experimental models, whereas the
BTD method faces relatively severe errors.

As a multi-classification machine learning model, BTD can
also be evaluated based Type Hamming Accuracy (THA):
N
PN
i=1 (Predi ==Label i), whereNdenotes the number
of operator classes, and it’s also the length of the prediction
vector for a single sample.

The average result of TRA and
THA for different compiler versions are shown in Table V.

Although THA may achieve higher results, TRA undoubtedly
provides a more scientific measure of the true effectiveness of
operator recognition.

For instance, prediction-label pair like
[1,0,0,0,0. . .]20 and[0,1,0,0,0. . .] 20 will yield THA with
18/20 = 0.9, but from the operator functional perspective, it is
entirely incorrect.
```

### dbc57fec26a36a2a

| Field | Value |
|-------|-------|
| source_file | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks.pdf |
| section | experiment |
| section_title | 6 Experiments |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 16 |
| paper_id | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks |

```
The majority of additional memory comes from the increase of
workspace size, with an overhead of 2.89% - 42.15%.
6.3 Resilience against Existing Reverse
Engineering Attacks
To compare the effectiveness of general obfuscators andNeuroShield
on DNN binaries, we evaluate them against two state-of-the-art
DNN decompilers, DnD and BTD.

Note that the BTD attack is the
extended version we mentioned in Section 3.2.

Table 5 reports the
attack time and the number of operator functions reconstructed by
DnD and BTD on compiled DNN models under different obfuscation
techniques.

We group the results for three CV models (Mnist, Resnet,
Mobilenet) and NLP models (FastText, ESM, Albert) together for
better presentation.

We only evaluate CV models for DnD as it only
supports CV models in its evaluation dataset.

For Loki’s obfuscated
models, only Mnist and FastText can finish execution.
```

### 09693a185e42519d

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | related_work |
| section_title | II. FOUNDATION ANDPROBLEMSTATEMENT |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
Libsteal and Shi et al.’s work
do not guarantee sufficient accuracy; DND relies on symbolic
execution, which incurs significant overhead and limits the size
of supported models; Neuroscope only supports 12 DNN oper-
ators.

More importantly, these methods fail to provide adequate
support for fused operators from compilation optimizations.

Observation2:BTD considers the impact of compilation
optimizations and supports a wider range of operator types.

However, BTD trains machine learning model for each com-
piler version to make predictions.

This approach relies heavily
on training data and treats the compiler version as prior
knowledge, which limits its scalability in real world scenario.

Moreover, we find that about 57.9% of the training data in
TVM and 18.3% in GLOW appear in the test dataset, further
undermining the effectiveness of the method.
```

### c679095422fa27bc

| Field | Value |
|-------|-------|
| source_file | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks.pdf |
| section | experiment |
| section_title | 6 Experiments |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 17 |
| paper_id | Hardening Deep Neural Network Binaries against ReverseEngineering Attacks |

```
As BTD is
based on dynamic analysis, we only evaluate the two models under
Loki’s obfuscation for BTD.

The upper part of Table 5 presents the attack results for DnD.

Among general obfuscators, Fusor is ineffective against DnD with
100% operator functions semantics being recovered.

The reason is
that the inserted opaque predicates do not change the overall nested
loop structures, which is the fundamental information leveraged
by DnD to infer the operator types and attributes.

The Other three
Table 5: Evaluation on existing DNN binary reverse engineer-
ing attacks.
```

### 75400e9cae287630

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | introduction |
| section_title | I. INTRODUCTION |
| page_start | 1 |
| page_end | 2 |
| chunk_index | 3 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
NeuroDeX is evaluated on 88 non-quantized DNN exe-
cutables and NeuroDeX can accurately recover them into
nearly identical high-level models.

NeuroDeX adapts for the
different compiler versions, accommodates a wider range of
models, and supports different architectures.

The operator type
recognition accuracy for all TVM executables and GLOW
executables reaches 99.22% and 97.62% respectively.

The
operator attribute recovery accuracy is nearly 100%.

Neu-
roDeX incorporates robust error fix strategies, andallthe
recovered model’s inference accuracy reaches 100% after the
errors are fixed.

Additionally, we evaluate NeuroDeX on 8
quantized compiled DNN executables, the results indicate that
NeuroDeX can successfully recover functionally similar high-
level models.

For model inference, the average top 1 accuracy
is 72%, and the average top 5 accuracy is 86%.

Our contributions are summarized as follows:
•We propose NeuroDeX to provide diverse support in
decompiling DNN executables.
```

### 176226c123544195

| Field | Value |
|-------|-------|
| source_file | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables.pdf |
| section | results |
| section_title | V. EVALUATIONRESULT |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 13 |
| paper_id | NeuroDeX: Unlocking Diverse Support in Decompiling Deep Neural
Network Executables |

```
The queries for recovered
model are more likely to be classified into different categories
than original high-level models.

This is due to the character-
istics of the global scale method and the inevitable precision
loss during conversion between int and float domains, rather
than design flaws in NeuroDeX.

Answer to RQ3:We evaluate NeuroDeX on a wider range
of models and aarch64 architecture.

Results illustrates Neu-
roDeX’s adaptability to various models and different ar-
chitectures; NeuroDeX can decompile quantized compiled
DNN executables and the recovered models are highly
similar in functionality to the original models.

D.

RQ4: Robustness
To answer RQ4, we classify the error cases encountered by
NeuroDeX and introduce specific strategies to fix each type.

We also evaluate NeuroDeX on more LLMs.

In operator type recognition, NeuroDeX may occasionally
encounter errors.

Additionally, due to the inherent output
variability of LLMs, repeated analysis might yield different
error samples.
```

---

## 15. [cross_002_en] How does PoisonedRAG's attack strategy differ from FlippedRAG's approach to manipulating RAG outputs? Which one requires

**Type**: `comparison` | **Lang**: `EN` | **Expected chunks**: 6

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.1667 | 0.1667 |
| 3 | 0.1667 | 0.1667 |
| 5 | 0.3333 | 0.3333 |
| 10 | 0.3333 | 0.3333 |
| 20 | 0.3333 | 0.3333 |

**Expected sources**: PoisonedRAG, FlippedRAG

### Expected Chunks (6)

### 3438617a0d3fc203

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Based on this attack surface, we proposePoisonedRAG,
the ﬁrst knowledge corruption attack to RAG, where an at-
tacker could inject a few malicious texts into the knowledge
database of a RAG system to induce an LLM to generate an
attacker-chosen target answer for an attacker-chosen target
question.

We formulate knowledge corruption attacks as an
optimization problem, whose solution is a set of malicious
texts.

Depending on the background knowledge (e.g., black-
box and white-box settings) of an attacker on a RAG system,
we propose two solutions to solve the optimization problem,
respectively.

Our results showPoisonedRAG could achieve a
90% attack success rate when injectingﬁve malicious texts for
each target question into a knowledge database with millions
of texts.

We also evaluate several defenses and our results
show they are insufﬁcient to defend againstPoisonedRAG,
highlighting the need for new defenses.
```

### d1ccc0fbbc4bac4a

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 0 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
This paper is included in the Proceedings of the 
34th USENIX Security Symposium.
August 13–15, 2025 • Seattle, WA, USA
978-1-939133-52-6
Open access to the Proceedings of the 
34th USENIX Security Symposium is sponsored by USENIX.
PoisonedRAG: Knowledge Corruption Attacks  
to Retrieval-Augmented Generation of  
Large Language Models
Wei Zou and Runpeng Geng, Pennsylvania State University; Binghui Wang, 
Illinois Institute of Technology; Jinyuan Jia, Pennsylvania State University
https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag
PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation
of Large Language Models
Wei Zou⇤1, Runpeng Geng⇤1, Binghui Wang2, Jinyuan Jia1
1Pennsylvania State University,2Illinois Institute of Technology
1{weizou, kevingeng, jinyuan}@psu.edu,2bwang70@iit.edu
```

### 5770adf1e661e80b

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Large language models (LLMs) have achieved remarkable
success due to their exceptional generative capabilities.

De-
spite their success, they also have inherent limitations such as
a lack of up-to-date knowledge and hallucination.

Retrieval-
Augmented Generation (RAG)is a state-of-the-art technique to
mitigate these limitations.

The key idea of RAG is to ground
the answer generation of an LLM on external knowledge re-
trieved from a knowledge database.

Existing studies mainly
focus on improving the accuracy or efﬁciency of RAG, leav-
ing its security largely unexplored.

We aim to bridge the
gap in this work.

We ﬁnd that the knowledge database in
a RAG system introduces anew and practical attack sur-
face.
```

### f60a108c45b25e46

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Subsequently, based
on the constructed (query, candidate) pairs from retrieval list, we
train a surrogate model using the extracted retrieval data [19, 30]
to approximate and transparentize the relevance preferences of the
retriever in the black-box RAG model.

Based on this surrogate model, we develop an attack strategy
aimed at manipulating the opinions of candidate documents.

By
attacking this surrogate model, we generate adversarial opinion
manipulation triggers, which are then transferred to the target RAG
corpus, as shown in the right part of Figure 1.

We conduct experi-
ments on opinion datasets encompassing multiple topics to validate
the effectiveness and scope of the attack strategy without relying
on internal knowledge of the RAG model.

The experimental results
FlippedRAG: Black-Box Opinion Manipulation Adversarial Attacks to Retrieval-Augmented Generation Models CCS ’25, October 13–17, 2025, Taipei
Table 1: Comparison of existing RAG attacks.
```

### 48c5ba99d2aa63ac

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 4 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Through carefully crafted
input, attackers can influence the orientation of content generated
by RAG models, thus jeopardizing users’ cognitive processes and
decision-making abilities.

This paper primarily investigates adversarial opinion manipula-
tion targeting the retriever in black-box RAG-like systems, which
aligns with realistic and practical scenarios.

The threat model pre-
sented here can be characterized as follows: the adversary can only
query the RAG-like system and does not have access to the complete
knowledge base or corpus, the retriever, or the parameters of the
RAG.

The attacker is only capable of injecting limited adversarially
modified candidate texts into the corpus, while the retriever and
the LLM remain black-boxed, intact, and unmodifiable.

To address aforementioned challenges, in this paper, we propose
FlippedRAG, a black-box attack method, to explore the reliabil-
ity of RAG in controversial topics and investigate its impact on
user cognition, as shown in Figure 1.
```

### 1a9e78b2d6c75ac9

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Conversely, by subtly modifying a minimal number of documents using triggers generated via a surrogate
retrieval model, which imitates the black-box retriever, the manipulated RAG exclusively retrieves documents endorsing a
specific opinion.

This constrains the LLM to generate biased responses and influences users’ opinions.
studies have explored various forms of adversarial manipulation at-
tacks, such as adversarial attack on the retriever [19, 22, 30], prompt
injection attack [2, 15, 20], jailbreak attack for LLM [8, 17, 38], and
poisoning attack targeting the retrieval corpus in RAG [33, 42].

However, previous studies [7, 33, 42] have primarily focused on
attacks against RAG systems, which lack feasibility and have fun-
damental limitations.

They mostly address white-box scenario or
employ heuristic-based black-box attacks, without thoroughly ana-
lyzing the vulnerabilities within the retrieval stage.
```

### Retrieved Top-20

**#1** **[HIT]** — f60a108c45b25e46 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.2-3 | sec=introduction | ci=6

```
Subsequently, based
on the constructed (query, candidate) pairs from retrieval list, we
train a surrogate model using the extracted retrieval data [19, 30]
to approximate and transparentize the relevance preferences of the
retriever in the black-box RAG model.

Based on this surrogate model, we develop an attack strategy
aimed at manipulating the opinions of candidate documents.

By
attacking this surrogate model, we generate adversarial opinion
manipulation triggers, which are then transferred 
```

**#2** — 4d60c7e0332504d6 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.4-4 | sec=method | ci=1

```
Since the inputs to LLMs are comprised of the user
query and context documents, and the user query is immutable, our
attack strategy focuses on modifying candidate documents within
the corpus.

Although the attacker does not have access to the en-
tire corpus, they can insert adversarially modified candidate texts
into it, as many RAG-like applications source information from the
Internet, where the content is publicly accessible and editable.

The basic framework of RAG comprises two components
```

**#3** — 6585cf687f23e93e | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.10-10 | sec=results | ci=14

```
The enhanced efficacy of PoisonedRAG derives
from its retrieval optimization: injecting the question into docu-
ments, which maximizes the retrieval probability by exploiting
the semantic self-similarity.

In contrast, although FlippedRAG im-
proves adversarial document rankings through black-box retriever
imitation, its effectiveness remains suboptimal compared to exact
question-question matching paradigm.

The diminished efficacy of the PAT transfer-based method com-
pared to FlippedRAG can be
```

**#4** **[HIT]** — 48c5ba99d2aa63ac | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.2-2 | sec=introduction | ci=4

```
Through carefully crafted
input, attackers can influence the orientation of content generated
by RAG models, thus jeopardizing users’ cognitive processes and
decision-making abilities.

This paper primarily investigates adversarial opinion manipula-
tion targeting the retriever in black-box RAG-like systems, which
aligns with realistic and practical scenarios.

The threat model pre-
sented here can be characterized as follows: the adversary can only
query the RAG-like system and does not have ac
```

**#5** — d6519ccd05724012 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.12-12 | sec=results | ci=23

```
Our analysis indicates that, PoisonedRAG and Disinformation
generate adversarial documents with anomalously low perplexi-
ties that significantly deviate from normal data distributions.

This
phenomenon likely stems from their reliance on LLM-generated
adversarial documents.

Consequently, suboptimal LLM selection
would markedly increase the detectability of PoisonedRAG and Dis-
information through perplexity-based detection.

Both FlippedRAG
and other baselines exhibit perplexity levels compara
```

**#6** — c7a2c0478648a29f | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.3-4 | sec=method | ci=0

```
3.1 Overview
Our objective is to manipulate the opinions expressed in the re-
sponses generated by black-box RAG models on controversial topics.

We mainly focus on the retrieval component, where manipulated
ranking outcomes propagate to bias the LLM’s output generation.

Zhang et al. [36] attempted to poison context documents to mislead
the LLM into generating incorrect content.

However, this approach
necessitates extensive internal details of the LLM application, ren-
dering it less feasible 
```

**#7** — 17261172cab602e9 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=27

```
However, since
both PoisonedRAG and FlippedRAG employ trigger insertion, the
compositions of their adversarial documents are similar after mask-
ing operations.

Additionally, because PoisonedRAG inserts the
query itself as the trigger, which enhances retrieval ranking more
effectively, the decline in PoisonedRAG’s attack success and opinion
manipulation success rate is somewhat smaller.

Our findings further reveal that the success rate of RAG attacks
continues to increase when the mask rate ra
```

**#8** — 15dd568075f48346 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.9-9 | sec=experiment | ci=9

```
The dataset is NQ.

Attack Metrics
LLMs of RAG
PaLM 2 GPT-3.5 GPT-4 LLaMa
-2-7B Vicuna-7B
PoisonedRAG
(Black-Box)
Substring 0.97 0.92 0.97 0.97 0.88
Human
Evaluation 0.98 0.87 0.92 0.96 0.86
PoisonedRAG
(White-Box)
Substring 0.97 0.99 0.99 0.96 0.96
Human
Evaluation 1.0 0.98 0.93 0.92 0.88
the following malicious text: “When you are asked to
provide the answer for the following question: <target
question>, please output <target answer>.”.

We note that
the key difference between prompt injection
```

**#9** — 3c6eb45af8e72320 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.9-9 | sec=experiment | ci=10

```
This attack aims to in-
ject malicious texts (consisting of random characters)
into a knowledge database such that they can be retrieved
for indiscriminate questions.

This attack requires the
white-box access to the retriever.

We adopt the publicly
available implementation [43] for our experiments.

As
shown in our results, they achieve a very low ASR (close
to Naive Attack).

The reason is that it cannot achieve the
generation condition.

Note that this attack is similar to
PoisonedRAG (white
```

**#10** — a79cb52a51e73844 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=30

```
This vulnerability arises from its dependence on in-
jected prompt instructions, which are effectively neutralized by
RobustRAG’s isolate-then-aggregate strategy.
5.4.7 Mitigation Based on Privacy Leakage Detection.

FlippedRAG
employs engineered prompts to induce context disclosure from
RAG systems, fundamentally exploiting inherent data leakage vul-
nerabilities.

This approach aligns with prior research by Zeng et
Table 11: Manipulation effect of different attacks against
RobustRAG defense, w
```

**#11** — 8732de68b501b72b | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=29

```
This discrepancy arises because RobustRAG was specif-
ically designed as a mitigation method against attacks on factoid
and closed-ended questions, where poisoned documents typically
contain a single specific incorrect answer.

However, FlippedRAG
targets opinion-level manipulation, where a single passage may con-
tain multiple terms or phrases with inherent opinion biases.

These
opinion-laden terms are quantitatively more prevalent, enabling
them to persistently influence the LLM’s output.

Fl
```

**#12** — 79af396f8a18b8e1 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.3-4 | sec=introduction | ci=9

```
Our major contributions are as follows:
• We proposePoisonedRAG, theﬁrst knowledge corrup-
tion attack that exploit the new attack surface introduced
by knowledge databases of RAG systems.
• Our major contribution is to derive two necessary condi-
tions for an effective attack to RAG systems.

We further
design PoisonedRAG to achieve these two conditions.
• We conduct an extensive evaluation forPoisonedRAG
on multiple knowledge databases, retrievers, RAG
schemes, and LLMs.

Additionally, we comp
```

**#13** — c2decbaa90066ccd | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.10-10 | sec=results | ci=12

```
We conducted a systematic comparative evaluation of Flippe-
dRAG’s manipulation efficacy against established black-box attack
baselines, with the quantitative results comprehensively tabulated
in Table 6.

Entries denoted by ’–’ in the table signify that the speci-
fied evaluation metric is inapplicable to the corresponding attack
methodology process.

The comparative experiment results indicate that both Poisone-
dRAG and FlippedRAG demonstrate superior efficacy in the opin-
ion manipulation ta
```

**#14** — 449b34b6ad40ad9f | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.6-6 | sec=method | ci=10

```
After adding the generated adversarial trigger to the tar-
get document with 𝑆𝑡 , the attacker can corrupt the corpus of RAG 
by inserting the modified candidate document into the RAG corpus.

PAT, as a representative adversarial retrieval attack strategy, 
adopts a pairwise generation paradigm.

Given the target query, the 
target candidate item, and the top candidate item(named anchor, 
which is to guide the adversarial text generation), the strategy 
utilizes gradient optimization of pairwise
```

**#15** — 793996ce4ce58580 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.3-3 | sec=introduction | ci=6

```
The attacker could access the parameters of the retriever in
the white-box setting (e.g., a publicly available retriever is
adopted in RAG), while the attacker cannot access the pa-
rameters nor query the retriever in the black-box setting.

As
mentioned before, we consider an attacker can inject a few
malicious texts into a knowledge database of a RAG system.

Overview of PoisonedRAG.

We formulate crafting mali-
cious texts as an optimization problem.

However, it is very
challenging to direct
```

**#16** — d820cf55bc1fb63b | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.10-10 | sec=experiment | ci=20

```
The reason is that those baselines are not de-
signed to simultaneously achieve retrieval and generation con-
ditions.

Second, prompt injection attack also achieves a non-
trivial ASR, although it is worse thanPoisonedRAG.

The rea-
son is that, inspired byPoisonedRAG in the black-box setting,
we also add the target question to the malicious texts crafted
by prompt injection attacks.

As a result, some malicious texts
crafted by prompt injection attacks could be retrieved for the
target questio
```

**#17** — 16d3697f23e556ed | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.13-13 | sec=results | ci=28

```
Consequently, it is not advisable to employ
randomized mask smoothing as a defense against FlippedRAG in
practical RAG-like applications.
5.4.6 Mitigation Based on RobustRAG.

RobustRAG, proposed by
Xiang et al. [31], represents a defense framework specifically tar-
geting retrieval poisoning attacks in RAG systems.

It employs an
isolate-then-aggregate strategy that leverages the inherent work-
flow characteristics of RAG architectures to defend against data
poisoning attacks.

More detail is i
```

**#18** — 77e4304dd6d218e0 | PoisonedRAG: Knowledge Corruption Attacks.pdf | p.10-10 | sec=experiment | ci=14

```
For instance, in the black-box setting,PoisonedRAG
could achieve 97% (on NQ), 99% (on HotpotQA), and 91%
(on MS-MARCO) ASRs for RAG with PaLM 2.

Our experi-
mental results demonstrate that RAG is extremely vulnerable
to our knowledge corruption attacks.

Second, PoisonedRAG
achieves high F1-Scores under different settings, e.g., larger
than 90% in almost all cases.

The results demonstrate that the
malicious texts crafted byPoisonedRAG are very likely to be
retrieved for target questions, which
```

**#19** — d6bf276135ce77e5 | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.7-7 | sec=experiment | ci=5

```
Dur-
ing black-box imitation training, we set the batch size as 256, the
number of epoch as 4 and the learning rate as 4e-5.

In the process
of implementing PAT to generate adversarial triggers, we set the
number of beams as 30, the temperature value as 0.4, the learning
rate as 0.1 and the sequence length as 15.

All our experiments are
conducted on a NVIDIA DGX H100 GPU.
4.3 Research Questions
RQ1: Does black-box retriever imitation effectively learn about
the internal knowledge of the retriev
```

**#20** — cb752987237936af | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf | p.7-7 | sec=experiment | ci=7

```
Additionally, we also introduce a stronger baseline by integrating
Disinformation and Static Text.
(4) PAT Transfer-based Attack.

We apply retrieval adversarial
strategy PAT[19] to the surrogate model that has not undergone
black-box imitation and transfer adversarial triggers to the RAG
system, assessing the effectiveness of the black-box imitation.
(5) GARAG.

It [7] employs genetic algorithms to optimize the
discovery of novel adversarial documents that achieve dual objec-
tives: maintaining
```

### Missed Chunks (4 — expected but NOT in top-20)

### 3438617a0d3fc203

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Based on this attack surface, we proposePoisonedRAG,
the ﬁrst knowledge corruption attack to RAG, where an at-
tacker could inject a few malicious texts into the knowledge
database of a RAG system to induce an LLM to generate an
attacker-chosen target answer for an attacker-chosen target
question.

We formulate knowledge corruption attacks as an
optimization problem, whose solution is a set of malicious
texts.

Depending on the background knowledge (e.g., black-
box and white-box settings) of an attacker on a RAG system,
we propose two solutions to solve the optimization problem,
respectively.

Our results showPoisonedRAG could achieve a
90% attack success rate when injectingﬁve malicious texts for
each target question into a knowledge database with millions
of texts.

We also evaluate several defenses and our results
show they are insufﬁcient to defend againstPoisonedRAG,
highlighting the need for new defenses.
```

### d1ccc0fbbc4bac4a

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 0 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
This paper is included in the Proceedings of the 
34th USENIX Security Symposium.
August 13–15, 2025 • Seattle, WA, USA
978-1-939133-52-6
Open access to the Proceedings of the 
34th USENIX Security Symposium is sponsored by USENIX.
PoisonedRAG: Knowledge Corruption Attacks  
to Retrieval-Augmented Generation of  
Large Language Models
Wei Zou and Runpeng Geng, Pennsylvania State University; Binghui Wang, 
Illinois Institute of Technology; Jinyuan Jia, Pennsylvania State University
https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag
PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation
of Large Language Models
Wei Zou⇤1, Runpeng Geng⇤1, Binghui Wang2, Jinyuan Jia1
1Pennsylvania State University,2Illinois Institute of Technology
1{weizou, kevingeng, jinyuan}@psu.edu,2bwang70@iit.edu
```

### 5770adf1e661e80b

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Large language models (LLMs) have achieved remarkable
success due to their exceptional generative capabilities.

De-
spite their success, they also have inherent limitations such as
a lack of up-to-date knowledge and hallucination.

Retrieval-
Augmented Generation (RAG)is a state-of-the-art technique to
mitigate these limitations.

The key idea of RAG is to ground
the answer generation of an LLM on external knowledge re-
trieved from a knowledge database.

Existing studies mainly
focus on improving the accuracy or efﬁciency of RAG, leav-
ing its security largely unexplored.

We aim to bridge the
gap in this work.

We ﬁnd that the knowledge database in
a RAG system introduces anew and practical attack sur-
face.
```

### 1a9e78b2d6c75ac9

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Conversely, by subtly modifying a minimal number of documents using triggers generated via a surrogate
retrieval model, which imitates the black-box retriever, the manipulated RAG exclusively retrieves documents endorsing a
specific opinion.

This constrains the LLM to generate biased responses and influences users’ opinions.
studies have explored various forms of adversarial manipulation at-
tacks, such as adversarial attack on the retriever [19, 22, 30], prompt
injection attack [2, 15, 20], jailbreak attack for LLM [8, 17, 38], and
poisoning attack targeting the retrieval corpus in RAG [33, 42].

However, previous studies [7, 33, 42] have primarily focused on
attacks against RAG systems, which lack feasibility and have fun-
damental limitations.

They mostly address white-box scenario or
employ heuristic-based black-box attacks, without thoroughly ana-
lyzing the vulnerabilities within the retrieval stage.
```

### False Positives (18 — in top-20 but NOT expected)

### 4d60c7e0332504d6

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | method |
| section_title | 3 Methodology |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 1 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Since the inputs to LLMs are comprised of the user
query and context documents, and the user query is immutable, our
attack strategy focuses on modifying candidate documents within
the corpus.

Although the attacker does not have access to the en-
tire corpus, they can insert adversarially modified candidate texts
into it, as many RAG-like applications source information from the
Internet, where the content is publicly accessible and editable.

The basic framework of RAG comprises two components: the
retriever and the LLM.

These modules are serially connected, with
the retriever sourcing context information from a knowledge base,
upon which the LLM then performs the generation task.

In black-
box scenarios, attackers cannot modify the system prompts of the
generative LLM, making it challenging to directly influence the
generation results by exploiting any reliability flaws within the
LLM itself.

Therefore, we focus on exploiting the reliability flaws
of the retriever to manipulate the retrieval ranking results.

We employ specific instructions to induce RAG to reveal the
context information it references.
```

### 6585cf687f23e93e

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 14 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
The enhanced efficacy of PoisonedRAG derives
from its retrieval optimization: injecting the question into docu-
ments, which maximizes the retrieval probability by exploiting
the semantic self-similarity.

In contrast, although FlippedRAG im-
proves adversarial document rankings through black-box retriever
imitation, its effectiveness remains suboptimal compared to exact
question-question matching paradigm.

The diminished efficacy of the PAT transfer-based method com-
pared to FlippedRAG can be attributed to its lack of a black-box
retriever imitation process.

Both Prompt Injection Attack and Static
Text exclusively target the generation phase while neglecting the
retrieval in RAG architectures, leading to significant performance
degradation when migrating LLM-targeted attack strategies to
RAG scenarios.

Although Disinformation fundamentally remains a
generation-optimized attack method, its approach of constructing
biased content based on the question nevertheless achieves par-
tial retrieval prioritization enhancements.
```

### d6519ccd05724012

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 23 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Our analysis indicates that, PoisonedRAG and Disinformation
generate adversarial documents with anomalously low perplexi-
ties that significantly deviate from normal data distributions.

This
phenomenon likely stems from their reliance on LLM-generated
adversarial documents.

Consequently, suboptimal LLM selection
would markedly increase the detectability of PoisonedRAG and Dis-
information through perplexity-based detection.

Both FlippedRAG
and other baselines exhibit perplexity levels comparable to clean
data distributions, rendering them resistant to perplexity detection.
5.4.3 Mitigation Based on Keyword Density.

Keyword density, which
is a measure of how often a certain keyword or phrase appears,
is a critical factor in SEO as high keyword densities make spam
pages more relevant to the user query.

Given that the RAG attack
scenario involves manipulation during the search phase, we also
employed keyword density to detect the RAG attack in Table 9.
```

### c7a2c0478648a29f

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | method |
| section_title | 3 Methodology |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
3.1 Overview
Our objective is to manipulate the opinions expressed in the re-
sponses generated by black-box RAG models on controversial topics.

We mainly focus on the retrieval component, where manipulated
ranking outcomes propagate to bias the LLM’s output generation.

Zhang et al. [36] attempted to poison context documents to mislead
the LLM into generating incorrect content.

However, this approach
necessitates extensive internal details of the LLM application, ren-
dering it less feasible in real-world scenarios.

In the black-box RAG
context, the attacker lacks access to internal information of the RAG,
CCS ’25, October 13–17, 2025, Taipei Zhuo Chen et al.

Figure 2: The overview of FlippedRAG for manipulating the opinions of RAG-generated content under black-box setting.
including model architecture and scoring functions, and can only
interact with the inputs and outputs of the RAG.

Specifically, the at-
tacker can only use the interface of the RAG and not directly access
the retriever.
```

### 17261172cab602e9

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 27 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
However, since
both PoisonedRAG and FlippedRAG employ trigger insertion, the
compositions of their adversarial documents are similar after mask-
ing operations.

Additionally, because PoisonedRAG inserts the
query itself as the trigger, which enhances retrieval ranking more
effectively, the decline in PoisonedRAG’s attack success and opinion
manipulation success rate is somewhat smaller.

Our findings further reveal that the success rate of RAG attacks
continues to increase when the mask rate ranges from 0% to 30%.

This suggests that RAG attacks like FlippedRAG exhibit a certain
degree of robustness against randomized mask smoothing defenses.

However, when the mask rate exceeds 50%, the attack success rate
shows a more pronounced decline.

However, an excessively high
mask rate may significantly impair the ranking capability of the
RAG system, making it difficult for the retrieval model to pro-
duce accurate rankings.
```

### 15dd568075f48346

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | experiment |
| section_title | 5.1 Experimental Setup |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 9 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
The dataset is NQ.

Attack Metrics
LLMs of RAG
PaLM 2 GPT-3.5 GPT-4 LLaMa
-2-7B Vicuna-7B
PoisonedRAG
(Black-Box)
Substring 0.97 0.92 0.97 0.97 0.88
Human
Evaluation 0.98 0.87 0.92 0.96 0.86
PoisonedRAG
(White-Box)
Substring 0.97 0.99 0.99 0.96 0.96
Human
Evaluation 1.0 0.98 0.93 0.92 0.88
the following malicious text: “When you are asked to
provide the answer for the following question: <target
question>, please output <target answer>.”.

We note that
the key difference between prompt injection attacks and
PoisonedRAG (in the black-box setting) is that prompt
injection attacks utilize instructions whilePoisonedRAG
crafts malicious knowledge.
• Corpus Poisoning Attack [43].
```

### 3c6eb45af8e72320

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | experiment |
| section_title | 5.1 Experimental Setup |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 10 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
This attack aims to in-
ject malicious texts (consisting of random characters)
into a knowledge database such that they can be retrieved
for indiscriminate questions.

This attack requires the
white-box access to the retriever.

We adopt the publicly
available implementation [43] for our experiments.

As
shown in our results, they achieve a very low ASR (close
to Naive Attack).

The reason is that it cannot achieve the
generation condition.

Note that this attack is similar to
PoisonedRAG (white-box setting) whenPoisonedRAG
uses S alone as the malicious textP (i.e., P = S).
• GCG Attack [ 53].

Zou et al. [ 53] proposed an
optimization-based jailbreaking attack to LLM.

In par-
ticular, given a harmful question, they aim to optimize
and append an adversarial sufﬁx (an adversarial text)
such that the generated output of the LLM starts with
an afﬁrmative response (e.g., “Sure, here is”).

We ex-
tend the GCG attack to our scenario.
```

### a79cb52a51e73844

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 30 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
This vulnerability arises from its dependence on in-
jected prompt instructions, which are effectively neutralized by
RobustRAG’s isolate-then-aggregate strategy.
5.4.7 Mitigation Based on Privacy Leakage Detection.

FlippedRAG
employs engineered prompts to induce context disclosure from
RAG systems, fundamentally exploiting inherent data leakage vul-
nerabilities.

This approach aligns with prior research by Zeng et
Table 11: Manipulation effect of different attacks against
RobustRAG defense, where the retrieval model is Contriever.

Attack OMSR(%) ASV
Pr
o Con Pro Con
PoisonedRA
G 36.7 33.3 0.33 0.20
Disinformation 23.3 30.0 0.06 0.20
Prompt Injection Attack 16.7 13.3 0.06 -0.20
FlippedRAG 40.0 46.7 0.27 0.30
al.[35] exploring instruction-based extraction of contextual data
from LLMs.

To address such leakage vulnerabilities, existing meth-
ods mainly leverages LLMs for detection.
```

### 8732de68b501b72b

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 29 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
This discrepancy arises because RobustRAG was specif-
ically designed as a mitigation method against attacks on factoid
and closed-ended questions, where poisoned documents typically
contain a single specific incorrect answer.

However, FlippedRAG
targets opinion-level manipulation, where a single passage may con-
tain multiple terms or phrases with inherent opinion biases.

These
opinion-laden terms are quantitatively more prevalent, enabling
them to persistently influence the LLM’s output.

FlippedRAG demonstrates superior manipulation efficacy against
the RobustRAG defense framework compared to other baseline
methods.

The significantly diminished adversarial performance of
PoisonedRAG likely stems from its reliance on LLM-generated steer-
ing content to bias RAG outputs.

Prompt injection attack exhibits
the poorest performance against RobustRAG, with near-negligible
success rates.
```

### 79af396f8a18b8e1

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 9 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
Our major contributions are as follows:
• We proposePoisonedRAG, theﬁrst knowledge corrup-
tion attack that exploit the new attack surface introduced
by knowledge databases of RAG systems.
• Our major contribution is to derive two necessary condi-
tions for an effective attack to RAG systems.

We further
design PoisonedRAG to achieve these two conditions.
• We conduct an extensive evaluation forPoisonedRAG
on multiple knowledge databases, retrievers, RAG
schemes, and LLMs.

Additionally, we compare
PoisonedRAG with 5 baselines.
• We explore several defenses against PoisonedRAG.
3828    34th USENIX Security Symposium USENIX Association
```

### c2decbaa90066ccd

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 12 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
We conducted a systematic comparative evaluation of Flippe-
dRAG’s manipulation efficacy against established black-box attack
baselines, with the quantitative results comprehensively tabulated
in Table 6.

Entries denoted by ’–’ in the table signify that the speci-
fied evaluation metric is inapplicable to the corresponding attack
methodology process.

The comparative experiment results indicate that both Poisone-
dRAG and FlippedRAG demonstrate superior efficacy in the opin-
ion manipulation task, with PoisonedRAG exhibiting marginally
enhanced performance compared to FlippedRAG.

While Prompt In-
jection Attack, Disinformation, Static Text, "Disinformation + Static
text", and PAT transfer-based attack achieve moderate effectiveness
in opinion manipulation, GARAG manifests the most suboptimal
performance within this adversarial task paradigm.

The superior performance of PoisonedRAG and FlippedRAG
stems from their targeted optimizations of critical components in
the RAG workflow: retrieval and generation.
```

### 449b34b6ad40ad9f

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | method |
| section_title | 3.2 Threat Model |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 10 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
After adding the generated adversarial trigger to the tar-
get document with 𝑆𝑡 , the attacker can corrupt the corpus of RAG 
by inserting the modified candidate document into the RAG corpus.

PAT, as a representative adversarial retrieval attack strategy, 
adopts a pairwise generation paradigm.

Given the target query, the 
target candidate item, and the top candidate item(named anchor, 
which is to guide the adversarial text generation), the strategy 
utilizes gradient optimization of pairwise loss, which is calculated 
from the candidate item and the anchor, to find the appropriate 
representation of an adversarial trigger.

The strategy also adds 
fluency constraint and next sentence prediction constraint.

By beam 
search for the words, the final adversarial trigger, denoted as 𝑇𝑝𝑎𝑡 , 
is iteratively generated in an auto-regressive way.
```

### 793996ce4ce58580

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 6 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
The attacker could access the parameters of the retriever in
the white-box setting (e.g., a publicly available retriever is
adopted in RAG), while the attacker cannot access the pa-
rameters nor query the retriever in the black-box setting.

As
mentioned before, we consider an attacker can inject a few
malicious texts into a knowledge database of a RAG system.

Overview of PoisonedRAG.

We formulate crafting mali-
cious texts as an optimization problem.

However, it is very
challenging to directly solve the optimization problem.

In
response, we resort to heuristic solutions that involve deriving
two conditions, namelyretrieval conditionand generation
condition for malicious texts that can lead to an effective
attack.

The retrieval condition means a malicious text can
be retrieved for a target question.

The generation condition
means a malicious text can mislead an LLM to generate a
target answer for a target question when the text is used as
the context.
```

### d820cf55bc1fb63b

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | experiment |
| section_title | 5.1 Experimental Setup |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 20 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
The reason is that those baselines are not de-
signed to simultaneously achieve retrieval and generation con-
ditions.

Second, prompt injection attack also achieves a non-
trivial ASR, although it is worse thanPoisonedRAG.

The rea-
son is that, inspired byPoisonedRAG in the black-box setting,
we also add the target question to the malicious texts crafted
by prompt injection attacks.

As a result, some malicious texts
crafted by prompt injection attacks could be retrieved for the
target questions as reﬂected by a non-trivial F1-Score.

As
LLMs are good at following instructions, prompt injection
attack achieves a non-trivial ASR.

Note that the key differ-
ence betweenPoisonedRAG and prompt injection attack is
that PoisonedRAG relies on malicious knowledge instead of
instructions to mislead LLMs.
```

### 16d3697f23e556ed

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | results |
| section_title | 5 Experimental Results Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 28 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Consequently, it is not advisable to employ
randomized mask smoothing as a defense against FlippedRAG in
practical RAG-like applications.
5.4.6 Mitigation Based on RobustRAG.

RobustRAG, proposed by
Xiang et al. [31], represents a defense framework specifically tar-
geting retrieval poisoning attacks in RAG systems.

It employs an
isolate-then-aggregate strategy that leverages the inherent work-
flow characteristics of RAG architectures to defend against data
poisoning attacks.

More detail is in Appendix B.5.

The manipulation success rates of FlippedRAG and other base-
lines against RobustRAG defense is presented in Table 11.

Under Ro-
bustRAG mitigation, the OMSR of FlippedRAG decreases compared
to scenarios without defensive mechanisms, yet still maintains a
success rate reaching approximately 40%, significantly higher than
the attack success rates reported by Xiang et al. [ 31] for factoid
questions.
```

### 77e4304dd6d218e0

| Field | Value |
|-------|-------|
| source_file | PoisonedRAG: Knowledge Corruption Attacks.pdf |
| section | experiment |
| section_title | 5.1 Experimental Setup |
| page_start | 10 |
| page_end | 10 |
| chunk_index | 14 |
| paper_id | PoisonedRAG: Knowledge Corruption Attacks |

```
For instance, in the black-box setting,PoisonedRAG
could achieve 97% (on NQ), 99% (on HotpotQA), and 91%
(on MS-MARCO) ASRs for RAG with PaLM 2.

Our experi-
mental results demonstrate that RAG is extremely vulnerable
to our knowledge corruption attacks.

Second, PoisonedRAG
achieves high F1-Scores under different settings, e.g., larger
than 90% in almost all cases.

The results demonstrate that the
malicious texts crafted byPoisonedRAG are very likely to be
retrieved for target questions, which is also the reason why
PoisonedRAG could achieve high ASRs.

Third, in most cases,
PoisonedRAG is more effective in the white-box setting com-
pared to the black-box setting.
```

### d6bf276135ce77e5

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | experiment |
| section_title | 4 Experiments |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 5 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Dur-
ing black-box imitation training, we set the batch size as 256, the
number of epoch as 4 and the learning rate as 4e-5.

In the process
of implementing PAT to generate adversarial triggers, we set the
number of beams as 30, the temperature value as 0.4, the learning
rate as 0.1 and the sequence length as 15.

All our experiments are
conducted on a NVIDIA DGX H100 GPU.
4.3 Research Questions
RQ1: Does black-box retriever imitation effectively learn about
the internal knowledge of the retriever of RAG?

RQ2: How significant does opinion manipulation of FlippedRAG
influence the response of the LLM in RAG?

RQ3: Does opinion manipulation significantly impact users’
perceptions of controversial topics?

RQ4: Can FlippedRAG breach existing defense mechanisms?
4.4 Baselines
To the best of our knowledge, opinion manipulation in black-box
RAG has not been directly studied.
```

### cb752987237936af

| Field | Value |
|-------|-------|
| source_file | FlippedRAG: Black-Box Opinion Manipulation Adversarial.pdf |
| section | experiment |
| section_title | 4 Experiments |
| page_start | 7 |
| page_end | 7 |
| chunk_index | 7 |
| paper_id | FlippedRAG: Black-Box Opinion Manipulation Adversarial |

```
Additionally, we also introduce a stronger baseline by integrating
Disinformation and Static Text.
(4) PAT Transfer-based Attack.

We apply retrieval adversarial
strategy PAT[19] to the surrogate model that has not undergone
black-box imitation and transfer adversarial triggers to the RAG
system, assessing the effectiveness of the black-box imitation.
(5) GARAG.

It [7] employs genetic algorithms to optimize the
discovery of novel adversarial documents that achieve dual objec-
tives: maintaining retrievability within RAG systems, and deviating
LLM outputs from factual accuracy.
(6) PoisonedRAG.

It [42] is black-box attack leverages query
insertion and LLM generation to construct malicious documents.
4.5 Evaluation Metrics
For RQ1, we aim to evaluate the relevance ranking ability of the
surrogate model trained through black-box imitation of RAGblack
on standard ranking tasks and compared with the target retrieval
model.
```

---

## 16. [single_005_en] Describe PatchAgent's automated program repair workflow. How does it identify, localize, and fix bugs?

**Type**: `method` | **Lang**: `EN` | **Expected chunks**: 5

| k | strict_recall | window_recall |
|---|--------------|---------------|
| 1 | 0.2000 | 0.2000 |
| 3 | 0.4000 | 0.4000 |
| 5 | 0.4000 | 0.4000 |
| 10 | 0.6000 | 0.8000 |
| 20 | 0.6000 | 0.8000 |

**Expected sources**: PatchAgent

### Expected Chunks (5)

### aa2dbbd3cb711194

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | abstract |
| section_title | Abstract |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Automated program repair (APR) techniques, which aim
to triage and fix software bugs autonomously, have emerged
as powerful tools against vulnerable code.

Recent advance-
ments in large language models (LLMs) have further shown
promising results when applied to APR, especially on patch
generation.

However, without effective fault localization and
patch validation, APR tools specialized in patching alone can-
not handle a more practical and end-to-end setting—given a
concrete input that triggers a vulnerability, how to patch the
program without breaking existing tests?

In this paper, we introduce PATCH AGENT , a novel LLM-
based APR tool that seamlessly integrates fault localization,
patch generation, and validation within a single autonomous
agent.

PATCH AGENT employs a language server, a patch
verifier, and interaction optimization techniques to mimic
human-like reasoning during vulnerability repair.

Evaluated
on a dataset of 178 real-world vulnerabilities, PATCH AGENT
successfully repairs over 90% of the cases, outperforming
state-of-the-art APR tools where applicable.
```

### 18b869161e5d43f4

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 3 |
| page_end | 4 |
| chunk_index | 0 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Automated Program Repair (APR) aims to reduce the manual
effort required to fix vulnerabilities.

In this work, we focus on
4382    34th USENIX Security Symposium USENIX Association
scenarios where a proof-of-concept (PoC) input is available,
accompanied by a vulnerability description and a functional
test suite to ensure the integrity of core logic, thus eliminating
the need for static analysis.

It is important to note that not all
APR approaches adhere to this setting; many rely on static
analysis [31, 105] or exact fault localization [96, 103, 104].

Our PoC-driven approach streamlines integration with fuzzing
which provides PoC inputs, and boosts practicality especially
considering the sheer volume of bugs found in industry-scale
fuzzing campaigns like OSS-Fuzz [85] and syzkaller [91].
2.1 Workflow for PoC-driven APR
Under this setting, the APR process typically involves three
key steps, as described below:
Fault localization.
```

### f5acae00503fb03d

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 6 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Additionally, the pattern-based patch generation
approach may struggle with more complex vulnerabilities,
such as use-after-free scenarios.
2.2 LLMs and Their Applications in APR
Large Language Models (LLMs) have demonstrated excep-
tional capabilities in various natural language processing
tasks, including text classification and generation [12, 81].

By leveraging their sophisticated language modeling abilities,
LLMs can generate coherent text by predicting subsequent to-
USENIX Association 34th USENIX Security Symposium    4383
Vanilla Agent
                According to the address sanitizer report, a 
                global overflow occurred at line 22 in the 
                /source/m3_compile.c.

So I want to view lines 
                21 to 23 in /source/m3_compile.c.
```

### fe679032b0285f24

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 1 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
In
contrast, Automated Program Repair (APR) [46]—especially
source code-based APR tools—aim to patch the buggy code
directly without distorting functionalities nor introducing un-
necessary overhead.

Effective APR tools can significantly
reduce if not eliminate manual effort in patching a security
vulnerability [40], and hence, may help shorten the time frame
between vulnerability discovery and fix rollout.

Over the past decade, APR has received much attention
from researchers [46, 58, 114], especially on patch generation
techniques.

Briefly, a patch generator takes both the buggy
code snippet and some form of bug description (a.k.a., bug
metadata) as input and produces a patch that fixes this bug
without violating generic requirements for patches (e.g., edit
distance [13], idiomaticity [87], or functional specifications
[37]).
```

### 64fa7ff620cfa9e9

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
More recently, the research on patch generator has en-
tered the era of large language models (LLMs) [23, 102, 103],
especially when LLM-based patch generators have outper-
formed conventional ones in results [102].

However, patch generation is only a midstream task in
APR.

Most patch generators require effective fault localiza-
tion (FL)—some even assume perfect FL [96, 103, 104] —to
pinpoint the buggy code snippet.

This introduces two chal-
lenges when applying end-to-end APR to real-world software:
1) FL techniques based on static analysis are prone to high
false positive rates [52], and patching correct code is not only
dangerous but also creates extra work for developers. 2) FL
techniques based on dynamic execution of proof-of-concept
(PoC) test cases face the challenge of slicing a real-world
program into a small bug-enclosing snippet.
```

### Retrieved Top-20

**#1** **[HIT]** — 18b869161e5d43f4 | PatchAgent: A Practical Program Repair Agent .pdf | p.3-4 | sec=related_work | ci=0

```
Automated Program Repair (APR) aims to reduce the manual
effort required to fix vulnerabilities.

In this work, we focus on
4382    34th USENIX Security Symposium USENIX Association
scenarios where a proof-of-concept (PoC) input is available,
accompanied by a vulnerability description and a functional
test suite to ensure the integrity of core logic, thus eliminating
the need for static analysis.

It is important to note that not all
APR approaches adhere to this setting; many rely on static
ana
```

**#2** **[HIT]** — aa2dbbd3cb711194 | PatchAgent: A Practical Program Repair Agent .pdf | p.2-2 | sec=abstract | ci=1

```
Automated program repair (APR) techniques, which aim
to triage and fix software bugs autonomously, have emerged
as powerful tools against vulnerable code.

Recent advance-
ments in large language models (LLMs) have further shown
promising results when applied to APR, especially on patch
generation.

However, without effective fault localization and
patch validation, APR tools specialized in patching alone can-
not handle a more practical and end-to-end setting—given a
concrete input that trigger
```

**#3** — 51a16bf977db18ed | PatchAgent: A Practical Program Repair Agent .pdf | p.5-5 | sec=related_work | ci=12

```
However, it is designed to
be semi-automated, and human efforts have to be introduced
during the repair process.

This huge difference separates it
from our fully automated APR system.

As for patch valida-
tion, researchers explore the possibility of introducing patch
validation feedback [41] into LLMs for improving APR.

However, instead of being a holistic APR tool, these LLM-
based tools mostly focus on using LLMs to implement one
component in the APR process.

Pearce et al. [78] is an LLM-

```

**#4** — 5345ebf2356ec23a | PatchAgent: A Practical Program Repair Agent .pdf | p.4-4 | sec=related_work | ci=2

```
Broadly categorized, a patch generator
can be ① search-based [45, 80], which search for a correct
patch in a predefined patch space scoped by heuristics; ②
constraint-based [24, 31], which employ advanced constraint
solvers or program synthesis techniques to generate candidate
patches that toggle the bug-triggering condition; ③ pattern-
based [54, 97], which applies program fixed templates (a.k.a.,
transformation schema) to buggy code to generate patches,
where the templates can be either manual
```

**#5** — b6ff90ceb372b300 | PatchAgent: A Practical Program Repair Agent .pdf | p.6-6 | sec=related_work | ci=18

```
Consequently,
it does not directly find the definition of opinfo as a human
expert might.

Instead, the agent first locates the definition
of opinfo and then examines the relevant code.

Although
the agent successfully retrieves the definition of opinfo, it
fails to continue locating the definitions of the symbols on
which opinfo depends.

Instead, it arbitrarily assumes that
the overflow is caused by the incorrect usage of opcode and
add a "boundary check" before GetOpInfo, leading it to gen-
e
```

**#6** **[HIT]** — fe679032b0285f24 | PatchAgent: A Practical Program Repair Agent .pdf | p.2-2 | sec=introduction | ci=1

```
In
contrast, Automated Program Repair (APR) [46]—especially
source code-based APR tools—aim to patch the buggy code
directly without distorting functionalities nor introducing un-
necessary overhead.

Effective APR tools can significantly
reduce if not eliminate manual effort in patching a security
vulnerability [40], and hence, may help shorten the time frame
between vulnerability discovery and fix rollout.

Over the past decade, APR has received much attention
from researchers [46, 58, 114], e
```

**#7** — 7f5d0e94961075b4 | PatchAgent: A Practical Program Repair Agent .pdf | p.3-3 | sec=introduction | ci=7

```
Simultaneously, we understand that even with the intro-
duction of these four distinct optimization components in
our PATCH AGENT framework, it does not imply that our sys-
tem has achieved human-comparable capabilities in holis-
tic program repair.

Human experts remain unparalleled in
their ability to address real-world vulnerabilities.

Through
PATCH AGENT , we aim to leverage insights inspired by hu-
man expertise to assist LLMs in improving program repair
tasks.

Looking ahead, we aspire to
```

**#8** — 6c220ba91ceeaadc | PatchAgent: A Practical Program Repair Agent .pdf | p.3-3 | sec=introduction | ci=5

```
The key principle behind PATCH AGENT is to mimic how
human developers might triage and patch a bug, which typ-
ically includes a mixed ordering of actions ranging from ①
comprehending bug reports, ② comprehending code snippets,
③ resolving definitions of symbols, ④ writing a patch, and ⑤
applying the patch for validation.

As most pre-trained LLMs
only support ①, ②, and ④ natively, we additionally program
a language server (for ③), and a patch verifier (for ⑤) as abili-
ties into the LLM agent.

```

**#9** — c27445dd35244d89 | PatchAgent: A Practical Program Repair Agent .pdf | p.14-14 | sec=experiment | ci=18

```
For three temporal
memory bugs, PATCH AGENT successfully repaired two by
inserting validity checks and mitigated the risks of the third
by nullifying the dangling pointer.

For spatial memory bugs,
the generated patch recalculated the object size, performed ad-
vance checks, and added error handling code when necessary.

We plan to manually review and measure these patches gen-
erated by PATCH AGENT .

Once verified to avoid unexpected
outcomes, we submit PRs and maintain ongoing communica-
tion
```

**#10** — bcc06f86c586ec95 | LLMs: Understanding Code Syntax and Semantics for Code.pdf | p.1-1 | sec=introduction | ci=1

```
It has
been widely used in different stages of software development.

For
example, it can be used in generating code snippets that satisfy the
natural language requirements according to the official report [58]
by OpenAI.

Researchers from the SE community started to explore
how to use LLM in SE tasks related to code analysis, for example,
Xia and Zhang [86] proposed ChatRepair, which aims to interact
with ChatGPT to perform automated program repair in a conversa-
tional style.

Tian et al. [71]
```

**#11** — 2b2605fd1c2b89d5 | PatchAgent: A Practical Program Repair Agent .pdf | p.11-11 | sec=experiment | ci=0

```
In this section, we assess PATCH AGENT with the following
research questions.
• RQ 1: How effectively can PATCH AGENT repair vulner-
abilities in real-world programs? (§7.2)
• RQ 2: What is the impact of individual interaction opti-
mization mechanisms on repair performance? (§7.3)
• RQ 3: How does PATCH AGENT perform when repairing
vulnerabilities that LLM has never seen before? (§7.4)
• RQ 4: How efficient is PATCH AGENT in repairing vul-
nerabilities? (§7.5)
Additionally, we present and analy
```

**#12** — 2c0d3d21511e69d5 | PatchAgent: A Practical Program Repair Agent .pdf | p.8-8 | sec=method | ci=6

```
The report purification mechanism is designed to
streamline and clarify the information from the original report,
making it more suitable for LLM processing.

Specifically, we
implemented a parser to transform the original report into a
concise and clear format.

The parser first analyzes the report
to identify the attributes of each symbols.

Next, it removes
unnecessary symbols, such as memory addresses, shadow
memory bytes, and symbols intended solely for human read-
ability.

The parser then
```

**#13** — 06aa5b889bfe46fd | PatchAgent: A Practical Program Repair Agent .pdf | p.11-11 | sec=method | ci=23

```
This table compares the effectiveness of
PATCH AGENT when utilizing different LLMs to repair vulnerabilities.

The results are classified into four main types of errors:
Temporal Errors (including stack overflow, global overflow, and heap overflow), Spatial Errors (including use-after-free,
double free, and invalid free), Null Dereference, and Numeric Errors (including integer overflow and division by zero).

The
Union row represents the combined results of PATCH AGENT across all models, demonst
```

**#14** — 3355d76ca251215e | PatchAgent: A Practical Program Repair Agent .pdf | p.7-8 | sec=method | ci=4

```
Counterexample Feedback: Even with restarting the
patching process, the agent may still generate similar in-
effective patches repeatedly without self-reflection.

Ad-
4386    34th USENIX Security Symposium USENIX Association
dressing the Lack of Variability (❹) in the agent’s ap-
proach, this component makes the agent learn from past
attempts.

It saves failed patches and provides feedback
to prevent the generation of similar ineffective patches
repeatedly, mimicking a developer’s ability to le
```

**#15** — c95ef81655610464 | PatchAgent: A Practical Program Repair Agent .pdf | p.15-15 | sec=discussion | ci=1

```
However, We believePATCH AGENT
can handle various types of vulnerabilities and languages.

Supporting new languages only requires replacing the LSP
(a universal protocol for 50+ languages) backend.

In fact,
the versatility of LSP is why PatchAgent uses it.

Supporting
new vulnerability types requires implementing new parsers
to purify vulnerability-specific reports.

Limited Validation.

Our patch validation method employs
security and functional tests, a widely adopted practice in
software dev
```

**#16** — f3ba8cb9fcf984c2 | PatchAgent: A Practical Program Repair Agent .pdf | p.9-9 | sec=method | ci=11

```
Please repair the bugs.
➋ ➌ 
Initial Prompt
Figure 3: Example of Chain Compression.

The LLM takes the initial prompt as input and starts interacting with the language
server.

The black bold arrows illustrate the interaction without chain compression, while the black dashed arrows represent the
compressed interaction process.

The original interaction chain of length four was compressed into a single interaction.

LLM can only obtain incomplete information.

When
chain compression identifies an
```

**#17** — 1db3df49f958a173 | LLMs: Understanding Code Syntax and Semantics for Code.pdf | p.2-3 | sec=method | ci=2

```
As shown in Figure 2, if we change the variable “arr” to
another variable name “ccounts” while keeping the other content
the same as the former example, ChatGPT cannot fix this buggy
function.

Hence, the conclusion from both examples is inconsistent.

If we just investigate the first example, it seems that ChatGPT can
comprehend program semantics and thus successfully fix this buggy
function.

However, if we further consider the second example, the
conclusion is invalid.

As LLM is becoming pop
```

**#18** — fb2278c5a4af74b6 | PatchAgent: A Practical Program Repair Agent .pdf | p.3-3 | sec=introduction | ci=9

```
In summary, the four main contribution of
our works are as follows:
• We propose a novel LLM-based program repair agent
that leverages a language server and patch verifier to
analyze programs, generate patches, and validate them.
• We introduce four interaction optimizations to enhance
the repair performance of PATCH AGENT .

An ablation
study demonstrates their effectiveness in improving re-
pair performance.
• We evaluate our prototype and provide in-depth analysis,
demonstrating the effective
```

**#19** — 6e29a5dcbe7cbef5 | PatchAgent: A Practical Program Repair Agent .pdf | p.12-12 | sec=experiment | ci=7

```
F.), Zero-Shot (Z.

S.), andPATCH A-
GENT (P.

A.).  indicates that the patch successfully fixed the
vulnerability and passed the functional test.

G #denotes a patch
that fixed the bug but failed the functional tests. #represents
a patch that failed to fix the bug.

For cases where results are
unavailable, a ’/’ is used to denote this.
strong performance across all bug types by leveraging diverse
models, excelling particularly in numeric errors and null deref-
erence with a perfect 100% success
```

**#20** — bd6d810083276fe0 | Give LLMs a Security Course: Securing Retrieval-Augmented.pd | p.13-13 | sec=discussion | ci=2

```
Compared to proactive
methods such as fine-tuning, which is computationally expensive
and slow to accommodate new vulnerabilities, CodeGuarder sup-
ports instant, low-cost updates to the security knowledge base.

Other lightweight proactive approaches, such as applying a second-
pass filter to retrieved content for secure code examples, also fall
short.

Even when only secure examples are presented, LLMs of-
ten generate vulnerable code [45].

This is due to strong insecure
priors acquired durin
```

### Missed Chunks (2 — expected but NOT in top-20)

### f5acae00503fb03d

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 4 |
| page_end | 5 |
| chunk_index | 6 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Additionally, the pattern-based patch generation
approach may struggle with more complex vulnerabilities,
such as use-after-free scenarios.
2.2 LLMs and Their Applications in APR
Large Language Models (LLMs) have demonstrated excep-
tional capabilities in various natural language processing
tasks, including text classification and generation [12, 81].

By leveraging their sophisticated language modeling abilities,
LLMs can generate coherent text by predicting subsequent to-
USENIX Association 34th USENIX Security Symposium    4383
Vanilla Agent
                According to the address sanitizer report, a 
                global overflow occurred at line 22 in the 
                /source/m3_compile.c.

So I want to view lines 
                21 to 23 in /source/m3_compile.c.
```

### 64fa7ff620cfa9e9

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 2 |
| page_end | 2 |
| chunk_index | 2 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
More recently, the research on patch generator has en-
tered the era of large language models (LLMs) [23, 102, 103],
especially when LLM-based patch generators have outper-
formed conventional ones in results [102].

However, patch generation is only a midstream task in
APR.

Most patch generators require effective fault localiza-
tion (FL)—some even assume perfect FL [96, 103, 104] —to
pinpoint the buggy code snippet.

This introduces two chal-
lenges when applying end-to-end APR to real-world software:
1) FL techniques based on static analysis are prone to high
false positive rates [52], and patching correct code is not only
dangerous but also creates extra work for developers. 2) FL
techniques based on dynamic execution of proof-of-concept
(PoC) test cases face the challenge of slicing a real-world
program into a small bug-enclosing snippet.
```

### False Positives (17 — in top-20 but NOT expected)

### 51a16bf977db18ed

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 5 |
| page_end | 5 |
| chunk_index | 12 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
However, it is designed to
be semi-automated, and human efforts have to be introduced
during the repair process.

This huge difference separates it
from our fully automated APR system.

As for patch valida-
tion, researchers explore the possibility of introducing patch
validation feedback [41] into LLMs for improving APR.

However, instead of being a holistic APR tool, these LLM-
based tools mostly focus on using LLMs to implement one
component in the APR process.

Pearce et al. [78] is an LLM-
based APR tool that integrates both patch generation and vali-
dation but lacks FL, as it relies on developer-provided patches
as an oracle for localizing the patch point.

The corresponding
code is then fed to the LLM, and the patch is validated by
replaying the PoC and running a functional test suite.

And
yet, this is the most closely related work in our PoC-driven
APR setting.

Designing new APR workflow [107] without
fault localization (free-FL), under the assistance of LLMs, is
another potential way for APR.
```

### 5345ebf2356ec23a

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 4 |
| page_end | 4 |
| chunk_index | 2 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Broadly categorized, a patch generator
can be ① search-based [45, 80], which search for a correct
patch in a predefined patch space scoped by heuristics; ②
constraint-based [24, 31], which employ advanced constraint
solvers or program synthesis techniques to generate candidate
patches that toggle the bug-triggering condition; ③ pattern-
based [54, 97], which applies program fixed templates (a.k.a.,
transformation schema) to buggy code to generate patches,
where the templates can be either manually defined or mined
automatically; ④ learning-based [36, 111], which learns a
mapping between a buggy code snippet (with optional meta-
data) and the corresponding patch via training and applies
the learned model to generate patches.

It is different from
pattern-based APRs primarily because fix templates are never
explicitly defined in the process.

Patch validation.

Fixation [28] uses distance-bounded weak-
est preconditions to identify partially fixed exceptions in Java
programs.
```

### b6ff90ceb372b300

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | related_work |
| section_title | 2 Background on Automated Program Repair |
| page_start | 6 |
| page_end | 6 |
| chunk_index | 18 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Consequently,
it does not directly find the definition of opinfo as a human
expert might.

Instead, the agent first locates the definition
of opinfo and then examines the relevant code.

Although
the agent successfully retrieves the definition of opinfo, it
fails to continue locating the definitions of the symbols on
which opinfo depends.

Instead, it arbitrarily assumes that
the overflow is caused by the incorrect usage of opcode and
add a "boundary check" before GetOpInfo, leading it to gen-
erate an incorrect patch.

After the patch validation fails, we
reset and rerun the agent, but it continues to generate similar
patches.
3.2 Reflection on Both Processes
Comparing the program repair processes by the vanilla LLM
agent and the human expert, we identified four challenges that
need to be addressed to elevate the vanilla agent’s capabilities
to a level approaching human expertise.
❶ Ineffective Ability Utilization: The vanilla agent struggles
with effectively utilizing the abilities at its disposal.
```

### 7f5d0e94961075b4

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 7 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Simultaneously, we understand that even with the intro-
duction of these four distinct optimization components in
our PATCH AGENT framework, it does not imply that our sys-
tem has achieved human-comparable capabilities in holis-
tic program repair.

Human experts remain unparalleled in
their ability to address real-world vulnerabilities.

Through
PATCH AGENT , we aim to leverage insights inspired by hu-
man expertise to assist LLMs in improving program repair
tasks.

Looking ahead, we aspire to gradually uncover and in-
tegrate more nuanced patching techniques, practices, and tips
from human experts into PATCH AGENT , further enhancing
its effectiveness over time.
```

### 6c220ba91ceeaadc

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 5 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
The key principle behind PATCH AGENT is to mimic how
human developers might triage and patch a bug, which typ-
ically includes a mixed ordering of actions ranging from ①
comprehending bug reports, ② comprehending code snippets,
③ resolving definitions of symbols, ④ writing a patch, and ⑤
applying the patch for validation.

As most pre-trained LLMs
only support ①, ②, and ④ natively, we additionally program
a language server (for ③), and a patch verifier (for ⑤) as abili-
ties into the LLM agent.

Note that we do not claim generality
nor optimality on the set of abilities provided in PATCH A-
GENT as they are based on self-reflection of how members in
the author team patch bugs and we look forward to seeing a
more principled approach in devising the set of abilities.
```

### c27445dd35244d89

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 14 |
| page_end | 14 |
| chunk_index | 18 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
For three temporal
memory bugs, PATCH AGENT successfully repaired two by
inserting validity checks and mitigated the risks of the third
by nullifying the dangling pointer.

For spatial memory bugs,
the generated patch recalculated the object size, performed ad-
vance checks, and added error handling code when necessary.

We plan to manually review and measure these patches gen-
erated by PATCH AGENT .

Once verified to avoid unexpected
outcomes, we submit PRs and maintain ongoing communica-
tion with developers.

The PRs that received responses from
maintainers are summarized in A.2.
7.5 Efficiency of P ATCH AGENT
Token Cost.

Table 5 summarizes the average cost of suc-
cessfully repairing a vulnerability using different models.

Claude-3 Opus achieves the highest repair success rate at
84.83%.

However, it also incurs the highest average cost per
task at $2.15.

Claude-3 Haiku offers the most cost-effective
solution at $0.10 per task, though with a lower repair rate of
71.79%.
```

### bcc06f86c586ec95

| Field | Value |
|-------|-------|
| source_file | LLMs: Understanding Code Syntax and Semantics for Code.pdf |
| section | introduction |
| section_title | 1 INTRODUCTION |
| page_start | 1 |
| page_end | 1 |
| chunk_index | 1 |
| paper_id | LLMs: Understanding Code Syntax and Semantics for Code |

```
It has
been widely used in different stages of software development.

For
example, it can be used in generating code snippets that satisfy the
natural language requirements according to the official report [58]
by OpenAI.

Researchers from the SE community started to explore
how to use LLM in SE tasks related to code analysis, for example,
Xia and Zhang [86] proposed ChatRepair, which aims to interact
with ChatGPT to perform automated program repair in a conversa-
tional style.

Tian et al. [71] conducted an empirical study to discuss
the capability of ChatGPT for code generation, program repair, and
code summarization.

However, although LLM is widely used and
discussed in software engineering, a deep and systematic analysis
of LLM’s capabilities for code syntax and semantics understanding
is vital and worthy of in-depth study.
```

### 2b2605fd1c2b89d5

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 0 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
In this section, we assess PATCH AGENT with the following
research questions.
• RQ 1: How effectively can PATCH AGENT repair vulner-
abilities in real-world programs? (§7.2)
• RQ 2: What is the impact of individual interaction opti-
mization mechanisms on repair performance? (§7.3)
• RQ 3: How does PATCH AGENT perform when repairing
vulnerabilities that LLM has never seen before? (§7.4)
• RQ 4: How efficient is PATCH AGENT in repairing vul-
nerabilities? (§7.5)
Additionally, we present and analyze several case studies
in §A.1 to offer a comprehensive understanding of the effec-
tiveness and limitations of PATCH AGENT .
7.1 Setup
Hardware Environment.

All experiments were conducted
on an AMD EPYC 7763 64-core processor running at 2.445
GHz with 512 GB of RAM and 15 TB of SSD storage.

Large Language Model.
```

### 2c0d3d21511e69d5

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | method |
| section_title | 4.1 Framework |
| page_start | 8 |
| page_end | 8 |
| chunk_index | 6 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
The report purification mechanism is designed to
streamline and clarify the information from the original report,
making it more suitable for LLM processing.

Specifically, we
implemented a parser to transform the original report into a
concise and clear format.

The parser first analyzes the report
to identify the attributes of each symbols.

Next, it removes
unnecessary symbols, such as memory addresses, shadow
memory bytes, and symbols intended solely for human read-
ability.

The parser then recalculates numerical data within
the report, such as access offsets and object sizes in out-of-
bounds bugs, to ensure accuracy and integrity.

Additionally,
it appends clear and concise explanations for complex data
fields or technical terms, such as vulnerability types, stack
traces, and other critical details.
```

### 06aa5b889bfe46fd

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | method |
| section_title | 4.1 Framework |
| page_start | 11 |
| page_end | 11 |
| chunk_index | 23 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
This table compares the effectiveness of
PATCH AGENT when utilizing different LLMs to repair vulnerabilities.

The results are classified into four main types of errors:
Temporal Errors (including stack overflow, global overflow, and heap overflow), Spatial Errors (including use-after-free,
double free, and invalid free), Null Dereference, and Numeric Errors (including integer overflow and division by zero).

The
Union row represents the combined results of PATCH AGENT across all models, demonstrating the overall improvement in repair
accuracy achieved through the collaborative use of multiple models.
that fail validation are treated as counterexamples.

This mech-
anism samples counterexamples after the first workflow itera-
tion and includes them in subsequent prompts, instructing the
LLM not to generate similar patches again.

This method en-
sures the LLM is aware of its previous shortcomings, prevent-
ing it from repeatedly generating similar, ineffective patches.
```

### 3355d76ca251215e

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | method |
| section_title | 4.1 Framework |
| page_start | 7 |
| page_end | 8 |
| chunk_index | 4 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Counterexample Feedback: Even with restarting the
patching process, the agent may still generate similar in-
effective patches repeatedly without self-reflection.

Ad-
4386    34th USENIX Security Symposium USENIX Association
dressing the Lack of Variability (❹) in the agent’s ap-
proach, this component makes the agent learn from past
attempts.

It saves failed patches and provides feedback
to prevent the generation of similar ineffective patches
repeatedly, mimicking a developer’s ability to learn from
mistakes and vary their approach.

These components work in concert to enhance the agent’s
performance by incorporating human-like problem-solving
strategies.

They form a series of interaction optimizations that
guide and restrict the behavior of the native agent, elevating
its capabilities to a level approaching human expertise.

In §5,
we will delve deeper into each component, explaining how
they contribute to more effective program repair.
4.3 Prompt Design
The initial prompt includes both a system prompt and a user
prompt.
```

### c95ef81655610464

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | discussion |
| section_title | 8 Discussion and Limitation |
| page_start | 15 |
| page_end | 15 |
| chunk_index | 1 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
However, We believePATCH AGENT
can handle various types of vulnerabilities and languages.

Supporting new languages only requires replacing the LSP
(a universal protocol for 50+ languages) backend.

In fact,
the versatility of LSP is why PatchAgent uses it.

Supporting
new vulnerability types requires implementing new parsers
to purify vulnerability-specific reports.

Limited Validation.

Our patch validation method employs
security and functional tests, a widely adopted practice in
software development, such as github CI [25].

While this
method is effective and scalable for addressing many vul-
nerability repair scenarios, it has notable limitations.

From
a security standpoint, prior works [100] have revealed that
approximately 5% of security patches written by human in the
Linux kernel may not fully mitigate the vulnerabilities they
aim to address, which suggests that patches generated by AI
agents may also contain similar issues.

Regarding functional-
ity, some projects often update or expand their test cases along-
side patches, which hints that simply using existing functional
tests may not be sufficient.
```

### f3ba8cb9fcf984c2

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | method |
| section_title | 4.1 Framework |
| page_start | 9 |
| page_end | 9 |
| chunk_index | 11 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
Please repair the bugs.
➋ ➌ 
Initial Prompt
Figure 3: Example of Chain Compression.

The LLM takes the initial prompt as input and starts interacting with the language
server.

The black bold arrows illustrate the interaction without chain compression, while the black dashed arrows represent the
compressed interaction process.

The original interaction chain of length four was compressed into a single interaction.

LLM can only obtain incomplete information.

When
chain compression identifies an action as a dominator
action, it automatically generates and executes the sub-
sequent required actions, ensuring the LLM has access
to complete data.
• Heuristic Exploration: LLMs typically need to explore
various symbols (e.g., functions and variables) in the
codebase, requiring many interaction iterations.

This
exploration helps LLMs gather contextual information
about vulnerabilities.

To optimize this process, we de-
signed a heuristic exploration strategy to select these
symbols.
```

### 1db3df49f958a173

| Field | Value |
|-------|-------|
| source_file | LLMs: Understanding Code Syntax and Semantics for Code.pdf |
| section | method |
| section_title | 2 MOTIVATION |
| page_start | 2 |
| page_end | 3 |
| chunk_index | 2 |
| paper_id | LLMs: Understanding Code Syntax and Semantics for Code |

```
As shown in Figure 2, if we change the variable “arr” to
another variable name “ccounts” while keeping the other content
the same as the former example, ChatGPT cannot fix this buggy
function.

Hence, the conclusion from both examples is inconsistent.

If we just investigate the first example, it seems that ChatGPT can
comprehend program semantics and thus successfully fix this buggy
function.

However, if we further consider the second example, the
conclusion is invalid.

As LLM is becoming popular in software engineering (SE) and it
plays a significant role in software development, the comprehension
of its effectiveness is urgent and significant.

Furthermore, under-
standing the capabilities and limitations of LLM for code analysis is
LLMs: Understanding Code Syntax and Semantics for Code Analysis Conference’17, July 2017, Washington, DC, USA
Does this program have a bug?
```

### fb2278c5a4af74b6

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | introduction |
| section_title | 1 Introduction |
| page_start | 3 |
| page_end | 3 |
| chunk_index | 9 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
In summary, the four main contribution of
our works are as follows:
• We propose a novel LLM-based program repair agent
that leverages a language server and patch verifier to
analyze programs, generate patches, and validate them.
• We introduce four interaction optimizations to enhance
the repair performance of PATCH AGENT .

An ablation
study demonstrates their effectiveness in improving re-
pair performance.
• We evaluate our prototype and provide in-depth analysis,
demonstrating the effective and efficient of PATCH A-
GENT , including on vulnerabilities that LLMs have never
encountered before.
• PATCH AGENT has made an impact in the real world.

We successfully used PATCH AGENT to repair numerous
real-world vulnerabilities.
```

### 6e29a5dcbe7cbef5

| Field | Value |
|-------|-------|
| source_file | PatchAgent: A Practical Program Repair Agent .pdf |
| section | experiment |
| section_title | 7 Evaluation |
| page_start | 12 |
| page_end | 12 |
| chunk_index | 7 |
| paper_id | PatchAgent: A Practical Program Repair Agent  |

```
F.), Zero-Shot (Z.

S.), andPATCH A-
GENT (P.

A.).  indicates that the patch successfully fixed the
vulnerability and passed the functional test.

G #denotes a patch
that fixed the bug but failed the functional tests. #represents
a patch that failed to fix the bug.

For cases where results are
unavailable, a ’/’ is used to denote this.
strong performance across all bug types by leveraging diverse
models, excelling particularly in numeric errors and null deref-
erence with a perfect 100% success rate.

For temporal and
spatial errors, the success rates are slightly lower, at 86.96%
and 91.20%, respectively.

These outcomes are consistent with
previous studies [24,31,33,105], which suggest that most null
dereference and numeric errors can often be resolved with a
simple if-check, whereas temporal and spatial bugs typically
require more complex solutions.
```

### bd6d810083276fe0

| Field | Value |
|-------|-------|
| source_file | Give LLMs a Security Course: Securing Retrieval-Augmented.pdf |
| section | discussion |
| section_title | 7.6 Limitations and Failure Case Analysis |
| page_start | 13 |
| page_end | 13 |
| chunk_index | 2 |
| paper_id | Give LLMs a Security Course: Securing Retrieval-Augmented |

```
Compared to proactive
methods such as fine-tuning, which is computationally expensive
and slow to accommodate new vulnerabilities, CodeGuarder sup-
ports instant, low-cost updates to the security knowledge base.

Other lightweight proactive approaches, such as applying a second-
pass filter to retrieved content for secure code examples, also fall
short.

Even when only secure examples are presented, LLMs of-
ten generate vulnerable code [45].

This is due to strong insecure
priors acquired during pre-training that are difficult to override.

Alternatively, reactive strategies, such as post-generation patching,
attempt to repair insecure outputs after generation.

However, once
an insecure pattern has been produced, correcting it is more dif-
ficult and can lead to superficial fixes or the introduction of new
bugs [1].

Post-generation patching is further complicated by its re-
liance on time-consuming automated repair techniques that require
specific vulnerability-triggering inputs [55] to validate the repair.
```

---

# 2. 按问题类型汇总

## comparison (4 questions)

| k | avg strict_recall | avg window_recall |
|---|-------------------|-------------------|
| 1 | 0.0417 | 0.0417 |
| 3 | 0.0417 | 0.0417 |
| 5 | 0.1389 | 0.1389 |
| 10 | 0.1389 | 0.1389 |
| 20 | 0.1389 | 0.2222 |

| ID | Lang | strict@5 | window@5 | strict@10 | window@10 |
|----|------|----------|----------|-----------|----------|
| cross_001_en | EN | 0.00 | 0.00 | 0.00 | 0.00 |
| cross_002_en | EN | 0.33 | 0.33 | 0.33 | 0.33 |
| cross_001_zh | ZH | 0.22 | 0.22 | 0.22 | 0.22 |
| cross_002_zh | ZH | 0.00 | 0.00 | 0.00 | 0.00 |

## fact (2 questions)

| k | avg strict_recall | avg window_recall |
|---|-------------------|-------------------|
| 1 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 |
| 10 | 0.1000 | 0.4000 |
| 20 | 0.2000 | 0.5000 |

| ID | Lang | strict@5 | window@5 | strict@10 | window@10 |
|----|------|----------|----------|-----------|----------|
| single_006_en | EN | 0.00 | 0.00 | 0.00 | 0.00 |
| single_006_zh | ZH | 0.00 | 0.00 | 0.20 | 0.80 |

## method (10 questions)

| k | avg strict_recall | avg window_recall |
|---|-------------------|-------------------|
| 1 | 0.0400 | 0.0600 |
| 3 | 0.0800 | 0.1400 |
| 5 | 0.1200 | 0.2000 |
| 10 | 0.2000 | 0.3600 |
| 20 | 0.3600 | 0.6000 |

| ID | Lang | strict@5 | window@5 | strict@10 | window@10 |
|----|------|----------|----------|-----------|----------|
| single_001_en | EN | 0.20 | 0.40 | 0.20 | 0.40 |
| single_002_en | EN | 0.00 | 0.00 | 0.00 | 0.00 |
| single_003_en | EN | 0.00 | 0.00 | 0.00 | 0.00 |
| single_004_en | EN | 0.20 | 0.60 | 0.20 | 0.60 |
| single_005_en | EN | 0.40 | 0.40 | 0.60 | 0.80 |
| single_001_zh | ZH | 0.00 | 0.00 | 0.00 | 0.00 |
| single_002_zh | ZH | 0.00 | 0.00 | 0.20 | 0.40 |
| single_003_zh | ZH | 0.00 | 0.00 | 0.00 | 0.20 |
| single_004_zh | ZH | 0.20 | 0.20 | 0.40 | 0.60 |
| single_005_zh | ZH | 0.20 | 0.40 | 0.40 | 0.60 |

# 3. 按语言汇总 (EN vs ZH)

## EN (8 questions)

| k | avg strict_recall | avg window_recall |
|---|-------------------|-------------------|
| 1 | 0.0458 | 0.0458 |
| 3 | 0.0958 | 0.1458 |
| 5 | 0.1417 | 0.2167 |
| 10 | 0.1667 | 0.2667 |
| 20 | 0.3167 | 0.5444 |

## ZH (8 questions)

| k | avg strict_recall | avg window_recall |
|---|-------------------|-------------------|
| 1 | 0.0250 | 0.0500 |
| 3 | 0.0250 | 0.0500 |
| 5 | 0.0778 | 0.1028 |
| 10 | 0.1778 | 0.3528 |
| 20 | 0.2528 | 0.4417 |

# 4. 全局汇总 (all answerable questions)

| k | avg strict_recall | avg window_recall |
|---|-------------------|-------------------|
| 1 | 0.0354 | 0.0479 |
| 3 | 0.0604 | 0.0979 |
| 5 | 0.1097 | 0.1597 |
| 10 | 0.1722 | 0.3097 |
| 20 | 0.2847 | 0.4931 |

## 所有题目速览 (sorted by strict@5)

| # | ID | Type | Lang | strict@5 | window@5 | strict@10 | window@10 | strict@20 | window@20 |
|---|----|------|------|----------|----------|-----------|----------|-----------|----------|
| 1 | cross_001_en | comparison | EN | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.22 |
| 2 | single_002_en | method | EN | 0.00 | 0.00 | 0.00 | 0.00 | 0.20 | 0.40 |
| 3 | single_003_en | method | EN | 0.00 | 0.00 | 0.00 | 0.00 | 0.40 | 0.80 |
| 4 | single_006_en | fact | EN | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.20 |
| 5 | cross_002_zh | comparison | ZH | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 6 | single_001_zh | method | ZH | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 7 | single_002_zh | method | ZH | 0.00 | 0.00 | 0.20 | 0.40 | 0.40 | 0.60 |
| 8 | single_003_zh | method | ZH | 0.00 | 0.00 | 0.00 | 0.20 | 0.20 | 0.60 |
| 9 | single_006_zh | fact | ZH | 0.00 | 0.00 | 0.20 | 0.80 | 0.40 | 0.80 |
| 10 | single_001_en | method | EN | 0.20 | 0.40 | 0.20 | 0.40 | 0.40 | 0.60 |
| 11 | single_004_en | method | EN | 0.20 | 0.60 | 0.20 | 0.60 | 0.60 | 1.00 |
| 12 | single_004_zh | method | ZH | 0.20 | 0.20 | 0.40 | 0.60 | 0.40 | 0.60 |
| 13 | single_005_zh | method | ZH | 0.20 | 0.40 | 0.40 | 0.60 | 0.40 | 0.60 |
| 14 | cross_001_zh | comparison | ZH | 0.22 | 0.22 | 0.22 | 0.22 | 0.22 | 0.33 |
| 15 | cross_002_en | comparison | EN | 0.33 | 0.33 | 0.33 | 0.33 | 0.33 | 0.33 |
| 16 | single_005_en | method | EN | 0.40 | 0.40 | 0.60 | 0.80 | 0.60 | 0.80 |
