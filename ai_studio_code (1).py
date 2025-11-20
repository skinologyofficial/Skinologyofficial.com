    # Informative message about backend URL
    if BACKEND_URL == "https://your-backend-service/analyze/":
        st.info("Note: The backend URL is a placeholder. Replace BACKEND_URL with your live endpoint to enable analysis.")
        # For local testing, we can skip the POST or show what would be sent.
        st.write("Payload preview:", data)
        if files:
            st.write("Files uploaded:", [f for f in files.keys()])
    else:
        try:
            with st.spinner("Sending data to analysis backend..."):
                # Optionally set a timeout
                res = requests.post(BACKEND_URL, files=files if files else None, data=data, timeout=60)
            if res.status_code == 200:
                try:
                    result_dict = res.json()
                except ValueError:
                    st.error("Backend did not return valid JSON.")
                    st.write(res.text)
                else:
                    st.success(labels["success"])
                    # Present result safely
                    result_text = result_dict.get("result") or result_dict
                    st.write(result_text)
                    pdf_url = result_dict.get("pdf_url", "")
                    if pdf_url:
                        st.markdown(f"[{labels['pdf_download']}]({pdf_url})")
            else:
                st.error(labels["fail"])
                st.write(f"Status code: {res.status_code}")
                st.write(res.text)
        except requests.exceptions.RequestException as e:
            st.error(f"{labels['fail']}")
            st.write(str(e))