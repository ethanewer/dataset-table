| dataset_name | hf_split | reasoning | teacher_model | num_rows | parent_num_rows |
| --- | --- | --- | --- | --- | --- |
| allenai/dolma3_dolmino_pool | cranecode | true | not_specified |  | 2520000000 |
| allenai/dolma3_dolmino_pool | code_meta_reasoning | true | not_specified |  | 2520000000 |
| nvidia/Nemotron-CC-Code-v1 | data | false | not_specified | 216347017 | 216347017 |
| nvidia/Nemotron-Pretraining-Code-v1 | Nemotron-Code-Metadata | false | not_specified |  | 935545665 |
| nvidia/Nemotron-Pretraining-Code-v2 | Nemotron-Code-Metadata | false | not_specified |  | 835834532 |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Question-Answering | false | not_specified |  | 835834532 |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Student-Teacher | false | not_specified |  | 835834532 |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Code-Review | false | not_specified |  | 835834532 |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Rewriting | false | not_specified |  | 835834532 |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Transpilation | false | not_specified |  | 835834532 |
| nvidia/Nemotron-Pretraining-SFT-v1 | Nemotron-SFT-Code | [true,true,false,false] | ["Qwen3","DeepSeek-V3","Qwen2.5-Coder-32B-Instruct","Mixtral-8x22B-v0.1"] |  | 299245017 |
| nvidia/Nemotron-Pretraining-Specialized-v1 | Nemotron-Pretraining-Scientific-Coding | [true,true,true] | ["Qwen2.5-72B","DeepSeek-V3","Phi-4"] | 905966 | 60655840 |
| nvidia/Nemotron-Pretraining-Specialized-v1.1 | Nemotron-Pretraining-Code-Concepts | [false,false,false,true,false] | ["gpt-oss-20b","gpt-oss-120b","Qwen3-235B-A22B","Qwen3-235B-A22B-Thinking-2507","DeepSeek-v3"] | 15225409 | 19772096 |

## Code SWE Terminal Pretraining Datasets

| readable_name | reasoning | teacher_model | num_rows_total | downloaded |
| --- | --- | --- | --- | --- |
| Dolma3 Dolmino - code splits | true | not_specified | 23016206 | false |
| Dolma3 Dolmino 10B 1025 - CraneCode | true | not_specified | 636007 | false |
| Nemotron CC Code v1 - data | false | not_specified | 216347017 | false |
| Nemotron Pretrain Code - 7 splits | false | not_specified | 1771380197 | false |
| Nemotron Pretrain SFT v1 - SFT Code | [true,true,false,false] | ["Qwen3","DeepSeek-V3","Qwen2.5-Coder-32B-Instruct","Mixtral-8x22B-v0.1"] | 56188967 | false |
| Nemotron Spec v1 - Scientific Coding | [true,true,true] | ["Qwen2.5-72B","DeepSeek-V3","Phi-4"] | 905966 | false |
| Nemotron Spec v1.1 - Code Concepts | [false,false,false,true,false] | ["gpt-oss-20b","gpt-oss-120b","Qwen3-235B-A22B","Qwen3-235B-A22B-Thinking-2507","DeepSeek-v3"] | 15225409 | false |

## Code SWE Terminal Non-Pretraining Datasets

