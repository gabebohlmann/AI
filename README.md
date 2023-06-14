# AI
This is a ChatGPT based voice chat bot that is meant for language learning. The app is written in python and meant to be run from the command line with voice input from the user. Voice input from the user can be taken in their native language, target language, or some combination of the two. The intention of the program is for the user to push the limits of what they can say in the target language and allow for them to use their native language to fill in the gaps. The chatbot then responds to the user in their target language followed by a native language translation. The bot also specifically corrects any words or grammar that the user didn't say correctly in the target language. The app uses OpenAI's whisper API to detect voice input in any language and then prompts OpenAI's ChatGPT 4 API with a formatted version of the user's input. The ChatGPT 4 API response is then played back to the user with Google's latest Neural2 voices in the user's target and native language. The user can continually prompt the bot as if it is a natural conversation. 

The app currently only supports native english speakers with spanish as their target language but can be easily updated to work with any combination of languages. Performance will be closely tied to the ChatGPT training dataset so your mileage may vary.

The app requires Google Cloud API access through a Google Cloud ADC (Application Default Credential) JSON file set as an environmental variable with 
```bash set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json" ```
see https://cloud.google.com/docs/authentication/provide-credentials-adc for more details.
The app also requires a OpenAI API key to be specified in the openai.api_key variable. The app was designed and tested around the capabilities of ChatGPT 4 but it will function with ChatGPT 3.5-turbo. The app's ChatGPT API calls use the most recent ChatCompletion API call to specify the system's goal, provide an example response, and chat history(coming soon).
If you would like to test out this app and do not have ChatGPT4 API access please contact gabe at gabebohlmann@gmail.com 

