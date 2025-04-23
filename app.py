import streamlit as st
import pickle
import numpy as np

with open('model.pkl', 'rb') as fil:
    model = pickle.load(fil)
st.title('توقع أداء الفريلانسر')
st.write("""
أدخل المعلومات أدناه للحصول على التوقع:
""")

with st.form("prediction_form"):
    job_completed = st.number_input('عدد المهام المكتملة', min_value=0.0)
    earnings_usd = st.number_input('الأرباح بالدولار', min_value=0.0)
    hourly_rate = st.number_input('سعر الساعة (دولار)', min_value=0.0)
    job_success_rate = st.number_input('نسبة نجاح الوظائف (%)', min_value=0.0, max_value=100.0)
    client_rating = st.number_input('تقييم العميل (من 5)', min_value=0.0, max_value=5.0)
    job_duration_days = st.number_input('مدة العمل بالأيام', min_value=0.0)
    rehire_rate = st.number_input('نسبة إعادة التوظيف (%)', min_value=0.0, max_value=100.0)
    marketing_spend = st.number_input('الإنفاق على التسويق بالدولار', min_value=0.0)

    job_category = st.selectbox('تصنيف الوظيفة', ['App Development', 'Content Writing', 'Customer Support', 'Data Entry', 'Digital Marketing', 'Graphic Design', 'SEO', 'Web Development'])
    platform = st.selectbox('المنصة', ['Fiverr', 'Freelancer', 'PeoplePerHour', 'Toptal', 'Upwork'])
    experience_level = st.selectbox('مستوى الخبرة', ['Beginner', 'Intermediate', 'Expert'])
    client_region = st.selectbox('منطقة العميل', ['Asia', 'Australia', 'Canada', 'Europe', 'Middle East', 'UK', 'USA'])
    payment_method = st.selectbox('طريقة الدفع', ['Bank Transfer', 'Crypto', 'Mobile Banking', 'PayPal'])
    project_type = st.selectbox('نوع المشروع', ['Fixed', 'Hourly'])

    submit = st.form_submit_button("توقع")

if submit:
    try:
        features = [
            job_completed, earnings_usd, hourly_rate, job_success_rate,
            client_rating, job_duration_days, rehire_rate, marketing_spend
        ]

        job_category_options = ['App Development', 'Content Writing', 'Customer Support', 'Data Entry', 'Digital Marketing', 'Graphic Design', 'SEO', 'Web Development']
        features.extend([1 if job_category == option else 0 for option in job_category_options])
        platform_options = ['Fiverr', 'Freelancer', 'PeoplePerHour', 'Toptal', 'Upwork']
        features.extend([1 if platform == option else 0 for option in platform_options])
        experience_options = ['Beginner', 'Intermediate', 'Expert']
        features.extend([1 if experience_level == option else 0 for option in experience_options])
        client_region_options = ['Asia', 'Australia', 'Canada', 'Europe', 'Middle East', 'UK', 'USA']
        features.extend([1 if client_region == option else 0 for option in client_region_options])
        payment_options = ['Bank Transfer', 'Crypto', 'Mobile Banking', 'PayPal']
        features.extend([1 if payment_method == option else 0 for option in payment_options])
        project_type_options = ['Fixed', 'Hourly']
        features.extend([1 if project_type == option else 0 for option in project_type_options])

        final_features = np.array([features])
        prediction = model.predict(final_features)

        st.success(f'التوقع: {prediction[0]}')

    except Exception as e:
        st.error("حدث خطأ في معالجة البيانات.")
