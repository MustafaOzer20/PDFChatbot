
# PDF Chatbot

## [TR]
Bir pdf dosyasını vektörlere dönüştürerek kullanıcının sorduğu soruya benzeyen metinlerle eşleştirir. Soruları ve bu eşleşen metinleri birleştirerek sorunun cevabını ilgili doküman üzerinden almayı amaçlar.

### Kullanılan teknolojiler
- Python
- FastAPI
- OpenAI
- LangChain

### Önemli
1. Eğer projeyi çalıştırmak istiyorsanız;
- 'app/settings.py' içerisindeki OPENAI_API_KEY değişkenini, kendi sahip olduğunuz OPENAI key ile değiştirmeniz gerekmektedir.
2. Eğer bilgisayarınızda docker kurulu ise;
- 'docker-compose up --build' komutu ile çalıştırabilirsiniz.
3. Docker kurulu değil ise main.py dosyasını çalıştırabilirsiniz.

<b>1.maddeyi uygulamadan proje çalışmayacaktır.</b>

## [EN]
Converts a pdf file to vectors and matches it with text that resembles the user's question. It aims to get the answer of the question through the relevant document by combining the questions and these matching texts.

### Used technologies
- Python
- FastAPI
- OpenAI
- LangChain

### Important
1. If you want to run the project;
- You need to replace the OPENAI_API_KEY variable in 'app/settings.py' with your own OPENAI key.
2. If docker is installed on your computer;
- You can run it with the command 'docker-compose up --build'.
3. If Docker is not installed, you can run the main.py file.

<b>The project will not work without applying the 1st item.</b>