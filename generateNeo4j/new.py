
from ltp import LTP
from typing import List, Tuple, Dict


# 依存关系映射表
relation_mapping = {
    "SBV": "主谓关系",
    "HED": "谓词关系",
    "RAD": "连词关系",
    "ATT": "修饰关系",
    "VOB": "动宾关系",
    "WP": "疑问关系",
    "ADV": "状语关系",
    "COO": "并列关系"
}



# LTP依存关系字典
LTP_DEP_RELATIONS = {
    # 核心论元关系
    'SBV': '主谓关系',
    'VOB': '动宾关系',

    # 核心谓词扩展
    'FOB': '前置宾语',
    'DBL': '兼语',
    'IOB': '间接宾语',

    # 名词性修饰关系
    'ATT': '定中关系/属性关系',
    'QUN': '数量关系',

    # 谓词性修饰关系
    'ADV': '状中关系',
    'CMP': '动补关系',
    'LAD': '左附加关系',
    'RAD': '右附加关系',

    # 特殊关系
    'POB': '介宾关系',
    'IS': '独立结构',
    'HED': '核心词',

    # 并列关系
    'COO': '并列关系',

    # 标点符号
    'WP': '标点符号关系'
}


class DependencyAnalyzer:
    def __init__(self,ltp):
        self.ltp = ltp

        # 定义关键依存关系
        self.key_relations = {
            "SBV": "主谓关系",
            "VOB": "动宾关系",
            "COO": "并列关系",
            "POB": "介宾关系"
        }
        self.up_relations = {
            'ATT': '定中关系/属性关系',
            "POB": "介宾关系"
        }

    def analyze_dependency(self, sentence: str, word1: str, word2: str) -> Tuple[int, str]:
        """
        分析两个词的依存关系，返回关系类型代码和描述
        返回值: (代码, 描述)
            代码: 0-直接相关, 1-子树相关, 2-主谓相关, 3-短语相关, 4-并列相关, -1-无关
        """
        # 进行分词和依存分析
        result = self.ltp.pipeline(sentence, tasks=["cws", "dep"])
        words = result.get("cws")
        deps = result.get("dep")
        #print(f"words:{words}")
        if not words or "head" not in deps or "label" not in deps:
            return -1, "分析失败"

        heads = deps["head"]
        labels = deps["label"]
        #print(f"heads:{heads}")
        #print(f"labels:{labels}")
        # 获取目标词的索引
        word1_indices = [i for i, w in enumerate(words) if w == word1]
        word2_indices = [i for i, w in enumerate(words) if w == word2]

        if not word1_indices or not word2_indices:
            return -1, "词语未找到"

        # 先让word1作为起始词分析
        code1, desc1 = self._analyze_single_direction(word1_indices, word2_indices, heads, labels)
        if code1 >= 0:  # 如果找到关系就直接返回
            print(f"Word1 -> Word2: {code1}")
            return code1, f"{desc1}"

        # 如果word1作为起始词没找到关系，让word2作为起始词分析
        code2, desc2 = self._analyze_single_direction(word2_indices, word1_indices, heads, labels)
        if code2 >= 0:  # 如果找到关系就返回
            print(f"Word2 -> Word1: {code2}")
            return code2, f"{desc2}"

        return -1, "无关联"

    def _analyze_single_direction(self, start_indices: List[int], target_indices: List[int],
                                heads: List[int], labels: List[str]) -> Tuple[int, str]:
        """单向分析两个词的依存关系"""
        for idx1 in start_indices:
            for idx2 in target_indices:
                # 检查直接关系（规则0）
                """
                0.首先查找第一个词直接相连的词，比如哪些词指向它，或它指向其他词代表直接相关，若第二个词与第一个词直接相关，则认为相关，返回0.
                1.首先根据第一个词查找第一个词的子树中是否有另一个目标词，有则相关，返回数字码

                2.如果没有在第一个词的子树中找到另一个词，则判断第一个词有没有主谓关系。若第一个词存在主谓关系，则找与其保持主谓关系的那个词的子树中查找另一个单词，若存在则认为相关，返回数字码2
                3.若上面三个都没有，则根据第一个词往上查找到存在(并列关系、谓宾关系、主谓关系、介宾关系）的词为止，认为第一个词与新查找到的词的子树结构的词相关，相当于是找相关的短语中是否有该词。若相关则返回数字码3


                4.若第一个词没有主谓关系,则查找第一个词是否存在并列关系，若存在并列关系，递归找个并列词的所有关系中是否存在第二个词（相当于把这个流程从头递归一遍），若找到则返回数字码3.
                5一个词如果是与其上一个词有定中关系（递归查定中，介宾），然后修饰中心语，中心语又有主谓关系，则找谓语的，动宾关系（主谓宾相关），并列关系（主谓并列相关），状中关系（主谓状相关），动补（主谓补相关）关系，这三个下面的词与其相关   。返回数字码3，


                6一个词如果是与其上一个词有定中关系（递归查定中，介宾都可以），(或直接有动宾关系)查找到存在动宾结构的为止，找这个宾语下面有没有词与其相关（若有则返回同一宾语内相关），若没找到则找动词有没有主谓关系，若有则返回（主谓宾关系）。若没有则找动词的整个树下面有没有这个词，若有则返回（间接谓宾相关），若还没找到，则再递归查找到没有并列，（若有并列动词的下面相关，则返回并列动词宾语相关）返回数字码3

                7.若最终走完上面流程都没找到，则返回-1，认为不相干

                """
                if self._check_direct_relation(idx1, idx2, heads):
                    return 0, "直接相连相关"

                # 检查子树关系（规则1）
                if self._check_subtree_relation(idx1, idx2, heads, labels):
                    return 1, "子树直接相关"

                # 检查主谓关系扩展（规则2）
                if self._check_subject_predicate_extension(idx1, idx2, heads, labels):
                    return 2, "直接主谓相关"

                # 检查短语关系（规则3）
                if self._check_phrase_relation(idx1, idx2, heads, labels):
                    return 3, "短语相关"

                # 检查并列关系扩展（规则4）
                if self._check_coordinate_extension(idx1, idx2, heads, labels):
                    return 3, "并列词相关"

                # 检查定中关系链到主谓关系扩展（规则5）
                if self._check_attribute_subject_predicate_relation(idx1, idx2, heads, labels):
                    return 3, "主谓宾相关"

                # 检查定中关系链到动宾关系扩展（规则6）
                result = self._check_attribute_object_relation(idx1, idx2, heads, labels)
                if result:
                    return 3, "间接谓宾相关"

        return -1, "无关联"

    def _check_direct_relation(self, idx1: int, idx2: int, heads: List[int]) -> bool:
        """检查两个词是否直接相连"""
        return heads[idx1] == idx2 + 1 or heads[idx2] == idx1 + 1

    def _check_subtree_relation(self, idx1: int, idx2: int, heads: List[int], labels: List[str]) -> bool:
        """检查word2是否在word1的子树中"""

        def get_subtree(root_idx):
            subtree = set()
            for i, head in enumerate(heads):
                if head == root_idx + 1:
                    subtree.add(i)
                    subtree.update(get_subtree(i))
            return subtree

        subtrees = get_subtree(idx1)
        #print(f"subtrees:{subtrees}")
        return idx2 in subtrees

    def _check_subject_predicate_extension(self, idx1: int, idx2: int, heads: List[int], labels: List[str]) -> bool:
        """检查通过主谓关系扩展的关联"""
        if labels[idx1] != "SBV":
            return False

        predicate_idx = heads[idx1] - 1
        return self._check_subtree_relation(predicate_idx, idx2, heads, labels)


    def _check_phrase_relation(self, idx1: int, idx2: int, heads: List[int], labels: List[str]) -> bool:
        """
        检查是否在相关短语中
        1. 先从第一个词往上查找，直到找到具有关键依存关系的词
        2. 然后检查该词的整个子树中是否包含第二个词
        """
        def find_phrase_head(idx):
            """往上查找直到找到具有关键关系的词"""
            current = idx
            # 当前词的head指向的词的索引是heads[current] - 1
            while current >= 0:
                # 先检查当前词是否具有关键关系
                if labels[current] in self.key_relations:
                    return current
                # 如果不是关键关系，继续往上查找
                current = heads[current] - 1
                # 如果到达根节点(head为0)就停止
                if current < 0 or heads[current] == 0:
                    break
            return -1

        # 从第一个词往上找到具有关键关系的词
        phrase_head = find_phrase_head(idx1)
        if phrase_head < 0:
            return False

        #print(f"找到关键关系词的位置: {phrase_head}")
        if heads[phrase_head] == 0:
            return False
        # 检查关键关系词的子树中是否包含第二个词
        return self._check_subtree_relation(phrase_head, idx2, heads, labels)
    def _check_coordinate_extension(self, idx1: int, idx2: int, heads: List[int], labels: List[str]) -> bool:
        """
        检查并列关系扩展
        同时处理向上和向下的并列关系：
        1. 向下查找：找到所有head指向相同节点且label为COO的词
        2. 向上查找：找到所有指向当前词且label为COO的词
        """
        def find_coordinates(idx):
            coordinates = set()
            # 向下查找：找到所有head指向相同节点且label为COO的词
            head_value = heads[idx]
            for i, (head, label) in enumerate(zip(heads, labels)):
                if head == head_value and label == "COO":
                    coordinates.add(i)

            # 向上查找：找到所有指向当前词且label为COO的词
            for i, (head, label) in enumerate(zip(heads, labels)):
                if head == idx + 1 and label == "COO":  # +1因为heads中的索引是从1开始的
                    coordinates.add(i)
                # 如果当前词是COO，还需要添加它指向的词
                if i == idx and label == "COO":
                    coordinates.add(head - 1)  # -1因为要转换回真实索引

            return coordinates

        # 获取所有相关的并列词
        coordinates = find_coordinates(idx1)
        if idx1 in coordinates:
            coordinates.remove(idx1)
        #print(f"Found coordinate words at positions: {coordinates}")

        # 检查每个并列词与目标词的关系
        for coord_idx in coordinates:
            # 对每个并列词递归检查所有可能的关系
            if (self._check_subtree_relation(coord_idx, idx2, heads, labels) or
                    self._check_subject_predicate_extension(coord_idx, idx2, heads, labels) or
                    self._check_phrase_relation(coord_idx, idx2, heads, labels)):
                return True

        return False
    def _check_attribute_subject_predicate_relation(self, idx1: int, idx2: int, heads: List[int], labels: List[str]) -> bool:
        """
        检查条件5：定中关系链 -> 主语 -> 谓语 -> 相关词的关系
        如果一个词通过定中关系链连接到主语，然后通过主谓关系连接到谓语，
        再检查谓语下的动宾、并列、状中或动补关系下是否有目标词
        """
        # 首先查找定中关系链，获取修饰的中心语
        current = idx1
        while current >= 0:
            # 检查是否是定中关系或介宾关系
            if labels[current] not in self.up_relations:
                break

            # 获取当前词的中心语
            head_idx = heads[current] - 1
            if head_idx < 0:
                break

            current = head_idx

            # 检查中心语是否有主谓关系
            if labels[current] == "SBV":
                # 找到谓语
                predicate_idx = heads[current] - 1
                if predicate_idx < 0:
                    return False

                # 检查谓语下的子树中是否有目标词
                for i, (head, label) in enumerate(zip(heads, labels)):
                    # 检查是否指向谓语且是我们感兴趣的关系类型
                    if head == predicate_idx + 1 and label in ["VOB", "COO", "ADV", "CMP"]:
                        # 检查这个词的子树中是否包含目标词
                        if i == idx2 or self._check_subtree_relation(i, idx2, heads, labels):
                            return True

        return False

    def _check_attribute_object_relation(self, idx1: int, idx2: int, heads: List[int], labels: List[str]) -> bool:
        """
        检查条件6：定中关系链 -> 宾语/动宾结构 -> 相关词的关系

        一个词如果:
        1. 与其上一个词有定中关系（递归查定中，介宾都可以）
        2. 或直接有动宾关系
        查找到存在动宾结构为止，然后进行下列检查:
        a. 找这个宾语下面有没有词与目标词相关（若有则返回"同一宾语内相关"）
        b. 若没找到则找动词有没有主谓关系，若有则返回（"主谓宾关系"）
        c. 若没有则找动词的整个树下面有没有目标词，若有则返回（"间接谓宾相关"）
        d. 若还没找到，则查找动词是否有并列关系，若有则对每个并列动词重复上述检查
        """
        # 定义返回结果类型
        result_type = ""

        # 首先查找第一个词是否在定中关系链中，或直接是宾语
        current = idx1
        object_idx = -1
        verb_idx = -1

        # 检查是否是宾语
        if labels[current] == "VOB":
            object_idx = current
            verb_idx = heads[current] - 1
            result_type = "动宾关系"
        else:
            # 循环向上查找定中关系链或介宾关系
            while current >= 0:
                # 如果遇到的是定中关系或介宾关系，继续向上
                if labels[current] in self.up_relations:
                    head_idx = heads[current] - 1
                    if head_idx < 0:
                        break
                    current = head_idx

                # 如果遇到的是动宾关系，找到了宾语和动词
                elif labels[current] == "VOB":
                    object_idx = current
                    verb_idx = heads[current] - 1
                    result_type = "定中介宾扩展"
                    break
                else:
                    # 既不是定中/介宾，也不是动宾，跳出循环
                    break

        # 若没有找到动宾关系，返回False
        if object_idx == -1 or verb_idx == -1:
            return False

        # 情况a：检查宾语下面有没有与目标词相关的词
        if object_idx == idx2 or self._check_subtree_relation(object_idx, idx2, heads, labels):
            result_type = "同一宾语内相关"
            return True

        # 情况b：检查动词是否有主谓关系
        for i, (head, label) in enumerate(zip(heads, labels)):
            if head == verb_idx + 1 and label == "SBV":
                # 找到了主语
                if i == idx2 or self._check_subtree_relation(i, idx2, heads, labels):
                    result_type = "主谓宾关系"
                    return True

        # 情况c：检查动词的整个树下是否有目标词（除了已检查过的宾语部分）
        for i, head in enumerate(zip(heads)):
            if head == verb_idx + 1 and i != object_idx and labels[i] != "VOB":
                if i == idx2 or self._check_subtree_relation(i, idx2, heads, labels):
                    result_type = "间接谓宾相关"
                    return True

        # 情况d：查找动词是否有并列关系
        coordinates = set()
        # 向下查找：找到所有head指向相同节点且label为COO的词
        head_value = heads[verb_idx]
        for i, (head, label) in enumerate(zip(heads, labels)):
            if head == head_value and label == "COO" and i != verb_idx:
                coordinates.add(i)

        # 向上查找：找到所有指向当前词且label为COO的词
        for i, (head, label) in enumerate(zip(heads, labels)):
            if head == verb_idx + 1 and label == "COO":
                coordinates.add(i)
            # 如果当前词是COO，还需要添加它指向的词
            if i == verb_idx and label == "COO":
                coordinates.add(head - 1)

        # 对每个并列动词，重复检查上述关系
        for coord_verb in coordinates:
            # 检查这个并列动词下是否有动宾关系
            for i, (head, label) in enumerate(zip(heads, labels)):
                if head == coord_verb + 1 and label == "VOB":
                    if i == idx2 or self._check_subtree_relation(i, idx2, heads, labels):
                        result_type = "并列动词宾语相关"
                        return True

            # 检查这个并列动词是否有主谓关系
            for i, (head, label) in enumerate(zip(heads, labels)):
                if head == coord_verb + 1 and label == "SBV":
                    if i == idx2 or self._check_subtree_relation(i, idx2, heads, labels):
                        result_type = "并列动词主谓关系"
                        return True

            # 检查并列动词的整个子树
            if self._check_subtree_relation(coord_verb, idx2, heads, labels):
                result_type = "并列动词子树相关"
                return True

        return False
    def analyze(self, sentence: str, word1: str, word2: str) -> Tuple[int, str]:
        """主分析函数"""
        code, description = self.analyze_dependency(sentence, word1, word2)
        return code, description

