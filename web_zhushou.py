import streamlit as st
from openai import OpenAI
import json

# ================= 配置 =================
# 请填入你的真实 Key
MY_API_KEY = "sk-ea7bb62d17fc49cd9be62b4fee255387" 

if MY_API_KEY == "sk-这里填入你的真实Key":
    st.error("请先在代码里配置你的 DeepSeek API Key！")
    st.stop()

client = OpenAI(api_key=MY_API_KEY, base_url="https://api.deepseek.com")

# ================= 页面设置 =================
st.set_page_config(page_title="室内设计助手 + 数据导出", page_icon="🏡", layout="wide")

st.title("🏡 室内设计助手 (带数据导出)")
st.write("AI 生成方案 + 导出 JSON 数据，用于 SketchUp 自动建模。")

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
if st.button("🚀 生成设计方案 & 导出数据"):
    try:
        # 构建提示词，要求 AI 同时输出文字方案和 JSON 数据
        prompt = f"""
        你是一位拥有20年经验的高级室内设计师。请根据以下用户需求，提供一份专业的设计方案。

        【用户需求】
        - 空间类型：{room_type}
        - 设计风格：{style}
        - 面积：{area}
        - 预算：{budget}
        - 特殊需求：{special_req if special_req else "无"}

        【输出要求】
        1. 先输出完整的、详细的设计方案（文字版），包含：设计理念、色彩、材质、灯光、家具布局、软装、预算。
        2. 在文字方案的最后，用 ---JSON_START--- 和 ---JSON_END--- 标记，输出一份纯 JSON 格式的数据。
        3. JSON 数据必须包含以下字段：
        - "width": 房间宽度（米）
        - "length": 房间长度（米）
        - "height": 房间高度（米）
        - "wall_color": 墙面颜色 (Hex色号)
        - "floor_material": 地面材质
        - "furniture": [{"name": "沙发", "x": 1.5, "y": 2.0, "width": 2.0, "depth": 0.8}]
        - "windows": [{"wall": "south", "width": 1.2, "height": 1.5, "x": 2.0}]
        - "doors": [{"wall": "north", "width": 0.9, "height": 2.1, "x": 1.5}]
        4. 请确保 JSON 数据是有效的，且与文字方案内容一致。
        """

        with st.spinner("AI 正在构思方案..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的设计顾问和数据分析师。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            result = response.choices[0].message.content

            # 显示文字方案
            st.success("✅ 方案生成完毕！")
            st.markdown("---")
            st.markdown(result)

            # 尝试提取 JSON 数据
            try:
                # 寻找 JSON 标记
                start_marker = "---JSON_START---"
                end_marker = "---JSON_END---"
                
                if start_marker in result and end_marker in result:
                    start_idx = result.find(start_marker) + len(start_marker)
                    end_idx = result.find(end_marker)
                    json_str = result[start_idx:end_idx].strip()
                    
                    # 解析 JSON 确保格式正确
                    data = json.loads(json_str)
                    
                    # 提供下载按钮
                    st.download_button(
                        label="📥 下载建模数据 (JSON)",
                        data=json_str,
                        file_name="design_data.json",
                        mime="application/json"
                    )
                    st.success("✅ 建模数据已准备好！")
                else:
                    st.warning("⚠️ AI 未能正确生成 JSON 数据，请重试。")
            except Exception as e:
                st.error(f"提取 JSON 时出错：{e}")

    except Exception as e:
        st.error(f"出错了：{e}")

else:
    st.info("👈 填写需求后点击按钮生成。")