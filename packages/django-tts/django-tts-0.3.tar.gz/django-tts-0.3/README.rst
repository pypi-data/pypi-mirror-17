=====
Django Text to Speach generator
=====

Django Text to Speach is a simple Django app to create .wav files from your text

Must be installed RHVoice-test utilite on Unix Machine

Detailed documentation is in the "docs" directory.

Quick start
-----------


1. On your machine which you launch django applicaton must be installed RHVoice-test utilite, which create wav files from text.
   Instalation instructions and documentation see there: https://github.com/Olga-Yakovleva/RHVoice.
   Also see there Docker all installed in. https://github.com/g10k/sw_tts

2. Add some apps  to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'rest_framework',
        'tts',
    ]

3. Include the polls URLconf in your project urls.py like this::

    url(r'^tts/', include('tts.urls')),

4. Run `python manage.py migrate` to create the polls models.

5. Start the development server and visit http://127.0.0.1:8000/tts/
   to see docs and available api