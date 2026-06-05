| dataset_name | hf_split | reasoning | teacher_model | num_rows | parent_num_rows | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- | --- |
| AlienKevin/SWE-ZERO-12M-trajectories | train | true | ricdomolm/mini-coder-1.7b | 12290800 | 12290800 | 112.000B |
| openbmb/UltraData-SFT-2605 | Code/think | true | not_specified | 2788465 | 15036178 | 69.339B |
| nvidia/Nemotron-Competitive-Programming-v1 | infinibyte_part01 | true | DeepSeek-R1-0528 |  | 3927984 | 60.054B |
| nvidia/Nemotron-Competitive-Programming-v1 | infinibyte_part00 | true | DeepSeek-R1-0528 |  | 3927984 | 60.000B |
| nvidia/Nemotron-Competitive-Programming-v1 | competitive_coding_cpp_part00 | true | DeepSeek-R1-0528 |  | 3927984 | 59.593B |
| nvidia/Nemotron-Competitive-Programming-v1 | competitive_coding_python_part00 | true | DeepSeek-R1-0528 |  | 3927984 | 59.070B |
| nvidia/Nemotron-Competitive-Programming-v1 | competitive_coding_python_part01 | true | DeepSeek-R1-0528 |  | 3927984 | 58.993B |
| nvidia/Nemotron-Competitive-Programming-v1 | competitive_coding_cpp_part01 | true | DeepSeek-R1-0528 |  | 3927984 | 58.827B |
| allenai/dolma3_dolmino_pool | cranecode | true | not_specified |  | 2520000000 | 42.013B |
| allenai/dolma3_dolmino_mix-100B-1025 | cranecode | true | not_specified |  | 14091980 | 22.340B |
| open-thoughts/AgentTrove | train | [true, true, true, true, true, true, true, true, true, true, true, true, true, true] | ["GLM-4.6", "GLM-4.7", "GLM-5.0", "GPT 5.1 Nano", "GPT-4o", "GPT-5", "GPT-5-mini", "GPT-5-nano", "GPT-OSS-120B", "Gemini-2.5-Flash", "Kimi K2.0 Thinking", "Kimi-2.5", "MiniMax M2.0", "Qwen3"] | 1696847 | 1696847 | 17.361B |
| nvidia/Nemotron-SFT-Competitive-Programming-v2 | competitive_coding_python | [true, true] | ["DeepSeek-R1-0528", "QwQ"] | 336568 | 844935 | 11.645B |
| nvidia/Nemotron-SFT-Competitive-Programming-v2 | competitive_coding_cpp | [true, true] | ["DeepSeek-R1-0528", "QwQ"] | 332559 | 844935 | 11.170B |
| nvidia/SWE-Zero-openhands-trajectories | train | true | Qwen3-Coder-480B-A35B-Instruct | 318115 | 318115 | 10.823B |
| nvidia/Nemotron-Pretraining-Specialized-v1.1 | Nemotron-Pretraining-Code-Concepts | [false,false,false,true,false] | ["gpt-oss-20b","gpt-oss-120b","Qwen3-235B-A22B","Qwen3-235B-A22B-Thinking-2507","DeepSeek-v3"] | 15225409 | 19772096 | 8.055B |
| allenai/Dolci-Think-SFT-Python | train | true | QwQ-32B | 1090000 | 1090000 | 6.326B |
| nvidia/Nemotron-Terminal-Corpus | dataset_adapters | true | DeepSeek-V3.2 | 226313 | 366154 | 4.960B |
| openbmb/UltraData-SFT-2605 | Code/no_think | false | not_specified | 3000000 | 15036178 | 2.755B |

## Code SWE Terminal Pretraining Datasets

| readable_name | reasoning | teacher_model | num_rows_total | downloaded | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- |
| Nemotron Spec v1 - Scientific Coding | [true,true,true] | ["Qwen2.5-72B","DeepSeek-V3","Phi-4"] | 905966 | true | 1.308B |
| Nemotron Spec v1.1 - Code Concepts | [false,false,false,true,false] | ["gpt-oss-20b","gpt-oss-120b","Qwen3-235B-A22B","Qwen3-235B-A22B-Thinking-2507","DeepSeek-v3"] | 15225409 | true | 8.055B |
| Dolma3 Dolmino - code splits | true | not_specified | 23016206 | false |  |
| Dolma3 Dolmino 10B 1025 - CraneCode | true | not_specified | 636007 | false |  |
| Nemotron CC Code v1 - data | false | not_specified | 216347017 | false |  |
| Nemotron Pretrain Code - 7 splits | false | not_specified | 1771380197 | false |  |
| Nemotron Pretrain SFT v1 - SFT Code | [true,true,false,false] | ["Qwen3","DeepSeek-V3","Qwen2.5-Coder-32B-Instruct","Mixtral-8x22B-v0.1"] | 56188967 | false |  |

