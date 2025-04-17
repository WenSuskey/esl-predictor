import streamlit as st
import pandas as pd
from xgboost import XGBRegressor
import math

# 载入模型
models = {
    "1.54\"": XGBRegressor(),
    "2.66\"": XGBRegressor(),
    "4.20\"": XGBRegressor()
}
models["1.54\""].load_model("final_model_1.54.json")
models["2.66\""].load_model("final_model_2.66.json")
models["4.20\""].load_model("final_model_4.20.json")


# 页面布局
st.title("Store ESL Prediction Assistant")

total_sq_ft = st.number_input("Total SQ FT", value=100000)
sales_sq_ft = st.number_input("Sales SQ FT", value=70000)
major_type = st.selectbox("Major Type", ["MARKETPLACE", "COMBINATION"])
major_type_code = 0 if major_type == "MARKETPLACE" else 1

res = []
if st.button("Start Prediction"):
    input_df = pd.DataFrame([{
        "Total SQ FT": total_sq_ft,
        "Sales SQ FT": sales_sq_ft,
        "Sales / Total": sales_sq_ft / total_sq_ft,
        "Major Type_Code": major_type_code
    }])

    st.subheader("Prediction Results")
    for size, model in models.items():
        pred = model.predict(input_df)[0]
        pred_with_buffer = 0
        if size == "1.54\"":
            pred_with_buffer = int(round(max(pred * 1.05, pred + 271)))
        elif size == "2.66\"":
            pred_with_buffer = int(round(max(pred * 1.05, pred + 241)))
        elif size == "4.20\"":
            pred_with_buffer = int(round(max(pred * 1.05, pred + 27)))

        st.write(f"🔹 {size}: {int(pred_with_buffer)} Esls")
        res.append({"size": size, "esl": int(pred_with_buffer)})
    st.subheader("Prediction Results（5% Buffer Included)")
    for item in res:
        count = int(item['esl'] * 1.05)
        st.write(f"🔹 {item['size']}: {count} Esls")
    st.subheader("Suggested PO Quantity")
    totalEsl = 0
    for item in res:
        count = int(item['esl'] * 1.05)

        boxCount = 0
        if size == "1.54\"":
            boxCount = 300
        elif size == "2.66\"":
            boxCount = 280
        elif size == "4.20\"":
            boxCount = 140
        po = count / boxCount
        orderEsls = math.ceil(po)*boxCount
        st.write(
            f"🔹 {item['size']}: {math.ceil(po)} Boxs,  Total:  {orderEsls} Esls")
        totalEsl += orderEsls
    st.subheader(f"TTotal ESLs to order: {totalEsl}")
