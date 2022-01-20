# initializing string 
test_string = "45.657"

# printing original string 
print("The original string : " + str(test_string))


res = test_string.replace('.', '', 1).isdigit()

# print result
print(res)
print("Is string a possible float number ? : " + str(res))