Some of the available LLMs on OpenRouter with pricing information:

| Provider     | Model (slug)                                                                    |            Input $/M |            Output $/M | Notes                                       |
| ------------ | ------------------------------------------------------------------------------- | -------------------: | --------------------: | ------------------------------------------- |
| OpenAI       | **GPT-4.1** (`openai/gpt-4.1`)                                                  |                 2.00 |                  8.00 | 1M ctx.                                     |
| OpenAI       | **GPT-4.1 Mini** (`openai/gpt-4.1-mini`)                                        |                 0.40 |                  1.60 | 1M ctx.                                     |
| OpenAI       | **GPT-4o** (`openai/gpt-4o`)                                                    | **Starting at** 2.50 | **Starting at** 10.00 | OpenRouter lists “starting at” pricing.     |
| OpenAI       | **o3-mini** (`openai/o3-mini`)                                                  |                 1.10 |                  4.40 | Reasoning/tunable effort.                   |
| OpenAI       | **o3-mini-high** (`openai/o3-mini-high`)                                        |                 1.10 |                  4.40 | Same model, effort default “high”.          |
| OpenAI       | **o3-pro** (`openai/o3-pro`)                                                    |                20.00 |                 80.00 | Reasoning-heavy tier.                       |
| OpenAI       | **o4-mini** (`openai/o4-mini`)                                                  |                 1.10 |                  4.40 | Listed in OpenRouter tools-supported table. |
| xAI          | **Grok 3** (`x-ai/grok-3`)                                                      |                 3.00 |                 15.00 | 131k ctx.                                   |
| xAI          | **Grok 3 Mini** (`x-ai/grok-3-mini`)                                            |                 0.30 |                  0.50 | 131k ctx.                                   |
| Anthropic    | **Claude Sonnet 4** (`anthropic/claude-sonnet-4`)                               | **Starting at** 3.00 | **Starting at** 15.00 | 1M ctx.                                     |
| Anthropic    | **Claude 3.7 Sonnet** (`anthropic/claude-3.7-sonnet`)                           |                 3.00 |                 15.00 | 200k ctx.                                   |
| Anthropic    | **Claude 3.5 Sonnet** (`anthropic/claude-3.5-sonnet`)                           |                 3.00 |                 15.00 | Same Sonnet price tier.                     |
| Anthropic    | **Claude 3.5 Haiku** (`anthropic/claude-3.5-haiku`)                             |                 0.80 |                  4.00 | Fast/cheap tier.                            |
| Anthropic    | **Claude Opus 4** (`anthropic/claude-opus-4`)                                   |                15.00 |                 75.00 | Flagship tier.                              |
| Google       | **Gemini 2.5 Flash** (`google/gemini-2.5-flash`)                                |                 0.30 |                  2.50 | 1,048,576 ctx.                              |
| Google       | **Gemini 2.5 Flash-Lite** (`google/gemini-2.5-flash-lite`)                      |                 0.10 |                  0.40 | Lightweight/low-latency.                    |
| DeepSeek     | **R1** (`deepseek/deepseek-r1`)                                                 |                 0.40 |                  2.00 | Reasoning model.                            |
| DeepSeek     | **V3** (`deepseek/deepseek-chat`)                                               |                 0.30 |                  0.85 | Instruction/chat.                           |
| DeepSeek     | **V3.1** (`deepseek/deepseek-chat-v3.1`)                                        |                 0.20 |                  0.80 | Updated V3 series.                          |
| Meta (Llama) | **Llama 3.3 70B Instruct** (`meta-llama/llama-3.3-70b-instruct`)                |                 0.13 |                  0.39 | 131k ctx.                                   |
| Mistral      | **Mistral Small 3.1 24B Instruct** (`mistralai/mistral-small-3.1-24b-instruct`) |                 0.05 |                  0.10 | Low-cost small model.                       |
| Qwen         | **Qwen2.5 72B Instruct** (`qwen/qwen-2.5-72b-instruct`)                         |                 0.07 |                  0.26 | Strong value large open model.              |
