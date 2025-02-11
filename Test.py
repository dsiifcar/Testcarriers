import streamlit as st
import google.generativeai as genai

# Configure Gemini API with Streamlit Secrets
# This assumes you have the API keys stored in Streamlit secrets
# For example, in your Streamlit app's settings (Secrets section), you'd have:
# api_keys:
#   key1: "YOUR_API_KEY_1"
#   key2: "YOUR_API_KEY_2"
#   key3: "YOUR_API_KEY_3"
#   key4: "YOUR_API_KEY_4"
#   key5: "YOUR_API_KEY_5"


# List of 5 API keys
api_keys = [
    st.secrets["api_keys"]["key1"],
    st.secrets["api_keys"]["key2"],
    st.secrets["api_keys"]["key3"],
    st.secrets["api_keys"]["key4"],
    st.secrets["api_keys"]["key5"],
]

# Track the last used API key index
api_key_index = 0

# Function to set API key and configure the model in order
def configure_api_key():
    global api_key_index
    while api_key_index < len(api_keys):
        try:
            key = api_keys[api_key_index]  # Select the current API key
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash')  # Configure the model with the API key
            return model
        except Exception as e:
            st.error(f"Failed to configure API with key {key}: {e}")
            api_key_index += 1  # Move to the next API key
            continue
    # If all keys fail, show a message and return None
    st.error("Sorry, the service is temporarily unavailable. Please try again later.")
    return None  # If all keys fail

# Initialize the model using the first working API key
model = None