## Code SWE Terminal Non-Pretraining Datasets

| readable_name | reasoning | teacher_model | num_rows_total | downloaded | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- |
| Dolci RL Zero Code 7B | false | QwQ-32B + DeepSeek-R1 + DeepSeek-R1-0528 | 13312 | true |  |
| Dolci Think SFT Python | true | QwQ-32B | 1090000 | true | 6.326B |
| GooseReason - code | false | GPT-5 | 281793 | true |  |
| Nemotron Cascade RL SWE | false | not_specified | 27369 | true |  |
| Nemotron Cascade SFT Stage 1 - code | true | DeepSeek-R1 | 186323 | true | 1.553B |
| Nemotron Cascade SFT Stage 2 - code splits | [true,false,false] | ["DeepSeek-R1-0528","DeepSeek-V3","DeepSeek-V3-0324"] | 322860 | true | 3.027B |
| Nemotron Cascade SFT SWE | true | DeepSeek-R1-0528 | 162262 | true | 1.225B |
| Nemotron Competitive Programming v1 - 6 splits | true | DeepSeek-R1-0528 | 3927984 | true | 356.536B |
| Nemotron CP SFT v2 - 4 splits | [true, true] | ["DeepSeek-R1-0528", "QwQ"] | 844935 | true | 23.401B |
| Nemotron Multilingual SFT v1 - code splits | true | Qwen2.5-14B-Instruct | 825113 | true | 11.659B |
| Nemotron RL Competitive Coding | false | not_specified | 16083 | true |  |
| Nemotron SWE SFT v2 - agentless | [false, true] | ["Qwen3-Coder-480B-A35B-Instruct", "DeepSeek-R1-0528"] | 209976 | true | 1.676B |
| UltraData SFT 2605 - Code non-thinking | false | not_specified | 3000000 | true | 2.755B |
| UltraData SFT 2605 - Code thinking | true | not_specified | 2788465 | true | 69.339B |

## Code SWE Terminal Agent Datasets

