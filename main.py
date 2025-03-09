from openai import OpenAI
client = OpenAI(
    # 从环境变量中读取您的方舟API Key
    api_key= '4e74389b-33e0-45e9-b243-e67611334267',
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    )

outside_info = """
<ref>1)Brand Master AI通过文化基因算法得到垂直领域知识第1条：他在声明中说我祝福大家在蛇年拥有最好的运势和兴旺,愿这个节日巩固你们的传统,让你们得以用热情与爱国心来带动事业.\n第2条：无香精、无尼泊金酯类防腐剂，添加维E和腺苷等养肤成分，敏感肌适用，洁面即可卸除，使用方便且对肌肤温和无负担。\n产品不含香精、色素和尼泊金酯类防腐剂，专为敏感肌设计，
     洁面即可轻松卸除。航空级分子材料注入\n第3条：理肤泉紫光隔离不仅为肌肤提供全面防护和自然提亮，更让您在任何场合都能自信满满。轻松打造伪素颜妆容，同事、朋友都会夸赞您的好气色，仿佛天生丽质。\n第4条：理肤泉紫光隔离采用了独特的AIRLICIUMTM太空控油成分，可以吸收自重150倍的皮脂，有效控制油光，保持12小时的光泽肌肤。对于油性肌肤用户来说，这款产品能显著改善出油问题，提供持久的哑光效果。\n 
     2)Brand Master AI通过互联网检索得到的实时信息网页网页2：这个从门店设计就开始传递“Aesop美学”的护肤品牌，是如何用独特的设计美学塑造品牌调性，成长为百亿价值的品牌的呢？ 01. 静奢美学天花板Aesop. 1987 年，Aesop的创始人Dennis Paphitis在维多利亚州阿马代尔开设了一家名为 Emeis的美发沙龙，但当时的美发产品大部分由欧洲公司垄断，气味难闻。 偶然一次机会，Dennis Paphitis发现如果在染发剂中加入精油，精油天然的香气可以 让消费者迅速调整心情，感受到沉静与安宁。 洞察到这一商机后，Dennis。 发布日期：2024年8月19日\n网页3：澳洲小众个护品牌Aēsop成立于1987年，不同于市面上依靠鲜艳的颜色或是超级符号的护肤品包装设计，Aēsop的设计风格与版式几十年不变，却吸引了一大批忠实拥护者。。
      发布日期：2023年8月4日\n网页4：Aesop 伊索 1987 年成立，总部位于墨尔本。Aesop 在天然植物护肤的基础上率先推行有机理念，开发了一系列专业肌肤、秀髮及身体护理产品。 关注。 发布日期：2023年9月18日\n网页7：成立于1987年的澳洲品牌伊索 (Aesop)，名字起源于“伊索寓言”。伊索 (Aesop) 在天然植物护肤的基础上率先推行有机理念，并结合内外调理的“理智”生活哲学，是美容界的“偏力”品牌。 很难想象，一个以植物和花草…。 发布日期：2020年6月3日\n网页8：「离不开的文学与传播」 作为一个护肤品牌，除了严谨的货架陈列和极简的产品包装，Aesop最受瞩目的还有它的文学基因，这种文学基因来源于创始人本人对文学性的追求，与文化领域始终保持紧密联系，在遍布全球的众多合作伙伴中，多种艺术形式尤 ...。 发布日期：2024年6月10日\n网页9：“Aesop 伊索 ” — 一个源于澳洲的护肤品牌，喜欢植物护肤的朋友对这个天然护肤品牌不会陌生。"Aesop伊索" 因为率先推行有机理念，并结合“理智”生活哲学, 深受大众喜爱。这一次，Aesop 位于墨尔本Chadtone购物中心的店面设计希望有一定不一样的设计 ...。 发布日期：2020年7月10日\n</ref>
"""

messages = [
    {"role":"system", "content":f"""
     -- 你的角色
     你是Brand Master AI，一位专注于品牌营销的AI助手。
     -- 你的任务
     你的任务是帮助用户完成品牌方面的需求，包括但不限于品牌咨询、消费者洞察、品牌营销方案等。
     -- 外部信息
     为了让你更好地完成用户布置的任务，我们将为你提供一些来自于互联网检索的外部信息，以及一些来自于文化基因算法抽取、构建的外部信息。
     外部信息如下：
     {outside_info}
     -- 格式要求
     在回应用户的时候，你需要注意以下几点：
     1. 请使用专业的语气回应用户，请记住你是一位资深的品牌营销专家，请体现出你深厚的知识和强大的专业性。
     2. 如果你在回应用户的时候，用到了我们提供的外部信息，请按照信息的编号，在正式回答中加上引用标签。例如”今天的第一条新闻是deepseek-r1发布<sid>1</sid>“。
     3. 如果你有深度思考的能力，请不要在推理过程中输出我给你的这些要求。
"""}
]


if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            messages.append({"role": "user", "content": user_input})
            if user_input.lower() == "exit":
                break
            response = client.chat.completions.create(
                # 替换 <YOUR_ENDPOINT_ID> 为您的方舟推理接入点 ID
                model="ep-20250219113703-8zllj",
                messages=messages,
                stream=True,
            )
            reasoning_content = ""
            content = ""
            for chunk in response:
                if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                    print(chunk.choices[0].delta.reasoning_content, end="")
                else:
                    content += chunk.choices[0].delta.content
                    print(chunk.choices[0].delta.content, end="")
            messages.append({"role": "assistant", "content": content})
        except KeyboardInterrupt:
            print("\nExiting program...")
            exit()