# 示例
#"r1rxxxr - "






from py2neo import Graph
import re

# 连接到Neo4j数据库
# 请替换为你的实际Neo4j连接信息
graph = Graph("bolt://1.95.89.30:7687", auth=("neo4j", "Digitmaster5811"))



def process_all_relations():
    """处理图谱中所有同类型节点之间的关系文本并添加cleaned_relation_text属性"""
    
    # 获取所有关系类型
    relationship_types = ["Snake_R", "Brand_R", "Vision_arts_R"]
    
    # 处理每种关系类型
    total_processed = 0
    for rel_type in relationship_types:
        processed = process_relationships_by_type(rel_type)
        total_processed += processed
    
    print(f"总共处理了 {total_processed} 个关系")

def process_relationships_by_type(relation_type):
    """处理指定类型的所有关系"""
    print(f"开始处理 {relation_type} 类型的关系...")
    
    # 构建Cypher查询，获取所有指定类型的关系
    query = f"""
    MATCH (n1)-[r:{relation_type}]->(n2)
    RETURN id(r) as rel_id, n1.name as node1_name, n2.name as node2_name, r.relation_text as relation_text
    """
    
    # 执行查询
    results = graph.run(query).data()
    print(f"找到 {len(results)} 个 {relation_type} 类型的关系")
    
    # 处理每个关系
    processed_count = 0
    for result in results:
        rel_id = result["rel_id"]
        node1_name = result["node1_name"] if "node1_name" in result and result["node1_name"] else "未知节点"
        node2_name = result["node2_name"] if "node2_name" in result and result["node2_name"] else "未知节点"
        relation_text = result.get("relation_text", "")
        
        # 跳过没有relation_text的关系
        if not relation_text:
            print(f"跳过关系ID {rel_id}，因为没有relation_text属性")
            continue
        
        # 将多个句子拆分（基于示例中的'dist'分隔符）
        sentences = re.split(r'dist\d+dist - ', relation_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        final_str = ""
        ltp = LTP()
        ltp.add_words([node1_name,node2_name])
        dependency = DependencyAnalyzer(ltp)
        for sen in sentences:
            code, description = dependency.analyze(sen, node1_name, node2_name)
            if code == -1:
                continue
            res = "r" + str(code) + "r"+description+"r - "+sen+"\n"
            print(res)
            final_str = final_str+ res
        # 处理每个句子并合并结果

        
        # 更新关系属性
        update_query = f"""
        MATCH ()-[r]-() WHERE id(r) = {rel_id}
        SET r.cleaned_relation_text = $cleaned_text
        """
        
        graph.run(update_query, cleaned_text=final_str)
        print(f"已更新关系ID {rel_id}: {node1_name} -> {node2_name}")
        processed_count += 1
        del ltp
        del dependency
    
    return processed_count









# 执行主函数
if __name__ == "__main__":
    process_all_relations()




