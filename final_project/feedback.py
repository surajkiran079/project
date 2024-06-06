import streamlit as st
import subprocess

# Title of the feedback form
st.title("Feedback Form")

# Gather user's name
name = st.text_input("Your Name")

# Gather user's feedback
feedback = st.text_area("Feedback", height=200)

# Gather user's rating
rating = st.slider("Rating (1-5)", min_value=1, max_value=5, step=1)

# Submit button
if st.button("Submit"):
    # Process the feedback (in this example, we print it)
    st.success("Feedback Submitted!")
    st.write(f"Name: {name}")
    st.write(f"Feedback: {feedback}")
    st.write(f"Rating: {rating}")

    # Save the feedback to a file or database
    with open("feedbacks.txt", "a") as f:
        f.write(f"Name: {name} \n")
        f.write(f"Feedback: {feedback} \n")
        f.write(f"Rating: {rating}\n")
        f.write("\n")

# Display all feedbacks below the form
st.subheader("All Feedbacks")
with open("feedbacks.txt", "r") as f:
    all_feedbacks = f.readlines()
    for feedback in all_feedbacks:
        st.write(feedback.strip())

