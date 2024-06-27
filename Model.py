import requests
import json

class OllamaModel:
    def __init__(self, model_name, host="127.0.0.1", port=11434):
        self.model_name =  model_name # 模型名字 比如 llama3:8b 不可以少了:8b 
        self.base_url = f"http://{host}:{port}/api"
       

    def generate_completion(self, prompt, stream=False):  # 已测试,功能正常 6/27/2024
        url = f"{self.base_url}/generate"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.model_name, "prompt": prompt, "stream": stream}

        try:
            if stream:
                with requests.post(url, json=payload, headers=headers, stream=True) as response:
                    response.raise_for_status()
                    for raw_response in response.iter_lines():
                        if raw_response:
                            try:
                                data = json.loads(raw_response.decode('utf-8'))
                                response_part = data.get('response', '')
                                print(response_part, end='', flush=True)
                            except json.JSONDecodeError:
                                print(f"Failed to parse JSON object: {raw_response}")
            else:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data.get('response', '')

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def create_model(self, model_config):  # 不打算测试
        url = f"{self.base_url}/creat"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.model_name, **model_config}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model {self.model_name} created successfully.")
        except requests.RequestException as e:
            print(f"An error occurred while creating the model: {e}")

    def list_local_models(self): #  已测试正常 6/27/2024
        url = f"{self.base_url}/tags"
        try:
            response = requests.get(url)
            response.raise_for_status()
            models = response.json()
            # 提取name字段
            model_names = []
            for model in models["models"]:
                model_names.append(model["name"])
            return model_names
        except requests.RequestException as e:
            print(f"An error occurred while listing the models: {e}")
            return []


    def show_model_info(self, name):  #已测试正常 6/27/2024
        url = f"{self.base_url}/show"
        payload = {"name": name}
        try:
            response = requests.post(url, json=payload)  # 使用 params 参数传递查询参数
            response.raise_for_status()
            model_info = response.json()
            return model_info
        except requests.RequestException as e:
            print(f"An error occurred while retrieving the model information: {e}")
            return {}
    
    def copy_model(self, source_model): # 不打算测试
        url = f"{self.base_url}/copy"
        headers = {"Content-Type": "application/json"}
        payload = {"source_model": source_model, "destination_model": self.model_name}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model {self.model_name} copied successfully from {source_model}.")
        except requests.RequestException as e:
            print(f"An error occurred while copying the model: {e}")

    def delete_model(self): # 不打算测试
        url = f"{self.base_url}/delete"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            print(f"Model {self.model_name} deleted successfully.")
        except requests.RequestException as e:
            print(f"An error occurred while deleting the model: {e}")
    
    """
    name:要拉取的模型的名称
    insecure:(可选)允许不安全的库连接。仅当您在开发过程中从自己的库中提取时才使用此功能。
    stream:(可选)如果false响应将作为单个响应对象而不是对象流返回
    
    """

    def pull_model(self, name): # 不打算测试

        url = f"{self.base_url}/pull"
        headers = {"Content-Type": "application/json"}
        payload = {"name": name}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model {name} pulled successfully .")
        except requests.RequestException as e:
            print(f"An error occurred while pulling the model: {e}")

    def push_model(self, name): #不打算测试
        url = f"{self.base_url}/push"
        headers = {"Content-Type": "application/json"}
        payload = {"name": name}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model {name} pushed successfully.")
        except requests.RequestException as e:
            print(f"An error occurred while pushing the model: {e}")
    """"
    model：生成嵌入的模型名称
    prompt：要生成嵌入的文本
    用于从指定模型生成文本的嵌入（embedding）。文本嵌入是将文本转化为数值向量的过程，这些向量可以在机器学习和自然语言处理任务中用于表示和操作文本数据。
    """
    """我决定把这个单独拿出来做文章
    def generate_embeddings(self, prompt):
        url = f"{self.base_url}/embeddings"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.model_name, "prompt": prompt}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            embeddings = response.json()

            # 将嵌入向量保存到文件中
            with open("embeddings.json", "w") as f:
                json.dump(embeddings, f, indent=4)

            # 仅打印成功消息
            print("Embeddings have been saved to embeddings.json")

            return embeddings
        except requests.RequestException as e:
            print(f"An error occurred while generating embeddings: {e}")
            return {}

        """

    def list_running_model(self): # 已测试功能正常 6/27/2024
        url = f"{self.base_url}/ps"
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()

            # 提取name字段
            for running_model   in json_data["models"]:
                running_model=running_model  ["name"]

            return running_model  # 返回 运行中的模型名
        
        except requests.RequestException as e:
            print(f"An error occurred while listing running models: {e}")
            return []

"""
API接口如下
This class provides APIs for interacting with a model. It includes methods for creating, copying, pulling, pushing, and deleting models, as well as generating embeddings and listing running models.
    API Interface:
        * Generate a completion
        * Generate a chat completion
        * Create a Model
        * List Local Models
        * Show Model Information
        * Copy a Model
        * Delete a Model
        * Pull a Model
        * Push a Model
        * Generate Embeddings
        * List Running Models
    # API 接口:
        # 生成完成
        # 生成聊天完成
        # 创建模型
        # 列出本地模型
        # 展示模型信息
        # 拷贝模型
        # 删除模型
        # 拉取模型
        # 推送模型
        # 生成嵌入向量
        # 列出运行中的模型
"""

class EmbeddingGenerator:
    def __init__(self, base_url, model_name, index_file="index.json"):
        self.base_url = base_url
        self.model_name = model_name
        self.index_file = index_file
        # 创建索引文件，如果不存在的话
        if not os.path.exists(self.index_file):
            with open(self.index_file, 'w') as f:
                json.dump([], f)

    def generate_embeddings(self, prompt):
        url = f"{self.base_url}/embeddings"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.model_name, "prompt": prompt}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            embeddings_response = response.json()

            # 生成文件名
            safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{self.model_name}_{safe_prompt}_{timestamp}.json"

            # 将嵌入向量保存到文件中
            with open(file_name, "w") as file:
                json.dump(embeddings_response, file, indent=4)

            # 更新索引文件
            with open(self.index_file, 'r+') as f:
                index = json.load(f)
                index_entry = {
                    "file_name": file_name,
                    "timestamp": timestamp,
                    "model_name": self.model_name,
                    "prompt": prompt
                }
                index.append(index_entry)
                f.seek(0)
                json.dump(index, f, indent=4)

            # 打印成功消息
            print(f"Embeddings have been saved to {file_name}")
            
            return embeddings_response
        except requests.RequestException as error:
            print(f"An error occurred while generating embeddings: {error}")
            return {}

    def get_embedding_file(self, query_prompt):
        with open(self.index_file, 'r') as f:
            index = json.load(f)
            for entry in index:
                if query_prompt in entry['prompt']:
                    return entry['file_name']
        return None




"""
# Example usage:
# Initialize the model
ollama_model = OllamaModel(model_name="llama3:8b")

# Generate completion with streaming
ollama_model.generate_completion("Why is the sky blue?", stream=True)

# Generate completion without streaming
final_response = ollama_model.generate_completion("Why is the sky blue?", stream=False)
print(final_response)

# List local models
models = ollama_model.list_local_models()
print(models)

# Show model information
model_info = ollama_model.show_model_info()
print(model_info)

"""
ollama_model = OllamaModel(model_name="llama3:8b")

print(ollama_model.generate_embeddings("你好"))