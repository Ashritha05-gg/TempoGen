/* Minimal_Resume.jsx*/
import "./Minimal_Resume.css";

export default function MinimalResume() {
  return (
    <div className="resume-page">
      <div className="resume-container">
        
        {/* Header */}
        <header className="resume-header">
          <h1 className="name">Your Name</h1>
          <p className="title">Software Engineer</p>

          <div className="contact">
            <span>email@example.com</span>
            <span> | </span>
            <span>+91 9XXXXXXXXX</span>
            <span> | </span>
            <span>Hyderabad, India</span>
          </div>
        </header>

        {/* Section */}
        <section>
          <h2 className="section-title">Summary</h2>
          <p className="text">
            Results-driven software engineer with experience in building
            scalable web applications and REST APIs. Strong in problem solving
            and clean code practices.
          </p>
        </section>

        <section>
          <h2 className="section-title">Skills</h2>
          <ul className="skills">
            <li>Java</li>
            <li>Python</li>
            <li>React</li>
            <li>SQL</li>
            <li>Git</li>
          </ul>
        </section>

        <section>
          <h2 className="section-title">Experience</h2>

          <div className="item">
            <div className="item-header">
              <strong>Software Intern</strong>
              <span>2024 – Present</span>
            </div>
            <p className="company">ABC Technologies</p>
            <ul>
              <li>Developed REST APIs using Spring Boot</li>
              <li>Built responsive UI using React</li>
              <li>Improved application performance by 25%</li>
            </ul>
          </div>
        </section>

        <section>
          <h2 className="section-title">Education</h2>

          <div className="item">
            <div className="item-header">
              <strong>B.Tech – Computer Science</strong>
              <span>2021 – 2025</span>
            </div>
            <p className="company">XYZ University</p>
          </div>
        </section>

      </div>
    </div>
  );
}