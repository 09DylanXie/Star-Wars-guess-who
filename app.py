import streamlit as st
from PIL import Image, ImageOps
import os

# Configure the Streamlit page layout
st.set_page_config(page_title="Star Wars Guess Who", layout="wide")

st.title("Star Wars: Guess Who?")

# Character roster 
characters = [
    "Luke Skywalker", "Obi-Wan Kenobi", "Anakin Skywalker", "Yoda",
    "Leia Organa", "Ahsoka Tano", "Padmé Amidala", "Grogu",
    "Darth Vader", "Emperor Palpatine", "Count Dooku", "Asajj Ventress",
    "Jabba the Hutt", "R2-D2", "C-3PO", "Captain Rex",
    "Commander Cody", "Jawa", "Mace Windu", "Boba Fett", 
    "Han Solo", "Darth Maul", "Thrawn", "Pellaeon", 
    "Admiral Ackbar", "George Lucas", "The Mandalorian", "Chewbacca"
]

# Deep Lore (Used for the dedicated deep-dive tab)
deep_lore = {
    "Luke Skywalker": "Raised as a moisture farmer on the desert planet of Tatooine, Luke Skywalker rose from humble beginnings to become one of the greatest Jedi the galaxy has ever known. He destroyed the first Death Star, trained under Jedi Masters Obi-Wan Kenobi and Yoda, and ultimately achieved the impossible: redeeming his father, Darth Vader, and bringing balance to the Force.",
    "Obi-Wan Kenobi": "A legendary Jedi Master, Obi-Wan was a noble man and gifted in the ways of the Force. He trained Anakin Skywalker, served as a General in the Republic Army during the Clone Wars, and guided Luke Skywalker as a mentor. Following the execution of Order 66, he lived in exile on Tatooine to watch over young Luke.",
    "Anakin Skywalker": "Discovered as a slave on Tatooine by Qui-Gon Jinn, Anakin was believed to be the prophesied Chosen One destined to bring balance to the Force. He was a brilliant pilot and a heroic Jedi Knight during the Clone Wars, but his deep-seated fears of loss were manipulated by Supreme Chancellor Palpatine, leading to his tragic fall to the dark side.",
    "Yoda": "Standing at only two feet tall, Yoda was the legendary Grand Master of the Jedi Order. For over 800 years, he trained generations of Jedi Knights. Despite his small stature and unusual speech patterns, he was one of the most powerful and wise Force users in galactic history, commanding immense respect across the Republic.",
    "Leia Organa": "Adopted into the royal family of Alderaan, Leia Organa was one of the Rebel Alliance's greatest leaders, fearless on the battlefield and brilliant in the Senate. She is the twin sister of Luke Skywalker. Her unbreakable spirit led the galaxy to victory over the Galactic Empire and later the First Order.",
    "Ahsoka Tano": "Discovered by Master Plo Koon, Ahsoka Tano became the Padawan learner to Anakin Skywalker during the Clone Wars. After being framed for a crime she didn't commit, she made the difficult choice to walk away from the Jedi Order. She survived the Great Jedi Purge and continued to fight for the light side as a rebel operative known as 'Fulcrum'.",
    "Padmé Amidala": "Elected Queen of Naboo at a remarkably young age, Padmé later served her people as a Senator in the Galactic Republic. She was a courageous and idealistic leader who fought tirelessly for democracy during the Clone Wars. She secretly married Anakin Skywalker and died tragically after giving birth to twins, Luke and Leia.",
    "Grogu": "A mysterious and incredibly highly Force-sensitive child belonging to the same unknown species as Jedi Grand Master Yoda. After surviving the siege of the Jedi Temple during Order 66, he was hidden away for decades until he was rescued by the Mandalorian bounty hunter Din Djarin, who became a father figure to him.",
    "Darth Vader": "Once the heroic Jedi Knight Anakin Skywalker, Darth Vader is a terrifying Sith Lord encased in iconic black cybernetic armor. As the Emperor's chief enforcer, he hunted down the surviving Jedi Knights and crushed rebellion across the galaxy with an iron fist, fueled by his mastery of the dark side of the Force.",
    "Emperor Palpatine": "Publicly known as the benevolent Supreme Chancellor of the Republic, Sheev Palpatine was secretly Darth Sidious, the Dark Lord of the Sith. A master manipulator, he orchestrated the Clone Wars, destroyed the Jedi Order, and transformed the democratic Republic into the oppressive Galactic Empire, ruling as its Emperor.",
    "Count Dooku": "A former respected Jedi Master who grew disillusioned with the corruption of the Republic Senate. He fell to the dark side, becoming the Sith Lord Darth Tyranus. Dooku led the Separatist Alliance during the Clone Wars, acting as the public face of the rebellion while secretly serving under Darth Sidious.",
    "Asajj Ventress": "Hailing from the mystical world of Dathomir, Ventress was a deadly Nightsister and an exceptionally skilled Sith assassin. She wielded dual curved-hilt lightsabers and served as Count Dooku's enforcer during the Clone Wars before he betrayed her, forcing her to forge a new path as a bounty hunter.",
    "Jabba the Hutt": "A massive, slug-like alien and one of the galaxy's most powerful and ruthless crime lords. Operating out of his desert palace on Tatooine, Jabba controlled illegal smuggling rings, slavery operations, and bounty hunters. His massive criminal empire came to a sudden end when he crossed paths with Jedi Knight Luke Skywalker and Princess Leia.",
    "R2-D2": "A courageous, stubborn, and highly resourceful astromech droid. R2-D2 has served the Republic, the Rebellion, and the Resistance. Unlike most droids, his memory was never wiped, allowing him to accumulate decades of experience. He is rarely seen without his anxious protocol droid counterpart, C-3PO.",
    "C-3PO": "Built by a young Anakin Skywalker from spare parts, C-3PO is a gold-plated protocol droid fluent in over six million forms of communication. Programmed for etiquette and protocol, he is notoriously anxious and risk-averse, which constantly puts him at odds with the incredibly dangerous situations he and his counterpart, R2-D2, constantly find themselves in.",
    "Captain Rex": "CT-7567, known as Rex, was a fiercely loyal Clone Captain who served under Anakin Skywalker and Ahsoka Tano in the 501st Legion. He was one of the most decorated soldiers in the Grand Army of the Republic. Crucially, he managed to have his behavioral inhibitor chip removed, allowing him to resist the tragic programming of Order 66.",
    "Commander Cody": "CC-2224, known as Cody, was a disciplined and highly effective Clone Commander who worked closely alongside Jedi Master Obi-Wan Kenobi. They formed a strong bond of mutual respect during the Clone Wars. Tragically, Cody's inhibitor chip functioned perfectly, and he unflinchingly ordered his troops to fire upon Kenobi when Order 66 was issued.",
    "Jawa": "Small, fiercely opportunistic humanoid scavengers native to the deserts of Tatooine. They traverse the harsh dune seas in massive, treaded vehicles called Sandcrawlers, searching for discarded droids, crashed ships, and mechanical scrap to refurbish and sell to moisture farmers.",
    "Mace Windu": "A severe and incredibly powerful Jedi Master who held a senior seat on the Jedi High Council. Windu created and mastered Vaapad, a dangerous lightsaber combat form that skirts the edge of the dark side. He is instantly recognizable on the battlefield by his uniquely amethyst-colored lightsaber.",
    "Boba Fett": "The most feared bounty hunter in the galaxy. Boba is an unaltered clone of his father, the famous Jango Fett, whom he watched die at the hands of Mace Windu. Clad in customized Mandalorian armor and piloting the fearsome ship Slave I, he built a legendary reputation in the criminal underworld working for Jabba the Hutt and the Empire.",
    "Han Solo": "A cynical, fast-talking smuggler who boasts that his ship, the Millennium Falcon, made the Kessel Run in less than twelve parsecs. Despite his initial insistence that he only cared about money, Solo proved to have a heart of gold, becoming a hero of the Rebel Alliance alongside his best friend and co-pilot, Chewbacca.",
    "Darth Maul": "A terrifying Sith assassin trained by Emperor Palpatine. Maul is recognizable by his striking red and black facial tattoos, crown of horns, and mastery of a double-bladed lightsaber. Though presumed dead after being cut in half by Obi-Wan Kenobi, his pure hatred and mastery of the dark side allowed him to survive and build a vast criminal syndicate.",
    "Thrawn": "Mitth'raw'nuruodo, better known as Thrawn, is a Chiss Grand Admiral in the Imperial Navy. Unlike other Imperial leaders who rely on brute force and fear, Thrawn is a brilliant tactician who defeats his enemies by deeply studying their history, philosophy, and art to predict their strategies.",
    "Pellaeon": "Gilad Pellaeon is an incredibly loyal, pragmatic, and level-headed officer in the Imperial Navy. He famously served as the right-hand man to Grand Admiral Thrawn. After the fragmentation of the Empire, Pellaeon's steady leadership eventually guided the Imperial Remnant away from pure tyranny and toward a negotiated peace.",
    "Admiral Ackbar": "Gial Ackbar is a veteran Mon Calamari military commander. A brilliant tactician, he dedicated his life to fighting against the tyranny of the Galactic Empire. He famously led the Rebel Alliance fleet during the climactic Battle of Endor, where he quickly realized the Emperor had lured them into a trap.",
    "George Lucas": "The Creator himself! The visionary filmmaker who brought the Star Wars universe to life.",
    "The Mandalorian": "Din Djarin, a stoic bounty hunter clad in shiny beskar armor.",
    "Chewbacca": "A tall, furry Wookiee warrior and Han Solo's incredibly loyal co-pilot."
}

