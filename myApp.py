import streamlit as st
from searchFunctions import isValid,isValidProximity,proximitySearch,findDocs

def loadIndex(filename):
    index = {}
    with open(filename,'r') as f:
        for line in f:
            term,docIDs = line.strip().split(' -> ')
            index[term] = eval(docIDs)
    return index

st.sidebar.title("ℹ️ How to Use")
st.sidebar.markdown("""
- **Boolean Queries:**
  1. Use **AND, OR, NOT** operators.
  2. Max **5 words** including operators.
  3. Only **alphabets** allowed.
  
                    
- **Proximity Queries:**
  1. Enter **two words only**.
  2. Only **alphabets** allowed.
""")
st.sidebar.write("💡 Try queries like:")
st.sidebar.code("image and restoration")
st.sidebar.code("data OR mining")
st.sidebar.code('"artificial intelligence"')

st.title("_Boolean_ _Retrieval_ :blue[Model] :sunglasses:")
st.header("Developed by: :blue[Ahsan Ali]")
st.markdown("This model supports Boolean Queries and Proximity Queries\n")
st.markdown(
    "<hr style='border:1px solid #ddd'>",unsafe_allow_html=True
)  

flag = False
st.markdown("### 📌 Boolean Query Search")
query = st.text_input("Enter a boolean Query: ")
if not query:
    st.write("Query cannot be empty")
    flag = False
words = query.strip().split()

if len(words)>5:
    st.error("🚨 Only 5 words allowed at Max")
    flag = False
for word in words:
    if not word.isalpha():
        st.error("⚠️ Only alphabets allowed")
        flag = False
        break
flag = True

invertedIndex = loadIndex('22K4036_invertedIndex.txt')
positionalIndex = loadIndex('22K4036_positionalIndex.txt')
if flag == True:
    result = isValid(query)
    if isinstance(result,tuple):
        terms,ops,res = result
    if res:
        ans = findDocs(terms,ops,invertedIndex)
        if ans:
            st.success("**✅ Documents Found:**")
            for i,doc in enumerate(ans):
                st.write(f"📄 Document {i+1}: {doc}") 
        else:
            st.warning("🚫 No document found")
        st.markdown("------\n")
    else:
        st.error("❌ Invalid Query! Please enter correct query\n")
else:
    st.error("❌ Invalid Query! Please enter correct query\n")

st.markdown("### 📌 Proximity Query Search")
flag1 = False
proximityQuery = st.text_input("📍 Enter a proximity query: ")
if not proximityQuery:
    st.write("Query cannot be empty")
    flag1 = False
words = proximityQuery.strip().split()
if len(words)!=2:
    st.error("⚠️ Enter only two words")
    flag1 = False
for word in words:
    if not word.isalpha():
        st.error("⚠️ Only alphabets allowed")
        flag1 = False
        break
flag1 = True
if flag1 == True:
    result = isValidProximity(proximityQuery)
    if isinstance(result,tuple):
        terms,res = result
    k = st.number_input("🔢 Enter the value of K: ",min_value=1,step=1,format="%d")
    if res:
        ans = proximitySearch(terms,k,positionalIndex)
        if ans:
            st.success("**✅ Documents Found:**")
            for i,doc in enumerate(ans):
                st.write(f"📄 Document {i+1}: {doc}") 
        else:
            st.warning("🚫 No document found")
        st.markdown("----\n")
    else:
        st.error("❌ Invalid Query! Please enter correct query\n")
else:
    st.error("❌ Invalid Query! Please enter a valid query\n")



