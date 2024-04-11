global hello
hello = "Cool"

def main():
    global hello
    if hello == "Bad":
        print("Epic")
        hello = "Lit"
    print (hello)

main()
