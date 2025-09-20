from manim import *
import numpy as np

class PersonalityAnalysisAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Personality Analysis System", font_size=48, color=BLUE)
        subtitle = Text("Trait-Based Job Matching", font_size=32, color=TEAL)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle))
        self.wait(2)

        # Clear screen for architecture overview
        self.play(FadeOut(title), FadeOut(subtitle))

        # Architecture Components
        self.show_architecture()

        # Data Flow
        self.show_data_flow()

        # Matching Process
        self.show_matching_process()

        # Technical Details
        self.show_technical_details()

        # Conclusion
        self.show_conclusion()

    def show_architecture(self):
        """Show the main components of the system"""
        # Component boxes
        traits_box = Rectangle(width=2, height=1, color=GREEN).shift(LEFT * 3 + UP * 2)
        persons_box = Rectangle(width=2, height=1, color=BLUE).shift(LEFT * 3 + DOWN * 2)
        companies_box = Rectangle(width=2, height=1, color=RED).shift(RIGHT * 3 + UP * 2)
        matching_box = Rectangle(width=2, height=1, color=YELLOW).shift(RIGHT * 3 + DOWN * 2)

        # Labels
        traits_label = Text("Traits DB", font_size=20, color=GREEN).move_to(traits_box)
        persons_label = Text("Persons DB", font_size=20, color=BLUE).move_to(persons_box)
        companies_label = Text("Companies", font_size=20, color=RED).move_to(companies_box)
        matching_label = Text("Matching Engine", font_size=20, color=YELLOW).move_to(matching_box)

        # Animate components appearing
        self.play(Create(traits_box), Write(traits_label))
        self.play(Create(persons_box), Write(persons_label))
        self.play(Create(companies_box), Write(companies_label))
        self.play(Create(matching_box), Write(matching_label))

        # Show connections
        arrow1 = Arrow(traits_box.get_right(), persons_box.get_left(), color=WHITE)
        arrow2 = Arrow(traits_box.get_right(), companies_box.get_left(), color=WHITE)
        arrow3 = Arrow(persons_box.get_right(), matching_box.get_left(), color=BLUE)
        arrow4 = Arrow(companies_box.get_right(), matching_box.get_left(), color=RED)

        self.play(Create(arrow1), Create(arrow2), Create(arrow3), Create(arrow4))

        # Title for this section
        section_title = Text("System Architecture", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(section_title))

        self.wait(3)

        # Clear for next section
        self.play(FadeOut(section_title), FadeOut(traits_box), FadeOut(traits_label),
                 FadeOut(persons_box), FadeOut(persons_label), FadeOut(companies_box),
                 FadeOut(companies_label), FadeOut(matching_box), FadeOut(matching_label),
                 FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3), FadeOut(arrow4))

    def show_data_flow(self):
        """Show how data flows through the system"""
        # Create a person
        person_circle = Circle(radius=0.5, color=BLUE).shift(LEFT * 4)
        person_text = Text("Alice", font_size=20, color=BLUE).move_to(person_circle)

        # Description input
        desc_text = Text('"friendly and outgoing"', font_size=16, color=GREEN).next_to(person_circle, RIGHT)

        # Arrow to processing
        arrow1 = Arrow(person_circle.get_right(), desc_text.get_left(), color=WHITE)

        # Processing box
        process_box = Rectangle(width=2, height=1, color=YELLOW).shift(RIGHT * 2)
        process_text = Text("Analyze", font_size=20, color=YELLOW).move_to(process_box)

        # Arrow to traits
        arrow2 = Arrow(desc_text.get_right(), process_box.get_left(), color=WHITE)

        # Traits found
        traits_text = Text("friendly: 7.0F, 6.0D\noutgoing: 9.0F, 5.0D", font_size=16, color=GREEN).next_to(process_box, RIGHT)

        # Arrow to personality
        arrow3 = Arrow(process_box.get_right(), traits_text.get_left(), color=WHITE)

        # Final personality
        personality_text = Text("Personality: 8.0F, 5.5D", font_size=20, color=BLUE).shift(RIGHT * 1 + DOWN * 2)

        # Arrow to final
        arrow4 = Arrow(traits_text.get_bottom(), personality_text.get_top(), color=WHITE)

        # Animate the flow
        self.play(Create(person_circle), Write(person_text))
        self.play(Create(desc_text), Create(arrow1))
        self.play(Create(process_box), Write(process_text), Create(arrow2))
        self.play(Create(traits_text), Create(arrow3))
        self.play(Create(personality_text), Create(arrow4))

        # Section title
        section_title = Text("Data Processing Flow", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(section_title))

        self.wait(4)

        # Clear for next section
        self.play(FadeOut(section_title), FadeOut(person_circle), FadeOut(person_text),
                 FadeOut(desc_text), FadeOut(arrow1), FadeOut(process_box), FadeOut(process_text),
                 FadeOut(arrow2), FadeOut(traits_text), FadeOut(arrow3),
                 FadeOut(personality_text), FadeOut(arrow4))

    def show_matching_process(self):
        """Show the company matching process"""
        # Company job description
        company_text = Text("Tech Startup Job:\n'innovative leader'", font_size=24, color=RED).shift(LEFT * 3 + UP * 2)

        # Target personality
        target_text = Text("Target Personality:\n8.5F, 7.0D", font_size=20, color=RED).next_to(company_text, DOWN)

        # Available candidates
        alice_text = Text("Alice: 8.0F, 5.5D", font_size=20, color=BLUE).shift(RIGHT * 3 + UP * 1)
        bob_text = Text("Bob: 6.5F, 8.0D", font_size=20, color=BLUE).shift(RIGHT * 3)
        charlie_text = Text("Charlie: 9.0F, 7.5D", font_size=20, color=BLUE).shift(RIGHT * 3 + DOWN * 1)

        # Distance calculations
        alice_dist = Text("Distance: 1.8", font_size=16, color=YELLOW).next_to(alice_text, RIGHT)
        bob_dist = Text("Distance: 1.2", font_size=16, color=YELLOW).next_to(bob_text, RIGHT)
        charlie_dist = Text("Distance: 0.7", font_size=16, color=YELLOW).next_to(charlie_text, RIGHT)

        # Arrows
        arrow1 = Arrow(company_text.get_right(), alice_text.get_left(), color=WHITE)
        arrow2 = Arrow(company_text.get_right(), bob_text.get_left(), color=WHITE)
        arrow3 = Arrow(company_text.get_right(), charlie_text.get_left(), color=WHITE)

        # Ranking
        ranking_text = Text("Ranking by Distance:", font_size=24, color=GREEN).shift(DOWN * 2)
        rank1 = Text("1. Charlie (0.7)", font_size=20, color=GOLD).next_to(ranking_text, DOWN)
        rank2 = Text("2. Bob (1.2)", font_size=20, color=GRAY).next_to(rank1, DOWN)
        rank3 = Text("3. Alice (1.8)", font_size=20, color=ORANGE).next_to(rank2, DOWN)

        # Animate
        self.play(Write(company_text))
        self.play(Write(target_text))
        self.play(Write(alice_text), Write(bob_text), Write(charlie_text))
        self.play(Create(arrow1), Create(arrow2), Create(arrow3))
        self.play(Write(alice_dist), Write(bob_dist), Write(charlie_dist))

        # Show ranking
        self.play(Write(ranking_text))
        self.play(Write(rank3))  # Alice
        self.play(Write(rank2))  # Bob
        self.play(Write(rank1))  # Charlie

        # Section title
        section_title = Text("Personality Matching Process", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(section_title))

        self.wait(4)

        # Clear for next section
        self.play(FadeOut(section_title), FadeOut(company_text), FadeOut(target_text),
                 FadeOut(alice_text), FadeOut(bob_text), FadeOut(charlie_text),
                 FadeOut(alice_dist), FadeOut(bob_dist), FadeOut(charlie_dist),
                 FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3),
                 FadeOut(ranking_text), FadeOut(rank1), FadeOut(rank2), FadeOut(rank3))

    def show_technical_details(self):
        """Show technical implementation details"""
        # Code snippets
        code1 = Text("python main.py person create Alice", font_size=16, color=BLUE).shift(LEFT * 3 + UP * 2)
        code2 = Text("python main.py person add_desc Alice 'friendly outgoing'", font_size=16, color=BLUE).next_to(code1, DOWN)
        code3 = Text("python main.py company query TechCorp 'innovative leader'", font_size=16, color=RED).next_to(code2, DOWN)

        # Results
        results = Text("Results:\n- Charlie: Distance 0.7\n- Bob: Distance 1.2\n- Alice: Distance 1.8", font_size=20, color=GREEN).shift(RIGHT * 3)

        # Database structure
        db_text = Text("Database Structure:", font_size=24, color=YELLOW).shift(LEFT * 3 + DOWN * 2)
        traits_db = Text("traits.db: trait, friendliness, dominance", font_size=16, color=YELLOW).next_to(db_text, DOWN)
        persons_db = Text("persons.db: name, friendliness, dominance, n_traits", font_size=16, color=YELLOW).next_to(traits_db, DOWN)

        # Animate
        self.play(Write(code1), Write(code2), Write(code3))
        self.play(Write(results))

        self.play(Write(db_text))
        self.play(Write(traits_db))
        self.play(Write(persons_db))

        # Section title
        section_title = Text("Technical Implementation", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(section_title))

        self.wait(4)

        # Clear for conclusion
        self.play(FadeOut(section_title), FadeOut(code1), FadeOut(code2), FadeOut(code3),
                 FadeOut(results), FadeOut(db_text), FadeOut(traits_db), FadeOut(persons_db))

    def show_conclusion(self):
        """Show conclusion and key takeaways"""
        # Key features
        features = [
            "✓ Trait-based personality analysis",
            "✓ Dynamic profile updates",
            "✓ Euclidean distance matching",
            "✓ CLI and service-based architecture",
            "✓ SQLite database backend"
        ]

        feature_texts = []
        for i, feature in enumerate(features):
            text = Text(feature, font_size=24, color=GREEN).shift(UP * (2 - i * 0.8))
            feature_texts.append(text)

        # Animate features
        for text in feature_texts:
            self.play(Write(text))

        # Final title
        conclusion = Text("Personality Analysis System", font_size=48, color=BLUE).shift(DOWN * 2)
        tagline = Text("Matching people to jobs through personality traits", font_size=24, color=TEAL).next_to(conclusion, DOWN)

        self.play(Write(conclusion), Write(tagline))

        self.wait(3)

        # Fade out everything
        self.play(FadeOut(*feature_texts), FadeOut(conclusion), FadeOut(tagline))

if __name__ == "__main__":
    # This will be run by manim command
    pass