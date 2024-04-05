import streamlit as st
import gccompute 

def main():
    st.title("GC Content")
    st.write("Upload a sequence in fasta format.")
    user_input = st.text_area("Enter sequence", height=100)
    if st.button("Calculate"):
    # Trigger the method when the button is clicked
        gccompute.main(user_input, type='text')

    # Display a file uploader widget
    uploaded_file = st.file_uploader("Upload a file")


    # Check if a file was uploaded
    if uploaded_file is not None:
        # Process the uploaded file
        st.write("File uploaded:", uploaded_file.name)
        file_name = uploaded_file.name
        # Check the file extension
        if file_name.endswith(('.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn')):
            st.success("File uploaded successfully!")
            input = uploaded_file.read()
            gccompute.main(input, type='text')
            # Process the uploaded file
        else:
            st.error("Invalid file format. Please upload a PNG, JPG, or JPEG file.")


if __name__ == "__main__":
    main()