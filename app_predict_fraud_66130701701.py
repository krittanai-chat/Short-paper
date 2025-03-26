
import streamlit as st
import pandas as pd
import pickle

# โหลดโมเดลที่ฝึกเสร็จแล้ว
with open('model_fraud_66130701701.pkl', 'rb') as file:
    model = pickle.load(file)

# ฟังก์ชันในการทำนายการฉ้อโกง
def predict_fraud(step, txn_type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFlaggedFraud):
    input_data = pd.DataFrame({
        'step': [step],
        'type': [txn_type],  # ต้องใช้ค่าที่ถูกต้องจาก LabelEncoder
        'amount': [amount],
        'oldbalanceOrg': [oldbalanceOrg],
        'newbalanceOrig': [newbalanceOrig],
        'oldbalanceDest': [oldbalanceDest],
        'newbalanceDest': [newbalanceDest],
        'isFlaggedFraud': [isFlaggedFraud]
    })
    prediction = model.predict(input_data)
    return prediction[0]

# การตั้งค่าหน้า Streamlit
st.title("ระบบทำนายการฉ้อโกงทางการเงิน")
st.write("กรุณากรอกข้อมูลธุรกรรมเพื่อทำนายว่ามีการฉ้อโกงหรือไม่")

# ช่องกรอกข้อมูลของผู้ใช้
step = st.number_input("Step (ลำดับของธุรกรรม)", min_value=1, value=1)
txn_type = st.selectbox("ประเภทธุรกรรม", [1, 2, 3, 4, 5])  # ต้องตรงกับค่าที่ใช้ใน LabelEncoder
amount = st.number_input("จำนวนเงินที่โอน", min_value=0.0, value=5000.0)
oldbalanceOrg = st.number_input("ยอดเงินเดิมของผู้ส่ง", min_value=0.0, value=20000.0)
newbalanceOrig = st.number_input("ยอดเงินใหม่ของผู้ส่ง", min_value=0.0, value=15000.0)
oldbalanceDest = st.number_input("ยอดเงินเดิมของผู้รับ", min_value=0.0, value=5000.0)
newbalanceDest = st.number_input("ยอดเงินใหม่ของผู้รับ", min_value=0.0, value=10000.0)
isFlaggedFraud = st.selectbox("ธุรกรรมถูกตั้งค่าสถานะฉ้อโกงหรือไม่", [0, 1])

# ปุ่มพยากรณ์
if st.button("ทำนายการฉ้อโกง"):
    result = predict_fraud(step, txn_type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFlaggedFraud)
    st.write(f"ผลการพยากรณ์: {'เป็นการฉ้อโกง' if result == 1 else 'ไม่ใช่การฉ้อโกง'}")