| readable_name | reasoning | teacher_model | num_rows_total | downloaded |
| --- | --- | --- | --- | --- |
| Dolci Think SFT Python | true | QwQ-32B | 1090000 | false |
| Nemotron Cascade SFT SWE | true | DeepSeek-R1-0528 | 162262 | false |
| Nemotron Cascade SFT Stage 1 - code | true | DeepSeek-R1 | 186323 | false |
| Nemotron Cascade SFT Stage 2 - code splits | [true,false,false] | ["DeepSeek-R1-0528","DeepSeek-V3","DeepSeek-V3-0324"] | 322860 | false |
| Nemotron Competitive Programming v1 - 6 splits | true | DeepSeek-R1-0528 | 3927984 | true |
| Nemotron CP SFT v2 - 4 splits | [true, true] | ["DeepSeek-R1-0528", "QwQ"] | 844935 | true |
| Nemotron Multilingual SFT v1 - code splits | true | Qwen2.5-14B-Instruct | 825113 | true |
| Nemotron SWE SFT v2 - agentless | [false, true] | ["Qwen3-Coder-480B-A35B-Instruct", "DeepSeek-R1-0528"] | 209976 | true |
| UltraData SFT 2605 - Code non-thinking | false | not_specified | 3000000 | false |
| UltraData SFT 2605 - Code thinking | true | not_specified | 2788465 | false |

## Code SWE Terminal Agent Datasets

| readable_name | reasoning | teacher_model | agent_harness | num_rows_total | downloaded |
| --- | --- | --- | --- | --- | --- |
| SWE-Zero 12M Trajectories | true | ricdomolm/mini-coder-1.7b | mini-swe-agent v1 | 12290800 | false |
| OpenThoughts Agent SFT | true | QuantTrio/GLM-4.6-AWQ | Terminus-2 | 15209 | false |
| DeepSeek Pro Agent | true | deepseek/deepseek-v4-pro | pi | 4006 | false |
| Sera 4.6 Lite | true | GLM-4.6 | SVG | 74229 | false |
| Sera 4.5A all domains | true | GLM-4.5-Air | SVG | 152559 | false |
| Sera 4.5A T2 docs/math | true | GLM-4.5-Air | SVG | 38073 | false |
| Hermes Agent Traces - GLM 5.1, Kimi | [true, true] | ["moonshotai/Kimi-K2.5", "zai-org/GLM-5.1-FP8"] | Hermes Agent | 14701 | false |
| SWE Agent Trajectories | [true, true, true] | ["swe-agent-llama-8b", "swe-agent-llama-70b", "swe-agent-llama-405b"] | SWE-agent | 80036 | false |
| Nemotron Cascade 2 SFT Data - SWE | [true,true,true,true,true,false] | ["DeepSeek-V3.2","DeepSeek-V3.2-Speciale","GPT-OSS-120B","Qwen3-235B-A22B-Thinking-2507","Qwen3-32B","Qwen3-235B-A22B-Instruct-2507"] |  | 21953 | false |
| Nemotron Cascade 2 SFT Data - terminal agent | [true,true,true,true,true,false] | ["DeepSeek-V3.2","DeepSeek-V3.2-Speciale","GPT-OSS-120B","Qwen3-235B-A22B-Thinking-2507","Qwen3-32B","Qwen3-235B-A22B-Instruct-2507"] | Terminus-2 | 82710 | false |
| Nemotron OpenCode SFT - 6 splits | false | Qwen3-Coder-480B-A35B-Instruct | OpenCode CLI | 460254 | true |
| Nemotron SWE SFT v2 - OpenHands SWE | [false, true] | ["Qwen3-Coder-480B-A35B-Instruct", "DeepSeek-R1-0528"] | OpenHands | 46278 | true |
| Nemotron SWE v1 - R2E Gym | false | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 24875 | true |
| Nemotron Terminal Corpus - 4 splits | true | DeepSeek-V3.2 | Terminus-2 | 366154 | true |
| SWE-Hero OpenHands | true | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 34269 | false |
| SWE-Zero OpenHands | true | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 318115 | false |
| AgentTrove | [true, true, true, true, true, true, true, true, true, true, true, true, true, true] | ["GLM-4.6", "GLM-4.7", "GLM-5.0", "GPT 5.1 Nano", "GPT-4o", "GPT-5", "GPT-5-mini", "GPT-5-nano", "GPT-OSS-120B", "Gemini-2.5-Flash", "Kimi K2.0 Thinking", "Kimi-2.5", "MiniMax M2.0", "Qwen3"] | Terminus-2 | 1696847 | false |
