#################################
# Guloader strings deobfuscator 
#################################
# Created: 7 June 2024          
# Author: 0xB4DC0DE          
# Last updated: 10 June 2024    
#################################


import re
# Global variables #
filename = "C:\\Users\\Flare\\Desktop\\New folder\\Stage3_testing.ps1"
# Encoding may have to be changed to UTF-16 if working from a file dumped from powershell
encoding = "UTF-8"
search_index = 5
xor_value = 114

# Open file and decode as UTF-16 and split on newline character #
with open(filename,'rb') as f:
    contents = f.read().decode(encoding)
clean_contents = contents
contents = contents.splitlines()

# Use regex to match all lines containing strings enclosed within single quotes #
match = []
for i in contents:
    res = re.search("'(.*?)'",i)
    if res:
        match.append(res.group().replace("'",""))

# Decrypt strings using substring algorithm #
def search_string_algo(encrypted_string):
    output_string = ""
    length = len(encrypted_string) - 1
    for i in range(search_index,length,search_index+1):
        output_string += encrypted_string[i:i+1]
    return(output_string)

# Decrypt strings using XOR algorithm #
def xor_string_algo(encoded_string):
    length = len(encoded_string)
    output_string = ""
    byte_array = ([encoded_string[i:i+2] for i in range(0, len(encoded_string), 2)])
    for i in byte_array:
        try:
            output_string += chr(int(i,16) ^ xor_value)
        except:
            break
    return (output_string)

# Determine what algorithm to use and drop values into their respective arrays #
found_variables = []
other_strings = []
for i in match:
    
    decrypted_string = search_string_algo(i)
    if decrypted_string[0:1] == "$" or decrypted_string[0:1] == "i" or decrypted_string[0:1] == "\\"  or decrypted_string[0:1] == "p" or decrypted_string[0:1] == "e":
        found_variables.append([i,decrypted_string])
    else:
        decoded_string = xor_string_algo(i)
        other_strings.append([i,decoded_string])

# Remove all lines starting with '#' #
clean_contents = re.sub('^#.*$',"",clean_contents, flags=re.MULTILINE)

for i in found_variables[::-1]:
    print(i[0][0:10],":",i[1])
    clean_contents = clean_contents.replace(i[0],i[1])

for i in other_strings[::-1]:
    print(i[0][0:25],":",i[1])
    clean_contents = clean_contents.replace(i[0],i[1])

# Remove all extra spacing in the deobfuscated output #
clean_contents = clean_contents.replace("\n\n","\n")
clean_contents = clean_contents.replace("\r","")
print("\n\n",clean_contents)

# Write changes to a new file and append .deobfuscated to the end #
with open(filename + "_deobfuscated.ps1", 'w') as file:
  file.write(clean_contents)
    