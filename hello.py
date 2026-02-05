# streamlit_vokabeltrainer.py
import streamlit as st
import random

# -----------------------------
# 1. Begrüßung und Einführung
# -----------------------------
st.set_page_config(page_title="Vokabeltrainer Deutsch → Englisch", page_icon="📝")
st.title("📝 Interaktiver Vokabeltrainer (Deutsch → Englisch)")
st.markdown("""
Willkommen zum Vokabeltrainer!  
Wir üben Deutsch → Englisch.  
Du kannst zwischen **Multiple-Choice** oder **Karteikarten** wählen.  
Jede Runde besteht aus 10 Vokabeln.  
Falsch beantwortete Vokabeln werden wiederholt, damit du sie besser lernst.  
Los geht's! 🚀
""")

# -----------------------------
# 2. Beispiel-Vokabeln
# -----------------------------
# Du kannst diese Liste leicht erweitern
VOCABULARY = [
    {"de": "Haus", "en": "house", "example": "I live in a big house."},
    {"de": "Baum", "en": "tree", "example": "The tree is very tall."},
    {"de": "Katze", "en": "cat", "example": "The cat is sleeping."},
    {"de": "Hund", "en": "dog", "example": "The dog is barking."},
    {"de": "Buch", "en": "book", "example": "I read a book every night."},
    {"de": "Stuhl", "en": "chair", "example": "The chair is comfortable."},
    {"de": "Tisch", "en": "table", "example": "The table is round."},
    {"de": "Fenster", "en": "window", "example": "Please open the window."},
    {"de": "Tür", "en": "door", "example": "Close the door, please."},
    {"de": "Auto", "en": "car", "example": "My car is red."},
    {"de": "Straße", "en": "street", "example": "The street is busy."},
    {"de": "Wasser", "en": "water", "example": "I drink water every day."},
]

# -----------------------------
# 3. Session State Initialisierung
# -----------------------------
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'vocab_list' not in st.session_state:
    st.session_state.vocab_list = random.sample(VOCABULARY, len(VOCABULARY))
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = []
if 'round_finished' not in st.session_state:
    st.session_state.round_finished = False

# -----------------------------
# 4. Auswahl des Trainingsmodus
# -----------------------------
if st.session_state.mode is None:
    mode = st.radio("Wähle deinen Trainingsmodus:", ["Multiple-Choice", "Karteikarten"])
    if st.button("Start"):
        st.session_state.mode = mode
        st.experimental_rerun()

# -----------------------------
# 5. Funktionen für das Training
# -----------------------------
def get_choices(correct, n=4):
    """Erstellt Multiple-Choice-Optionen inkl. der richtigen Antwort"""
    all_answers = [v['en'] for v in VOCABULARY if v['en'] != correct]
    choices = random.sample(all_answers, k=n-1)
    choices.append(correct)
    random.shuffle(choices)
    return choices

def show_feedback(is_correct, vocab):
    """Zeigt Feedback nach jeder Antwort"""
    if is_correct:
        st.success("✅ Richtig!")
    else:
        st.error(f"❌ Falsch! Richtig: **{vocab['en']}**")
        st.info(f"Beispiel: {vocab['example']}")

def next_question():
    """Springt zur nächsten Vokabel"""
    st.session_state.current_index += 1
    if st.session_state.current_index >= len(st.session_state.vocab_list):
        st.session_state.round_finished = True

# -----------------------------
# 6. Training starten
# -----------------------------
if st.session_state.mode and not st.session_state.round_finished:
    vocab = st.session_state.vocab_list[st.session_state.current_index]
    st.markdown(f"**Vokabel {st.session_state.current_index + 1} / 10:** {vocab['de']}")

    if st.session_state.mode == "Multiple-Choice":
        choices = get_choices(vocab['en'])
        answer = st.radio("Wähle die richtige Übersetzung:", choices)
        if st.button("Antwort prüfen"):
            if answer == vocab['en']:
                show_feedback(True, vocab)
            else:
                show_feedback(False, vocab)
                st.session_state.wrong_answers.append(vocab)
            next_question()
            st.experimental_rerun()

    elif st.session_state.mode == "Karteikarten":
        answer = st.text_input("Tippe die englische Übersetzung:")
        if st.button("Antwort prüfen"):
            if answer.strip().lower() == vocab['en'].lower():
                show_feedback(True, vocab)
            else:
                show_feedback(False, vocab)
                st.session_state.wrong_answers.append(vocab)
            next_question()
            st.experimental_rerun()

# -----------------------------
# 7. Runde beendet
# -----------------------------
if st.session_state.round_finished:
    st.balloons()
    st.success("🎉 Runde beendet!")
    st.markdown(f"Du hattest **{len(st.session_state.wrong_answers)}** falsche Antworten.")

    if st.session_state.wrong_answers:
        st.markdown("Wir wiederholen die falschen Vokabeln in der nächsten Runde.")
        st.session_state.vocab_list = st.session_state.wrong_answers.copy()
    else:
        st.session_state.vocab_list = random.sample(VOCABULARY, 10)

    if st.button("Weiter zur nächsten Runde"):
        st.session_state.current_index = 0
        st.session_state.wrong_answers = []
        st.session_state.round_finished = False
        st.experimental_rerun()

# -----------------------------
# 8. Motivation am Ende
# -----------------------------
st.markdown("💡 Tipp: Übe regelmäßig, und die Vokabeln bleiben im Gedächtnis!")
