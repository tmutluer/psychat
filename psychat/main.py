import whisper
import openai
import pyttsx3
import os


def transcribe(audio, whisper_model='medium', write_dir='./'):
    # Transcribe the input audio
    model = whisper.load_model(whisper_model)
    result = model.transcribe(audio)

    with open(os.path.join(write_dir, 'input_transcript.txt'), 'w') as f:
        f.write(result['text'])

    return result


def chatgpt_response(text, system_instruction, write_dir='./'):
    # Talk with ChatGPT
    openai.api_key = os.environ['OPENAI_API_KEY']
    completion = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                              messages=[
                                                  {'role': 'system',
                                                   'content': system_instruction
                                                   },
                                                  {'role': 'user',
                                                   'content': text
                                                   }
                                              ])
    gpt_response = completion.choices[0].message.content
    with open(os.path.join(write_dir, 'output_transcript.txt'), 'w') as f:
        f.write(gpt_response)

    return completion, gpt_response


def say(gpt_response, reply_audio_filename="reply_audio.mp3", rate=180, language='tr'):
    # Text to speech
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    trvoice = None
    for i in voices:
        lang = i.languages[0]
        if language in lang:
            trvoice = i

    engine.setProperty('voice', trvoice.id)
    engine.setProperty('rate', rate)

    engine.save_to_file(text=gpt_response, filename=reply_audio_filename)
    engine.runAndWait()
    engine.say(gpt_response)
    engine.runAndWait()


def talk_with_chatgpt(audio, system_instruction, reply_audio_filename="reply_audio.mp3",
                      whisper_model='medium', rate=180, language='tr',  write_dir='./'):

    result = transcribe(audio, whisper_model=whisper_model, write_dir=write_dir)
    _, gpt_response = chatgpt_response(result['text'],
                                       system_instruction=system_instruction,
                                       write_dir=write_dir)

    say(gpt_response, reply_audio_filename=reply_audio_filename,
        rate=rate, language=language)
