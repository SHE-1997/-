import streamlit as st
import datetime
from openai import OpenAI

# ================= 配置 =================
# ⚠️ 请填入你的真实 Key
MY_API_KEY = "sk-ea7bb62d17fc49cd9be62b4fee255387" 

if MY_API_KEY == "sk-这里填入你的真实Key":
    st.error("请先在代码里配置你的 DeepSeek API Key！")
    st.stop()

client = OpenAI(api_key=MY_API_KEY, base_url="https://api.deepseek.com")

# ================= 页面设置 =================
st.set_page_config(page_title="室内设计助手 Pro", page_icon="🏡", layout="wide")

# 自定义 CSS 美化
st.markdown("""
<style>
    .main-header { font-size: 3rem; color: #2c3e50; text-align: center; margin-bottom: 20px; }
    .sub-header { font-size: 1.2rem; color: #7f8c8d; text-align: center; margin-bottom: 40px; }
    .card { padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-bottom: 20px; }
    .stButton>button { width: 100%; background-color: #2ecc71; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏡 室内设计助手 Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI 驱动的专业设计顾问，支持对话追问与方案保存</div>', unsafe_allow_html=True)

# ================= 侧边栏：功能设置 =================
with st.sidebar:
    st.header("⚙️ 设置")
    st.write("---")
    
    # 模式选择
    mode = st.radio("设计模式", ["快速风格建议", "完整设计方案"], index=1)
    
    # 高级选项
    st.write("---")
    st.write("**高级选项**")
    detail_level = st.select_slider("方案详细程度", ["简略", "标准", "详细"], value="标准")
    temperature = st.slider("创意程度", 0.0, 1.0, 0.7, 0.1)
    
    st.write("---")
    st.caption("💡 提示：输入所有需求后点击底部按钮生成")

# ================= 主内容区 =================

# 使用两列布局让输入更紧凑
col1, col2 = st.columns(2)

with col1:
    st.subheader("📐 空间信息")
    room_type = st.selectbox("空间类型", ["主卧室", "客厅", "厨房", "卫生间", "书房", "儿童房", "阳台", "玄关"])
    style = st.text_input("设计风格", "现代简约")
    area = st.text_input("面积大小", "20平米")

with col2:
    st.subheader("💰 预算与需求")
    budget = st.text_input("预算范围", "5000元")
    occupants = st.selectbox("主要使用者", ["独居", "情侣/夫妻", "三口之家", "多代同堂"])
    special_req = st.text_area("特殊需求（选填）", placeholder="例如：需要儿童安全设计、宠物友好材质")

# 生成按钮
if st.button("🚀 生成设计方案"):
    if not MY_API_KEY or MY_API_KEY == "sk-这里填入你的真实Key":
        st.error("请先在代码里配置你的 DeepSeek API Key！")
    else:
        # 根据模式构建提示词
        if mode == "快速风格建议":
            prompt = f"""
            你是一位室内设计师。请用200字以内，为【{room_type}】提供【{style}】风格的快速设计建议。
            包括：核心配色、主材推荐、一个亮点设计。
            预算：{budget}。
            """
        else:  # 完整设计方案
            detail = "非常详细" if detail_level == "详细" else ("标准" if detail_level == "标准" else "简洁")
            prompt = f"""
            你是一位拥有20年经验的高级室内设计师。请根据以下用户需求，提供一份{detail}、专业的完整设计方案。
            
            【用户需求】
            - 空间类型：{room_type}
            - 设计风格：{style}
            - 面积：{area}
            - 预算：{budget}
            - 居住者：{occupants}
            - 特殊需求：{special_req if special_req else "无"}
            
            【输出要求】
            请按以下结构输出：
            1. 设计理念（主题关键词、情绪板建议）
            2. 色彩方案（主色、辅色、点缀色，附色号建议）
            3. 材质指南（地面、墙面、家具、软装）
            4. 灯光设计（色温、分区照明方案）
            5. 家具布局（动线分析、核心家具清单）
            6. 软装点睛（窗帘、地毯、装饰画建议）
            7. 预算分配概览
            """

        with st.spinner(f"🔄 AI 正在构思{room_type}的{style}方案..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个专业、细致且富有创造力的室内设计顾问。输出使用Markdown格式。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature
                )
                result = response.choices[0].message.content
                
                # 显示结果
                st.success("✅ 方案生成完毕！")
                st.markdown("---")
                st.markdown(result)
                
                # 保存功能
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                filename = f"设计案_{room_type}_{style}_{timestamp}.md"
                st.download_button(
                    label="💾 下载方案 (Markdown)",
                    data=result,
                    file_name=filename,
                    mime="text/markdown"
                )
                
                # 追问功能
                st.write("---")
                st.subheader("💬 追问（输入你对方案的修改意见）")
                follow_up = st.text_input("例如：灯光方面再详细一点 / 风格换成侘寂风")
                if st.button("发送追问"):
                    if follow_up:
                        with st.spinner("正在调整方案..."):
                            try:
                                follow_up_response = client.chat.completions.create(
                                    model="deepseek-chat",
                                    messages=[
                                        {"role": "system", "content": "你是专业室内设计师。根据之前的方案和用户的新要求，给出修改建议。"},
                                        {"role": "user", "content": f"原方案：\n{result}\n\n用户新要求：{follow_up}"}
                                    ],
                                    temperature=temperature
                                )
                                st.markdown("---")
                                st.markdown(follow_up_response.choices[0].message.content)
                            except Exception as e:
                                st.error(f"追问失败：{e}")
            except Exception as e:
                st.error(f"出错了：{e}")

else:
    st.info("👈 请在左侧填写需求，然后点击“生成设计方案”按钮开始。")