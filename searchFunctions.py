from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
def isValid(query):
    #there can be maximum of three words in a boolean query so there would be max of 5 words including operators(AND,OR,NOT)
    query = query.lower().strip() #remove any extra spaces
    if not query:
        print("Query cannot be empty")
        return None,None,False

    words = query.split()
    if len(words)>5:
        print("Only 3 words allowed at Max")
        return None,None,False
    
    for word in words:
        if not word.isalpha():
            print("Only alphabets allowed")
            return None,None,False

    operators = {'and','or','not'}
    for i in range(len(words)):
        if i%2==1:  #operators would be at odd positions
            if words[i] not in operators:
                print("Invalid Operators or invalid format")
                return None,None,False
        elif i%2==0:
            if words[i] in operators:
                print("Operator at wrong position")
                return None,None,False
    terms = []
    ops = []
    for word in words:
        if word in operators:
            ops.append(word)
        else:
            terms.append(ps.stem(word))

    return terms,ops,True


def findDocs(terms,ops,invertedIndex):
    all_docs = set()
    for doc_list in invertedIndex.values():
        all_docs.update(doc_list)

    if len(terms) == 1:
        if terms[0] in invertedIndex:
            return invertedIndex[terms[0]]
        else:
            print(f"Term: {terms[0]} not found in documents")
            return []
    elif len(terms) == 2:
        l1 = []
        l2 = []
        if terms[0] in invertedIndex:
            l1 = invertedIndex[terms[0]]
        else:
            print(f"Term: {terms[0]} not found in documents")
            return []
        if terms[1] in invertedIndex:
            l2 = invertedIndex[terms[1]]
        else:
            print(f"Term: {terms[1]} not found in documents")
            return []
        if len(ops) == 1:
            if ops[0] == 'and':
                ans = []
                i,j = 0,0 #Two pointer approach
                while i<len(l1) and j<len(l2):
                    if l1[i] == l2[j]:
                        ans.append(l1[i])
                        i+=1
                        j+=1
                    elif l1[i]<l2[j]:
                        i+=1
                    else:
                        j+=1
                return ans
            #Could have implemented or and not as well with two pointer but code would have been longer so i used set operations
            if ops[0] == 'or':
                return list(set(l1+l2))  #union
            if ops[0] == 'not':
                return list(set(l1)-set(l2))
    elif len(terms) == 3:
        l1 = []
        l2 = []
        l3 = []
        if terms[0] in invertedIndex:
            l1 = invertedIndex[terms[0]]
        else:
            print(f"Term: {terms[0]} not found in documents")
            return []
        if terms[1] in invertedIndex:
            l2 = invertedIndex[terms[1]]
        else:
            print(f"Term: {terms[1]} not found in documents")
            return []
        if terms[2] in invertedIndex:
            l3 = invertedIndex[terms[2]]
        else:
            print(f"Term: {terms[2]} not found in documents")
        #Logical rule = (term1 op term2) op term 3
        if ops[0] == 'and' and ops[1] == 'and':
            return list(set(l1) & set(l2) & set(l3))

        if ops[0] == 'and' and ops[1] == 'or':
            return list((set(l1) & set(l2)) | set(l3))

        if ops[0] == 'or' and ops[1] == 'and':
            return list((set(l1) | set(l2)) & set(l3))

        if ops[0] == 'or' and ops[1] == 'or':
            return list(set(l1) | set(l2) | set(l3))

        if ops[0] == 'and' and ops[1] == 'not':
            return list(set(l1) & (set(l2) - set(l3)))

        if ops[0] == 'or' and ops[1] == 'not':
            return list((set(l1) | set(l2)) - set(l3))
        
        if ops[0] == 'not' and ops[1] == 'and':
            return list((all_docs - set(l1)) & set(l3))
        
        if ops[0] == 'not' and ops[1] == 'or':
            return list((all_docs - set(l1)) | set(l3))
        
        if ops[0] == 'not' and ops[1] == 'not':
            return list(all_docs - set(l1) - set(l2))
    return []
    
#Query Validation
def isValidProximity(query):
    query = query.lower().strip() #remove any extra spaces
    if not query:
        print("Query cannot be empty")
        return [],False

    words = query.split()
    if len(words)!=2:
        print("enter only two words")
        return [],False
    
    for word in words:
        if not word.isalpha():
            print("Only alphabets allowed")
            return [],False

    terms = []
    ps = PorterStemmer()
    for word in words:
        terms.append(ps.stem(word))

    return tuple(terms),True


def proximitySearch(terms,k,positionalIndex):

    term1,term2 = terms
    if term1 not in positionalIndex or term2 not in positionalIndex:
        print(f"Either term: {term1} or term: {term2} not found in documents")
        return []
    
    ans = set()
    for doc in positionalIndex[term1].keys() & positionalIndex[term2].keys():  #finds common docs
        pos1 = sorted(positionalIndex[term1][doc])
        pos2 = sorted(positionalIndex[term2][doc])

        i,j = 0,0
        while i<len(pos1) and j<len(pos2):
            if abs(pos1[i]-pos2[j]) <= k:
                ans.add(doc)
                i+=1
            elif pos1[i]<pos2[j]:
                i+=1
            else:
                j+=1
    return list(ans)






