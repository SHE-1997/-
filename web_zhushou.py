import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="室内设计智能助手", page_icon="🪑")

st.title("🪑 室内设计智能助手")
st.write("🏠 请输入你的需求，AI 将为你生成专业的设计方案。")

api_key = st.text_input("请输入你的 DeepSeek API Key", type="password")

col1, col2 = st.columns(2)
with col1:
    room_type = st.text_input("空间类型", "主卧室")
    style = st.text_input("设计风格", "现代简约")
with col2:
    area = st.text_input("面积大小", "20平米")
    budget = st.text_input("预算范围", "5000元")

special_req = st.text_area("特殊需求（选填）", "")

if st.button("生成设计方案"):
    if not api_key:
        st.error("⚠️ 请输入你的 DeepSeek API Key！")
    else:
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            
            prompt = f"""
            你是一位拥有20年经验的高级室内设计师。请根据以下用户需求，提供一份专业、详细且具有可操作性的设计方案。
            
            【用户需求】
            - 空间类型：{room_type}
            - 设计风格：{style}
            - 面积大小：{area}
            - 预算范围：{budget}
            - 特殊需求：{special_req if special_req else "无"}
            
            【输出要求】
            请按以下结构输出：
            1. 设计理念
            2. 色彩搭配
            3. 材质推荐
            4. 灯光设计
            5. 家具布局建议
            6. 软装推荐
            7. 预算分配建议
            """
            
            with st.spinner("AI 正在构思方案..."):
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个专业、细致且富有创造力的室内设计顾问。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.write(result)
        except Exception as e:
            st.error(f"出错了：{e}")