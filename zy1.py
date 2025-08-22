import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from io import BytesIO
import uuid

# 页面配置
st.set_page_config(
    page_title="汽车索赔管理系统",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .warning-message {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'owners_data' not in st.session_state:
    st.session_state.owners_data = None
if 'claims_data' not in st.session_state:
    st.session_state.claims_data = None
if 'initialized' not in st.session_state:
    st.session_state.initialized = False


def generate_sample_data():
    """生成示例数据"""
    # 生成车主信息示例数据
    owner_names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十",
                   "郑十一", "王十二", "陈十三", "褚十四", "卫十五", "蒋十六", "沈十七"]

    cities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉", "西安", "天津"]
    car_brands = ["奔驰", "宝马", "奥迪", "大众", "丰田", "本田", "日产", "现代", "起亚", "福特"]
    car_models = ["A4L", "3系", "C级", "凯美瑞", "雅阁", "天籁", "朗逸", "轩逸", "卡罗拉", "速腾"]

    # 车主数据
    owners_data = []
    for i in range(50):
        owner_id = f"OW{str(i + 1).zfill(6)}"
        owners_data.append({
            "车主编号": owner_id,
            "姓名": random.choice(owner_names) + str(random.randint(1, 999)),
            "身份证号": f"{random.randint(110000, 999999)}{random.randint(1950, 2005)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(1000, 9999)}",
            "电话号码": f"1{random.randint(3, 9)}{random.randint(0, 9)}{random.randint(10000000, 99999999)}",
            "邮箱": f"user{i + 1}@example.com",
            "地址": f"{random.choice(cities)}市{random.choice(['朝阳', '海淀', '西城', '东城', '丰台'])}区{random.choice(['中山', '建国', '长安', '民族', '和平'])}路{random.randint(1, 999)}号",
            "车牌号": f"{random.choice(['京', '沪', '粤', '浙', '苏'])}{chr(random.randint(65, 90))}{random.randint(10000, 99999)}",
            "车辆品牌": random.choice(car_brands),
            "车辆型号": random.choice(car_models),
            "购买日期": (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime("%Y-%m-%d"),
            "保险到期日": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "注册时间": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d %H:%M:%S")
        })

    # 索赔数据
    claim_types = ["车辆碰撞", "自然灾害", "盗抢", "自燃", "涉水", "玻璃破损", "轮胎损坏", "划痕"]
    claim_status = ["待审核", "审核中", "已批准", "已拒绝", "已结案"]

    claims_data = []
    for i in range(120):
        claim_id = f"CL{str(i + 1).zfill(6)}"
        owner_id = random.choice([owner["车主编号"] for owner in owners_data])
        claim_amount = random.randint(500, 50000)
        approved_amount = claim_amount if random.choice([True, False, True]) else random.randint(0, claim_amount)

        claims_data.append({
            "索赔编号": claim_id,
            "车主编号": owner_id,
            "索赔类型": random.choice(claim_types),
            "事故日期": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "申请日期": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            "索赔金额": claim_amount,
            "批准金额": approved_amount,
            "处理状态": random.choice(claim_status),
            "事故描述": f"在{random.choice(cities)}市发生{random.choice(claim_types)}事故，造成车辆不同程度损坏。",
            "处理备注": "正在处理中..." if random.choice([True, False]) else "已完成处理",
            "处理人员": random.choice(["王处理员", "李审核员", "张专员", "赵主管", "钱经理"]),
            "创建时间": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d %H:%M:%S"),
            "更新时间": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
        })

    return pd.DataFrame(owners_data), pd.DataFrame(claims_data)


def initialize_data():
    """初始化数据"""
    if not st.session_state.initialized:
        owners_df, claims_df = generate_sample_data()
        st.session_state.owners_data = owners_df
        st.session_state.claims_data = claims_df
        st.session_state.initialized = True


def export_to_excel(dataframes, sheet_names):
    """导出数据到Excel"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for df, sheet_name in zip(dataframes, sheet_names):
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()


def main():
    # 初始化数据
    initialize_data()

    # 侧边栏导航
    st.sidebar.title("🚗 汽车索赔管理系统")
    st.sidebar.markdown("---")

    pages = {
        "📊 系统概览": "dashboard",
        "👥 车主管理": "owners",
        "📋 索赔管理": "claims",
        "📈 数据统计": "statistics",
        "💾 数据导出": "export"
    }

    selected_page = st.sidebar.radio("选择功能模块", list(pages.keys()))

    # 侧边栏信息
    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **系统信息**
    - 车主数量: {len(st.session_state.owners_data)}
    - 索赔记录: {len(st.session_state.claims_data)}
    - 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """)

    # 页面路由
    page_key = pages[selected_page]

    if page_key == "dashboard":
        show_dashboard()
    elif page_key == "owners":
        show_owners_management()
    elif page_key == "claims":
        show_claims_management()
    elif page_key == "statistics":
        show_statistics()
    elif page_key == "export":
        show_export()


def show_dashboard():
    """显示系统概览页面"""
    st.markdown('<h1 class="main-header">🚗 汽车索赔管理系统概览</h1>', unsafe_allow_html=True)

    # 核心指标
    col1, col2, col3, col4 = st.columns(4)

    total_owners = len(st.session_state.owners_data)
    total_claims = len(st.session_state.claims_data)
    total_claim_amount = st.session_state.claims_data["索赔金额"].sum()
    approved_claims = len(st.session_state.claims_data[st.session_state.claims_data["处理状态"] == "已批准"])

    with col1:
        st.metric("车主总数", f"{total_owners:,}", delta="12 本月新增")
    with col2:
        st.metric("索赔总数", f"{total_claims:,}", delta="8 本周新增")
    with col3:
        st.metric("索赔总额", f"¥{total_claim_amount:,.0f}", delta="¥12,500 本月")
    with col4:
        st.metric("已批准案件", f"{approved_claims:,}", delta=f"{(approved_claims / total_claims * 100):.1f}% 通过率")

    st.markdown("---")

    # 图表区域
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 月度索赔趋势")
        # 生成月度趋势数据
        months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        monthly_claims = [random.randint(15, 35) for _ in months]
        monthly_amounts = [random.randint(50000, 150000) for _ in months]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[m.strftime('%Y-%m') for m in months],
            y=monthly_claims,
            mode='lines+markers',
            name='索赔数量',
            line=dict(color='#1f77b4')
        ))
        fig.update_layout(
            title="月度索赔数量趋势",
            xaxis_title="月份",
            yaxis_title="索赔数量",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🏷️ 索赔类型分布")
        claim_type_counts = st.session_state.claims_data["索赔类型"].value_counts()

        fig = px.pie(
            values=claim_type_counts.values,
            names=claim_type_counts.index,
            title="索赔类型占比分布"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # 最新动态
    st.subheader("📊 最新索赔动态")
    recent_claims = st.session_state.claims_data.nlargest(10, "创建时间")[
        ["索赔编号", "车主编号", "索赔类型", "索赔金额", "处理状态", "申请日期"]
    ]
    st.dataframe(recent_claims, use_container_width=True)

    # 状态统计
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 处理状态统计")
        status_counts = st.session_state.claims_data["处理状态"].value_counts()

        fig = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="各状态案件数量",
            color=status_counts.values,
            color_continuous_scale="Blues"
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🚗 热门车型统计")
        brand_counts = st.session_state.owners_data["车辆品牌"].value_counts().head(8)

        fig = px.bar(
            x=brand_counts.values,
            y=brand_counts.index,
            orientation='h',
            title="车辆品牌分布",
            color=brand_counts.values,
            color_continuous_scale="Greens"
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)


def show_owners_management():
    """显示车主管理页面"""
    st.markdown('<h1 class="main-header">👥 车主信息管理</h1>', unsafe_allow_html=True)

    # 功能选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 查询车主", "➕ 新增车主", "✏️ 修改信息", "📋 车主列表"])

    with tab1:
        st.subheader("🔍 车主信息查询")

        col1, col2, col3 = st.columns(3)
        with col1:
            search_type = st.selectbox("查询方式", ["车主编号", "姓名", "车牌号", "电话号码"])
        with col2:
            search_value = st.text_input("请输入查询内容")
        with col3:
            st.write("")  # 空格
            search_btn = st.button("🔍 查询", type="primary")

        if search_btn and search_value:
            if search_type == "车主编号":
                result = st.session_state.owners_data[
                    st.session_state.owners_data["车主编号"].str.contains(search_value, na=False)]
            elif search_type == "姓名":
                result = st.session_state.owners_data[
                    st.session_state.owners_data["姓名"].str.contains(search_value, na=False)]
            elif search_type == "车牌号":
                result = st.session_state.owners_data[
                    st.session_state.owners_data["车牌号"].str.contains(search_value, na=False)]
            elif search_type == "电话号码":
                result = st.session_state.owners_data[
                    st.session_state.owners_data["电话号码"].str.contains(search_value, na=False)]

            if not result.empty:
                st.success(f"找到 {len(result)} 条匹配记录")
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("未找到匹配的车主信息")
        else:
            # 显示示例数据
            st.info("💡 以下是车主信息示例数据")
            sample_data = st.session_state.owners_data.head(10)
            st.dataframe(sample_data, use_container_width=True)

    with tab2:
        st.subheader("➕ 新增车主信息")

        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("姓名", placeholder="请输入车主姓名")
            new_id_card = st.text_input("身份证号", placeholder="请输入18位身份证号")
            new_phone = st.text_input("电话号码", placeholder="请输入11位手机号")
            new_email = st.text_input("邮箱", placeholder="请输入邮箱地址")
            new_address = st.text_area("地址", placeholder="请输入详细地址")

        with col2:
            new_plate = st.text_input("车牌号", placeholder="例：京A12345")
            new_brand = st.selectbox("车辆品牌",
                                     ["奔驰", "宝马", "奥迪", "大众", "丰田", "本田", "日产", "现代", "起亚", "福特"])
            new_model = st.text_input("车辆型号", placeholder="请输入车辆型号")
            new_buy_date = st.date_input("购买日期")
            new_insurance_expire = st.date_input("保险到期日")

        if st.button("💾 保存车主信息", type="primary"):
            if new_name and new_id_card and new_phone:
                new_owner_id = f"OW{str(len(st.session_state.owners_data) + 1).zfill(6)}"
                new_row = {
                    "车主编号": new_owner_id,
                    "姓名": new_name,
                    "身份证号": new_id_card,
                    "电话号码": new_phone,
                    "邮箱": new_email,
                    "地址": new_address,
                    "车牌号": new_plate,
                    "车辆品牌": new_brand,
                    "车辆型号": new_model,
                    "购买日期": new_buy_date.strftime("%Y-%m-%d"),
                    "保险到期日": new_insurance_expire.strftime("%Y-%m-%d"),
                    "注册时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.owners_data = pd.concat([st.session_state.owners_data, pd.DataFrame([new_row])],
                                                         ignore_index=True)
                st.success("✅ 车主信息保存成功！")
                st.balloons()
            else:
                st.error("❌ 请填写必填字段（姓名、身份证号、电话号码）")

    with tab3:
        st.subheader("✏️ 修改车主信息")

        # 选择要修改的车主
        owner_ids = st.session_state.owners_data["车主编号"].tolist()
        selected_owner_id = st.selectbox("选择车主", owner_ids)

        if selected_owner_id:
            owner_info = \
            st.session_state.owners_data[st.session_state.owners_data["车主编号"] == selected_owner_id].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                edit_name = st.text_input("姓名", value=owner_info["姓名"])
                edit_phone = st.text_input("电话号码", value=owner_info["电话号码"])
                edit_email = st.text_input("邮箱", value=owner_info["邮箱"])
                edit_address = st.text_area("地址", value=owner_info["地址"])

            with col2:
                edit_plate = st.text_input("车牌号", value=owner_info["车牌号"])
                edit_brand = st.selectbox("车辆品牌",
                                          ["奔驰", "宝马", "奥迪", "大众", "丰田", "本田", "日产", "现代", "起亚",
                                           "福特"],
                                          index=["奔驰", "宝马", "奥迪", "大众", "丰田", "本田", "日产", "现代", "起亚",
                                                 "福特"].index(owner_info["车辆品牌"]) if owner_info["车辆品牌"] in [
                                              "奔驰", "宝马", "奥迪", "大众", "丰田", "本田", "日产", "现代", "起亚",
                                              "福特"] else 0)
                edit_model = st.text_input("车辆型号", value=owner_info["车辆型号"])
                edit_insurance_expire = st.date_input("保险到期日",
                                                      value=pd.to_datetime(owner_info["保险到期日"]).date())

            if st.button("💾 更新信息", type="primary"):
                # 更新数据
                idx = st.session_state.owners_data[st.session_state.owners_data["车主编号"] == selected_owner_id].index[
                    0]
                st.session_state.owners_data.loc[idx, "姓名"] = edit_name
                st.session_state.owners_data.loc[idx, "电话号码"] = edit_phone
                st.session_state.owners_data.loc[idx, "邮箱"] = edit_email
                st.session_state.owners_data.loc[idx, "地址"] = edit_address
                st.session_state.owners_data.loc[idx, "车牌号"] = edit_plate
                st.session_state.owners_data.loc[idx, "车辆品牌"] = edit_brand
                st.session_state.owners_data.loc[idx, "车辆型号"] = edit_model
                st.session_state.owners_data.loc[idx, "保险到期日"] = edit_insurance_expire.strftime("%Y-%m-%d")

                st.success("✅ 车主信息更新成功！")
                st.balloons()

    with tab4:
        st.subheader("📋 车主信息列表")

        # 筛选选项
        col1, col2, col3 = st.columns(3)
        with col1:
            brand_filter = st.selectbox("品牌筛选", ["全部"] + list(st.session_state.owners_data["车辆品牌"].unique()))
        with col2:
            city_filter = st.selectbox("城市筛选", ["全部"] + [addr.split("市")[0] + "市" for addr in
                                                               st.session_state.owners_data["地址"] if "市" in addr])
        with col3:
            sort_by = st.selectbox("排序方式", ["注册时间", "姓名", "车主编号"])

        # 应用筛选
        filtered_data = st.session_state.owners_data.copy()
        if brand_filter != "全部":
            filtered_data = filtered_data[filtered_data["车辆品牌"] == brand_filter]

        # 排序
        if sort_by == "注册时间":
            filtered_data = filtered_data.sort_values("注册时间", ascending=False)
        elif sort_by == "姓名":
            filtered_data = filtered_data.sort_values("姓名")
        else:
            filtered_data = filtered_data.sort_values("车主编号")

        st.info(f"共找到 {len(filtered_data)} 条车主记录")
        st.dataframe(filtered_data, use_container_width=True)


def show_claims_management():
    """显示索赔管理页面"""
    st.markdown('<h1 class="main-header">📋 索赔信息管理</h1>', unsafe_allow_html=True)

    # 功能选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 查询索赔", "➕ 新增索赔", "⚙️ 处理索赔", "📋 索赔列表"])

    with tab1:
        st.subheader("🔍 索赔信息查询")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            search_type = st.selectbox("查询方式", ["索赔编号", "车主编号", "索赔类型", "处理状态"])
        with col2:
            if search_type in ["索赔类型", "处理状态"]:
                if search_type == "索赔类型":
                    search_value = st.selectbox("选择类型", st.session_state.claims_data["索赔类型"].unique())
                else:
                    search_value = st.selectbox("选择状态", st.session_state.claims_data["处理状态"].unique())
            else:
                search_value = st.text_input("请输入查询内容")
        with col3:
            date_range = st.date_input("申请日期范围",
                                       value=[datetime.now().date() - timedelta(days=30), datetime.now().date()],
                                       key="search_date")
        with col4:
            st.write("")
            search_btn = st.button("🔍 查询索赔", type="primary")

        if search_btn:
            if search_type == "索赔编号":
                result = st.session_state.claims_data[
                    st.session_state.claims_data["索赔编号"].str.contains(str(search_value), na=False)]
            elif search_type == "车主编号":
                result = st.session_state.claims_data[
                    st.session_state.claims_data["车主编号"].str.contains(str(search_value), na=False)]
            elif search_type == "索赔类型":
                result = st.session_state.claims_data[st.session_state.claims_data["索赔类型"] == search_value]
            elif search_type == "处理状态":
                result = st.session_state.claims_data[st.session_state.claims_data["处理状态"] == search_value]

            # 应用日期筛选
            if len(date_range) == 2:
                result = result[
                    (pd.to_datetime(result["申请日期"]) >= pd.to_datetime(date_range[0])) &
                    (pd.to_datetime(result["申请日期"]) <= pd.to_datetime(date_range[1]))
                    ]

            if not result.empty:
                st.success(f"找到 {len(result)} 条匹配记录")
                st.dataframe(result, use_container_width=True)

                # 显示统计信息
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("索赔总额", f"¥{result['索赔金额'].sum():,.0f}")
                with col2:
                    st.metric("批准总额", f"¥{result['批准金额'].sum():,.0f}")
                with col3:
                    approved_rate = (result[result["处理状态"] == "已批准"].shape[0] / len(result) * 100) if len(
                        result) > 0 else 0
                    st.metric("通过率", f"{approved_rate:.1f}%")
            else:
                st.warning("未找到匹配的索赔记录")
        else:
            # 显示示例数据
            st.info("💡 以下是索赔信息示例数据")
            sample_data = st.session_state.claims_data.head(10)
            st.dataframe(sample_data, use_container_width=True)

    with tab2:
        st.subheader("➕ 新增索赔申请")

        col1, col2 = st.columns(2)
        with col1:
            owner_ids = st.session_state.owners_data["车主编号"].tolist()
            new_owner_id = st.selectbox("选择车主", owner_ids)
            new_claim_type = st.selectbox("索赔类型",
                                          ["车辆碰撞", "自然灾害", "盗抢", "自燃", "涉水", "玻璃破损", "轮胎损坏",
                                           "划痕"])
            new_accident_date = st.date_input("事故日期")
            new_claim_amount = st.number_input("索赔金额", min_value=0, value=5000, step=100)

        with col2:
            new_description = st.text_area("事故描述", placeholder="请详细描述事故经过...")
            new_handler = st.selectbox("处理人员", ["王处理员", "李审核员", "张专员", "赵主管", "钱经理"])

            # 显示选中车主信息
            if new_owner_id:
                owner_info = \
                st.session_state.owners_data[st.session_state.owners_data["车主编号"] == new_owner_id].iloc[0]
                st.info(f"""
                **车主信息**
                - 姓名: {owner_info['姓名']}
                - 车牌号: {owner_info['车牌号']}
                - 车辆: {owner_info['车辆品牌']} {owner_info['车辆型号']}
                - 保险到期: {owner_info['保险到期日']}
                """)

        if st.button("💾 提交索赔申请", type="primary"):
            if new_owner_id and new_claim_type and new_description:
                new_claim_id = f"CL{str(len(st.session_state.claims_data) + 1).zfill(6)}"
                new_row = {
                    "索赔编号": new_claim_id,
                    "车主编号": new_owner_id,
                    "索赔类型": new_claim_type,
                    "事故日期": new_accident_date.strftime("%Y-%m-%d"),
                    "申请日期": datetime.now().strftime("%Y-%m-%d"),
                    "索赔金额": new_claim_amount,
                    "批准金额": 0,
                    "处理状态": "待审核",
                    "事故描述": new_description,
                    "处理备注": "新提交的索赔申请",
                    "处理人员": new_handler,
                    "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.claims_data = pd.concat([st.session_state.claims_data, pd.DataFrame([new_row])],
                                                         ignore_index=True)
                st.success(f"✅ 索赔申请提交成功！申请编号：{new_claim_id}")
                st.balloons()
            else:
                st.error("❌ 请填写所有必填字段")

    with tab3:
        st.subheader("⚙️ 索赔处理")

        # 选择要处理的索赔
        pending_claims = st.session_state.claims_data[
            st.session_state.claims_data["处理状态"].isin(["待审核", "审核中"])]

        if not pending_claims.empty:
            claim_ids = pending_claims["索赔编号"].tolist()
            selected_claim_id = st.selectbox("选择待处理索赔", claim_ids)

            if selected_claim_id:
                claim_info = \
                st.session_state.claims_data[st.session_state.claims_data["索赔编号"] == selected_claim_id].iloc[0]

                # 显示索赔详情
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"""
                    **索赔详情**
                    - 索赔编号: {claim_info['索赔编号']}
                    - 车主编号: {claim_info['车主编号']}
                    - 索赔类型: {claim_info['索赔类型']}
                    - 事故日期: {claim_info['事故日期']}
                    - 申请日期: {claim_info['申请日期']}
                    - 索赔金额: ¥{claim_info['索赔金额']:,.0f}
                    """)

                with col2:
                    st.text_area("事故描述", value=claim_info['事故描述'], disabled=True)

                # 处理选项
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_status = st.selectbox("处理结果", ["审核中", "已批准", "已拒绝", "已结案"])
                with col2:
                    approved_amount = st.number_input("批准金额", min_value=0, max_value=int(claim_info['索赔金额']),
                                                      value=int(claim_info['索赔金额']))
                with col3:
                    handler = st.selectbox("处理人员", ["王处理员", "李审核员", "张专员", "赵主管", "钱经理"],
                                           index=["王处理员", "李审核员", "张专员", "赵主管", "钱经理"].index(
                                               claim_info['处理人员']) if claim_info['处理人员'] in ["王处理员",
                                                                                                     "李审核员",
                                                                                                     "张专员", "赵主管",
                                                                                                     "钱经理"] else 0)

                remarks = st.text_area("处理备注", placeholder="请输入处理备注...")

                if st.button("💾 保存处理结果", type="primary"):
                    # 更新索赔信息
                    idx = \
                    st.session_state.claims_data[st.session_state.claims_data["索赔编号"] == selected_claim_id].index[0]
                    st.session_state.claims_data.loc[idx, "处理状态"] = new_status
                    st.session_state.claims_data.loc[idx, "批准金额"] = approved_amount
                    st.session_state.claims_data.loc[idx, "处理人员"] = handler
                    st.session_state.claims_data.loc[idx, "处理备注"] = remarks
                    st.session_state.claims_data.loc[idx, "更新时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    st.success("✅ 索赔处理结果保存成功！")
                    st.balloons()
        else:
            st.info("🎉 暂无待处理的索赔申请")
            # 显示最近处理的索赔
            recent_processed = st.session_state.claims_data[
                st.session_state.claims_data["处理状态"].isin(["已批准", "已拒绝", "已结案"])].nlargest(10, "更新时间")
            st.subheader("最近处理的索赔")
            st.dataframe(recent_processed, use_container_width=True)

    with tab4:
        st.subheader("📋 索赔记录列表")

        # 筛选选项
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            type_filter = st.selectbox("类型筛选", ["全部"] + list(st.session_state.claims_data["索赔类型"].unique()))
        with col2:
            status_filter = st.selectbox("状态筛选", ["全部"] + list(st.session_state.claims_data["处理状态"].unique()))
        with col3:
            amount_range = st.selectbox("金额范围", ["全部", "0-5000", "5000-20000", "20000-50000", "50000以上"])
        with col4:
            sort_by = st.selectbox("排序方式", ["申请日期", "索赔金额", "更新时间"])

        # 应用筛选
        filtered_data = st.session_state.claims_data.copy()
        if type_filter != "全部":
            filtered_data = filtered_data[filtered_data["索赔类型"] == type_filter]
        if status_filter != "全部":
            filtered_data = filtered_data[filtered_data["处理状态"] == status_filter]

        # 金额筛选
        if amount_range == "0-5000":
            filtered_data = filtered_data[filtered_data["索赔金额"] <= 5000]
        elif amount_range == "5000-20000":
            filtered_data = filtered_data[(filtered_data["索赔金额"] > 5000) & (filtered_data["索赔金额"] <= 20000)]
        elif amount_range == "20000-50000":
            filtered_data = filtered_data[(filtered_data["索赔金额"] > 20000) & (filtered_data["索赔金额"] <= 50000)]
        elif amount_range == "50000以上":
            filtered_data = filtered_data[filtered_data["索赔金额"] > 50000]

        # 排序
        if sort_by == "申请日期":
            filtered_data = filtered_data.sort_values("申请日期", ascending=False)
        elif sort_by == "索赔金额":
            filtered_data = filtered_data.sort_values("索赔金额", ascending=False)
        else:
            filtered_data = filtered_data.sort_values("更新时间", ascending=False)

        # 显示统计信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("记录总数", len(filtered_data))
        with col2:
            st.metric("索赔总额", f"¥{filtered_data['索赔金额'].sum():,.0f}")
        with col3:
            st.metric("批准总额", f"¥{filtered_data['批准金额'].sum():,.0f}")
        with col4:
            if len(filtered_data) > 0:
                avg_amount = filtered_data['索赔金额'].mean()
                st.metric("平均金额", f"¥{avg_amount:,.0f}")

        st.dataframe(filtered_data, use_container_width=True)


def show_statistics():
    """显示数据统计页面"""
    st.markdown('<h1 class="main-header">📈 数据统计分析</h1>', unsafe_allow_html=True)

    # 统计概览
    col1, col2, col3, col4 = st.columns(4)

    total_owners = len(st.session_state.owners_data)
    total_claims = len(st.session_state.claims_data)
    avg_claim_amount = st.session_state.claims_data["索赔金额"].mean()
    max_claim_amount = st.session_state.claims_data["索赔金额"].max()

    with col1:
        st.metric("车主总数", f"{total_owners:,}")
    with col2:
        st.metric("索赔总数", f"{total_claims:,}")
    with col3:
        st.metric("平均索赔金额", f"¥{avg_claim_amount:,.0f}")
    with col4:
        st.metric("最高索赔金额", f"¥{max_claim_amount:,.0f}")

    st.markdown("---")

    # 图表分析
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 索赔金额分布")

        # 创建金额区间
        bins = [0, 5000, 10000, 20000, 50000, float('inf')]
        labels = ['0-5K', '5K-10K', '10K-20K', '20K-50K', '50K+']
        st.session_state.claims_data['金额区间'] = pd.cut(st.session_state.claims_data['索赔金额'], bins=bins,
                                                          labels=labels)
        amount_dist = st.session_state.claims_data['金额区间'].value_counts()

        fig = px.bar(
            x=amount_dist.index,
            y=amount_dist.values,
            title="索赔金额区间分布",
            color=amount_dist.values,
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🕒 申请时间趋势")

        # 按月统计
        st.session_state.claims_data['申请月份'] = pd.to_datetime(
            st.session_state.claims_data['申请日期']).dt.to_period('M')
        monthly_claims = st.session_state.claims_data['申请月份'].value_counts().sort_index()

        fig = px.line(
            x=[str(month) for month in monthly_claims.index],
            y=monthly_claims.values,
            title="月度申请趋势",
            markers=True
        )
        fig.update_layout(xaxis_title="月份", yaxis_title="申请数量")
        st.plotly_chart(fig, use_container_width=True)

    # 详细分析
    tab1, tab2, tab3 = st.tabs(["🚗 车辆分析", "💰 金额分析", "⏱️ 时间分析"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("车辆品牌索赔统计")

            # 获取车主信息与索赔信息的合并数据
            merged_data = st.session_state.claims_data.merge(
                st.session_state.owners_data[['车主编号', '车辆品牌']],
                on='车主编号',
                how='left'
            )

            brand_claims = merged_data['车辆品牌'].value_counts()

            fig = px.pie(
                values=brand_claims.values,
                names=brand_claims.index,
                title="各品牌索赔案件占比"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("品牌平均索赔金额")

            brand_avg_amount = merged_data.groupby('车辆品牌')['索赔金额'].mean().sort_values(ascending=True)

            fig = px.bar(
                x=brand_avg_amount.values,
                y=brand_avg_amount.index,
                orientation='h',
                title="各品牌平均索赔金额",
                color=brand_avg_amount.values,
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("索赔类型金额分析")

            type_amount = st.session_state.claims_data.groupby('索赔类型')['索赔金额'].sum().sort_values(
                ascending=False)

            fig = px.bar(
                x=type_amount.index,
                y=type_amount.values,
                title="各类型索赔总金额",
                color=type_amount.values,
                color_continuous_scale="Greens"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("批准率分析")

            approval_stats = st.session_state.claims_data.groupby('索赔类型').agg({
                '索赔编号': 'count',
                '处理状态': lambda x: (x == '已批准').sum()
            }).rename(columns={'索赔编号': '总数', '处理状态': '批准数'})
            approval_stats['批准率'] = (approval_stats['批准数'] / approval_stats['总数'] * 100).round(1)

            fig = px.bar(
                x=approval_stats.index,
                y=approval_stats['批准率'],
                title="各类型索赔批准率",
                color=approval_stats['批准率'],
                color_continuous_scale="RdYlBu"
            )
            fig.update_layout(yaxis_title="批准率 (%)", xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("处理时效分析")

            # 计算处理天数
            st.session_state.claims_data['申请日期_dt'] = pd.to_datetime(st.session_state.claims_data['申请日期'])
            st.session_state.claims_data['更新日期_dt'] = pd.to_datetime(st.session_state.claims_data['更新时间'])
            st.session_state.claims_data['处理天数'] = (
                        st.session_state.claims_data['更新日期_dt'] - st.session_state.claims_data[
                    '申请日期_dt']).dt.days

            processing_time = st.session_state.claims_data[
                st.session_state.claims_data['处理状态'].isin(['已批准', '已拒绝', '已结案'])]
            avg_processing_by_type = processing_time.groupby('索赔类型')['处理天数'].mean().sort_values()

            fig = px.bar(
                x=avg_processing_by_type.values,
                y=avg_processing_by_type.index,
                orientation='h',
                title="各类型平均处理天数",
                color=avg_processing_by_type.values,
                color_continuous_scale="Viridis"
            )
            fig.update_layout(xaxis_title="天数")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("季度索赔趋势")

            st.session_state.claims_data['申请季度'] = pd.to_datetime(
                st.session_state.claims_data['申请日期']).dt.to_period('Q')
            quarterly_claims = st.session_state.claims_data['申请季度'].value_counts().sort_index()
            quarterly_amount = st.session_state.claims_data.groupby('申请季度')['索赔金额'].sum()

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[str(q) for q in quarterly_claims.index],
                y=quarterly_claims.values,
                mode='lines+markers',
                name='索赔数量',
                yaxis='y'
            ))
            fig.add_trace(go.Scatter(
                x=[str(q) for q in quarterly_amount.index],
                y=quarterly_amount.values,
                mode='lines+markers',
                name='索赔金额',
                yaxis='y2',
                line=dict(color='red')
            ))

            fig.update_layout(
                title="季度索赔数量与金额趋势",
                xaxis_title="季度",
                yaxis=dict(title="索赔数量", side="left"),
                yaxis2=dict(title="索赔金额", side="right", overlaying="y"),
                legend=dict(x=0.01, y=0.99)
            )
            st.plotly_chart(fig, use_container_width=True)


def show_export():
    """显示数据导出页面"""
    st.markdown('<h1 class="main-header">💾 数据导出</h1>', unsafe_allow_html=True)

    st.subheader("📊 数据导出选项")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🗂️ 可导出数据")

        export_options = st.multiselect(
            "选择要导出的数据",
            ["车主信息", "索赔记录", "统计报告"],
            default=["车主信息", "索赔记录"]
        )

        file_format = st.selectbox("选择文件格式", ["Excel (.xlsx)", "CSV (.csv)"])

        date_filter = st.checkbox("按日期筛选索赔记录")
        if date_filter:
            date_range = st.date_input(
                "选择日期范围",
                value=[datetime.now().date() - timedelta(days=90), datetime.now().date()],
                key="export_date"
            )

    with col2:
        st.markdown("### 📈 数据预览")

        if "车主信息" in export_options:
            st.info(f"车主信息: {len(st.session_state.owners_data)} 条记录")
            st.dataframe(st.session_state.owners_data.head(3), use_container_width=True)

        if "索赔记录" in export_options:
            claims_to_export = st.session_state.claims_data.copy()
            if date_filter and len(date_range) == 2:
                claims_to_export = claims_to_export[
                    (pd.to_datetime(claims_to_export["申请日期"]) >= pd.to_datetime(date_range[0])) &
                    (pd.to_datetime(claims_to_export["申请日期"]) <= pd.to_datetime(date_range[1]))
                    ]
            st.info(f"索赔记录: {len(claims_to_export)} 条记录")
            st.dataframe(claims_to_export.head(3), use_container_width=True)

    st.markdown("---")

    # 生成导出文件
    if st.button("🎯 生成导出文件", type="primary"):
        if export_options:
            dataframes = []
            sheet_names = []

            if "车主信息" in export_options:
                dataframes.append(st.session_state.owners_data)
                sheet_names.append("车主信息")

            if "索赔记录" in export_options:
                claims_to_export = st.session_state.claims_data.copy()
                if date_filter and len(date_range) == 2:
                    claims_to_export = claims_to_export[
                        (pd.to_datetime(claims_to_export["申请日期"]) >= pd.to_datetime(date_range[0])) &
                        (pd.to_datetime(claims_to_export["申请日期"]) <= pd.to_datetime(date_range[1]))
                        ]
                dataframes.append(claims_to_export)
                sheet_names.append("索赔记录")

            if "统计报告" in export_options:
                # 生成统计报告
                stats_data = {
                    "统计项目": [
                        "车主总数", "索赔总数", "索赔总金额", "批准总金额",
                        "平均索赔金额", "最高索赔金额", "批准率", "拒绝率"
                    ],
                    "数值": [
                        len(st.session_state.owners_data),
                        len(st.session_state.claims_data),
                        st.session_state.claims_data["索赔金额"].sum(),
                        st.session_state.claims_data["批准金额"].sum(),
                        st.session_state.claims_data["索赔金额"].mean(),
                        st.session_state.claims_data["索赔金额"].max(),
                        len(st.session_state.claims_data[st.session_state.claims_data["处理状态"] == "已批准"]) / len(
                            st.session_state.claims_data) * 100,
                        len(st.session_state.claims_data[st.session_state.claims_data["处理状态"] == "已拒绝"]) / len(
                            st.session_state.claims_data) * 100
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                dataframes.append(stats_df)
                sheet_names.append("统计报告")

            if file_format == "Excel (.xlsx)":
                excel_data = export_to_excel(dataframes, sheet_names)
                filename = f"汽车索赔数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

                st.download_button(
                    label="📥 下载 Excel 文件",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                # CSV格式导出
                for df, name in zip(dataframes, sheet_names):
                    csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                    filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

                    st.download_button(
                        label=f"📥 下载 {name} CSV",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv"
                    )

            st.success("✅ 导出文件已生成！点击上方按钮下载。")
            st.balloons()
        else:
            st.error("❌ 请至少选择一项要导出的数据")

    # 快速导出按钮
    st.markdown("---")
    st.subheader("⚡ 快速导出")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 导出所有车主信息", use_container_width=True):
            csv_data = st.session_state.owners_data.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 下载车主信息CSV",
                data=csv_data,
                file_name=f"车主信息_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("📊 导出所有索赔记录", use_container_width=True):
            csv_data = st.session_state.claims_data.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 下载索赔记录CSV",
                data=csv_data,
                file_name=f"索赔记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col3:
        if st.button("📈 导出完整报告", use_container_width=True):
            excel_data = export_to_excel(
                [st.session_state.owners_data, st.session_state.claims_data],
                ["车主信息", "索赔记录"]
            )
            st.download_button(
                label="📥 下载完整报告Excel",
                data=excel_data,
                file_name=f"汽车索赔完整报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


if __name__ == "__main__":
    main()