# Schein Career Anchors Test Questions
questions = [
    "Mon rêve est d'être tellement bon(ne) dans ce que je fais que mes conseils d'expert seront recherchés en permanence.",
    "Je suis pleinement satisfait(e) dans mon travail quand j'ai réussi à intégrer et à gérer les efforts des autres.",
    "Je rêve d'avoir une carrière qui me donne la liberté de faire mon travail à ma façon et selon mon propre programme.",
    "J'attache plus d'importance à la sécurité et à la stabilité qu'à la liberté et l'autonomie.",
    "Je suis toujours à l'affût d'idées qui me permettraient de démarrer ma propre entreprise.",
    "J'estimerai avoir réussi ma carrière seulement si j'ai le sentiment de contribuer réellement au bien-être de la société.",
    "Je rêve d'une carrière dans laquelle je puisse résoudre ou venir à bout de situations particulièrement difficiles.",
    "Je préférerais quitter mon entreprise plutôt que d'être placé(e) sur un poste qui compromet ma capacité à poursuivre mes intérêts personnels et familiaux.",
    "Je rêve d'avoir une carrière internationale qui me permette de voyager et de travailler avec des personnes de diverses cultures.",
    "J'estimerai avoir réussi ma carrière seulement si je peux développer mes capacités techniques ou fonctionnelles à un très haut niveau de compétence.",
    "Je rêve d'être responsable d'une organisation complexe et de prendre des décisions qui touchent nombre de personnes.",
    "Je suis pleinement satisfait(e) dans mon travail quand je suis complètement libre de définir mes propres tâches, programmes et procédures.",
    "Je préférerais quitter définitivement mon entreprise plutôt que d'accepter une mission qui compromettrait ma sécurité dans cette entreprise.",
    "Monter ma propre affaire est plus important pour moi que d'atteindre un haut niveau de management dans l'organisation d'autrui.",
    "Je suis pleinement satisfait(e) dans ma carrière lorsque je peux mettre mes talents au service des autres.",
    "J'ai le sentiment de réussir dans ma carrière seulement si je peux faire face et surmonter des défis particulièrement retors.",
    "Je rêve d'une carrière qui me permette d'intégrer mes besoins personnels, familiaux et professionnels.",
    "Travailler à l'étranger m'attire.",
    "Devenir directeur de la fonction correspondant à mon domaine d'expertise m'attire plus que d'atteindre un poste de direction générale.",
    "J'estimerai avoir réussi dans ma carrière seulement si je deviens directeur général d'une organisation.",
    "J'estimerai avoir réussi dans ma carrière seulement si j'atteins une autonomie et une liberté totale.",
    "Je recherche des emplois dans des organisations qui me procureront un sentiment de sécurité et de stabilité.",
    "Je suis pleinement satisfait(e) dans mon travail quand j'ai pu construire quelque chose qui est entièrement le fruit de mes idées et efforts.",
    "Utiliser mes compétences pour que le monde devienne un endroit plus agréable pour vivre et travailler est plus important pour moi que d'atteindre une position managériale élevée.",
    "J'ai été pleinement satisfait(e) dans ma carrière quand j'ai résolu des problèmes apparemment insolubles ou quand je suis venu(e) à bout de situations apparemment impossibles.",
    "J'estimerai avoir réussi dans la vie seulement si j'ai pu trouver un équilibre entre mes besoins personnels, ceux liés à ma famille et ma carrière.",
    "J'estimerai avoir réussi dans ma carrière seulement si je parviens à travailler dans un environnement international.",
    "Je préférerais quitter mon entreprise plutôt que d'accepter une mission qui me ferait sortir de mon champ d'expertise.",
    "Atteindre un poste de direction générale m'attire plus que de devenir directeur de la fonction correspondant à mon domaine d'expertise.",
    "L'opportunité de faire mon travail à ma façon, libre de règles et de contraintes, est plus importante pour moi que la sécurité.",
    "Je suis pleinement satisfait(e) dans mon travail quand j'éprouve le sentiment d'une sécurité totale sur le plan financier et sur celui de l'emploi.",
    "J'estimerai avoir réussi ma carrière seulement si j'arrive à créer ou à élaborer quelque chose qui est ma propre idée ou mon propre produit.",
    "Je rêve d'avoir une carrière qui apporte une réelle contribution à l'humanité et à la société.",
    "Je recherche des opportunités de travail qui défient fortement mes capacités à résoudre des problèmes et/ou mon goût de la compétition.",
    "Équilibrer les exigences de la vie personnelle et professionnelle est plus important pour moi que d'atteindre une position managériale élevée.",
    "Je préférerais quitter mon entreprise plutôt que d'accepter une mission qui m'impliquerait pas la possibilité d'une mobilité internationale.",
    "Je suis pleinement satisfait(e) de mon travail quand j'ai été capable d'utiliser les compétences et talents rattachés à ma spécialisation.",
    "Je préférerais quitter mon entreprise plutôt que d'accepter un travail qui m'empêcherait d'atteindre une position de management général.",
    "Je préférerais quitter mon entreprise plutôt que d'accepter un travail qui réduirait mon autonomie et ma liberté.",
    "Je rêve d'avoir une carrière qui me permette d'éprouver un sentiment de sécurité et de stabilité.",
    "Je rêve de démarrer et de développer ma propre affaire.",
    "Je préférerais quitter définitivement mon entreprise plutôt que d'accepter une mission qui amoindrirait mes capacités d'être au service des autres.",
    "Travailler sur des problèmes quasiment insolubles est plus important pour moi que d'atteindre une position managériale élevée.",
    "J'ai toujours cherché des opportunités de travail qui minimisent les interférences avec les préoccupations personnelles ou familiales.",
    "Je rêve d'avoir une carrière qui me permette d'avoir des responsabilités internationales."
]

