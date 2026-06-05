| dataset_name | hf_split | reasoning | teacher_model | num_rows | parent_num_rows | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- | --- |
| nvidia/Nemotron-Pretraining-Specialized-v1.1 | Nemotron-Pretraining-Code-Concepts | [false,false,false,true,false] | ["gpt-oss-20b","gpt-oss-120b","Qwen3-235B-A22B","Qwen3-235B-A22B-Thinking-2507","DeepSeek-v3"] | 15225409 | 19772096 | 8.055B |
| nvidia/Nemotron-CC-Code-v1 | data | false | not_specified | 216347017 | 216347017 |  |
| nvidia/Nemotron-Pretraining-Code-v2 | Nemotron-Code-Metadata | false | not_specified |  | 835834532 |  |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Question-Answering | false | not_specified |  | 835834532 |  |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Student-Teacher | false | not_specified |  | 835834532 |  |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Code-Review | false | not_specified |  | 835834532 |  |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Rewriting | false | not_specified |  | 835834532 |  |
| nvidia/Nemotron-Pretraining-Code-v2 | Synthetic-Transpilation | false | not_specified |  | 835834532 |  |
| nvidia/Nemotron-Pretraining-Specialized-v1 | Nemotron-Pretraining-Scientific-Coding | [true,true,true] | ["Qwen2.5-72B","DeepSeek-V3","Phi-4"] | 905966 | 60655840 | 1.308B |
| nvidia/Nemotron-Pretraining-SFT-v1 | Nemotron-SFT-Code | [true,true,false,false] | ["Qwen3","DeepSeek-V3","Qwen2.5-Coder-32B-Instruct","Mixtral-8x22B-v0.1"] |  | 299245017 |  |
| nvidia/Nemotron-Pretraining-Code-v1 | Synthetic-Code | false | not_specified |  | 935545665 |  |
| nvidia/Nemotron-Pretraining-Code-v1 | Nemotron-Code-Metadata | false | not_specified |  | 935545665 |  |
| allenai/dolma3_dolmino_pool | cranecode | true | not_specified |  | 2520000000 | 42.013B |
| allenai/dolma3_dolmino_pool | code_meta_reasoning | true | not_specified |  | 2520000000 | 1.293B |
| allenai/dolma3_dolmino_mix-100B-1025 | cranecode | true | not_specified |  | 14091980 | 22.340B |
| allenai/dolma3_dolmino_mix-100B-1025 | code_meta_reasoning | true | not_specified |  | 14091980 | 512.761M |
| allenai/dolma3_dolmino_mix-10B-1025 | code_meta_reasoning | true | not_specified |  | 5037781 |  |
| allenai/dolma3_dolmino_mix-10B-1025 | cranecode | true | not_specified | 636007 | 5037781 |  |

## Code SWE Terminal Pretraining Datasets

| readable_name | reasoning | teacher_model | num_rows_total | downloaded | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- |
| Dolma3 Dolmino - code splits | true | not_specified | 23016206 | false |  |
| Dolma3 Dolmino 10B 1025 - CraneCode | true | not_specified | 636007 | false |  |
| Nemotron CC Code v1 - data | false | not_specified | 216347017 | false |  |
| Nemotron Pretrain Code - 7 splits | false | not_specified | 1771380197 | false |  |
| Nemotron Pretrain SFT v1 - SFT Code | [true,true,false,false] | ["Qwen3","DeepSeek-V3","Qwen2.5-Coder-32B-Instruct","Mixtral-8x22B-v0.1"] | 56188967 | false |  |
| Nemotron Spec v1 - Scientific Coding | [true,true,true] | ["Qwen2.5-72B","DeepSeek-V3","Phi-4"] | 905966 | true | 1.308B |
| Nemotron Spec v1.1 - Code Concepts | [false,false,false,true,false] | ["gpt-oss-20b","gpt-oss-120b","Qwen3-235B-A22B","Qwen3-235B-A22B-Thinking-2507","DeepSeek-v3"] | 15225409 | true | 8.055B |

## Code SWE Terminal Non-Pretraining Datasets

