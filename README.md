# AI_Unlocker

> ## *overview*
>
> 一个简单有效的越狱提示词生成对抗模型
>
> 以下是结构设计
>
> ```
> # 总体思路 让模型自己为自己生成提示词
> # 名词解释
> AI_Unlocker指代AI_Unlocker.py
> Model 模型对象
> 其他...
>
> ```

## 第一部分

### Model #引入模型 从(ollama)[https://github.com/ollama/ollama] 开始

## 第二部分

### trick_x #能有多少手段呢？

#### trick_1

#### trick_2

## 第三部分

AI_Unlocker #一键运行


## 第四部分

```
# 以下是 ollama run llama3:8b
# > /show modelfile
# 显示结果如下
TEMPLATE "{{ if .System }}<|start_header_id|>system<|end_header_id|>
{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>
{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>
{{ .Response }}<|eot_id|>"

PARAMETER num_keep 24
PARAMETER stop <|start_header_id|>
PARAMETER stop <|end_header_id|>
PARAMETER stop <|eot_id|>

# 例子 如下
{  
  "System": "欢迎使用我们的系统！",  
  "Prompt": "请问有什么我可以帮助您的吗？",  
  "Response": "我可以回答您的问题或提供相关信息。"  
}

<|start_header_id|>system<|end_header_id|>  
欢迎使用我们的系统！<|eot_id|>  
<|start_header_id|>user<|end_header_id|>  
请问有什么我可以帮助您的吗？<|eot_id|>  
<|start_header_id|>assistant<|end_header_id|>  
我可以回答您的问题或提供相关信息。<|eot_id|>


```