# New page content
def new_page():

    st.image(r"Logo.png")
    st.markdown("""
       ### 📊  Découvrez vos Ancres de Carrière avec IFCAR Solutions
       Chez **IFCAR Solutions**, nous comprenons l'importance de connaître vos motivations profondes et vos valeurs professionnelles. C'est pourquoi nous vous proposons un **test d'ancres de carrière gratuit**, conçu pour être **intuitif**, **rapide**, et **perspicace**.

       ### 🚀 Pourquoi faire notre test ?

       - **Comprenez vos priorités** : Identifiez les éléments essentiels à votre épanouissement professionnel.
       - **Alignez vos choix de carrière** : Prenez des décisions plus éclairées en fonction de vos ancres.
       - **Développez votre potentiel** : Optimisez votre parcours en accord avec vos valeurs fondamentales.

       ### 🎯 Pourquoi choisir IFCAR Solutions ?

       Forts de **12 ans d'expérience dans le recrutement**, nous aidons les individus à trouver des carrières qui leur correspondent vraiment. Notre test d'ancres de carrière témoigne de notre engagement à fournir des outils pertinents et efficaces pour une orientation professionnelle réussie.

       📌 **Passez notre test d'ancres de carrière dès aujourd'hui** et prenez le contrôle de votre avenir professionnel !
       """)

    # Add buttons linking to external resources
    st.markdown("---")  # Add a separator
    st.markdown("##### Ressources Utiles:")

    col1, col2, col3, col4 = st.columns(4)  # Create three columns

    with col1:
        st.link_button("Nos offres d'emploi", "https://ifcarjob.com/offres-demploi")

    with col2:
        st.link_button("Analyser vos CV", "https://cvanalyserapp.streamlit.app/")

    with col3:
        st.link_button("Déposez vos CV", "mailto:cv@ifcarjob.com")

    with col4:
        st.link_button("Notre page Linkedin", "https://www.linkedin.com/company/ifcarsolutions/")


# Main application
def main():
    st.sidebar.title("Pages")
    page = st.sidebar.radio("Aller à", ["Test d'orientation des carrières", "À propos de nous"])

    if page == "Test d'orientation des carrières":
        career_anchors_page()
    elif page == "À propos de nous":
        new_page()

def career_anchors_page():
    global model  # Declare that you're using the global model variable
    st.image(r"Logo.png")

    st.title("Test d'orientation des carrières : Par IFCAR Solutions")

    # Initialize session state
    if 'responses' not in st.session_state:
        st.session_state['responses'] = {}

    # Collect user information
    name = st.text_input("Nom et Prénom *")

    if not name:
        st.warning("Veuillez remplir le champ du nom.")
        return

    # Collect responses
    for i, question in enumerate(questions):
        key = f"Q{i+1}"
        st.markdown(f"### {i+1}. {question}")  # Make questions bigger

        # Implement the radio buttons for 1 to 5 scale
        st.session_state['responses'][key] = st.radio(
            "Sélectionnez votre réponse:",
            options=['Pas du tout vrai', 'Pas vraiment', 'Neutre', 'En partie vrai', 'Tout à fait vrai'],
            index=None,  # Default to the middle (3)
            horizontal=True,  # Ensures all options appear on the same line
            key=key
        )

    if st.button("Soumettre les réponses"):
        # Prepare the prompt for Gemini
        prompt = f"Analysez les réponses suivantes au test des ancres de carrière de Schein pour Moi, ca mon nom : {name} :\n\n"
        for q, response in st.session_state['responses'].items():
            prompt += f"{q}: {response}\n"
        prompt += "\nFournissez une analyse détaillée des ancres de carrière dominantes et des suggestions pour leur développement professionnel. Limitez votre réponse à 500 mots."

        # Send to Gemini API
        try:
            # Configure the model if it's not already configured (or has failed)
            if model is None:
                model = configure_api_key()

            if model is not None:  # only proceed if the model is configured
                response = model.generate_content(prompt)
                st.subheader("Résultats de l'analyse")
                st.write(response.text)
            else:
                st.error("Failed to configure the Gemini API after trying all available keys. Please check your secrets or try again later.")
        except Exception as e:
            st.error(f"Une erreur s'est produite lors de l'analyse: {e}")
            model = None  # Reset the model if there's an error, so it tries to reconfigure next time

        st.markdown("---")  # Add a separator
        st.markdown("##### Ressources Utiles:")

        col1, col2, col3, col4 = st.columns(4)  # Create three columns

        with col1:
            st.link_button("Nos offres d'emploi", "https://ifcarjob.com/offres-demploi")

        with col2:
            st.link_button("Analyser vos CV", "https://cvanalyserapp.streamlit.app/")

        with col3:
            st.link_button("Déposez vos CV", "mailto:cv@ifcarjob.com")

        with col4:
            st.link_button("Notre page Linkedin", "https://www.linkedin.com/company/ifcarsolutions/")





if __name__ == "__main__":
    main()
