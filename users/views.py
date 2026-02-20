from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from users.forms import UserRegistrationForm
from .models import UserRegistrationModel

import os
import re
import zlib
import mimetypes

import google.generativeai as genai
from django.conf import settings as django_settings

# ================= BASIC VIEWS ================= #

def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistration.html', {'form': form})
        else:
            messages.error(request, 'Email or Mobile Already Exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistration.html', {'form': form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('password')

        try:
            user = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            if user.status == "activated":
                request.session['id'] = user.id
                request.session['loggeduser'] = user.name
                return redirect('UserHome')
            else:
                messages.error(request, 'Your account is not activated.')
        except UserRegistrationModel.DoesNotExist:
            messages.error(request, 'Invalid Login ID or Password')

    return render(request, 'UserLogin.html')

def UserHome(request):
    if not request.session.get('loggeduser'):
        messages.error(request, 'Please login first.')
        return redirect('UserLogin')
    return render(request, 'users/UserHome.html')

def UserLogout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


# ================= GEMINI CONFIG ================= #

def _configure_genai():
    """Configure genai with the API key from Django settings (always fresh)."""
    api_key = django_settings.GOOGLE_API_KEY
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set in .env file")
    genai.configure(api_key=api_key)


# ================= PLANTUML ENCODING ================= #

def plantuml_encode(text):
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    compressed = compressor.compress(text.encode('utf-8')) + compressor.flush()
    return encode_plantuml_base64(compressed)

def encode_plantuml_base64(data):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    result = ""
    i = 0
    while i < len(data):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        i += 3

        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F

        result += alphabet[c1] + alphabet[c2] + alphabet[c3] + alphabet[c4]
    return result


# ================= SAFE FILE READER ================= #

def read_uploaded_file_safely(file_path):
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()

        if b'\x00' in raw:
            return None, "Binary file detected. Upload source code only."

        try:
            return raw.decode('utf-8'), None
        except UnicodeDecodeError:
            pass

        try:
            return raw.decode('latin-1'), None
        except UnicodeDecodeError:
            pass

        return raw.decode('utf-8', errors='ignore'), None

    except Exception as e:
        return None, f"File read error: {str(e)}"


# ================= GEMINI → PLANTUML (TEXT) ================= #

def generate_diagram_from_text(prompt):
    try:
        _configure_genai()
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        system_prompt = (
            "You are a PlantUML expert.\n"
            "Convert the following input into a UML diagram.\n"
            "Return ONLY valid PlantUML code.\n"
            "Start with @startuml and end with @enduml.\n"
            "Do not explain anything.\n\n"
            f"{prompt}"
        )
        response = model.generate_content(system_prompt)
        text = response.text.strip()
        match = re.search(r"@startuml[\s\S]*?@enduml", text)
        if not match:
            return None, "Invalid PlantUML returned by AI. Please try a different prompt."
        return match.group(), None
    except Exception as e:
        return None, f"Gemini Error: {str(e)}"


# ================= GEMINI → PLANTUML (IMAGE) ================= #

def generate_diagram_from_image(image_path):
    try:
        _configure_genai()
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        image_file = genai.upload_file(image_path)

        prompt = (
            "Analyze the diagram/image and generate equivalent PlantUML code.\n"
            "Return ONLY PlantUML code.\n"
            "Start with @startuml and end with @enduml.\n"
            "No explanation."
        )
        response = model.generate_content([prompt, image_file])
        text = response.text.strip()
        match = re.search(r"@startuml[\s\S]*?@enduml", text)
        if not match:
            return None, "Unable to convert image to PlantUML. Try a clearer diagram."
        return match.group(), None
    except Exception as e:
        return None, f"Gemini Image Error: {str(e)}"


# ================= MAIN FEATURE VIEW ================= #

def code_to_diagram_view(request):
    if not request.session.get('loggeduser'):
        messages.error(request, 'Please login first.')
        return redirect('UserLogin')

    ai_response = ""
    diagram_url = ""
    generated_code = ""
    image_detected = False
    image_url = ""

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        uploaded_file = request.FILES.get('code_file')
        prompt = query

        if not query and not uploaded_file:
            ai_response = "Please enter a description or upload a file."
        else:
            fs = FileSystemStorage()

            if uploaded_file:
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.path(filename)
                mime_type, _ = mimetypes.guess_type(filename)

                # IMAGE FILE
                if mime_type and mime_type.startswith('image'):
                    image_detected = True
                    image_url = fs.url(filename)
                    generated_code, ai_response = generate_diagram_from_image(file_path)

                # CODE / TEXT FILE
                else:
                    file_text, error = read_uploaded_file_safely(file_path)
                    if error:
                        ai_response = error
                    else:
                        if prompt:
                            prompt += "\n\n" + file_text
                        else:
                            prompt = file_text
                        generated_code, ai_response = generate_diagram_from_text(prompt)

            # TEXT ONLY INPUT
            elif query:
                generated_code, ai_response = generate_diagram_from_text(prompt)

            # GENERATE DIAGRAM URL
            if generated_code:
                encoded = plantuml_encode(generated_code)
                diagram_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
                ai_response = ""  # Clear error since we have a result

    return render(request, 'users/generate.html', {
        'ai_response': ai_response,
        'diagram_url': diagram_url,
        'generated_code': generated_code,
        'image_detected': image_detected,
        'image_url': image_url,
    })
