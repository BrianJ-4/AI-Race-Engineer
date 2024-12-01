from utils.intent_ner_integration import process_input
from SR.microphone_input import startRecord
#test

def main():    
    #print("Enter q to quit.")
    startRecord()

    # while True:
    #     # Get user inputC
    #     input_string = input("Enter query: ")

    #     if input_string.lower() == "q":
    #         print("Exiting system.")
    #         break

    #     # Process the input string through intent classification and NER
    #     action_data = process_input(input_string)
    #     print(action_data)

if __name__ == "__main__":
    main()
