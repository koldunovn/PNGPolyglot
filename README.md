# PGNPolyglot

**PGNPolyglot** is a Python script that translates chess annotations and comments in PGN (Portable Game Notation) files into any target language using OpenAI's language models. This tool is designed to help chess enthusiasts, coaches, and players around the world access annotated games in their preferred language.

**Cost:**: Script uses OpenAI API, that cost money. However translation of moderate-size file with comments will cost you just a few cents (also depends on the model you choose).

## Features

- Translates all comments in PGN files, including those before and after moves, as well as in variations.
- Supports batch processing of comments for efficient translation.
- Handles large PGN files with multiple games and extensive annotations.
- Easy configuration through a simple `config.txt` file.

## Requirements

- Python 3.7 or higher
- An OpenAI API key

## Installation

Follow these steps to set up PGNPolyglot on your system.

### 1. Install Python

If you don't already have Python installed, download and install the latest version of Python from the official website:

- [Download Python](https://www.python.org/downloads/)

Make sure to check the option to add Python to your system's PATH during installation.

### 2. Clone the Repository

Clone the PGNPolyglot repository from GitHub:

```bash
git clone https://github.com/koldunovn/PNGPolyglot.git
```

Alternatively, you can download the repository as a ZIP file and extract it to your desired location.

### 3. Install Required Packages

Navigate to the project directory and install the necessary Python packages using `pip`:

```bash
cd PGNPolyglot
pip install -r requirements.txt
```

The required packages are:

- `python-chess`
- `openai`
- `regex` (if not already installed)

### 4. Obtain an OpenAI API Key

To use PGNPolyglot, you need an API key from OpenAI.

#### Steps to Obtain an API Key:

1. **Sign Up or Log In**: If you don't have an OpenAI account, sign up at [OpenAI's website](https://platform.openai.com/signup/). If you already have an account, log in at [OpenAI's login page](https://platform.openai.com/login/).

2. **Navigate to API Keys**: Once logged in, go to the [API Keys page](https://platform.openai.com/account/api-keys).

3. **Create a New API Key**: Click on the "Create new secret key" button. A new API key will be generated.

4. **Copy the API Key**: Copy the generated API key. **Note**: This is the only time you will be shown the full API key. Make sure to save it securely.

5. **Billing Information**: Ensure that you have set up billing information if required. OpenAI offers a free trial with free credits, but usage beyond that will require payment.

### 5. Configure PGNPolyglot

Update the `config.txt` file in the project directory with your settings.

#### Steps:

1. Open `config.txt` in a text editor.

2. Update the following fields:

   ```plaintext
   API_KEY=your-api-key-here
   MODEL_VERSION=gpt-4o-mini
   TARGET_LANGUAGE=Russian
   INPUT_PGN=input.pgn
   OUTPUT_PGN=output_translated.pgn
   ```

   - **API_KEY**: Paste your OpenAI API key here.
   - **MODEL_VERSION**: Specify the OpenAI model to use (`gpt-4o-mini` is recommended). [List of OpenAI model versions and their prices](https://platform.openai.com/docs/models).
   - **TARGET_LANGUAGE**: Set the language you want to translate the comments into (e.g., `Spanish`, `French`, `German`, etc.).
   - **INPUT_PGN**: The path to your input PGN file with annotations to translate.
   - **OUTPUT_PGN**: The path where the translated PGN file will be saved.

3. Save and close the `config.txt` file.

## Usage

Once you have completed the installation and configuration, you can run PGNPolyglot to translate your PGN files.

### Running the Script

Open a terminal or command prompt in the project directory and run:

```bash
python PNGPolyglot.py
```

The script will process the PGN file specified in the `config.txt` file, translate all comments into the target language, and save the translated PGN to the specified output file.

### Monitoring Progress

As the script runs, it will display progress messages in the terminal:

- The current game being processed.
- The number of comments being translated.
- Any warnings or errors encountered.

Example output:

```plaintext
Processing Game 1: Spasov, Vasil vs Lilov, Valeri, Golden Sands Europe op 2nd, Golden Sands, 2013.06.17
Translating 25 comments...
Translating batch 1/3 with 10 comments...
Translating batch 2/3 with 10 comments...
Translating batch 3/3 with 5 comments...
Translation completed. Translated PGN saved to output_translated.pgn.
```

## Notes

- **API Usage and Costs**: Be aware that using the OpenAI API may incur costs, especially when processing large PGN files or multiple files. Monitor your usage and set up usage limits if necessary.

- **Rate Limits**: The OpenAI API has rate limits. If you process very large files or run multiple instances of the script simultaneously, you may encounter rate limit errors.

- **Translation Quality**: The quality of the translation depends on the model used. For higher quality, you may consider using more expensive models. [List of OpenAI model versions and their prices](https://platform.openai.com/docs/models).

- **Supported Languages**: The script supports translation into any language that the OpenAI model can handle. Common languages like Spanish, French, German, Russian, Chinese, etc., are well-supported.

- **Character Encoding**: Ensure that your input PGN files are encoded in UTF-8. The script reads and writes files using UTF-8 encoding.

## Troubleshooting

- **Import Errors**: If you encounter import errors when running the script, ensure that all required packages are installed. Run `pip install -r requirements.txt` again.

- **API Errors**: If you receive errors related to the OpenAI API, check that your API key is correct and that you have not exceeded your usage limits.

- **Script Crashes**: If the script crashes or exits unexpectedly, check the terminal output for error messages. Common issues include incorrect file paths, malformed PGN files, or network connectivity problems.

## Contributing

Contributions to PGNPolyglot are welcome! Feel free to submit issues or pull requests on the [GitHub repository](https://github.com/koldunovn/PNGPolyglot).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the `python-chess` library for providing a robust tool for handling PGN files.
- Thanks to OpenAI for providing accessible language models that make this project possible.

---

**Disclaimer**: This tool uses the OpenAI API to perform translations. Please ensure that your use complies with OpenAI's [Usage Policies](https://platform.openai.com/docs/usage-policies) and any local regulations regarding data privacy and processing.