| readable_name | reasoning | teacher_model | agent_harness | num_rows_total | downloaded | avg_estimated_tokens |
| --- | --- | --- | --- | --- | --- | --- |
| Agent Traces Swival | false | GPT-5.4 | Swival | 35219 | true |  |
| AgentTrove | [true, true, true, true, true, true, true, true, true, true, true, true, true, true] | ["GLM-4.6", "GLM-4.7", "GLM-5.0", "GPT 5.1 Nano", "GPT-4o", "GPT-5", "GPT-5-mini", "GPT-5-nano", "GPT-OSS-120B", "Gemini-2.5-Flash", "Kimi K2.0 Thinking", "Kimi-2.5", "MiniMax M2.0", "Qwen3"] | Terminus-2 | 1696847 | true | 17.361B |
| code contests noblock minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 6096 | true |  |
| DeepSeek Pro Agent | true | deepseek/deepseek-v4-pro | pi | 4006 | true | 306.178K |
| exp rpt curriculum easy minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 514 | true |  |
| exp rpt e2egit large minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 4975 | true |  |
| exp rpt e2egit v2 minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 497 | true |  |
| exp rpt methods2test large v3 minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 4453 | true |  |
| exp rpt nemotron junit minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 3969 | true |  |
| exp rpt pymethods2test v3 minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 465 | true |  |
| exp rpt stack junit v6 minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 872 | true |  |
| exp rpt unitsyn python large minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 4812 | true |  |
| exp rpt unitsyn python v3 minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 479 | true |  |
| glm 4.6 all puzzles 32ep 131k | true | GLM-4.6 | Terminus-2 | 8963 | true |  |
| GLM 4.6 codeforces 32eps 32k | true | GLM-4.6 | Terminus-2 | 4201 | true |  |
| glm 4.6 dclm baseline terminal traces 32ep 131k | true | GLM-4.6 | Terminus-2 | 6193 | true |  |
| glm 4.6 freelancer 32ep 131k torch | true | GLM-4.6 | Terminus-2 | 9811 | true |  |
| GLM 4.6 freelancer 32eps 131k | true | GLM-4.6 | Terminus-2 | 7597 | true |  |
| GLM 4.6 gemini25flash stackexchange overflow 32ep 512k | true | GLM-4.6 | Terminus-2 | 3280 | true |  |
| GLM 4.6 inferred bugs 32ep 131k nosumm | true | GLM-4.6 | Terminus-2 | 281 | true |  |
| GLM 4.6 inferredbugs 32ep 65k reasoning | true | GLM-4.6 | Terminus-2 | 8172 | true |  |
| glm 4.6 nemo prism | true | GLM-4.6 | Terminus-2 | 6931 | true |  |
| glm 4.6 r2egym 32ep 32k | true | GLM-4.6 | Terminus-2 | 4446 | true |  |
| GLM 4.6 selfinstruct naive 2 32ep 32k | true | GLM-4.6 | Terminus-2 | 2441 | true |  |
| GLM 4.6 stackexchange overflow sandboxes 32eps 65k reasoning | true | GLM-4.6 | Terminus-2 | 9367 | true |  |
| GLM 4.6 stackexchange superuser 32ep 32k | true | GLM-4.6 | Terminus-2 | 3272 | true |  |
| GLM 4.6 stackexchange superuser 32ep 32k etash | true | GLM-4.6 | Terminus-2 | 2140 | true |  |
| glm 4.6 stackexchange tezos 32ep 131k | true | GLM-4.6 | Terminus-2 | 9503 | true |  |
| glm 4.6 staqc 32ep 131k | true | GLM-4.6 | Terminus-2 | 9788 | true |  |
| GLM 4.6 swesmith 32ep 131k nosumm reasoning | true | GLM-4.6 | Terminus-2 | 5964 | true |  |
| GLM 4.6 swesmith 32ep 32k | true | GLM-4.6 | Terminus-2 | 665 | true |  |
| GLM 4.6 taskmaster2 32eps 32k | true | GLM-4.6 | Terminus-2 | 6427 | true |  |
| GLM 4.7 bash textbook tasks maxeps 131k | true | GLM-4.7 | Terminus-2 | 8731 | true |  |
| GLM 4.7 ling coder sft sandboxes 1 maxeps 131k | true | GLM-4.7 | Terminus-2 | 9798 | true |  |
| GLM 4.7 PyMethods2Test Hint | true | GLM-4.7 | Terminus-2 | 13033 | true |  |
| GLM 4.7 PyMethods2Test RL Base 24GPU | true | GLM-4.7 | Terminus-2 | 10842 | true |  |
| GLM 4.7 PyMethods2Test RL Shaped | true | GLM-4.7 | Terminus-2 | 21751 | true |  |
| GLM 4.7 PyMethods2Test RL Staleclip | true | GLM-4.7 | Terminus-2 | 42588 | true |  |
| GLM 4.7 PyMethods2Test RL Zclip | true | GLM-4.7 | Terminus-2 | 18802 | true |  |
| GLM 4.7 stackexchange tezos sandboxes maxeps 131k jup ctx131k | true | GLM-4.7 | Terminus-2 | 4138 | true |  |
| glm46 code feedback maxeps 131k | true | GLM-4.6 | Terminus-2 | 9836 | true |  |
| glm46 defects4j 32ep 131k | true | GLM-4.6 | Terminus-2 | 5806 | true |  |
| glm46 neulab agenttuning alfworld sandboxes maxeps 131k | true | GLM-4.6 | Terminus-2 | 4835 | true |  |
| glm46 neulab synatra 32ep 131k | true | GLM-4.6 | Terminus-2 | 8675 | true |  |
| glm46 qasper maxeps 131k | true | GLM-4.6 | Terminus-2 | 6308 | true |  |
| glm46 swesmith maxeps 131k | true | GLM-4.6 | Terminus-2 | 7617 | true |  |
| Hermes Agent Traces - GLM 5.1, Kimi | [true, true] | ["moonshotai/Kimi-K2.5", "zai-org/GLM-5.1-FP8"] | Hermes Agent | 14701 | true | 431.442M |
| inferredbugs GLM 4.6 32ep 32k | true | GLM-4.6 | Terminus-2 | 4019 | true |  |
| inferredbugs GLM 4.6 32ep 65k | true | GLM-4.6 | Terminus-2 | 4295 | true |  |
| inferredbugs sandboxes verifier minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 6919 | true |  |
| Kimi 2.5 inferredbugs sandboxes maxeps 32k | true | Kimi-2.5 | Terminus-2 | 9792 | true |  |
| Kimi 2.5 r2egym sandboxes maxeps 32k | true | Kimi-2.5 | Terminus-2 | 4316 | true |  |
| Kimi 2.5 SWE-Smith Verified | true | Kimi-2.5 | Terminus-2 | 9356 | true |  |
| llm verifier freelancer minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 7396 | true |  |
| MiniMax M2.7 stackexchange tezos sandboxes maxeps 32k jup | true | MiniMax-M2.7 | Terminus-2 | 1719 | true |  |
| Nemotron Cascade 2 SFT Data - SWE | [true,true,true,true,true,false] | ["DeepSeek-V3.2","DeepSeek-V3.2-Speciale","GPT-OSS-120B","Qwen3-235B-A22B-Thinking-2507","Qwen3-32B","Qwen3-235B-A22B-Instruct-2507"] |  | 21953 | true | 781.564M |
| Nemotron Cascade 2 SFT Data - terminal agent | [true,true,true,true,true,false] | ["DeepSeek-V3.2","DeepSeek-V3.2-Speciale","GPT-OSS-120B","Qwen3-235B-A22B-Thinking-2507","Qwen3-32B","Qwen3-235B-A22B-Instruct-2507"] | Terminus-2 | 82710 | true | 2.476B |
| nemotron code oracle filtered minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 10861 | true |  |
| Nemotron OpenCode SFT - 6 splits | false | Qwen3-Coder-480B-A35B-Instruct | OpenCode CLI | 460254 | true | 6.725B |
| Nemotron RL Super Blends - code splits | true | not_specified | ["responses_api_agents","OpenHands"] | 52105 | true |  |
| Nemotron RL SWE Pivot | true | not_specified | OpenHands | 50308 | true |  |
| Nemotron SWE SFT v2 - OpenHands SWE | [false, true] | ["Qwen3-Coder-480B-A35B-Instruct", "DeepSeek-R1-0528"] | OpenHands | 46278 | true | 1.531B |
| Nemotron SWE v1 - R2E Gym | false | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 24875 | true | 1.365B |
| Nemotron Terminal Corpus - 4 splits | true | DeepSeek-V3.2 | Terminus-2 | 366154 | true | 7.685B |
| Nemotron Terminal Tasks | false | DeepSeek-V3.2 | Terminus-2 | 0 | true |  |
| nl2bash tasks cleaned oracle minimax m27 131k traces | true | MiniMax-M2.7 | Terminus-2 | 1570 | true |  |
| NL2Bash Verified GLM 4.6 Reasoning | true | GLM-4.6 | Terminus-2 | 7037 | true |  |
| OpenThoughts Agent SFT | true | QuantTrio/GLM-4.6-AWQ | Terminus-2 | 15209 | true | 173.539M |
| rl 24GPU base exp rpt pymethods2test large qwen3base GLM 4 7 sw | true | GLM-4.7 | Terminus-2 | 36704 | true |  |
| rl 40GPU base 32b exp rpt codeelo v2 sft GLM 4 7 swesmith | true | GLM-4.7 | Terminus-2 | 331 | true |  |
| Sera 4.5A all domains | true | GLM-4.5-Air | SVG | 152559 | true | 12.655B |
| Sera 4.5A T2 docs/math | true | GLM-4.5-Air | SVG | 38073 | true | 2.526B |
| Sera 4.6 Lite | true | GLM-4.6 | SVG | 74229 | true | 4.442B |
| stackexchange tezos sandboxes Kimi 2.5 smaxeps 32k | true | Kimi-2.5 | Terminus-2 | 8619 | true |  |
| SWE Agent Trajectories | [true, true, true] | ["swe-agent-llama-8b", "swe-agent-llama-70b", "swe-agent-llama-405b"] | SWE-agent | 80036 | true | 1.457B |
| SWE-Hero OpenHands | true | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 34269 | true | 1.923B |
| SWE-Zero 12M Trajectories | true | ricdomolm/mini-coder-1.7b | mini-swe-agent v1 | 12290800 | true | 112.000B |
| SWE-Zero OpenHands | true | Qwen3-Coder-480B-A35B-Instruct | OpenHands | 318115 | true | 10.823B |
