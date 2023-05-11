# Rule Based Healthcare Chatbot using NLP and Machine Learning
 HealthBot - Diagnosis and Chatbot Application

This repository contains a Python application called HealthBot, which combines a diagnosis system and a chatbot to assist users in identifying potential health issues based on symptoms.

The HealthBot application consists of three main components:

1. Decision Tree Classifier for Disease Diagnosis:
   - The file `bot_training.py` contains code that trains a decision tree classifier using a provided dataset (`Training.csv` and `Testing.csv`) to predict diseases based on symptoms.
   - The classifier uses a dimensionality reduction technique and feature encoding to preprocess the data.
   - The code prompts the user with a series of questions about symptoms and provides a predicted diagnosis based on their responses.
   - The accuracy and confidence level of the diagnosis are also displayed.

2. User Interface:
   - The file `app.py` integrates the diagnosis code into a graphical user interface (GUI) application using the Tkinter library.
   - The GUI allows users to register, log in, and interact with the diagnosis system through a question-answer format.
   - The GUI provides a user-friendly interface for inputting symptoms, viewing diagnoses, and navigating between different screens.

3. Dataset:
   - The dataset used in the diagnosis system is stored in the `Training.csv`, `Testing.csv` and `doctors_dataset.csv` files.
   - This dataset, containing symptoms and corresponding disease labels, was obtained from [`doctors_dataset.csv`].
   - It is important to note that the dataset and code provided here are an enhancement of another person's work.

## Prerequisites

To run the HealthBot application, you need to have the following installed on your system:

- Python (version X.X)
- Tkinter library (included in Python's standard library)
- pandas
- numpy
- scikit learn

## Installation and Usage

1. Clone or download this repository to your local machine.
2. Install the required dependencies, if not already installed.
3. Run the `app.py` file using Python to start the HealthBot application.
4. The application window will open, allowing you to register or log in.
5. Once logged in, you can proceed with the diagnosis process by answering the questions about symptoms.
6. The application will provide a predicted diagnosis based on your responses.

## Contributing

Contributions to the HealthBot application are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Your feedback and contributions will help enhance the functionality and usability of the application.

## Acknowledgments

- The dataset used in this application was obtained from [shreyasharma04]. We acknowledge the original creators of the dataset for their valuable work.
- The code in this repository was inspired by [shreyasharma04] (please provide attribution to the original work if applicable). I have built upon their code to enhance the functionality and integrate it into a user-friendly interface.



