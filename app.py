# Fixed session state
if 'total_membership' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.total_membership = 1240394
    st.session_state.new_members = 11356
    st.session_state.total_contributions = 3061104  # Corrected total contributions value
    st.session_state.total_grants = 3055250
    st.session_state.data_loaded = True

# Fixed the story 3 in Member Care tab and fix the notes section placement
with tab7:
    st.markdown('<h3 class="section-title">Member Care Metrics</h3>', unsafe_allow_html=True)

    mc_col1, mc_col2 = st.columns(2)

    with mc_col1:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">MEMBER SATISFACTION RATING</p>'
            f'<p class="metric-value">95%</p>'
            f'<p>Goal: 85%</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with mc_col2:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">RESOLUTION/RESPONSIVENESS RATE</p>'
            f'<p class="metric-value">2 hours</p>'
            f'<p>Goal: 48 hours</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<h3>Top Member Issues/Concerns</h3>', unsafe_allow_html=True)
    st.markdown(
        """
        - The App & Join the Movement
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<h3>Voices from the Field: Top Inspirational Stories</h3>', unsafe_allow_html=True)
    
    with st.expander("Story 1: Crew Leader Nicole Crooks and the South Florida crew"):
        st.markdown(
            """
            Crew Leader Nicole Crooks and the South Florida crew understood the assignment during #SisterhoodSaturday! 
            Nicole's post says it best: "Simply grateful!!! #SisterhoodSaturday during Black Maternal Health Week was absolutely everything! 
            A huge thank you to Maya at Historic Virginia Key Beach Park, Kallima and the entire GirlTREK: Healthy Black Women village, 
            Cortes, Jamarrah and the entire https://southernbirthjustice.org/ (SBJN) village, Kedemah and the entire AKA village, 
            Mama Kuks, Mama Joy, Mama Sheila & Mama Wangari (our beautiful village of elders), to each and every sister who came or 
            supported in any way. AND a SUPER DUPER Thank you, thank you, THANK YOU!!! to Kukuwa Fitness and Nakreshia Causey Borno 
            Saturday was filled with magic and joy! And yep... you can grab those GirlTREK inspired leggings at https://www.kukuwafitness.com/ 
            I am so ready for this week's #selfcareschool hope you are too!!!"
            """
        )
    
    with st.expander("Story 2: Amazing Ted Talk used in class!"):
        st.write(
            "Hello ladies! First and foremost YOU ARE AMAZING. Sending so much love to you all and holding space for your amazing cause. "
            "I am a teacher in Ohio and I just wanted to tell you that I am using the TedTalk from 2018 in my Black History in America course. "
            "I can't wait to help my students use this frame of understanding. Thank you for shining a light on this - it is so needed! "
            "Thank you for taking action! Thank you for showing so much loving kindness! I appreciate you all and am so excited for this movement! "
            "Much love and respect, Kaitlin Finan"
        )
    
    with st.expander("Story 3: My Sister's Keeper"):
        st.markdown(
            """
            Morgan and Vanessa, I walked this evening. First chance I've had in a while.
            And I talked on the phone to a friend of mine who was also walking at the time and had not walked in a while. 
            I invited her to walk with me and told her about Harriet Day and the meeting last night. 
            I also shared GirlTREK information with her and invited her to join. We're going to start walking together!

            I used to walk all the time. I moved back closer to my hometown four years ago to be near Mama and help take care of her. 
            She got better and was doing great, then all of a sudden she wasn't. Mama transitioned to Heaven a little over a year ago 
            and life has been difficult. She was everything to me. It's just been hard — but by the grace of God, I'm still standing. 
            He did bless us with 3 more years after she was hospitalized 33 days. I'm trying to get my legs back under me. 
            But I am lonely for Mama.

            99% of the time, I walked alone…didn't have anyone to walk with. But I would listen in some Saturdays. 
            Everybody is a few towns over, so weekday scheduling is tough. But I also told my sisters and my brother 
            that they were going to walk with me as a part of this next 10-week commitment.

            Thank you for all that you do,  
            Sandy B. Carter
            """
        )
    
    # Fixed: Moved notes section outside of the expander
    st.markdown('<hr>', unsafe_allow_html=True)
    create_notes_section("Member Care")
