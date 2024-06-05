from abc import ABCMeta, abstractmethod
from module.interface import BasicModule


class CallerInterface(BasicModule, metaclass=ABCMeta):
    # Notice: 在抽象类中仅提供一个默认的 Prompt，不同的 LLM 可能需要分别优化
    default_system_prompt = """
### 人设
姓名：中小大
性别：女性
年龄：20岁
身份：中山大学大三学生，中山大学介绍官
专业：中山大学软件工程学院软件工程专业
性格特点：活泼开朗，热情友善，善于交流，喜欢探索和分享学校的历史和文化
爱好：写代码、阅读历史书籍、参加社团活动、参观校园景点、与新生交流

### 任务
你会收到一个{用户问题}以及几个参考资料，你需要回答用户的问题。

### 步骤
1. 判断每个参考资料是否与{用户问题}相关。若无关，请忽略；若相关，请参考。
2. 判断每个参考资料是否正确。若不正确，请忽略；若正确，请参考。
3. 根据参考资料以及你自己的知识，生成3个回答,从两个角度对每个回答进行评分：角色匹配程度、{用户问题}匹配程度
4. 每个角度的权重一样，最后计算每个回答的总分，给出总分最高的。最后只给出最好的回答，其他的回答不需要呈现。

### 规则
1. 只回答任何与学校有关的问题
2. 回答30字以内
3. 回答的情感和语气要符合人设
"""

    def __init__(self, system_prompt: str = None):
        super().__init__()
        self._system_prompt = (
            system_prompt
            if system_prompt is not None
            else CallerInterface.default_system_prompt
        )

    def check(self):
        """如果调用后不会报错且能够正常返回，则检验正常。
        在调用该函数时，会重新加载配置文件中的配置信息。
        因此该函数只运行一次即可。

        Returns:
            bool: 是否正常
        """
        self.single_call("hello", with_system_prompt=False)

    # 单条消息的调用（只能输入一条 query）
    @abstractmethod
    def single_call(self, query: str, with_system_prompt: bool = True) -> str: ...
