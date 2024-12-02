<<<<<<< HEAD
from SR.microphone_input import startRecord

def main():    
    startRecord()
=======
from utils.intent_ner_integration import process_input

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
        print(action_data)
>>>>>>> 4404cefe8f09da6523ac6e695757471c721f3c5c

if __name__ == "__main__":
    main()