| readable_name | reasoning | teacher_model | num_rows_total | downloaded | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- |
| Dolci RL Zero Code 7B | false | QwQ-32B + DeepSeek-R1 + DeepSeek-R1-0528 | 13312 | true |  |
| Dolci Think SFT Python | true | QwQ-32B | 1090000 | true | 6.326B |
| Nemotron Cascade RL SWE | false | not_specified | 27369 | true |  |
| Nemotron Cascade SFT SWE | true | DeepSeek-R1-0528 | 162262 | true | 1.225B |
| Nemotron Cascade SFT Stage 1 - code | true | DeepSeek-R1 | 186323 | true | 1.553B |
| Nemotron Cascade SFT Stage 2 - code splits | [true,false,false] | ["DeepSeek-R1-0528","DeepSeek-V3","DeepSeek-V3-0324"] | 322860 | true | 3.027B |
| Nemotron Competitive Programming v1 - 6 splits | true | DeepSeek-R1-0528 | 3927984 | true | 356.536B |
| Nemotron RL Competitive Coding | false | not_specified | 16083 | true |  |
| GooseReason - code | false | GPT-5 | 281793 | true |  |
| Nemotron CP SFT v2 - 4 splits | [true, true] | ["DeepSeek-R1-0528", "QwQ"] | 844935 | true | 23.401B |
| Nemotron Multilingual SFT v1 - code splits | true | Qwen2.5-14B-Instruct | 825113 | true | 11.659B |
| Nemotron SWE SFT v2 - agentless | [false, true] | ["Qwen3-Coder-480B-A35B-Instruct", "DeepSeek-R1-0528"] | 209976 | true | 1.676B |
| UltraData SFT 2605 - Code non-thinking | false | not_specified | 3000000 | true | 2.755B |
| UltraData SFT 2605 - Code thinking | true | not_specified | 2788465 | true | 69.339B |

## Code SWE Terminal Agent Datasets

| readable_name | reasoning | teacher_model | agent_harness | num_rows_total | downloaded | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- | --- |
| SWE-Zero 12M Trajectories | true | ricdomolm/mini-coder-1.7b | mini-swe-agent v1 | 12290800 | true | 112.000B |
| OpenThoughts Agent SFT | true | QuantTrio/GLM-4.6-AWQ | Terminus-2 | 15209 | true | 173.539M |
| DeepSeek Pro Agent | true | deepseek/deepseek-v4-pro | pi | 4006 | true | 306178 |
| Sera 4.6 Lite | true | GLM-4.6 | SVG | 74229 | true | 4.442B |
| Sera 4.5A all domains | true | GLM-4.5-Air | SVG | 152559 | true | 12.655B |
| Sera 4.5A T2 docs/math | true | GLM-4.5-Air | SVG | 38073 | true | 2.526B |
| Agent Traces Swival | false | GPT-5.4 | Swival | 35219 | false |  |
| Hermes Agent Traces - GLM 5.1, Kimi | [true, true] | ["moonshotai/Kimi-K2.5", "zai-org/GLM-5.1-FP8"] | Hermes Agent | 14701 | true | 431.442M |
| SWE Agent Trajectories | [true, true, true] | ["swe-agent-llama-8b", "swe-agent-llama-70b", "swe-agent-llama-405b"] | SWE-agent | 80036 | true | 1.457B |
| Nemotron Cascade 2 SFT Data - SWE | [true,true,true,true,true,false] | ["DeepSeek-V3.2","DeepSeek-V3.2-Speciale","GPT-OSS-120B","Qwen3-235B-A22B-Thinking-2507","Qwen3-32B","Qwen3-235B-A22B-Instruct-2507"] |  | 21953 | true | 781.564M |
| Nemotron Cascade 2 SFT Data - terminal agent | [true,true,true,true,true,false] | ["DeepSeek-V3.2","DeepSeek-V3.2-Speciale","GPT-OSS-120B","Qwen3-235B-A22B-Thinking-2507","Qwen3-32B","Qwen3-235B-A22B-Instruct-2507"] | Terminus-2 | 82710 | true | 2.476B |
| Nemotron RL SWE Pivot | true | not_specified | OpenHands | 50308 | true |  |
| Nemotron RL Super Blends - code splits | true | not_specified | ["responses_api_agents","OpenHands"] | 52105 | true |  |
| Nemotron OpenCode SFT - 6 splits | false | Qwen3-Coder-480B-A35B-Instruct | OpenCode CLI | 460254 | true | 6.725B |
| Nemotron SWE SFT v2 - OpenHands SWE | [false, true] | ["Qwen3-Coder-480B-A35B-Instruct", "DeepSeek-R1-0528"] | OpenHands | 46278 | true | 1.531B |
| Nemotron SWE v1 - R2E Gym | false | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 24875 | true | 1.365B |
| Nemotron Terminal Corpus - 4 splits | true | DeepSeek-V3.2 | Terminus-2 | 366154 | true | 7.685B |
| Nemotron Terminal Tasks | false | DeepSeek-V3.2 | Terminus-2 | 0 | true |  |
| SWE-Hero OpenHands | true | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 34269 | true | 1.923B |
| SWE-Zero OpenHands | true | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 318115 | true | 10.823B |
| AgentTrove | [true, true, true, true, true, true, true, true, true, true, true, true, true, true] | ["GLM-4.6", "GLM-4.7", "GLM-5.0", "GPT 5.1 Nano", "GPT-4o", "GPT-5", "GPT-5-mini", "GPT-5-nano", "GPT-OSS-120B", "Gemini-2.5-Flash", "Kimi K2.0 Thinking", "Kimi-2.5", "MiniMax M2.0", "Qwen3"] | Terminus-2 | 1696847 | true | 17.361B |
