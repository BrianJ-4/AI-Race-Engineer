from utils.intent_ner_integration import ProcessInput
from actions.action_handler import PerformAction

def main():    
    print("Enter q to quit.")
    
    while True:
        # Get user input
        input_string = input("Enter query: ")

        if input_string.lower() == "q":
            print("Exiting system.")
            break

        # Process the input string through intent classification and NER
        action_data = ProcessInput(input_string)
        PerformAction(action_data)

if __name__ == "__main__":
    main()