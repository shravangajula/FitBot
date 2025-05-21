import os
import streamlit as st
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceHub

# Setup credentials dictionary
creds = {
    'apikey': 'NOT MENTIONED HERE',
    'url': 'https://api-inference.huggingface.co/models/gpt2.5'
}

# Set the Hugging Face API token in the environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = creds['apikey']

# This function loads a PDF and creates a vector database
@st.cache_resource
def load_pdf():
    # Update PDF name here to whatever you like Chopra
    pdf_name = 'FitBot.pdf'
    loaders = [PyPDFLoader(pdf_name)]

    # Create index - aka vector database - aka chromadb
    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    ).from_loaders(loaders)

    # Return the vector database
    return index

# Extract legs workout specifically - uses multiple patterns to ensure we get all exercises
def extract_legs_workout(context):
    # Define various patterns to match leg exercises in different formats
    leg_patterns = [
        r"Legs\s+(\d+\.\s+[^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)",
        r"Legs\s*\d+\.\s+([^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)",
        r"Legs[^0-9]*?(\d+)\.\s+([^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)",
        r"Legs[^\n]*\n\s*(\d+)\.\s+([^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)"
    ]
    
    # Try direct extraction of leg section
    leg_section_pattern = r"Legs[^\n]*((?:\n.*?){1,10})"
    leg_section_match = re.search(leg_section_pattern, context, re.DOTALL)
    
    # Also look for the specific leg exercises mentioned in your PDF
    specific_leg_exercises = [
        r"Barbell Back Squats[^–]*–[^r]*reps",
        r"Romanian Deadlifts[^–]*–[^r]*reps",
        r"Leg Press[^–]*–[^r]*reps",
        r"Bulgarian Split Squats[^–]*–[^r]*reps",
        r"Seated Calf Raises[^–]*–[^r]*reps"
    ]
    
    leg_exercises = []
    
    # First try to extract from section if found
    if leg_section_match:
        section = leg_section_match.group(1)
        # Try to extract exercises from this section
        exercise_pattern = r"(\d+)\.\s+([^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)"
        exercises = re.findall(exercise_pattern, section)
        for num, ex, rep in exercises:
            leg_exercises.append((num, ex.strip(), rep.strip()))
    
    # If we didn't find enough exercises, try the specific patterns
    if len(leg_exercises) < 4:
        for pattern in leg_patterns:
            matches = re.findall(pattern, context)
            for match in matches:
                if len(match) == 2:  # If pattern has 2 groups
                    exercise, reps = match
                    # Check if this is a new exercise
                    if not any(exercise.strip() in ex for _, ex, _ in leg_exercises):
                        leg_exercises.append(("", exercise.strip(), reps.strip()))
                elif len(match) == 3:  # If pattern has 3 groups
                    num, exercise, reps = match
                    # Check if this is a new exercise
                    if not any(exercise.strip() in ex for _, ex, _ in leg_exercises):
                        leg_exercises.append((num, exercise.strip(), reps.strip()))
    
    # If we still don't have enough, search for specific exercises
    if len(leg_exercises) < 4:
        for idx, pattern in enumerate(specific_leg_exercises):
            match = re.search(pattern, context)
            if match:
                exercise_text = match.group(0)
                # Try to extract the exercise name and reps
                ex_match = re.match(r"([^–]+)–\s+([^r]+reps[^0-9]*)", exercise_text)
                if ex_match:
                    exercise, reps = ex_match.groups()
                    # Check if this is a new exercise
                    if not any(exercise.strip() in ex for _, ex, _ in leg_exercises):
                        leg_exercises.append((str(idx+1), exercise.strip(), reps.strip()))
    
    # Format the output
    if leg_exercises:
        formatted_workout = "**Legs Workout:**\n\n"
        # Sort exercises by their number if available
        leg_exercises.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 99)
        
        # Renumber exercises sequentially
        for i, (_, exercise, reps) in enumerate(leg_exercises, 1):
            formatted_workout += f"{i}. **{exercise}** – {reps}\n"
        
        return formatted_workout
    else:
        return "I couldn't find specific leg workouts in my knowledge base."

