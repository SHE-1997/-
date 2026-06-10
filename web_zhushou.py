import streamlit as st
from openai import OpenAI

# ================= 配置区 =================
# 在这里填入你自己的 DeepSeek API Key（注意：如果公开分享，这个 Key 会暴露，请谨慎）
MY_API_KEY = "sk-ea7bb62d17fc49cd9be62b4fee255387"

# 设置页面
st.set_page_config(page_title="室内设计智能助手", page_icon="🪑")
st.title("🪑 室内设计智能助手")
st.write("🏠 选择你的版本，AI 将为你生成设计方案。")

# ================= 会员/免费 选择 =================
plan = st.radio(
    "请选择你的版本：",
    ("免费版", "会员版"),
    index=0,
    help="会员版将生成更详细、更专业的设计方案。"
)

# ================= 输入区域 =================
col1, col2 = st.columns(2)
with col1:
    room_type = st.text_input("空间类型", "主卧室")
    style = st.text_input("设计风格", "现代简约")
with col2:
    area = st.text_input("面积大小", "20平米")
    budget = st.text_input("预算范围", "5000元")

special_req = st.text_area("特殊需求（选填）", "")

# ================= 生成按钮 =================
if st.button("生成设计方案"):
    # 检查 Key 是否配置
    if MY_API_KEY == "sk-这里填入你的真实Key":
        st.error("⚠️ 请先在代码里配置你的 DeepSeek API Key！")
    else:
        try:
            client = OpenAI(
                api_key=MY_API_KEY,
                base_url="https://api.deepseek.com"
            )
            
            # ----- 根据会员/免费 生成不同的提示词 -----
            if plan == "免费版":
                prompt = f"""
                你是一位室内设计师。请根据以下用户需求，提供一份简洁的设计建议（100字以内）。
                - 空间类型：{room_type}
                - 设计风格：{style}
                - 面积大小：{area}
                - 预算范围：{budget}
                """
            else:  # 会员版
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
                1. 设计理念（核心思路和情绪板关键词）
                2. 色彩搭配（主色、辅色、点缀色及占比）
                3. 材质推荐（地面、墙面、家具主材）
                4. 灯光设计（色温、主灯/辅助灯方案）
                5. 家具布局建议（动线分析）
                6. 软装推荐（窗帘、地毯、装饰画的关键元素）
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
                
                # 如果是会员版，显示一个小彩蛋
                if plan == "会员版":
                    st.success("🌟 感谢你选择会员版！")
                    
        except Exception as e:
            st.error(f"出错了：{e}")