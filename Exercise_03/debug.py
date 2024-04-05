import streamlit as st
import gccompute 
import hashlib

def main():
    st.title("GC Content")
    st.write("Upload a sequence in fasta format.")
    user_input = st.text_area("Enter sequence (if you want to process multiple sequences, include the headers!)", height=100)
    if st.button("Calculate"):
    # Trigger the method when the button is clicked
        try:
            gc_contents = gccompute.main(user_input)
            for header, gc_content in gc_contents.items():
                st.write(f"GC-content of {header}: {gc_content:.2f}%")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Display a file uploader widget
    uploaded_file = st.file_uploader("Upload a file")


    # Check if a file was uploaded
    if uploaded_file is not None:
        # Process the uploaded file
        file_name = uploaded_file.name
        st.write("File uploaded:", file_name)
        file_contents = uploaded_file.getvalue()
        md5_hash = hashlib.md5(file_contents).hexdigest()
        st.write("MD5 hash:", md5_hash)
  
        # Check the file extension
        if file_name.endswith(('.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn')):
            st.success("File uploaded successfully!")
            input = uploaded_file.read()
            print("Before gcc compute")
            try:
                gc_contents = gccompute.main(input)
                for header, gc_content in gc_contents.items():
                    st.write(f"GC-content of {header}: {gc_content:.2f}%")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            # Process the uploaded file
        else:
            st.error("Invalid file format. Please upload a valid FASTA file.")


if __name__ == "__main__":
    main()