# Function to extract workout information for a specific body part
def extract_workout(context, body_part):
    # Special case for legs
    if body_part.lower() == "legs":
        return extract_legs_workout(context)
    
    # Create a pattern to find the specified body part
    pattern = fr"{body_part}:(.*?)(?:Chest:|Triceps:|Back:|Legs|Shoulders:|Biceps:|Abs:|$)"
    match = re.search(pattern, context, re.DOTALL | re.IGNORECASE)
    
    if match:
        workout_section = match.group(1).strip()
        # Extract individual exercises using regex
        exercises = re.findall(r"(\d+)\.\s+([^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)", workout_section)
        
        if exercises:
            formatted_workout = f"**{body_part} Workout:**\n\n"
            for number, exercise, reps in exercises:
                formatted_workout += f"{number}. **{exercise.strip()}** – {reps.strip()}\n"
            return formatted_workout
    
    # Alternative pattern for when the exercise numbering continues from previous section
    if body_part.lower() in ["triceps", "biceps", "abs"]:
        pattern = fr"{body_part}:(.*?)(?:Chest:|Triceps:|Back:|Legs|Shoulders:|Biceps:|Abs:|$)"
        match = re.search(pattern, context, re.DOTALL | re.IGNORECASE)
        
        if match:
            workout_section = match.group(1).strip()
            # Extract individual exercises using regex with different pattern
            exercises = re.findall(r"(\d+)\.\s+([^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)", workout_section)
            
            if exercises:
                formatted_workout = f"**{body_part} Workout:**\n\n"
                for number, exercise, reps in exercises:
                    formatted_workout += f"{number}. **{exercise.strip()}** – {reps.strip()}\n"
                return formatted_workout
    
    # If specific regex extraction fails, fall back to a simpler approach
    body_part_lower = body_part.lower()
    if body_part_lower in context.lower():
        lines = context.split('\n')
        relevant_section = False
        section_lines = []
        
        for line in lines:
            # Start collecting when we find the body part heading
            if f"{body_part}:" in line or f"{body_part.lower()}:" in line:
                relevant_section = True
                section_lines.append(line)
                continue
                
            # Stop collecting when we hit the next body part
            if relevant_section and any(part in line for part in ["Chest:", "Triceps:", "Back:", "Legs:", "Shoulders:", "Biceps:", "Abs:"]) and not line.startswith(f"{body_part}:"):
                break
                
            # Collect lines in the relevant section
            if relevant_section:
                section_lines.append(line)
        
        if section_lines:
            # Clean up and format the collected section
            content = " ".join(section_lines)
            # Extract exercise items with numbers
            formatted_items = re.findall(r"(\d+)\.\s+([^–]+)–\s+(\d+\s+sets\s+×\s+[^r]+reps[^0-9]*)", content)
            
            if formatted_items:
                formatted_workout = f"**{body_part} Workout:**\n\n"
                for number, exercise, reps in formatted_items:
                    formatted_workout += f"{number}. **{exercise.strip()}** – {reps.strip()}\n"
                return formatted_workout
            else:
                # If we can't extract properly formatted items, return the raw section
                return f"**{body_part} Workout:**\n\n" + content.replace(f"{body_part}:", "").strip()
    
    return f"I couldn't find specific {body_part.lower()} workouts in my knowledge base."

def is_goodbye(text):
    # Check for goodbye phrases
    farewells = ["bye", "goodbye", "see you", "take care", "later", "farewell", "thank you", "thanks"]
    text_lower = text.lower()
    return any(farewell in text_lower for farewell in farewells) or text_lower.strip() in farewells

# Function to check if a message is a greeting
def is_greeting(text):
    greetings = ["hi", "hello", "hey", "howdy", "greetings", "good morning", "good afternoon", "good evening"]
    text_lower = text.lower()
    return any(greeting in text_lower for greeting in greetings) or text_lower.strip() in greetings

# Body part mapping for different variations of queries
body_part_mapping = {
    "chest": "Chest",
    "triceps": "Triceps", 
    "tricep": "Triceps",
    "back": "Back",
    "legs": "Legs", 
    "leg": "Legs",
    "shoulders": "Shoulders", 
    "shoulder": "Shoulders",
    "biceps": "Biceps", 
    "bicep": "Biceps",
    "abs": "Abs", 
    "ab": "Abs",
    "abdominal": "Abs",
    "core": "Abs"
}

