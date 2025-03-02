import streamlit as st
from web_functions import predict
import numpy as np
import pandas as pd

# 注入 CSS
st.markdown("""
<style>
/* 主内容容器（包含所有组件的区域） */
.block-container {
    max-width: 90% !important;  /* 调整为页面宽度的 90% */
    padding: 20px 5% !important;  /* 同步调整内边距 */
}

/* 调整列布局的间距（配合宽容器使用） */
[data-testid="column"] {
    padding: 0 1rem !important;  /* 减少列间空白 */
}
</style>
""", unsafe_allow_html=True)

# Add title to the page
st.title("中转剖预测")

# Add a brief description
st.markdown(
    """
        <p style="font-size:25px">
            该应用使用随机森林模型来预测产妇中转剖
        </p>
    """, unsafe_allow_html=True)

# Take feature input from the user
# Add a subheader
st.subheader("输入相关数据：")

col1, col2, col3 = st.columns(3)

with st.container():
    with col1:
        height = st.number_input(label="身高：", value=None, placeholder="请输入身高(cm)", step=1, format='%d')
        days = st.number_input(label="妊娠天数：", value=None, placeholder="请输入妊娠天数(天)", step=1, format='%d')
    with col2:
        body_mass_index = st.number_input(label="BMI：", value=None, placeholder="请输入BMI值", step=0.1, format='%0.2f')
        head_circumference = st.number_input(label="头围：", value=None, placeholder="请输入胎儿头围(mm)", step=1,
                                             format='%d')
    with col3:
        weight_gain = st.number_input(label="增重：", value=None, placeholder="请输入妊娠期体重增加的值(kg)", step=0.1,
                                      format='%0.1f')

    anemia = st.radio(
        "是否贫血：",
        options=['无', '轻度', '中度'],
        index=0,
        horizontal=True
    )

    premature_rupture_of_membranes = st.radio(
        "是否胎膜早破：",
        options=['是', '否'],
        index=0,
        horizontal=True
    )

    heat_disease = st.radio(
        "是否发热：",
        options=['是', '否'],
        index=0,
        horizontal=True
    )

    birth_fetal_position = st.radio(
        "胎位：",
        options=['左枕前(LOA)', '右枕前(ROA)', '左枕横(LOT)', '右枕横(ROT)', '左枕后(LOP)', '右枕后(ROP)'],
        index=0,
        horizontal=True
    )
anemia_mapping = {
    '无': 'no',
    '轻度': 'mild',
    '中度': 'moderate'
}
mapping = {"是": 'yes', "否": 'no'}
bfp_mapping = {
    '左枕前(LOA)': 'LOA',
    '右枕前(ROA)': 'ROA',
    '左枕横(LOT)': 'LOT',
    '右枕横(ROT)': 'ROT',
    '左枕后(LOP)': 'LOP',
    '右枕后(ROP)': 'ROP'
}

features = {
    'height': height,
    'body_mass_index': body_mass_index,
    'weight_gain': weight_gain,
    'days': days,
    'head_circumference': head_circumference,
    'anemia': anemia_mapping[anemia],
    'premature_rupture_of_membranes': mapping[premature_rupture_of_membranes],
    'heat_disease': mapping[heat_disease],
    'birth_fetal_position': bfp_mapping[birth_fetal_position],
}

columns = ['height',
           'body_mass_index',
           'weight_gain',
           'days',
           'head_circumference',
           'anemia_moderate',
           'anemia_no',
           'premature_rupture_of_membranes_yes',
           'heat_disease_yes',
           'birth_fetal_position_LOP',
           'birth_fetal_position_LOT',
           'birth_fetal_position_ROA',
           'birth_fetal_position_ROP',
           'birth_fetal_position_ROT'
           ]
column_type_map = {
    'height': 'int64',
    'body_mass_index': 'float64',
    'weight_gain': 'float64',
    'days': 'int64',
    'head_circumference': 'float64',
    'anemia_moderate': 'uint8',
    'anemia_no': 'uint8',
    'premature_rupture_of_membranes_yes': 'uint8',
    'heat_disease_yes': 'uint8',
    'birth_fetal_position_LOP': 'uint8',
    'birth_fetal_position_LOT': 'uint8',
    'birth_fetal_position_ROA': 'uint8',
    'birth_fetal_position_ROP': 'uint8',
    'birth_fetal_position_ROT': 'uint8'
}


@st.dialog("预测结果：")
def vote(res):
    if res == 1:
        st.write("当前预测的结果为： 有很大的可能会发生中转剖")
    else:
        st.write("当前预测的结果为： 有很大的可能自然分娩")
    if st.button("关闭"):
        st.rerun()


if st.button("预测"):
    df = pd.DataFrame(
        np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(1, -1),
        columns=columns
    )
    for column in columns:
        if column in features:
            df[column] = [features[column]]
        else:
            for key, value in features.items():
                str1 = "" + key + "_" + str(value)
                if str1 == column:
                    df[column] = [1]
        df[column] = df[column].astype(column_type_map[column])
    prediction = predict(df)
    vote(prediction[0])
