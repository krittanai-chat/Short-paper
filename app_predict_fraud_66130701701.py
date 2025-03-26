import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# โหลดโมเดลที่ฝึกเสร็จแล้ว
with open('model_fraud_66130701701.pkl', 'rb') as file:
    model = pickle.load(file)

# กำหนดค่า LabelEncoder สำหรับ type
txn_types = ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN']
le = LabelEncoder()
le.fit(txn_types)  # ฝึก encoder กับค่าที่ใช้ในการฝึก

# ฟังก์ชันในการทำนายการฉ้อโกง
def predict_fraud(step, txn_type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFlaggedFraud):
    input_data = pd.DataFrame({
        'step': [step],
        'type': [txn_type],  # ส่งค่า type ที่เป็นตัวเลขไปยังโมเดล
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
txn_type_input = st.selectbox("ประเภทธุรกรรม", txn_types)  # ให้ผู้ใช้เลือกจากประเภทธุรกรรม
txn_type = le.transform([txn_type_input])[0]  # แปลงค่าที่เลือกจากผู้ใช้ให้เป็นตัวเลข
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