# Initialize Streamlit session states 
if "eliminated" not in st.session_state:
    st.session_state.eliminated = {char: False for char in characters}
if "my_character" not in st.session_state:
    st.session_state.my_character = None

# Reset board functionality
def reset_board():
    for char in characters:
        st.session_state.eliminated[char] = False
    st.session_state.my_character = None

# Helper function to load and process character images
def load_character_image(char_name, is_eliminated):
    filename = char_name.lower().replace(" ", "_").replace("-", "_") + ".png"
    filepath = os.path.join("assets", filename)
    
    try:
        img = Image.open(filepath).convert("RGBA")
    except FileNotFoundError:
        img = Image.new('RGBA', (100, 100), color=(45, 52, 54, 255))
        
    img = ImageOps.fit(img, (100, 100), centering=(0.5, 0.5))
    
    if is_eliminated:
        alpha = img.split()[3]
        gray_img = ImageOps.grayscale(img)
        gray_img = gray_img.point(lambda p: p * 0.4)
        gray_img = gray_img.convert("RGBA")
        gray_img.putalpha(alpha)
        img = gray_img
        
    return img

# --- SIDEBAR FOR GAME CONTROLS ---
with st.sidebar:
    st.header("Player Status")
    
    if st.session_state.my_character is None:
        selected_char = st.selectbox("Choose your character:", characters)
        if st.button("Lock In", type="primary", use_container_width=True):
            st.session_state.my_character = selected_char
            st.rerun()
    else:
        st.success("Character Locked!")
        st.markdown(f"<h3 style='text-align: center;'>{st.session_state.my_character}</h3>", unsafe_allow_html=True)
        
        locked_img = load_character_image(st.session_state.my_character, False)
        st.image(locked_img.resize((150, 150)), use_container_width=True)
        
    st.markdown("---")
    st.button("Reset Game", on_click=reset_board, type="primary", use_container_width=True)