# Function to categorize the query type
def categorize_query(text):
    text_lower = text.lower()
    
    # Check for goodbye messages
    if is_goodbye(text_lower):
        return "goodbye", None
    
    # Check for workout queries first
    for keyword in body_part_mapping.keys():
        if keyword in text_lower and any(term in text_lower for term in ["workout", "exercise", "routine", "training"]):
            return "workout", body_part_mapping[keyword]
    
    # Special case to handle queries like "give me leg workout" without "leg workout" specifically
    leg_keywords = ["legs", "leg"]
    if any(keyword in text_lower for keyword in leg_keywords) and not any(term in text_lower for term in ["workout", "exercise", "routine", "training"]):
        for keyword in leg_keywords:
            if keyword in text_lower:
                return "workout", "Legs"
    
    # Check for greetings
    if is_greeting(text_lower):
        return "greeting", None
    
    # Check for nutrition questions
    if any(term in text_lower for term in ["food", "nutrition", "diet", "eat", "eating", "meal", "protein", "carb", "fat"]):
        return "nutrition", None
    
    # Check for cardio questions
    if any(term in text_lower for term in ["cardio", "running", "jogging", "cycling", "aerobic", "endurance"]):
        return "cardio", None
    
    # Default to general
    return "general", None

# Standard responses for common queries
STANDARD_RESPONSES = {
    "greeting": "Hi there! I'm FitBot, your personal fitness assistant. How can I help you today? You can ask me about workouts for different body parts like chest, back, legs, shoulders, biceps, triceps, or abs.",
    
    "nutrition": "While I focus primarily on workout routines, balanced nutrition is essential for fitness goals. Generally, focus on:\n\n- Protein (lean meats, fish, eggs, dairy, legumes)\n- Complex carbs (whole grains, fruits, vegetables)\n- Healthy fats (avocados, nuts, olive oil)\n- Hydration (water throughout the day)\n\nAsk me about workout routines for specific body parts for more detailed information!",
    
    "cardio": "Cardiovascular training is essential for heart health and endurance. Consider including:\n\n- Running or jogging\n- Cycling\n- Swimming\n- HIIT (High-Intensity Interval Training)\n- Rowing\n- Jump rope\n\nAim for 150+ minutes of moderate cardio or 75+ minutes of vigorous cardio per week for general health.",

    "goodbye": "Thank you for chatting with FitBot! Have a great workout and come back anytime for more fitness advice. Until then, stay strong and healthy!",
    
    "general": "I'm FitBot, your workout assistant! I can help you with exercise routines for different body parts. Try asking me for workout routines for chest, back, legs, shoulders, biceps, triceps, or abs."
}

# Bring in Streamlit for UI development
st.title('Welcome to FitBot - A Single Step Toward Leading an Active Life!!')

# Setup a session state message variable to hold all the old messages
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # We'll initialize the welcome message in the chat history but NOT display it immediately
    # (it will appear in the chat history when displayed in the loop below)
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hi! I'm FitBot. Ask me about workout routines and fitness advice!"
    })

# Attempt to load the vector database with error handling
try:
    # Load the vector database
    index = load_pdf()
except Exception as e:
    st.error(f"Failed to load PDF or initialize the RAG system: {str(e)}")
    st.stop()

# Display all the historical messages
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# Build a prompt input template to display the prompts
prompt = st.chat_input('Ask about fitness routines or exercises...')

# If the user hits enter then
if prompt:
    # Display the prompt
    st.chat_message('user').markdown(prompt)
    
    # Store the user prompt in session state
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Categorize the query
    query_type, body_part = categorize_query(prompt)
    
    # Handle "what about legs" type queries
    if "what about" in prompt.lower() and any(part in prompt.lower() for part in body_part_mapping.keys()):
        for part in body_part_mapping.keys():
            if part in prompt.lower():
                query_type = "workout"
                body_part = body_part_mapping[part]
                break
    
    try:
        # Handle different types of queries
        if query_type == "workout" and body_part:
            with st.spinner(f"Finding {body_part.lower()} workout information..."):
                docs = index.vectorstore.similarity_search(f"{body_part} workout", k=5)  # Increased to 5 docs
                context = " ".join([doc.page_content for doc in docs])
                response = extract_workout(context, body_part)
                
        elif query_type in STANDARD_RESPONSES:
            # Use predefined responses for common query types
            response = STANDARD_RESPONSES[query_type]
            
        else:
            # For unknown queries, provide a helpful default response
            response = "I'm your fitness assistant and can help with workout routines for different body parts. Try asking me for chest, back, legs, shoulders, biceps, triceps, or abs workouts!"
            
    except Exception as e:
        # Display error message
        st.error(f"The service is currently unavailable. Please try again later. Details: {str(e)}")
        response = "Sorry, I couldn't process your request at the moment."
    
    # Display the LLM response
    st.chat_message('assistant').markdown(response)
    
    # Store the LLM response in session state
    st.session_state.messages.append({'role': 'assistant', 'content': response})
