from utils.intent_ner_integration import process_input
#test

def main():    
    print("Enter q to quit.")
    
    while True:
        # Get user input
        input_string = input("Enter query: ")

        if input_string.lower() == "q":
            print("Exiting system.")
            break

        # Process the input string through intent classification and NER
        action_data = process_input(input_string)

if __name__ == "__main__":
    main()