# --- CREATE TABS (Now 3 Tabs) ---
tab1, tab2, tab3 = st.tabs(["🎮 Game Board", "📜 How to Play", "🌌 Deep Lore Database"])

# --- TAB 1: MAIN GAME BOARD ---
with tab1:
    st.markdown("Eliminate characters by clicking the button below their image.")
    cols = st.columns(7)
    
    for idx, char in enumerate(characters):
        col = cols[idx % 7]
        with col:
            eliminated_state = st.session_state.eliminated[char]
            
            img = load_character_image(char, eliminated_state)
            st.image(img, use_container_width=True)
            
            st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 0px;'>{char}</p>", unsafe_allow_html=True)
            
            button_label = "Restore" if eliminated_state else "Eliminate"
            if st.button(button_label, key=f"btn_{char}", use_container_width=True):
                st.session_state.eliminated[char] = not eliminated_state
                st.rerun()

# --- TAB 2: HOW TO PLAY ---
with tab2:
    st.header("Rules of Guess Who: Star Wars Edition")
    
    st.markdown("""
    **Objective:** Be the first player to guess your opponent's mystery character!
    
    ### ⚙️ Setup
    1. Both players open the game on their respective devices.
    2. Choose a character from the dropdown menu in the sidebar and click **Lock In**. Keep this a secret!
    
    ### 🎲 Gameplay
    1. The youngest player goes first.
    2. On your turn, ask your opponent a single **"Yes or No"** question about their locked character's visual traits.
        * *Example: "Does your character wear a black mask?"*
        * *Example: "Is your character small and green?"*
        * *Example: "Is your character made of gold metal?"*
    3. Based on their answer, click the **Eliminate** button under characters on your board that no longer match the description. They will turn grey.
    4. Alternate turns asking questions and eliminating characters until you think you know the answer.
    
    ### 🏆 Winning the Game
    * On your turn, instead of asking a trait question, you can use your turn to **Guess the Character**.
    * If you guess correctly, you win!
    * If you guess incorrectly, you lose the game immediately. Proceed with caution!
    
    When finished, click **Reset Game** in the sidebar to play again.
    """)

# --- TAB 3: DEEP LORE DATABASE ---
with tab3:
    st.header("Galactic Archives")
    st.markdown("Expand your knowledge of the Star Wars universe. Click on a character to read their full history.")
    
    # We use st.expander so the player isn't overwhelmed by a massive wall of text
    for char in characters:
        with st.expander(f"Data File: {char}"):
            col1, col2 = st.columns([1, 5]) # Creates a small column for the image, large for text
            with col1:
                img = load_character_image(char, False)
                st.image(img, use_container_width=True)
            with col2:
                st.markdown(f"### {char}")
                st.write(deep_lore[char])